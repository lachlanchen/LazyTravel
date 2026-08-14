#!/usr/bin/env python3
"""Run browser-level visual and interaction QA for the generated Xi'an website."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "data/china/cities/xian/book.json"
DEFAULT_OUTPUT = ROOT / "build/qa/site/xian"


def expected_counts(book_path: Path) -> dict[str, dict[str, int]]:
    document = json.loads(book_path.read_text(encoding="utf-8"))
    counts = {}
    for chapter in document["chapters"]:
        if not chapter["blocks"]:
            continue
        citation_ids = []
        ruby = 0
        for block in chapter["blocks"]:
            for language in ("zh", "ja"):
                ruby += sum(
                    "reading" in token for token in block["readings"][language]["tokens"]
                )
            for citation_id in block["citation_ids"]:
                if citation_id not in citation_ids:
                    citation_ids.append(citation_id)
        counts[chapter["id"]] = {
            "blocks": len(chapter["blocks"]),
            "ruby": ruby,
            "sources": len(citation_ids),
            "maps": sum(block["kind"] == "map" for block in chapter["blocks"]),
            "figures": sum(block["kind"] == "figure" for block in chapter["blocks"]),
        }
    return counts


def assert_no_page_overflow(page: Page, label: str) -> None:
    dimensions = page.evaluate(
        """() => ({
          viewport: window.innerWidth,
          document: document.documentElement.scrollWidth,
          body: document.body.scrollWidth
        })"""
    )
    if (
        dimensions["document"] > dimensions["viewport"]
        or dimensions["body"] > dimensions["viewport"]
    ):
        raise RuntimeError(f"{label} has page-level horizontal overflow: {dimensions}")


def assert_header_clear(page: Page, label: str) -> None:
    overlap = page.evaluate(
        """() => {
          const visible = [...document.querySelectorAll(
            '.brand, .destination-mark, .reader-controls'
          )]
            .filter((node) => getComputedStyle(node).display !== 'none')
            .map((node) => ({ name: node.className, rect: node.getBoundingClientRect() }));
          const conflicts = [];
          for (let i = 0; i < visible.length; i += 1) {
            for (let j = i + 1; j < visible.length; j += 1) {
              const a = visible[i].rect;
              const b = visible[j].rect;
              const area = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) *
                Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
              if (area > 1) conflicts.push([visible[i].name, visible[j].name, area]);
            }
          }
          return conflicts;
        }"""
    )
    if overlap:
        raise RuntimeError(f"{label} header controls overlap: {overlap}")


def assert_core_render(page: Page, counts: dict[str, int], label: str) -> dict[str, Any]:
    page.wait_for_selector("#chapter:not([hidden])")
    page.wait_for_function(
        """() => {
          const image = document.querySelector('.map-stage img');
          return image && image.complete && image.naturalWidth > 0;
        }"""
    )
    observed = {
        "blocks": page.locator(".reading-block").count(),
        "ruby": page.locator("ruby").count(),
        "sources": page.locator(".source-item").count(),
        "maps": page.locator(".map-figure").count(),
        "figures": page.locator(".editorial-figure").count(),
        "map_natural_width": page.locator(".map-stage img").first.evaluate(
            "image => image.naturalWidth"
        ),
        "map_source": page.locator(".map-stage img").first.evaluate("image => image.currentSrc"),
    }
    for key in ("blocks", "ruby", "sources", "maps", "figures"):
        if observed[key] != counts[key]:
            raise RuntimeError(f"{label} {key} mismatch: {observed[key]} != {counts[key]}")
    if not observed["map_source"].endswith(".svg") or observed["map_natural_width"] < 600:
        raise RuntimeError(f"{label} vector map did not load correctly: {observed}")
    assert_no_page_overflow(page, label)
    assert_header_clear(page, label)
    return observed


def run_qa(url: str, book_path: Path, output: Path) -> dict[str, Any]:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    if not chrome:
        raise RuntimeError("Google Chrome is required for browser QA")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    counts = expected_counts(book_path)
    chapter_1 = "ch01-ground-before-time"
    chapter_2 = "ch02-capitals-on-different-maps"
    chapter_3 = "ch03-army-under-earth"
    report: dict[str, Any] = {
        "url": url,
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
            desktop.set_default_timeout(5_000)
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
            desktop.goto(url, wait_until="networkidle")
            report["viewports"]["desktop_ch01"] = assert_core_render(
                desktop, counts[chapter_1], "desktop chapter 1"
            )
            columns = desktop.locator(".language-grid").first.evaluate(
                "node => getComputedStyle(node).gridTemplateColumns.split(' ').length"
            )
            if columns != 3:
                raise RuntimeError(
                    f"desktop parallel reading does not have three columns: {columns}"
                )
            if not desktop.locator(".book-rail").is_visible():
                raise RuntimeError("desktop chapter rail is hidden")
            desktop.screenshot(path=output / "desktop-ch01.png", full_page=True)

            desktop.locator(f'[data-chapter-id="{chapter_2}"]').click()
            desktop.wait_for_selector("#ch02-b001")
            desktop.locator(".editorial-figure").scroll_into_view_if_needed()
            desktop.wait_for_function(
                """() => {
                  const image = document.querySelector('.figure-image');
                  return image && image.complete && image.naturalWidth >= 1200;
                }"""
            )
            report["viewports"]["desktop_ch02"] = assert_core_render(
                desktop, counts[chapter_2], "desktop chapter 2"
            )
            desktop.screenshot(path=output / "desktop-ch02.png", full_page=True)

            desktop.locator('[data-mode-button="zh"]').click()
            if desktop.locator('.language-panel[data-lang="ja"]').first.is_visible():
                raise RuntimeError("Chinese focus mode still shows Japanese prose")
            desktop.locator(".ruby-switch").click()
            ruby_display = desktop.locator("rt").first.evaluate(
                "node => getComputedStyle(node).display"
            )
            if ruby_display != "none":
                raise RuntimeError("ruby toggle did not hide readings")
            desktop.locator(".ruby-switch").click()
            desktop.locator('[data-mode-button="parallel"]').click()
            map_stage = desktop.locator(".map-stage").first
            initial_width = map_stage.evaluate("node => node.getBoundingClientRect().width")
            desktop.get_by_role("button", name="Zoom in").click()
            zoomed_width = map_stage.evaluate("node => node.getBoundingClientRect().width")
            if zoomed_width <= initial_width:
                raise RuntimeError("map zoom control did not enlarge the map")
            desktop.get_by_role("button", name="Reset map").click()

            desktop.locator(f'[data-chapter-id="{chapter_3}"]').click()
            desktop.wait_for_selector("#ch03-b001")
            desktop.locator(".editorial-figure").scroll_into_view_if_needed()
            desktop.wait_for_function(
                """() => {
                  const image = document.querySelector('.figure-image');
                  return image && image.complete && image.naturalWidth >= 1200;
                }"""
            )
            report["viewports"]["desktop_ch03"] = assert_core_render(
                desktop, counts[chapter_3], "desktop chapter 3"
            )
            desktop.screenshot(path=output / "desktop-ch03.png", full_page=True)
            desktop_context.close()

            mobile_context = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=2,
                is_mobile=True,
                has_touch=True,
            )
            mobile = mobile_context.new_page()
            mobile.set_default_timeout(5_000)
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
            mobile_url = f"{url.rstrip('/')}?chapter={chapter_2}"
            mobile.goto(mobile_url, wait_until="networkidle")
            report["viewports"]["mobile_ch02"] = assert_core_render(
                mobile, counts[chapter_2], "mobile chapter 2"
            )
            if mobile.locator(".book-rail").is_visible():
                raise RuntimeError("mobile chapter rail should be replaced by the section menu")
            if not mobile.locator(".mobile-jump").is_visible():
                raise RuntimeError("mobile section menu is hidden")
            if mobile.locator("#chapter-select").input_value() != chapter_2:
                raise RuntimeError("mobile chapter menu did not select Chapter 2")
            map_overflow = mobile.locator(".map-viewport").evaluate(
                "node => ({client: node.clientWidth, scroll: node.scrollWidth})"
            )
            if map_overflow["scroll"] <= map_overflow["client"]:
                raise RuntimeError(f"mobile map lacks its legible scroll viewport: {map_overflow}")
            map_scroll_left = mobile.locator(".map-viewport").evaluate("node => node.scrollLeft")
            if map_scroll_left <= 0:
                raise RuntimeError("mobile map did not open on the Xi'an area")
            mobile.screenshot(path=output / "mobile-ch02.png", full_page=True)
            mobile.locator(".map-figure").scroll_into_view_if_needed()
            mobile.locator(".map-figure").screenshot(path=output / "mobile-map.png")

            mobile_url = f"{url.rstrip('/')}?chapter={chapter_3}"
            mobile.goto(mobile_url, wait_until="networkidle")
            report["viewports"]["mobile_ch03"] = assert_core_render(
                mobile, counts[chapter_3], "mobile chapter 3"
            )
            if mobile.locator("#chapter-select").input_value() != chapter_3:
                raise RuntimeError("mobile chapter menu did not select Chapter 3")
            mobile.locator(".editorial-figure").scroll_into_view_if_needed()
            mobile.wait_for_function(
                """() => {
                  const image = document.querySelector('.figure-image');
                  return image && image.complete && image.naturalWidth >= 1200;
                }"""
            )
            map_overflow = mobile.locator(".map-viewport").evaluate(
                "node => ({client: node.clientWidth, scroll: node.scrollWidth})"
            )
            if map_overflow["scroll"] <= map_overflow["client"]:
                raise RuntimeError(
                    f"Chapter 3 mobile map lacks a legible scroll viewport: {map_overflow}"
                )
            map_scroll_left = mobile.locator(".map-viewport").evaluate(
                "node => node.scrollLeft"
            )
            if map_scroll_left <= 0:
                raise RuntimeError("Chapter 3 mobile map did not open within its wide canvas")
            mobile.screenshot(path=output / "mobile-ch03.png", full_page=True)
            mobile.locator(".map-figure").scroll_into_view_if_needed()
            mobile.locator(".map-figure").screenshot(path=output / "mobile-ch03-map.png")
            mobile.locator(".editorial-figure").scroll_into_view_if_needed()
            mobile.locator(".editorial-figure").screenshot(
                path=output / "mobile-ch03-figure.png"
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
    parser.add_argument("--url", default="http://127.0.0.1:4173/")
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = run_qa(args.url, args.book.resolve(), args.output.resolve())
    totals = {
        key: sum(chapter[key] for chapter in report["expected"].values())
        for key in ("blocks", "ruby", "sources")
    }
    print(
        "website browser QA: pass "
        f"({totals['blocks']} blocks, {totals['ruby']} ruby nodes, "
        f"{totals['sources']} chapter-source entries)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
