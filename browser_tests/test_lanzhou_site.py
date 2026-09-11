from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from qa_website import expected_counts  # noqa: E402

from browser_tests.pages.destination_page import DestinationPage  # noqa: E402

BOOK = ROOT / "data/china/cities/lanzhou/book.json"
COUNTS = expected_counts(BOOK)
CHAPTER_IDS = tuple(COUNTS)


def test_all_chapters_match_canonical_content(destination_page: DestinationPage) -> None:
    destination_page.use_desktop()
    for chapter_id, counts in COUNTS.items():
        destination_page.open_chapter(chapter_id)
        destination_page.assert_canonical_content(chapter_id, counts)
    destination_page.assert_browser_clean()


def test_desktop_and_mobile_navigation_with_ruby(destination_page: DestinationPage) -> None:
    destination_page.use_desktop()
    destination_page.open_chapter(CHAPTER_IDS[0])
    destination_page.assert_navigation(mobile=False)
    destination_page.assert_ruby_toggle()
    destination_page.choose_chapter(CHAPTER_IDS[-1])
    destination_page.assert_canonical_content(CHAPTER_IDS[-1], COUNTS[CHAPTER_IDS[-1]])

    destination_page.use_mobile_width()
    destination_page.open_chapter(CHAPTER_IDS[0])
    destination_page.assert_navigation(mobile=True)
    destination_page.assert_ruby_toggle()
    destination_page.choose_chapter(CHAPTER_IDS[-1])
    destination_page.assert_canonical_content(CHAPTER_IDS[-1], COUNTS[CHAPTER_IDS[-1]])
    destination_page.assert_browser_clean()


def test_map_controls_and_browser_error_gate(destination_page: DestinationPage) -> None:
    map_chapter = next(chapter_id for chapter_id, counts in COUNTS.items() if counts["maps"])

    destination_page.use_desktop()
    destination_page.open_chapter(map_chapter)
    destination_page.assert_map_controls(require_horizontal_scroll=False)

    destination_page.use_mobile_width()
    destination_page.open_chapter(map_chapter)
    destination_page.assert_map_controls(require_horizontal_scroll=True)
    destination_page.assert_browser_clean()
