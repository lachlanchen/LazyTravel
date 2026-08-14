#!/usr/bin/env python3
"""Generate deterministic pinyin and furigana candidates for editorial review."""

from __future__ import annotations

import argparse
import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

import jieba
import unidic_lite
from fugashi import Tagger
from pypinyin import Style, pinyin

logging.getLogger("jieba").setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "data/china/cities/xian/book.json"
DEFAULT_OUTPUT = ROOT / "build/editorial/xian/reading-candidates.json"
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
HAN_RUN_RE = re.compile(r"([\u3400-\u4dbf\u4e00-\u9fff]+)")

ZH_OVERRIDES = {
    "阿房宫": "ēpánggōng",
    "八水": "bāshuǐ",
    "白鹿原": "báilùyuán",
    "兵马俑": "bīngmǎyǒng",
    "兵马俑坑": "bīngmǎyǒngkēng",
    "兵马俑博物馆": "bīngmǎyǒng bówùguǎn",
    "彩绘": "cǎihuì",
    "长安": "cháng'ān",
    "长": "cháng",
    "得": "de",
    "二号坑": "èrhàokēng",
    "丰镐": "fēnghào",
    "丰京": "fēngjīng",
    "封土": "fēngtǔ",
    "滈河": "hàohé",
    "关中": "guānzhōng",
    "汉长安": "hàn cháng'ān",
    "汉长安城": "hàn cháng'ānchéng",
    "皇城": "huángchéng",
    "宫城": "gōngchéng",
    "华清宫": "huáqīnggōng",
    "甲片": "jiǎpiàn",
    "将军俑": "jiāngjūnyǒng",
    "临潼": "líntóng",
    "陵园": "língyuán",
    "龙首原": "lóngshǒuyuán",
    "大明宫": "dàmínggōng",
    "大兴城": "dàxīngchéng",
    "大雁塔": "dàyàntǎ",
    "明清西安": "míng-qīng xī'ān",
    "哪个": "nǎge",
    "秦岭": "qínlǐng",
    "秦咸阳": "qín xiányáng",
    "秦始皇陵": "qín shǐhuánglíng",
    "秦始皇帝陵": "qín shǐhuángdìlíng",
    "秦始皇帝陵丽山园": "qín shǐhuángdìlíng lìshānyuán",
    "曲尺形": "qūchǐxíng",
    "三号坑": "sānhàokēng",
    "探方": "tànfāng",
    "陶俑": "táoyǒng",
    "未央宫": "wèiyānggōng",
    "少陵原": "shàolíngyuán",
    "隋大兴": "suí dàxīng",
    "隋大兴城": "suí dàxīngchéng",
    "外郭城": "wàiguōchéng",
    "一号坑": "yīhàokēng",
    "俑坑": "yǒngkēng",
    "台塬": "táiyuán",
    "唐长安": "táng cháng'ān",
    "唐长安城": "táng cháng'ānchéng",
    "西安": "xī'ān",
    "西安府": "xī'ānfǔ",
    "小雁塔": "xiǎoyàntǎ",
    "奉元路": "fèngyuánlù",
    "南大街": "nándàjiē",
    "镐京": "hàojīng",
    "潏河": "juéhé",
    "潏": "jué",
    "渭河": "wèihé",
    "泾河": "jīnghé",
    "沣河": "fēnghé",
    "涝河": "láohé",
    "涝": "láo",
    "浐河": "chǎnhé",
    "灞河": "bàhé",
    "丽山园": "lìshānyuán",
    "弩兵": "nǔbīng",
    "夯土": "hāngtǔ",
}

JA_OVERRIDES = {
    "一日": "いちにち",
    "阿房宮": "あぼうきゅう",
    "八水": "はっすい",
    "八つ": "やっつ",
    "白鹿原": "はくろくげん",
    "兵馬俑坑": "へいばようこう",
    "兵馬俑博物館": "へいばようはくぶつかん",
    "版築": "はんちく",
    "歩兵": "ほへい",
    "長安": "ちょうあん",
    "豊鎬": "ほうこう",
    "豊京": "ほうけい",
    "鎬京": "こうけい",
    "滈河": "こうが",
    "関中": "かんちゅう",
    "漢長安": "かんちょうあん",
    "漢長安城": "かんちょうあんじょう",
    "咸陽宮": "かんようきゅう",
    "華清宮": "かせいきゅう",
    "皇城": "こうじょう",
    "宮城": "きゅうじょう",
    "軍陣": "ぐんじん",
    "臨潼": "りんどう",
    "陵園": "りょうえん",
    "月": "がつ",
    "龍首原": "りゅうしゅげん",
    "大明宮": "だいめいきゅう",
    "大街": "だいがい",
    "大雁塔": "だいがんとう",
    "明清西安": "みんしんせいあん",
    "明代": "みんだい",
    "韓建": "かんけん",
    "秦嶺": "しんれい",
    "秦咸陽": "しんかんよう",
    "秦始皇帝陵": "しんしこうていりょう",
    "凹字形": "おうじけい",
    "三号坑": "さんごうこう",
    "陶俑": "とうよう",
    "未央宮": "びおうきゅう",
    "少陵原": "しょうりょうげん",
    "鐘楼": "しょうろう",
    "都城": "とじょう",
    "二関": "にかん",
    "二号坑": "にごうこう",
    "何が": "なにが",
    "何も": "なにも",
    "何を": "なにを",
    "四関": "しかん",
    "四つ": "よっつ",
    "大興城": "だいこうじょう",
    "外郭城": "がいかくじょう",
    "一号坑": "いちごうこう",
    "俑坑": "ようこう",
    "唐長安": "とうちょうあん",
    "唐長安城": "とうちょうあんじょう",
    "西安": "せいあん",
    "西安府": "せいあんふ",
    "小雁塔": "しょうがんとう",
    "奉元路": "ほうげんろ",
    "南大街": "なんだいがい",
    "潏河": "けつが",
    "渭河": "いが",
    "泾河": "けいが",
    "沣河": "ほうが",
    "涝河": "ろうが",
    "浐河": "さんが",
    "灞河": "はが",
    "弩兵": "どへい",
    "麗山園": "れいざんえん",
}


