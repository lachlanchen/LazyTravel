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

    def test_xian_departure_chinese_context_readings(self) -> None:
        tokens = zh_tokens("写在同一行，长时间步行不适合时拨一一〇。")
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["同一行"], "tóngyī háng")
        self.assertEqual(readings["长时间"], "chángshíjiān")
        self.assertEqual(readings["不适合"], "bù shìhé")
        self.assertEqual(readings["一一〇"], "yāo yāo líng")

    def test_xian_departure_japanese_context_readings(self) -> None:
        tokens = ja_tokens(
            "来館日の五日前、十七時。休館日と大気質を確認し、一一〇番へ。",
            unidic_tagger(),
        )
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["来館日"], "らいかんび")
        self.assertEqual(readings["五日前"], "いつかまえ")
        self.assertEqual(readings["十七時"], "じゅうしちじ")
        self.assertEqual(readings["休館日"], "きゅうかんび")
        self.assertEqual(readings["大気質"], "たいきしつ")
        self.assertEqual(readings["一一〇番"], "ひゃくとうばん")

    def test_qin_dynasty_reading_is_not_the_japanese_surname(self) -> None:
        tokens = ja_tokens("秦の軍陣", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["秦"], "しん")

    def test_lishan_garden_place_reading(self) -> None:
        tokens = ja_tokens("麗山園へ移る", unidic_tagger())
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["麗山園"], "りざんえん")

    def test_hakone_ryokan_chinese_context_readings(self) -> None:
        tokens = zh_tokens("一九六五年，睡前写下一行，取得答复后留出空档。")
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["一九六五年"], "yī jiǔ liù wǔ nián")
        self.assertEqual(readings["写下一行"], "xiěxià yī háng")
        self.assertEqual(pinyin_for_word("取得"), "qǔdé")
        self.assertEqual(pinyin_for_word("空档"), "kòngdàng")

    def test_hakone_ryokan_japanese_readings(self) -> None:
        tokens = ja_tokens(
            "箱根七湯で一夜湯治。一九六五年、芦之湯の貸切風呂と客室風呂、朝風呂、一泊二食。",
            unidic_tagger(),
        )
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["箱根七湯"], "はこねななゆ")
        self.assertEqual(readings["一夜湯治"], "いちやとうじ")
        self.assertEqual(readings["一九六五年"], "せんきゅうひゃくろくじゅうごねん")
        self.assertEqual(readings["芦之湯"], "あしのゆ")
        self.assertEqual(readings["貸切風呂"], "かしきりぶろ")
        self.assertEqual(readings["客室風呂"], "きゃくしつぶろ")
        self.assertEqual(readings["朝風呂"], "あさぶろ")
        self.assertEqual(readings["一泊二食"], "いっぱくにしょく")
        line_tokens = ja_tokens("何時までに、一行だけ書く", unidic_tagger())
        line_readings = {
            token["text"]: token.get("reading") for token in line_tokens
        }
        self.assertEqual(line_readings["何時"], "なんじ")
        self.assertEqual(line_readings["一行"], "いちぎょう")

    def test_hakone_food_chinese_readings(self) -> None:
        tokens = zh_tokens(
            "一泊二食、板蒸鱼糕、鱼糜、天明年间、一七八一至一七八九年、力饼、风祭、面衣、交叉接触、食用期限、天妇罗、炸鱼糕、炸公鱼。"
        )
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["一泊二食"], "yībó èrshí")
        self.assertEqual(readings["板蒸鱼糕"], "bǎnzhēng yúgāo")
        self.assertEqual(readings["鱼糜"], "yúmí")
        self.assertEqual(readings["天明年间"], "tiānmíng niánjiān")
        self.assertEqual(
            readings["一七八一至一七八九年"],
            "yī qī bā yī zhì yī qī bā jiǔ nián",
        )
        self.assertEqual(readings["力饼"], "lìbǐng")
        self.assertEqual(readings["风祭"], "fēngjì")
        self.assertEqual(readings["面衣"], "miànyī")
        self.assertEqual(readings["交叉接触"], "jiāochā jiēchù")
        self.assertEqual(readings["食用期限"], "shíyòng qīxiàn")
        self.assertEqual(readings["天妇罗"], "tiānfùluó")
        self.assertEqual(readings["炸鱼糕"], "zhá yúgāo")
        self.assertEqual(readings["炸公鱼"], "zhá gōngyú")

    def test_hakone_food_japanese_readings(self) -> None:
        tokens = ja_tokens(
            "板付き蒸しかまぼこ、天明年間、米麹、消費期限、風祭。一杯、一皿、一回か二回。店が開いていない。",
            unidic_tagger(),
        )
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["板付き蒸しかまぼこ"], "いたつきむしかまぼこ")
        self.assertEqual(readings["天明年間"], "てんめいねんかん")
        self.assertEqual(readings["米麹"], "こめこうじ")
        self.assertEqual(readings["消費期限"], "しょうひきげん")
        self.assertEqual(readings["風祭"], "かざまつり")
        self.assertEqual(readings["一杯"], "いっぱい")
        self.assertEqual(readings["一皿"], "ひとさら")
        self.assertEqual(readings["一回"], "いっかい")
        self.assertEqual(readings["二回"], "にかい")
        self.assertEqual(readings["開いていない"], "あいていない")

    def test_hakone_stay_chinese_readings(self) -> None:
        self.assertEqual(pinyin_for_word("宫城野"), "gōngchéngyě")
        self.assertEqual(pinyin_for_word("塔之泽"), "tǎzhīzé")
        self.assertEqual(pinyin_for_word("芦之汤"), "lúzhītāng")

    def test_hakone_stay_japanese_readings(self) -> None:
        tokens = ja_tokens(
            "宮城野、小涌谷、塔ノ沢。翌朝の一本、不確かな区間。",
            unidic_tagger(),
        )
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["宮城野"], "みやぎの")
        self.assertEqual(readings["小涌谷"], "こわきだに")
        self.assertEqual(readings["塔ノ沢"], "とうのさわ")
        self.assertEqual(readings["翌朝"], "よくあさ")
        self.assertEqual(readings["一本"], "いっぽん")
        self.assertEqual(readings["不確か"], "ふたしか")
        self.assertEqual(readings["区間"], "くかん")

    def test_hakone_itinerary_museum_and_highland_readings(self) -> None:
        tokens = ja_tokens(
            "一日に一館、二館は入れず、高原の美術館を選ぶ。",
            unidic_tagger(),
        )
        readings = {token["text"]: token.get("reading") for token in tokens}
        self.assertEqual(readings["一日"], "いちにち")
        self.assertEqual(readings["一館"], "いっかん")
        self.assertEqual(readings["二館"], "にかん")
        self.assertEqual(readings["高原"], "こうげん")

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
