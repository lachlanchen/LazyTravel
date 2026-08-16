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


def check_map_controls(page: Page, label: str, *, require_scroll: bool) -> dict[str, int]:
    viewport = page.locator(".map-viewport").first
    stage = page.locator(".map-stage").first
    dimensions = viewport.evaluate(
        "node => ({client: node.clientWidth, scroll: node.scrollWidth})"
    )
    if require_scroll and dimensions["scroll"] <= dimensions["client"]:
        raise RuntimeError(f"{label} map lacks a readable horizontal viewport: {dimensions}")
    initial = stage.evaluate("node => node.getBoundingClientRect().width")
    page.get_by_role("button", name="Zoom in").click()
    zoomed = stage.evaluate("node => node.getBoundingClientRect().width")
    if zoomed <= initial:
        raise RuntimeError(f"{label} map zoom did not enlarge the map")
    page.get_by_role("button", name="Reset map").click()
    return dimensions


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
                    report["viewports"][f"desktop_{chapter_id}"]["map_viewport"] = (
                        check_map_controls(
                            desktop, f"desktop {chapter_id}", require_scroll=False
                        )
                    )
                desktop.screenshot(
                    path=output / f"desktop-{chapter['order']:02d}.png", full_page=True
                )
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
                    report["viewports"][f"mobile_{chapter_id}"]["map_viewport"] = (
                        check_map_controls(
                            mobile, f"mobile {chapter_id}", require_scroll=True
                        )
                    )
                    screenshot_full_element(
                        mobile,
                        mobile.locator(".map-figure").first,
                        output / f"mobile-{chapter['order']:02d}-map.png",
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
                mobile.screenshot(
                    path=output / f"mobile-{chapter['order']:02d}.png", full_page=True
                )
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
