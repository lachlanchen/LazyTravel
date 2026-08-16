# Chapter 11 Reading Review

Status: reviewed on `2026-08-16`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses hiragana furigana on kanji-bearing tokens; kana, Latin text,
  numerals, and punctuation remain unannotated.
- Concatenating token text reproduces the final Chinese or Japanese prose
  exactly.
- The B6 pocket PDF and website consume the same arrays in
  `data/china/cities/xian/book.json`.

## Editorial Audit

The Chinese pass checked travel phrases whose readings change with context.
Protected forms include `同一行 (tóngyī háng)`, `长时间
(chángshíjiān)`, `长距离 (chángjùlí)`, `不适合 (bù shìhé)`,
`二十四小时内 (èrshísì xiǎoshí nèi)`, and the emergency numbers
`一一〇 (yāo yāo líng)`, `一一九 (yāo yāo jiǔ)`, and `一二〇
(yāo èr líng)`. Proper-name checks include `陕西历史博物馆 (shǎnxī
lìshǐ bówùguǎn)`, `秦始皇帝陵博物院 (qín shǐhuángdìlíng
bówùyuàn)`, and `中国环境监测总站 (zhōngguó huánjìng jiāncè
zǒngzhàn)`.

The Japanese prose was revised independently before pronunciation review so
booking, hotel, weather, and emergency language reads as ordinary Japanese.
The pass then checked `来館日 (らいかんび)`, `休館日
(きゅうかんび)`, `出勤日 (しゅっきんび)`, `宿泊日
(しゅくはくび)`, `五日前 (いつかまえ)`, `十七時
(じゅうしちじ)`, `大気質 (たいきしつ)`, and `辛い
(からい)`. The three emergency numbers are rendered as `一一〇番
(ひゃくとうばん)`, `一一九番 (ひゃくじゅうきゅうばん)`, and
`一二〇番 (ひゃくにじゅうばん)`.

## Validation

- Chapter 11 Chinese: `1,668` tokens, including `1,368` ruby-bearing tokens.
- Chapter 11 Japanese: `2,165` tokens, including `945` ruby-bearing tokens.
- Full canonical book after Chapter 11: `13,468` Chinese tokens and `17,299`
  Japanese tokens.
- All `13` Chapter 11 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` checks reconstruction, Han coverage, review
  status, and tone marks before release.
