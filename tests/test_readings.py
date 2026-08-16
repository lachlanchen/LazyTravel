from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_reading_candidates import (  # noqa: E402
    add_candidates,
    ja_tokens,
    katakana_to_hiragana,
    pinyin_for_word,
    unidic_tagger,
    zh_tokens,
)
from validate_readings import valid_furigana, valid_pinyin  # noqa: E402


class ReadingLayerTests(unittest.TestCase):
    def test_xian_river_overrides(self) -> None:
        self.assertEqual(pinyin_for_word("涝"), "láo")
        self.assertEqual(pinyin_for_word("潏"), "jué")

    def test_xian_food_pinyin_overrides(self) -> None:
        self.assertEqual(pinyin_for_word("饦饦馍"), "tuōtuōmó")
        self.assertEqual(pinyin_for_word("腊汁肉夹馍"), "làzhīròujiāmó")
        self.assertEqual(pinyin_for_word("水围城"), "shuǐwéichéng")
        self.assertEqual(pinyin_for_word("见长"), "jiàncháng")
        self.assertEqual(pinyin_for_word("嚼劲"), "jiáojìn")

    def test_xian_food_furigana_overrides(self) -> None:
        tokens = ja_tokens("飥飥饃と臘汁肉夾饃", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["飥飥饃"], "とぅおとぅおもー")
        self.assertEqual(readings["臘汁肉夾饃"], "らーじーろうじゃーもー")

        phrase_tokens = ja_tokens("辛さと餃子を一品", unidic_tagger())
        phrase_readings = {
            token["text"]: token.get("reading") for token in phrase_tokens
        }
        self.assertEqual(phrase_readings["辛さ"], "からさ")
        self.assertEqual(phrase_readings["餃子"], "ぎょうざ")
        self.assertEqual(phrase_readings["一品"], "いっぴん")

    def test_chinese_tokens_reconstruct_text(self) -> None:
        text = "西安在秦岭与渭河之间。"
        tokens = zh_tokens(text)
        self.assertEqual("".join(token["text"] for token in tokens), text)

    def test_ideographic_zero_years_keep_complete_pinyin(self) -> None:
        tokens = zh_tokens("一三八〇年到二〇二六年")
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["一三八〇年"], "yī sān bā líng nián")
        self.assertEqual(readings["二〇二六年"], "èr líng èr liù nián")

    def test_japanese_year_and_duration_readings(self) -> None:
        tokens = ja_tokens("一三八〇年より四年早い", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["一三八〇年"], "せんさんびゃくはちじゅうねん")
        self.assertEqual(readings["四年"], "よねん")

    def test_xian_itinerary_day_readings(self) -> None:
        tokens = ja_tokens("二日、三日、四日、五日", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["二日"], "ふつか")
        self.assertEqual(readings["三日"], "みっか")
        self.assertEqual(readings["四日"], "よっか")
        self.assertEqual(readings["五日"], "いつか")

    def test_xian_itinerary_duration_readings(self) -> None:
        tokens = ja_tokens("二日間、三日間、四日間、五日間", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["二日間"], "ふつかかん")
        self.assertEqual(readings["三日間"], "みっかかん")
        self.assertEqual(readings["四日間"], "よっかかん")
        self.assertEqual(readings["五日間"], "いつかかん")

    def test_xian_itinerary_chinese_phrase_segmentation(self) -> None:
        tokens = zh_tokens("把休息写进行程，参观从葬坑。")
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["写进行程"], "xiějìn xíngchéng")
        self.assertEqual(readings["从葬坑"], "cóngzàngkēng")

    def test_qin_dynasty_reading_is_not_the_japanese_surname(self) -> None:
        tokens = ja_tokens("秦の軍陣", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["秦"], "しん")

    def test_lishan_garden_place_reading(self) -> None:
        tokens = ja_tokens("麗山園へ移る", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["麗山園"], "りざんえん")

    def test_katakana_conversion(self) -> None:
        self.assertEqual(katakana_to_hiragana("セイアン"), "せいあん")

    def test_unicode_reading_validators(self) -> None:
        self.assertTrue(valid_pinyin("xī'ān"))
        self.assertTrue(valid_furigana("しょうろう"))
        self.assertFalse(valid_furigana("鐘楼"))

    def test_chapter_filter_preserves_other_reviewed_layers(self) -> None:
        reviewed = {
            "zh": {
                "system": "hanyu-pinyin-tone-marks",
                "status": "reviewed",
                "review_notes": ["keep"],
                "tokens": [{"text": "西安", "reading": "xī'ān"}],
            },
            "ja": {
                "system": "furigana",
                "status": "reviewed",
                "review_notes": ["keep"],
                "tokens": [{"text": "西安", "reading": "せいあん"}],
            },
        }
        document = {
            "chapters": [
                {
                    "id": "ch01",
                    "blocks": [
                        {
                            "text": {"zh": "西安", "ja": "西安"},
                            "readings": deepcopy(reviewed),
                        }
                    ],
                },
                {
                    "id": "ch04",
                    "blocks": [
                        {
                            "text": {"zh": "碑林", "ja": "碑林"},
                            "readings": {},
                        }
                    ],
                },
            ]
        }
        result = add_candidates(document, chapter_ids={"ch04"})
        self.assertEqual(result["chapters"][0]["blocks"][0]["readings"], reviewed)
        self.assertEqual(
            result["chapters"][1]["blocks"][0]["readings"]["zh"]["tokens"],
            [{"text": "碑林", "reading": "bēilín"}],
        )


if __name__ == "__main__":
    unittest.main()
