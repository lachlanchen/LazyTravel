#!/usr/bin/env python3
"""Run destination-neutral desktop and mobile QA on a built LazyTravel site."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright
from qa_website import (
    assert_core_render,
    expected_counts,
    screenshot_all_figures,
    screenshot_full_element,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "data/japan/prefectures/kanagawa/hakone/book.json"
DEFAULT_OUTPUT = ROOT / "build/qa/site/destination"


def check_ruby_toggle(page: Page, label: str) -> None:
    ruby = page.locator("rt").first
    if not ruby.count():
        raise RuntimeError(f"{label} has no ruby readings")
    page.locator(".ruby-switch").click()
    if ruby.evaluate("node => getComputedStyle(node).display") != "none":
        raise RuntimeError(f"{label} ruby toggle did not hide readings")
    page.locator(".ruby-switch").click()


def check_map_controls(
    page: Page, label: str, *, require_scroll: bool, map_index: int = 0
) -> dict[str, int]:
    figure = page.locator(".map-figure").nth(map_index)
    viewport = figure.locator(".map-viewport")
    stage = figure.locator(".map-stage")
    dimensions = viewport.evaluate(
        "node => ({client: node.clientWidth, scroll: node.scrollWidth, "
        "client_height: node.clientHeight, scroll_height: node.scrollHeight})"
    )
    if require_scroll and dimensions["scroll"] <= dimensions["client"]:
        raise RuntimeError(f"{label} map lacks a readable horizontal viewport: {dimensions}")
    if dimensions["scroll_height"] > dimensions["client_height"] + 2:
        raise RuntimeError(f"{label} map is vertically clipped: {dimensions}")
    initial = stage.evaluate("node => node.getBoundingClientRect().width")
    figure.get_by_role("button", name="Zoom in").click()
    zoomed = stage.evaluate("node => node.getBoundingClientRect().width")
    if zoomed <= initial:
        raise RuntimeError(f"{label} map zoom did not enlarge the map")
    figure.get_by_role("button", name="Reset map").click()
    return dimensions


def map_capture_stem(stem: str, map_index: int, map_count: int) -> str:
    if map_count == 1:
        return f"{stem}-map"
    return f"{stem}-map-{map_index + 1:02d}"


def screenshot_map_positions(
    page: Page, output: Path, stem: str, *, map_index: int, map_count: int
) -> list[int]:
    figure = page.locator(".map-figure").nth(map_index)
    viewport = figure.locator(".map-viewport")
    dimensions = viewport.evaluate(
        "node => ({client: node.clientWidth, scroll: node.scrollWidth})"
    )
    maximum = max(0, dimensions["scroll"] - dimensions["client"])
    positions = [0, round(maximum / 2), maximum]
    for name, position in zip(("left", "center", "right"), positions, strict=True):
        viewport.evaluate(
            "(node, left) => node.scrollTo({top: 0, left, behavior: 'auto'})",
            position,
        )
        page.wait_for_timeout(80)
        screenshot_full_element(page, figure, output / f"{stem}-{name}.png")
    viewport.evaluate("node => node.scrollTo({top: 0, left: 0, behavior: 'auto'})")
    return positions


def reset_capture_position(page: Page) -> None:
    page.evaluate(
        """() => {
          if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
          document.documentElement.style.scrollBehavior = 'auto';
          window.scrollTo({top: 0, left: 0, behavior: 'auto'});
          document.documentElement.scrollTop = 0;
          document.body.scrollTop = 0;
        }"""
    )
    page.wait_for_timeout(100)
    if page.evaluate("window.scrollY") > 1:
        raise RuntimeError("browser did not return to the page top before capture")


def run_qa(url: str, book_path: Path, output: Path) -> dict[str, Any]:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    if not chrome:
        raise RuntimeError("Google Chrome is required for browser QA")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    document = json.loads(book_path.read_text(encoding="utf-8"))
    counts = expected_counts(book_path)
    active = [chapter for chapter in document["chapters"] if chapter["blocks"]]
    if not active:
        raise RuntimeError("website QA requires at least one populated chapter")
    report: dict[str, Any] = {
        "url": url,
        "destination": document["book"]["id"],
        "browser": chrome,
        "expected": counts,
        "console_errors": [],
        "request_failures": [],
        "viewports": {},
    }

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=chrome)
        try:
            desktop_context = browser.new_context(viewport={"width": 1440, "height": 1000})
            desktop = desktop_context.new_page()
            desktop.set_default_timeout(8_000)
            desktop.on(
                "console",
                lambda message: report["console_errors"].append(message.text)
                if message.type == "error"
                else None,
            )
            desktop.on(
                "requestfailed",
                lambda request: report["request_failures"].append(request.url),
            )
            for index, chapter in enumerate(active, start=1):
                chapter_id = chapter["id"]
                desktop.goto(
                    f"{url.rstrip('/')}?chapter={chapter_id}", wait_until="networkidle"
                )
                observed = assert_core_render(
                    desktop, counts[chapter_id], f"desktop {chapter_id}"
                )
                report["viewports"][f"desktop_{chapter_id}"] = observed
                columns = desktop.locator(".language-grid").first.evaluate(
                    "node => getComputedStyle(node).gridTemplateColumns.split(' ').length"
                )
                if columns != 3:
                    raise RuntimeError(f"desktop {chapter_id} does not show three languages")
                if not desktop.locator(".book-rail").is_visible():
                    raise RuntimeError("desktop chapter rail is hidden")
                if index == 1:
                    check_ruby_toggle(desktop, "desktop")
                if counts[chapter_id]["maps"]:
                    map_count = counts[chapter_id]["maps"]
                    map_viewports = []
                    for map_index in range(map_count):
                        capture_stem = map_capture_stem(
                            f"desktop-{chapter['order']:02d}", map_index, map_count
                        )
                        map_viewports.append(
                            check_map_controls(
                                desktop,
                                f"desktop {chapter_id} map {map_index + 1}",
                                require_scroll=False,
                                map_index=map_index,
                            )
                        )
                        screenshot_full_element(
                            desktop,
                            desktop.locator(".map-figure").nth(map_index),
                            output / f"{capture_stem}.png",
                        )
                    map_key = "map_viewport" if map_count == 1 else "map_viewports"
                    report["viewports"][f"desktop_{chapter_id}"][map_key] = (
                        map_viewports[0] if map_count == 1 else map_viewports
                    )
                reset_capture_position(desktop)
                desktop.screenshot(
                    path=output / f"desktop-{chapter['order']:02d}-viewport.png"
                )
                capture_style = desktop.add_style_tag(
                    content=".app-header{position:static!important}.skip-link{display:none!important}"
                )
                desktop.screenshot(
                    path=output / f"desktop-{chapter['order']:02d}.png", full_page=True
                )
                capture_style.evaluate("node => node.remove()")
            desktop_context.close()

            mobile_context = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=2,
                is_mobile=True,
                has_touch=True,
            )
            mobile = mobile_context.new_page()
            mobile.set_default_timeout(8_000)
            mobile.on(
                "console",
                lambda message: report["console_errors"].append(message.text)
                if message.type == "error"
                else None,
            )
            mobile.on(
                "requestfailed",
                lambda request: report["request_failures"].append(request.url),
            )
            for index, chapter in enumerate(active, start=1):
                chapter_id = chapter["id"]
                mobile.goto(
                    f"{url.rstrip('/')}?chapter={chapter_id}", wait_until="networkidle"
                )
                observed = assert_core_render(
                    mobile, counts[chapter_id], f"mobile {chapter_id}"
                )
                report["viewports"][f"mobile_{chapter_id}"] = observed
                if mobile.locator("#chapter-select").input_value() != chapter_id:
                    raise RuntimeError(f"mobile chapter menu did not select {chapter_id}")
                if mobile.locator(".book-rail").is_visible():
                    raise RuntimeError("mobile chapter rail should be hidden")
                if not mobile.locator(".mobile-jump").is_visible():
                    raise RuntimeError("mobile section navigation is hidden")
                if index == 1:
                    check_ruby_toggle(mobile, "mobile")
                if counts[chapter_id]["maps"]:
                    map_count = counts[chapter_id]["maps"]
                    map_viewports = []
                    for map_index in range(map_count):
                        capture_stem = map_capture_stem(
                            f"mobile-{chapter['order']:02d}", map_index, map_count
                        )
                        map_viewport = check_map_controls(
                            mobile,
                            f"mobile {chapter_id} map {map_index + 1}",
                            require_scroll=True,
                            map_index=map_index,
                        )
                        map_viewport["pan_offsets_css_px"] = screenshot_map_positions(
                            mobile,
                            output,
                            capture_stem,
                            map_index=map_index,
                            map_count=map_count,
                        )
                        map_viewports.append(map_viewport)
                        screenshot_full_element(
                            mobile,
                            mobile.locator(".map-figure").nth(map_index),
                            output / f"{capture_stem}.png",
                        )
                    map_key = "map_viewport" if map_count == 1 else "map_viewports"
                    report["viewports"][f"mobile_{chapter_id}"][map_key] = (
                        map_viewports[0] if map_count == 1 else map_viewports
                    )
                screenshot_all_figures(
                    mobile, output, f"mobile-{chapter['order']:02d}"
                )
                for callout_index in range(
                    mobile.locator(".reading-block.kind-callout").count()
                ):
                    screenshot_full_element(
                        mobile,
                        mobile.locator(".reading-block.kind-callout").nth(callout_index),
                        output
                        / f"mobile-{chapter['order']:02d}-callout-{callout_index + 1:02d}.png",
                    )
                reset_capture_position(mobile)
                mobile.screenshot(
                    path=output / f"mobile-{chapter['order']:02d}-viewport.png"
                )
                capture_style = mobile.add_style_tag(
                    content=".app-header{position:static!important}.skip-link{display:none!important}"
                )
                mobile.screenshot(
                    path=output / f"mobile-{chapter['order']:02d}.png", full_page=True
                )
                capture_style.evaluate("node => node.remove()")
            mobile_context.close()
        finally:
            browser.close()

    if report["console_errors"] or report["request_failures"]:
        raise RuntimeError(
            "browser errors detected: "
            f"console={report['console_errors']} requests={report['request_failures']}"
        )
    (output / "qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = run_qa(args.url, args.book.resolve(), args.output.resolve())
    totals = {
        key: sum(chapter[key] for chapter in report["expected"].values())
        for key in ("blocks", "ruby", "sources")
    }
    print(
        "destination website QA: pass "
        f"({totals['blocks']} blocks, {totals['ruby']} ruby nodes, "
        f"{totals['sources']} chapter-source entries)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
