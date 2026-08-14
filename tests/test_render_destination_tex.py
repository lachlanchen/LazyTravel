from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_destination_tex import (  # noqa: E402
    block_tex,
    citation_order,
    reading_tokens_tex,
    tex_escape,
)


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

    def test_aligned_block_starts_on_a_clean_page(self) -> None:
        block = {
            "id": "ch01-b001",
            "kind": "prose",
            "text": {"zh": "中文", "ja": "日本語", "en": "English"},
            "readings": {
                "zh": {"tokens": [{"text": "中文", "reading": "zhōngwén"}]},
                "ja": {"tokens": [{"text": "日本語", "reading": "にほんご"}]},
            },
            "citation_ids": ["src-a"],
            "asset_ids": [],
        }
        rendered = block_tex(block, {"src-a": 1}, {})
        self.assertTrue(rendered.startswith("\\clearpage"))
        self.assertIn(r"\LTRubyZH{中文}{zhōngwén}", rendered)
        self.assertIn(r"\LTRubyJA{日本語}{にほんご}", rendered)

    def test_reading_tokens_preserve_plain_tokens(self) -> None:
        layer = {"tokens": [{"text": "西安", "reading": "xī'ān"}, {"text": "。"}]}
        self.assertEqual(
            reading_tokens_tex(layer, "LTRubyZH"),
            r"\LTRubyZH{西安}{xī'ān}\nobreak。",
        )

    def test_reading_tokens_bind_opening_and_closing_punctuation(self) -> None:
        layer = {
            "tokens": [
                {"text": "前", "reading": "qián"},
                {"text": "，"},
                {"text": "「"},
                {"text": "后", "reading": "hòu"},
                {"text": "」"},
            ]
        }
        rendered = reading_tokens_tex(layer, "LTRubyZH")
        self.assertIn(r"\LTRubyZH{前}{qián}\nobreak，\allowbreak{}", rendered)
        self.assertIn(r"「\nobreak\LTRubyZH{后}{hòu}\nobreak」", rendered)


if __name__ == "__main__":
    unittest.main()
