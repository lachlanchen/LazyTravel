"""Page Object for one published LazyTravel destination."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page
from qa_website import assert_core_render


class DestinationPage:
    """Exercise the reader through stable, user-facing controls."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"
        self.console_errors: list[str] = []
        self.request_failures: list[str] = []
        page.on(
            "console",
            lambda message: self.console_errors.append(message.text)
            if message.type == "error"
            else None,
        )
        page.on("requestfailed", lambda request: self.request_failures.append(request.url))

    def use_desktop(self) -> None:
        self.page.set_viewport_size({"width": 1440, "height": 1000})

    def use_mobile_width(self) -> None:
        self.page.set_viewport_size({"width": 390, "height": 844})

    def open_chapter(self, chapter_id: str) -> None:
        self.page.goto(
            f"{self.base_url}?chapter={chapter_id}",
            wait_until="networkidle",
        )
        self.page.locator("#chapter:not([hidden])").wait_for()
        assert self.page.locator("#chapter-select").input_value() == chapter_id

    def assert_canonical_content(self, chapter_id: str, counts: dict[str, int]) -> None:
        observed = assert_core_render(self.page, counts, f"browser case {chapter_id}")
        assert observed["blocks"] == counts["blocks"]
        assert observed["ruby"] == counts["ruby"]
        assert observed["sources"] == counts["sources"]

    def choose_chapter(self, chapter_id: str) -> None:
        chapter_select = self.page.locator("#chapter-select")
        if chapter_select.is_visible():
            chapter_select.select_option(chapter_id)
        else:
            self.page.locator(
                f'#chapter-outline a[data-chapter-id="{chapter_id}"]'
            ).click()
        self.page.wait_for_function(
            "expected => new URL(location.href).searchParams.get('chapter') === expected",
            arg=chapter_id,
        )
        assert self.page.locator("#chapter-select").input_value() == chapter_id
        self.page.locator("#chapter:not([hidden])").wait_for()
        self.page.wait_for_load_state("networkidle")

    def assert_navigation(self, *, mobile: bool) -> None:
        columns = self.page.locator(".language-grid").first.evaluate(
            "node => getComputedStyle(node).gridTemplateColumns.split(' ').length"
        )
        assert columns == (1 if mobile else 3)
        assert self.page.locator(".book-rail").is_visible() is (not mobile)
        assert self.page.locator(".mobile-jump").is_visible() is mobile

    def assert_ruby_toggle(self) -> None:
        ruby = self.page.locator("rt").first
        assert ruby.count() == 1
        self.page.locator(".ruby-switch").click()
        assert ruby.evaluate("node => getComputedStyle(node).display") == "none"
        self.page.locator(".ruby-switch").click()
        assert ruby.evaluate("node => getComputedStyle(node).display") != "none"

    def assert_map_controls(self, *, require_horizontal_scroll: bool) -> None:
        figure = self.page.locator(".map-figure").first
        viewport = figure.locator(".map-viewport")
        stage = figure.locator(".map-stage")
        dimensions = viewport.evaluate(
            "node => ({client: node.clientWidth, scroll: node.scrollWidth})"
        )
        if require_horizontal_scroll:
            assert dimensions["scroll"] > dimensions["client"]
        initial = stage.evaluate("node => node.getBoundingClientRect().width")
        figure.get_by_role("button", name="Zoom in").click()
        zoomed = stage.evaluate("node => node.getBoundingClientRect().width")
        assert zoomed > initial
        figure.get_by_role("button", name="Reset map").click()
        reset = stage.evaluate("node => node.getBoundingClientRect().width")
        assert abs(reset - initial) < 1

    def assert_browser_clean(self) -> None:
        assert self.console_errors == [], f"console errors: {self.console_errors}"
        assert self.request_failures == [], f"request failures: {self.request_failures}"

    def capture(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=path, full_page=False)
