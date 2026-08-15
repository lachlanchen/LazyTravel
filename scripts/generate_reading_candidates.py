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
HAN_RE = re.compile(r"[\u3007\u3400-\u4dbf\u4e00-\u9fff]")
HAN_RUN_RE = re.compile(r"([\u3007\u3400-\u4dbf\u4e00-\u9fff]+)")

ZH_OVERRIDES = {
    "阿房宫": "ēpánggōng",
    "八水": "bāshuǐ",
    "白鹿原": "báilùyuán",
    "兵马俑": "bīngmǎyǒng",
    "兵马俑坑": "bīngmǎyǒngkēng",
    "兵马俑博物馆": "bīngmǎyǒng bówùguǎn",
    "不适": "bùshì",
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
    "华清池": "huáqīngchí",
    "华山": "huàshān",
    "华山北站": "huàshān běizhàn",
    "华山南峰": "huàshān nánfēng",
    "汉景帝": "hàn jǐngdì",
    "汉景帝阳陵博物院": "hàn jǐngdì yánglíng bówùyuàn",
    "汉阳陵": "hàn yánglíng",
    "外藏坑": "wàicángkēng",
    "王皇后": "wáng huánghòu",
    "翠华山": "cuìhuáshān",
    "乾陵": "qiánlíng",
    "乾县": "qiánxiàn",
    "乾县站": "qiánxiànzhàn",
    "堰塞湖": "yànsèhú",
    "西安事变": "xī'ān shìbiàn",
    "唐御汤遗址博物馆": "táng yùtāng yízhǐ bówùguǎn",
    "五间厅": "wǔjiāntīng",
    "述圣纪碑": "shùshèngjìbēi",
    "无字碑": "wúzìbēi",
    "永泰公主墓": "yǒngtài gōngzhǔmù",
    "甲片": "jiǎpiàn",
    "将军俑": "jiāngjūnyǒng",
    "临潼": "líntóng",
    "陵园": "língyuán",
    "龙首原": "lóngshǒuyuán",
    "大慈恩寺": "dàcí'ēnsì",
    "大明宫": "dàmínggōng",
    "大秦景教流行中国碑": "dàqín jǐngjiào liúxíng zhōngguó bēi",
    "大唐三藏圣教序": "dàtáng sānzàng shèngjiàoxù",
    "大兴城": "dàxīngchéng",
    "大雁塔": "dàyàntǎ",
    "明清西安": "míng-qīng xī'ān",
    "碑林": "bēilín",
    "传拓": "chuántà",
    "拓包": "tàbāo",
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
    "舍利": "shèlì",
    "隋大兴": "suí dàxīng",
    "隋大兴城": "suí dàxīngchéng",
    "外郭城": "wàiguōchéng",
    "一号坑": "yīhàokēng",
    "一行行": "yīhángháng",
    "俑坑": "yǒngkēng",
    "台塬": "táiyuán",
    "唐长安": "táng cháng'ān",
    "唐长安城": "táng cháng'ānchéng",
    "褚遂良": "chǔ suìliáng",
    "荐福寺": "jiànfúsì",
    "密檐式": "mìyánshì",
    "景教": "jǐngjiào",
    "景净": "jǐngjìng",
    "经卷": "jīngjuàn",
    "开成石经": "kāichéng shíjīng",
    "吕大忠": "lǚ dàzhōng",
    "吕秀岩": "lǚ xiùyán",
    "墨拓": "mòtà",
    "石台孝经": "shítái xiàojīng",
    "拓本": "tàběn",
    "拓片": "tàpiàn",
    "稍干": "shāogān",
    "重刻": "chóngkè",
    "重排": "chóngpái",
    "西安": "xī'ān",
    "西安碑林博物馆": "xī'ān bēilín bówùguǎn",
    "西安博物院": "xī'ān bówùyuàn",
    "西安府": "xī'ānfǔ",
    "小雁塔": "xiǎoyàntǎ",
    "玄奘": "xuánzàng",
    "聂斯脱里": "nièsītuōlǐ",
    "叙利亚": "xùlìyà",
    "义净": "yìjìng",
    "奉元路": "fèngyuánlù",
    "安定门": "āndìngmén",
    "安远门": "ānyuǎnmén",
    "北广济街": "běiguǎngjìjiē",
    "北院门": "běiyuànmén",
    "长乐门": "chánglèmén",
    "大皮院": "dàpíyuàn",
    "鼓楼": "gǔlóu",
    "广济街": "guǎngjìjiē",
    "化觉巷": "huàjuéxiàng",
    "化觉巷清真大寺": "huàjuéxiàng qīngzhēn dàsì",
    "回坊": "huífāng",
    "回民街": "huímínjiē",
    "礼拜大殿": "lǐbài dàdiàn",
    "莲湖区志": "liánhú qūzhì",
    "南大街": "nándàjiē",
    "清真大寺": "qīngzhēn dàsì",
    "清真寺": "qīngzhēnsì",
    "陕西省志": "shǎnxī shěngzhì",
    "书院门": "shūyuànmén",
    "西安府志": "xī'ān fǔzhì",
    "西大街": "xīdàjiē",
    "西羊市": "xīyángshì",
    "永宁门": "yǒngníngmén",
    "钟楼": "zhōnglóu",
    "周长为": "zhōucháng wéi",
    "均为": "jūn wéi",
    "标为": "biāo wéi",
    "列为": "lièwéi",
    "为准": "wéi zhǔn",
    "走完": "zǒuwán",
    "全程": "quánchéng",
    "全圈": "quánquān",
    "征得": "zhēngdé",
    "四进院落": "sìjìn yuànluò",
    "十三点七四": "shísān diǎn qī sì",
    "一三八四年": "yī sān bā sì nián",
    "一五八二年": "yī wǔ bā èr nián",
    "一三八〇年": "yī sān bā líng nián",
    "一三九二年": "yī sān jiǔ èr nián",
    "七四二年": "qī sì èr nián",
    "二〇二六年": "èr líng èr liù nián",
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
    "官网": "guānwǎng",
    "神合": "shénhé",
    "译场": "yìchǎng",
    "白吉馍": "báijímó",
    "biangbiang面": "biangbiangmiàn",
    "报恩寺街": "bào'ēnsìjiē",
    "腊牛肉夹馍": "làniúròujiāmó",
    "腊羊肉夹馍": "làyángròujiāmó",
    "羊肉夹馍": "yángròujiāmó",
    "腊汁肉夹馍": "làzhīròujiāmó",
    "凉皮": "liángpí",
    "擀面皮": "gǎnmiànpí",
    "米皮": "mǐpí",
    "面皮": "miànpí",
    "牛羊肉泡馍": "niúyángròupàomó",
    "泡馍": "pàomó",
    "肉夹馍": "ròujiāmó",
    "肉丸胡辣汤": "ròuwán húlàtāng",
    "洒金桥": "sǎjīnqiáo",
    "少辣": "shǎolà",
    "水围城": "shuǐwéichéng",
    "饦饦馍": "tuōtuōmó",
    "小南门": "xiǎonánmén",
    "油茶麻花": "yóuchá máhuā",
    "永兴坊": "yǒngxīngfāng",
    "甑糕": "zènggāo",
    "臊子": "sàozi",
    "口汤": "kǒutāng",
    "干泡": "gānpào",
    "葫芦头泡馍": "húlutóu pàomó",
    "饺子宴": "jiǎozǐyàn",
    "干拌": "gānbàn",
    "干湿": "gānshī",
    "见长": "jiàncháng",
    "嚼劲": "jiáojìn",
    "为原料": "wéi yuánliào",
    "油泼": "yóupō",
    "一摊接一摊地": "yìtān jiē yìtān de",
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
    "華清池": "かせいち",
    "華山": "かざん",
    "華山北駅": "かざんきたえき",
    "漢景帝": "かんけいてい",
    "漢陽陵": "かんようりょう",
    "景帝": "けいてい",
    "王皇后": "おうこうごう",
    "外蔵坑": "がいぞうこう",
    "陪葬坑": "ばいそうこう",
    "陪葬墓": "ばいそうぼ",
    "陪葬": "ばいそう",
    "翠華山": "すいかざん",
    "乾陵": "けんりょう",
    "乾県": "けんけん",
    "乾県駅": "けんけんえき",
    "堰塞湖": "えんそくこ",
    "西安事件": "せいあんじけん",
    "唐御湯": "とうぎょとう",
    "遺跡博物館": "いせきはくぶつかん",
    "五間庁": "ごけんちょう",
    "驪山": "りざん",
    "西峰": "せいほう",
    "北峰": "ほくほう",
    "五峰": "ごほう",
    "秦陵": "しんりょう",
    "石海": "せっかい",
    "崩積洞": "ほうせきどう",
    "核心保護区域": "かくしんほごくいき",
    "縦走": "じゅうそう",
    "門闕跡": "もんけつあと",
    "翼馬": "よくば",
    "浮彫": "うきぼり",
    "述聖紀碑": "じゅつせいきひ",
    "無字碑": "むじひ",
    "儀仗": "ぎじょう",
    "帝陵": "ていりょう",
    "主墓室": "しゅぼしつ",
    "未発掘": "みはっくつ",
    "永泰公主墓": "えいたいこうしゅぼ",
    "墓道": "ぼどう",
    "山内": "さんない",
    "皇城": "こうじょう",
    "宮城": "きゅうじょう",
    "軍陣": "ぐんじん",
    "臨潼": "りんどう",
    "陵園": "りょうえん",
    "月": "がつ",
    "龍首原": "りゅうしゅげん",
    "大慈恩寺": "だいじおんじ",
    "大明宮": "だいめいきゅう",
    "大秦景教流行中国碑": "だいしんけいきょうりゅうこうちゅうごくひ",
    "大唐三蔵聖教序": "だいとうさんぞうしょうぎょうじょ",
    "大街": "だいがい",
    "大雁塔": "だいがんとう",
    "明清西安": "みんしんせいあん",
    "明代": "みんだい",
    "密檐式": "みつえんしき",
    "七層": "しちそう",
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
    "四年": "よねん",
    "大興城": "だいこうじょう",
    "外郭城": "がいかくじょう",
    "一号坑": "いちごうこう",
    "俑坑": "ようこう",
    "唐長安": "とうちょうあん",
    "唐長安城": "とうちょうあんじょう",
    "訳場": "やくじょう",
    "碑林": "ひりん",
    "景教": "けいきょう",
    "景浄": "けいじょう",
    "開成石経": "かいせいせっけい",
    "呂秀岩": "りょしゅうがん",
    "墨拓": "ぼくたく",
    "石台孝経": "せきだいこうきょう",
    "拓本": "たくほん",
    "褚遂良": "ちょすいりょう",
    "西安": "せいあん",
    "西安碑林博物館": "せいあんひりんはくぶつかん",
    "西安博物院": "せいあんはくぶついん",
    "西安府": "せいあんふ",
    "小雁塔": "しょうがんとう",
    "薦福寺": "せんぷくじ",
    "薦福寺塔": "せんぷくじとう",
    "玄奘": "げんじょう",
    "義浄": "ぎじょう",
    "奉元路": "ほうげんろ",
    "永寧門": "えいねいもん",
    "北院門": "ほくいんもん",
    "化覚巷清真大寺": "かかくこうせいしんだいじ",
    "化覚巷": "かかくこう",
    "清真大寺": "せいしんだいじ",
    "清真寺": "せいしんじ",
    "回族街区": "かいぞくがいく",
    "回民街": "かいみんがい",
    "鼓楼": "ころう",
    "広済街": "こうさいがい",
    "北広済街": "ほくこうさいがい",
    "書院門": "しょいんもん",
    "西大街": "せいだいがい",
    "西羊市": "せいようし",
    "大皮院": "だいひいん",
    "礼拝大殿": "れいはいだいでん",
    "蓮湖区志": "れんこくし",
    "陝西省志": "せんせいしょうし",
    "西安府志": "せいあんふし",
    "南大街": "なんだいがい",
    "一周": "いっしゅう",
    "明初": "みんしょ",
    "環城路": "かんじょうろ",
    "月台": "げつだい",
    "十三・七四": "じゅうさんてんななよん",
    "一三八四年": "せんさんびゃくはちじゅうよねん",
    "一五八二年": "せんごひゃくはちじゅうにねん",
    "一三八〇年": "せんさんびゃくはちじゅうねん",
    "一三九二年": "せんさんびゃくきゅうじゅうにねん",
    "七四二年": "ななひゃくよんじゅうにねん",
    "二〇二六年": "にせんにじゅうろくねん",
    "潏河": "けつが",
    "渭河": "いが",
    "泾河": "けいが",
    "沣河": "ほうが",
    "涝河": "ろうが",
    "浐河": "さんが",
    "灞河": "はが",
    "弩兵": "どへい",
    "甲片": "こうへん",
    "麗山園": "れいざんえん",
    "神合": "しんごう",
    "国子監": "こくしかん",
    "呂大忠": "りょだいちゅう",
    "114石": "ひゃくじゅうよんせき",
    "火曜日": "かようび",
    "白吉饃": "ばいじーもー",
    "報恩寺街": "ほうおんじがい",
    "臘牛肉夾饃": "らーにゅうろうじゃーもー",
    "臘羊肉夾饃": "らーやんろうじゃーもー",
    "羊肉夾饃": "やんろうじゃーもー",
    "臘汁肉夾饃": "らーじーろうじゃーもー",
    "臘牛肉": "らーにゅうろう",
    "臘羊肉": "らーやんろう",
    "涼皮": "りゃんぴー",
    "擀面皮": "がんみぇんぴー",
    "米皮": "みーぴー",
    "面皮": "みぇんぴー",
    "牛羊肉泡饃": "にゅうやんろうぱおもー",
    "泡饃": "ぱおもー",
    "肉夾饃": "ろうじゃーもー",
    "肉丸胡辣湯": "ろうわんふーらーたん",
    "洒金橋": "さいきんきょう",
    "水囲城": "しゅいうぇいちょん",
    "飥飥饃": "とぅおとぅおもー",
    "小南門": "しょうなんもん",
    "油茶麻花": "ようちゃーまーほわー",
    "油潑": "ようぽー",
    "永興坊": "えいこうぼう",
    "甑糕": "ずんがお",
    "臊子": "さおず",
    "口湯": "こうたん",
    "乾泡": "がんぱお",
    "葫蘆頭泡饃": "ふーるーとうぱおもー",
    "餃子宴": "ぎょうざえん",
    "夾饃": "じゃーもー",
    "小吃": "しゃおちー",
    "清真": "せいしん",
    "一か所": "いっかしょ",
    "一品": "いっぴん",
    "一種類": "いっしゅるい",
    "餃子": "ぎょうざ",
    "落花生": "らっかせい",
    "米": "こめ",
    "辛く": "からく",
    "辛さ": "からさ",
    "蒸す": "むす",
    "糖蒜": "たんすわん",
    "通ぶる": "つうぶる",
    "油茶": "ようちゃー",
    "麻花": "まーほわー",
    "饃": "もー",
}

