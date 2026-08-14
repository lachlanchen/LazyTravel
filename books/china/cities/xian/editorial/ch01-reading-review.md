# Chapter 1 Reading Review

Status: reviewed on `2026-08-14`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation and kana-only tokens remain unannotated.
- Concatenating token text must reproduce the canonical paragraph exactly.
- The book and website consume these same token arrays.

## Method

Candidate word boundaries came from Jieba for Chinese and UniDic Lite for
Japanese. Those tools did not decide publication readings. Proper names,
polyphonic characters, counters, and historical terms were reviewed and
overridden before the layers were marked `reviewed`.

The Chinese review checked `xī'ān`, `cháng'ān`, `qínlǐng`, `fēnghào`,
`shàolíngyuán`, `líntóng`, the eight river names, and dynasty-city compounds.
In particular, `潏` is `jué` in the Xi'an river name, not the more general
`yù` reading. The water-name reading is also documented in the 13th-edition
Xinhua Dictionary notice published by the
[Beijing municipal government](https://www.beijing.gov.cn/fuwu/bmfw/sy/jrts/202607/t20260727_4790219.html).

The Japanese review checked standard historical and geographic readings,
including `西安（せいあん）`, `長安（ちょうあん）`, `秦嶺（しんれい）`,
`鐘楼（しょうろう）`, `雁塔（がんとう）`, `関中（かんちゅう）`,
`豊鎬（ほうこう）`, `都城（とじょう）`, and the eight river names.
Counters such as `四つ（よっつ）` and `八つ（やっつ）` were corrected
rather than accepting isolated dictionary forms.

## Validation

- Chinese: `696` tokens; complete text reconstruction and Han-token coverage.
- Japanese: `886` tokens; complete text reconstruction and kanji-token coverage.
- No numeric-tone pinyin, missing reading, kanji-bearing furigana, or detached
  token is accepted by `scripts/validate_readings.py`.
