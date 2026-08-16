from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_xian_review import (  # noqa: E402
    BOOK_PATH,
    CHAPTER_IDS,
    extract_page_count,
    extract_page_size,
    validate_asset_qa,
    validate_cover_qa,
    validate_figure_cast,
    validate_fonts,
)


class XianReviewBuildTests(unittest.TestCase):
    def test_review_build_contains_all_eleven_chapters(self) -> None:
        self.assertEqual(len(CHAPTER_IDS), 11)
        self.assertEqual(CHAPTER_IDS[-1], "ch11-before-departure")

    def test_extracts_page_count(self) -> None:
        self.assertEqual(extract_page_count("Title: Test\nPages:          14\n"), 14)

    def test_extracts_page_size(self) -> None:
        self.assertEqual(
            extract_page_size("Page size:       354.331 x 498.898 pts (B6)\n"),
            (354.331, 498.898),
        )

    def test_accepts_reviewed_map_asset(self) -> None:
        document = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        validate_asset_qa(document)

    def test_accepts_reviewed_text_free_cover(self) -> None:
        validate_cover_qa()

    def test_rejects_unapproved_map_asset(self) -> None:
        document = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        document = copy.deepcopy(document)
        document["assets"][0]["qa"]["approved"] = False
        with self.assertRaisesRegex(RuntimeError, "visual QA"):
            validate_asset_qa(document)

    def test_accepts_required_figure_guides(self) -> None:
        provenance = {
            "source_images": [
                {"path": "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png"},
                {"path": "/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg"},
            ]
        }
        validate_figure_cast("asset-test", provenance)

    def test_rejects_figure_without_lala_xia(self) -> None:
        provenance = {
            "source_images": [
                {"path": "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png"}
            ]
        }
        with self.assertRaisesRegex(RuntimeError, "Aya-chan/Lala Xia"):
            validate_figure_cast("asset-test", provenance)

    def test_accepts_embedded_font_rows(self) -> None:
        output = (
            "name type encoding emb sub uni object ID\n"
            "------------------------------------------\n"
            "ABCDE+NotoSerif CID TrueType Identity-H yes yes yes 4 0\n"
        )
        self.assertEqual(validate_fonts(output), 1)

    def test_rejects_unembedded_font_rows(self) -> None:
        output = (
            "name type encoding emb sub uni object ID\n"
            "------------------------------------------\n"
            "NotoSerif CID TrueType Identity-H no no yes 4 0\n"
        )
        with self.assertRaisesRegex(RuntimeError, "unembedded"):
            validate_fonts(output)


if __name__ == "__main__":
    unittest.main()
