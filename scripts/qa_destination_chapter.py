#!/usr/bin/env python3
"""Run reusable desktop/mobile browser QA for one canonical destination chapter."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright
from qa_website import (
    assert_core_render,
    assert_scrolled_below_header,
    expected_counts,
    screenshot_all_figures,
    screenshot_full_element,
)

ROOT = Path(__file__).resolve().parents[1]


def assert_content_bounds(page: Page, label: str) -> None:
    failures = page.evaluate(
        """() => {
          const viewport = window.innerWidth;
          return [...document.querySelectorAll(
            '.reading-block, .map-figure, .editorial-figure, .block-heading'
          )]
            .map((node) => ({
              id: node.id || node.className,
              rect: node.getBoundingClientRect()
            }))
            .filter(({ rect }) =>
              rect.width <= 0 || rect.height <= 0 || rect.left < -1 || rect.right > viewport + 1
            )
            .map(({ id, rect }) => ({
              id,
              left: rect.left,
              right: rect.right,
              width: rect.width,
              height: rect.height,
              viewport
            }));
        }"""
    )
    if failures:
        raise RuntimeError(f"{label} content exceeds viewport: {failures}")


def exercise_controls(page: Page, *, has_map: bool, label: str) -> None:
    page.locator('[data-mode-button="zh"]').click()
    if page.locator('.language-panel[data-lang="ja"]').first.is_visible():
        raise RuntimeError(f"{label} Chinese focus mode still shows Japanese prose")
    page.locator(".ruby-switch").click()
    if page.locator("rt").first.evaluate("node => getComputedStyle(node).display") != "none":
        raise RuntimeError(f"{label} ruby toggle did not hide readings")
    page.locator(".ruby-switch").click()
    page.locator('[data-mode-button="parallel"]').click()
    if has_map:
        map_stage = page.locator(".map-stage").first
        initial = map_stage.evaluate("node => node.getBoundingClientRect().width")
        page.get_by_role("button", name="Zoom in").click()
        zoomed = map_stage.evaluate("node => node.getBoundingClientRect().width")
        if zoomed <= initial:
            raise RuntimeError(f"{label} map zoom did not enlarge the map")
        page.get_by_role("button", name="Reset map").click()


def capture_visuals(page: Page, output: Path, prefix: str) -> None:
    page.screenshot(path=output / f"{prefix}-full.png", full_page=True)
    maps = page.locator(".map-figure")
    for index in range(maps.count()):
        suffix = "" if index == 0 else f"-{index + 1:02d}"
        screenshot_full_element(
            page,
            maps.nth(index),
            output / f"{prefix}-map{suffix}.png",
        )
    screenshot_all_figures(page, output, prefix)


def inspect_viewport(
    page: Page,
    *,
    url: str,
    chapter_id: str,
    counts: dict[str, int],
    output: Path,
    prefix: str,
    mobile: bool,
) -> dict[str, Any]:
    page.goto(f"{url.rstrip('/')}?chapter={chapter_id}", wait_until="networkidle")
    page.wait_for_selector("#chapter:not([hidden])")
    if page.locator("#chapter-select").input_value() != chapter_id:
        raise RuntimeError(f"{prefix} chapter menu did not select {chapter_id}")
    observed = assert_core_render(page, counts, prefix)
    columns = page.locator(".language-grid").first.evaluate(
        "node => getComputedStyle(node).gridTemplateColumns.split(' ').length"
    )
    expected_columns = 1 if mobile else 3
    if columns != expected_columns:
        raise RuntimeError(
            f"{prefix} language grid has {columns} columns, expected {expected_columns}"
        )
    assert_content_bounds(page, prefix)
    exercise_controls(page, has_map=bool(counts["maps"]), label=prefix)
    if mobile and counts["maps"]:
        overflow = page.locator(".map-viewport").first.evaluate(
            "node => ({client: node.clientWidth, scroll: node.scrollWidth})"
        )
        if overflow["scroll"] <= overflow["client"]:
            raise RuntimeError(f"{prefix} map lacks a legible scroll viewport: {overflow}")
        observed["map_viewport"] = overflow
    if counts["maps"]:
        assert_scrolled_below_header(page, ".map-figure", f"{prefix} map")
    if counts["figures"]:
        assert_scrolled_below_header(page, ".editorial-figure", f"{prefix} figure")
    capture_visuals(page, output, prefix)
    return observed


def run_qa(url: str, book_path: Path, chapter_id: str, output: Path) -> dict[str, Any]:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    if not chrome:
        raise RuntimeError("Google Chrome is required for browser QA")
    counts_by_chapter = expected_counts(book_path)
    if chapter_id not in counts_by_chapter:
        raise RuntimeError(f"chapter has no canonical blocks: {chapter_id}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    counts = counts_by_chapter[chapter_id]
    report: dict[str, Any] = {
        "url": url,
        "book": str(book_path.relative_to(ROOT)),
        "chapter": chapter_id,
        "expected": counts,
        "console_errors": [],
        "request_failures": [],
        "viewports": {},
    }

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=chrome)
        try:
            for prefix, viewport, mobile in (
                ("desktop", {"width": 1440, "height": 1000}, False),
                ("mobile-390", {"width": 390, "height": 844}, True),
            ):
                context = browser.new_context(viewport=viewport)
                page = context.new_page()
                page.set_default_timeout(8_000)
                page.on(
                    "console",
                    lambda message: report["console_errors"].append(message.text)
                    if message.type == "error"
                    else None,
                )
                page.on(
                    "requestfailed",
                    lambda request: report["request_failures"].append(request.url),
                )
                report["viewports"][prefix] = inspect_viewport(
                    page,
                    url=url,
                    chapter_id=chapter_id,
                    counts=counts,
                    output=output,
                    prefix=prefix,
                    mobile=mobile,
                )
                context.close()
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
    parser.add_argument("--url", default="http://127.0.0.1:4175/")
    parser.add_argument("--book", type=Path, required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run_qa(
        args.url,
        args.book.resolve(),
        args.chapter,
        args.output.resolve(),
    )
    expected = report["expected"]
    print(
        "destination chapter browser QA: pass "
        f"({expected['blocks']} blocks, {expected['ruby']} ruby nodes, "
        f"{expected['maps']} maps, {expected['figures']} figures, "
        f"{expected['sources']} sources)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
