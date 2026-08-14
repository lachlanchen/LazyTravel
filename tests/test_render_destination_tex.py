from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_destination_tex import block_tex, citation_order, tex_escape  # noqa: E402


class DestinationTexTests(unittest.TestCase):
    def test_escapes_latex_metacharacters(self) -> None:
        self.assertEqual(tex_escape("A&B_50%"), r"A\&B\_50\%")

    def test_citations_follow_first_use_without_duplicates(self) -> None:
        chapter = {
            "blocks": [
                {"citation_ids": ["src-a", "src-b"]},
                {"citation_ids": ["src-b", "src-c"]},
            ]
        }
        self.assertEqual(citation_order(chapter), ["src-a", "src-b", "src-c"])

    def test_aligned_block_is_kept_as_one_page_object(self) -> None:
        block = {
            "id": "ch01-b001",
            "kind": "prose",
            "text": {"zh": "中文", "ja": "日本語", "en": "English"},
            "citation_ids": ["src-a"],
            "asset_ids": [],
        }
        rendered = block_tex(block, {"src-a": 1}, {})
        self.assertIn(r"\noindent\begin{minipage}{\linewidth}", rendered)
        self.assertIn(r"\end{minipage}\par", rendered)


if __name__ == "__main__":
    unittest.main()
