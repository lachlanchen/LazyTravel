from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_xian_review import extract_page_count, validate_fonts  # noqa: E402


class XianReviewBuildTests(unittest.TestCase):
    def test_extracts_page_count(self) -> None:
        self.assertEqual(extract_page_count("Title: Test\nPages:          14\n"), 14)

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