ZH_LITERAL_SPAN_OVERRIDES = {
    key: ZH_OVERRIDES[key] for key in ("一三八〇年", "二〇二六年")
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
    literal_pattern = re.compile(
        "("
        + "|".join(
            re.escape(key)
            for key in sorted(ZH_LITERAL_SPAN_OVERRIDES, key=len, reverse=True)
        )
        + ")"
    )
    for span in filter(None, literal_pattern.split(value)):
        if span in ZH_LITERAL_SPAN_OVERRIDES:
            pieces.append({"text": span, "reading": ZH_LITERAL_SPAN_OVERRIDES[span]})
            continue
        for token in jieba.cut(span, cut_all=False, HMM=False):
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


def add_candidates(
    document: dict[str, Any],
    status: str = "candidate",
    chapter_ids: set[str] | None = None,
) -> dict[str, Any]:
    tagger = unidic_tagger()
    review_note = (
        "Reviewed against the chapter-specific reading audit."
        if status == "reviewed"
        else "Machine-assisted candidate; editorial review required before publication."
    )
    for chapter in document["chapters"]:
        if chapter_ids is not None and chapter["id"] not in chapter_ids:
            continue
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
    parser.add_argument(
        "--chapter",
        action="append",
        dest="chapter_ids",
        help="update only this chapter; may be repeated (default: all chapters)",
    )
    args = parser.parse_args()

    for word in ZH_OVERRIDES:
        jieba.add_word(word, freq=2_000_000)
    document = json.loads(args.book.read_text(encoding="utf-8"))
    chapter_ids = set(args.chapter_ids) if args.chapter_ids else None
    if chapter_ids is not None:
        known_ids = {chapter["id"] for chapter in document["chapters"]}
        unknown_ids = sorted(chapter_ids - known_ids)
        if unknown_ids:
            parser.error(f"unknown chapter id(s): {', '.join(unknown_ids)}")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            add_candidates(document, args.status, chapter_ids),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"reading candidates: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
