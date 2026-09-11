from __future__ import annotations

import shutil
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from browser_tests.pages.destination_page import DestinationPage  # noqa: E402


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--base-url",
        default="https://lachlanchen.github.io/LazyTravel/china/cities/lanzhou/",
        help="Published or local Lanzhou destination URL.",
    )
    parser.addoption(
        "--browser-artifacts",
        default="build/qa/playwright-regression/failures",
        help="Directory for failure screenshots.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Iterator[None]:
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"report_{report.when}", report)


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    with sync_playwright() as playwright:
        launch_options = {"headless": True}
        if chrome:
            launch_options["executable_path"] = chrome
        instance = playwright.chromium.launch(**launch_options)
        yield instance
        instance.close()


@pytest.fixture
def destination_page(
    browser: Browser,
    request: pytest.FixtureRequest,
) -> Iterator[DestinationPage]:
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    page = context.new_page()
    page.set_default_timeout(10_000)
    destination = DestinationPage(page, request.config.getoption("--base-url"))
    yield destination
    report = getattr(request.node, "report_call", None)
    if report is not None and report.failed:
        artifact_root = Path(request.config.getoption("--browser-artifacts"))
        destination.capture(artifact_root / f"{request.node.name}.png")
    context.close()
