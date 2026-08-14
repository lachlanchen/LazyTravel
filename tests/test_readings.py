from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_reading_candidates import (  # noqa: E402
    katakana_to_hiragana,
    pinyin_for_word,
    zh_tokens,
)
from validate_readings import valid_furigana, valid_pinyin  # noqa: E402


class ReadingLayerTests(unittest.TestCase):
    def test_xian_river_overrides(self) -> None:
        self.assertEqual(pinyin_for_word("涝"), "láo")
        self.assertEqual(pinyin_for_word("潏"), "jué")

    def test_chinese_tokens_reconstruct_text(self) -> None:
        text = "西安在秦岭与渭河之间。"
        tokens = zh_tokens(text)
        self.assertEqual("".join(token["text"] for token in tokens), text)

    def test_katakana_conversion(self) -> None:
        self.assertEqual(katakana_to_hiragana("セイアン"), "せいあん")

    def test_unicode_reading_validators(self) -> None:
        self.assertTrue(valid_pinyin("xī'ān"))
        self.assertTrue(valid_furigana("しょうろう"))
        self.assertFalse(valid_furigana("鐘楼"))


if __name__ == "__main__":
    unittest.main()
