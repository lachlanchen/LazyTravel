from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_destination_tex import (  # noqa: E402
    block_tex,
    citation_order,
    citation_order_for_chapters,
    cover_tex,
    contents_tex,
    reading_tokens_tex,
    tex_escape,
)


class DestinationTexTests(unittest.TestCase):
    def test_cover_places_text_free_art_below_live_latex_text(self) -> None:
        book = {
            "titles": {"zh": "西安", "ja": "西安", "en": "Xi'an"},
            "subtitles": {"zh": "路线", "ja": "旅程", "en": "Routes"},
            "branding": {
                "studio": "lazying.art",
                "repository": "https://example/repo",
            },
        }
        chapters = [{"order": 1}, {"order": 10}]

        rendered = cover_tex(book, chapters)

        image_at = rendered.index("xian-cover-underlay.png")
        brand_at = rendered.index(r"\LTBrand")
        title_at = rendered.index("西安")
        self.assertLess(image_at, brand_at)
        self.assertLess(image_at, title_at)
        self.assertIn(r"\detokenize", rendered)
        self.assertIn("lazying.art · example/repo", rendered)
        self.assertNotIn("https://example/repo", rendered)

    def test_contents_use_separate_trilingual_entries(self) -> None:
        chapters = [
            {
                "order": 1,
                "titles": {"zh": "西安地图", "ja": "西安の地図", "en": "Map of Xi'an"},
            }
        ]

        rendered = contents_tex(chapters)

        self.assertIn(
            r"\LTContentsEntry{01}{西安地图}{西安の地図}{Map of Xi'an}", rendered
        )
        self.assertIn(r"\pageref{lt-chapter-01}", rendered)
        self.assertNotIn(r"\tableofcontents", rendered)

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

    def test_citations_remain_unique_across_chapters(self) -> None:
        chapters = [
            {"blocks": [{"citation_ids": ["src-a", "src-b"]}]},
            {"blocks": [{"citation_ids": ["src-b", "src-c"]}]},
        ]
        self.assertEqual(citation_order_for_chapters(chapters), ["src-a", "src-b", "src-c"])

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
            r"\LTRubyZH{西安}{xī'ān}\nobreak{}。",
        )

    def test_callout_keeps_ruby_inside_highlight_block(self) -> None:
        block = {
            "id": "ch06-b011",
            "kind": "callout",
            "heading": {
                "zh": "点单与过敏",
                "ja": "注文とアレルギー",
                "en": "ORDER & ALLERGIES",
            },
            "text": {"zh": "点单", "ja": "注文", "en": "Ask clearly."},
            "readings": {
                "zh": {"tokens": [{"text": "点单", "reading": "diǎndān"}]},
                "ja": {"tokens": [{"text": "注文", "reading": "ちゅうもん"}]},
            },
            "citation_ids": ["src-a"],
            "asset_ids": [],
        }
        rendered = block_tex(block, {"src-a": 1}, {})
        self.assertIn(r"\LTCalloutBlock", rendered)
        self.assertNotIn(r"\LTBlockStart", rendered)
        self.assertIn("点单与过敏 · 注文とアレルギー · ORDER \\& ALLERGIES", rendered)
        self.assertIn(r"\LTRubyZH{点单}{diǎndān}", rendered)
        self.assertIn(r"\LTRubyJA{注文}{ちゅうもん}", rendered)

    def test_practical_block_uses_its_trilingual_heading(self) -> None:
        block = {
            "id": "ch07-b006",
            "kind": "practical",
            "heading": {
                "zh": "先定山上路线",
                "ja": "山上ルートを先に決める",
                "en": "ROUTE FIRST",
            },
            "text": {"zh": "路线", "ja": "経路", "en": "Choose a route."},
            "readings": {
                "zh": {"tokens": [{"text": "路线", "reading": "lùxiàn"}]},
                "ja": {"tokens": [{"text": "経路", "reading": "けいろ"}]},
            },
            "citation_ids": ["src-a"],
            "asset_ids": [],
        }
        rendered = block_tex(block, {"src-a": 1}, {})
        self.assertIn(
            r"\LTPracticalHeading{先定山上路线 · 山上ルートを先に決める · ROUTE FIRST}",
            rendered,
        )

    def test_special_block_without_heading_is_rejected(self) -> None:
        block = {
            "id": "ch07-b006",
            "kind": "practical",
            "text": {"zh": "路线", "ja": "経路", "en": "Choose a route."},
            "readings": {
                "zh": {"tokens": [{"text": "路线", "reading": "lùxiàn"}]},
                "ja": {"tokens": [{"text": "経路", "reading": "けいろ"}]},
            },
            "citation_ids": ["src-a"],
            "asset_ids": [],
        }
        with self.assertRaisesRegex(ValueError, "requires a heading"):
            block_tex(block, {"src-a": 1}, {})

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
        self.assertIn(r"\LTRubyZH{前}{qián}\nobreak{}，\allowbreak{}", rendered)
        self.assertIn(r"「\nobreak{}\LTRubyZH{后}{hòu}\nobreak{}」", rendered)

    def test_opening_punctuation_terminates_nobreak_before_plain_kana(self) -> None:
        layer = {
            "tokens": [
                {"text": "「"},
                {"text": "すべて"},
                {"text": "」"},
            ]
        }
        self.assertEqual(
            reading_tokens_tex(layer, "LTRubyJA"),
            r"「\nobreak{}すべて\nobreak{}」",
        )

    def test_figure_block_renders_disclosed_trilingual_caption(self) -> None:
        block = {
            "id": "ch02-b007",
            "kind": "figure",
            "text": {"zh": "中文", "ja": "日本語", "en": "English"},
            "readings": {
                "zh": {"tokens": [{"text": "中文", "reading": "zhōngwén"}]},
                "ja": {"tokens": [{"text": "日本語", "reading": "にほんご"}]},
            },
            "citation_ids": ["src-a"],
            "asset_ids": ["asset-a"],
        }
        assets = {
            "asset-a": {
                "path": "assets/example.png",
                "captions": {"zh": "中文图注", "ja": "日本語図注", "en": "English caption"},
            }
        }
        rendered = block_tex(block, {"src-a": 1}, assets)
        self.assertIn(r"\LTFigurePage", rendered)
        self.assertIn("English caption", rendered)


if __name__ == "__main__":
    unittest.main()
