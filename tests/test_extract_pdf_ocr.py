from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_pdf_ocr import content_chars, source_page_from_reference  # noqa: E402


class PdfOcrHelpersTests(unittest.TestCase):
    def test_counts_cjk_and_latin_content(self) -> None:
        self.assertEqual(content_chars("西安 Xi'an 2026"), 10)

    def test_ignores_layout_punctuation(self) -> None:
        self.assertEqual(content_chars("  — … \n\t"), 0)

    def test_reads_marker_page_as_one_based(self) -> None:
        self.assertEqual(source_page_from_reference("_page_22_Picture_4.jpeg"), 23)

    def test_page_is_optional_for_unknown_names(self) -> None:
        self.assertIsNone(source_page_from_reference("cover.jpeg"))


if __name__ == "__main__":
    unittest.main()