def plain_syllable(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    return "".join(character for character in normalized if not unicodedata.combining(character))


def pinyin_for_word(value: str) -> str:
    if value in ZH_OVERRIDES:
        return ZH_OVERRIDES[value]
    syllables = [
        item[0]
        for item in pinyin(
            value,
            style=Style.TONE,
            heteronym=False,
            strict=False,
            errors=lambda text: list(text),
        )
    ]
    joined = ""
    for syllable in syllables:
        bare = plain_syllable(syllable).lower()
        if joined and bare.startswith(("a", "e", "o")):
            joined += "'"
        joined += syllable.lower()
    return joined


def zh_tokens(value: str) -> list[dict[str, str]]:
    pieces: list[dict[str, str]] = []
    for token in jieba.cut(value, cut_all=False, HMM=False):
        for part in filter(None, HAN_RUN_RE.split(token)):
            item = {"text": part}
            if HAN_RE.search(part):
                item["reading"] = pinyin_for_word(part)
            pieces.append(item)
    if "".join(item["text"] for item in pieces) != value:
        raise ValueError("Chinese tokenization did not preserve the source text")
    return pieces


def katakana_to_hiragana(value: str) -> str:
    return "".join(
        chr(ord(character) - 0x60) if "\u30a1" <= character <= "\u30f6" else character
        for character in value
    )


def unidic_tagger() -> Tagger:
    options = f"-r {unidic_lite.DICDIR}/mecabrc -d {unidic_lite.DICDIR}"
    return Tagger(options)


def ja_tokens(value: str, tagger: Tagger) -> list[dict[str, str]]:
    override_pattern = re.compile(
        "(" + "|".join(re.escape(key) for key in sorted(JA_OVERRIDES, key=len, reverse=True)) + ")"
    )
    pieces: list[dict[str, str]] = []
    for part in filter(None, override_pattern.split(value)):
        if part in JA_OVERRIDES:
            pieces.append({"text": part, "reading": JA_OVERRIDES[part]})
            continue
        for word in tagger(part):
            item = {"text": word.surface}
            if HAN_RE.search(word.surface):
                candidate = word.feature.kana or word.feature.pron
                if not candidate:
                    raise ValueError(f"missing Japanese reading for {word.surface!r}")
                item["reading"] = katakana_to_hiragana(candidate)
            pieces.append(item)
    if "".join(item["text"] for item in pieces) != value:
        raise ValueError("Japanese tokenization did not preserve the source text")
    return pieces


def add_candidates(document: dict[str, Any], status: str = "candidate") -> dict[str, Any]:
    tagger = unidic_tagger()
    review_note = (
        "Reviewed against the chapter-specific reading audit."
        if status == "reviewed"
        else "Machine-assisted candidate; editorial review required before publication."
    )
    for chapter in document["chapters"]:
        for block in chapter["blocks"]:
            block["readings"] = {
                "zh": {
                    "system": "hanyu-pinyin-tone-marks",
                    "status": status,
                    "review_notes": [review_note],
                    "tokens": zh_tokens(block["text"]["zh"]),
                },
                "ja": {
                    "system": "furigana",
                    "status": status,
                    "review_notes": [review_note],
                    "tokens": ja_tokens(block["text"]["ja"], tagger),
                },
            }
    return document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--status",
        choices=("candidate", "reviewed"),
        default="candidate",
        help="mark generated layers reviewed only after completing the editorial audit",
    )
    args = parser.parse_args()

    for word in ZH_OVERRIDES:
        jieba.add_word(word, freq=2_000_000)
    document = json.loads(args.book.read_text(encoding="utf-8"))
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(add_candidates(document, args.status), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"reading candidates: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
