# Chapter 7 Language and Reading Review

Status: text and readings reviewed on `2026-08-20`; strict B6 and website gates
passed.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation, kana-only spans, Latin text, Arabic digits, and literal
  whitespace remain unannotated.
- Concatenating token text reproduces each canonical paragraph exactly.
- The B6 PDF and website consume the same reviewed token arrays.

## Chinese Pass

The Chinese pass follows one evening-to-morning stay and removes translated or
abstract phrasing. Arrival protects the booked dinner; the historical section
changes what the traveler verifies; bath, meal, room, and departure sections
each end in a concrete choice. It does not rank properties, treat discomfort as
authenticity, or call generic multi-course dining a Hakone specialty.

Reviewed place and context readings include `箱根七汤（xiānggēn qītāng）`,
`塔之泽（tǎzhīzé）`, `堂岛（tángdǎo）`, `宫之下（gōngzhīxià）`,
`底仓（dǐcāng）`, `木贺（mùhè）`, `芦之汤（lúzhītāng）`,
`一夜汤治（yīyè tāngzhì）`, `箱根十七汤（xiānggēn shíqītāng）`, and
`一九六五年（yī jiǔ liù wǔ nián）`. Contextual corrections include
`取得（qǔdé）`, `空档（kòngdàng）`, and the written-line reading in
`写下一行（xiěxià yī háng）`.

## Japanese Pass

The Japanese pass was edited as Japanese guide prose rather than a sentence-by-
sentence mirror. It replaces translated constructions around meal service,
keeps arrival and bath instructions ordinary, and treats bed, chair, privacy,
tattoo, and accessibility requirements as valid booking conditions.

Reviewed readings include `箱根七湯（はこねななゆ）`,
`一夜湯治（いちやとうじ）`, `一九六五年（せんきゅうひゃくろくじゅうごねん）`,
`芦之湯（あしのゆ）`, `貸切風呂（かしきりぶろ）`,
`客室風呂（きゃくしつぶろ）`, `朝風呂（あさぶろ）`,
`食事処（しょくじどころ）`, and `一泊二食（いっぱくにしょく）`.
The chapter-specific clock and written-line contexts use
`何時（なんじ）` and `一行（いちぎょう）`.

## English Pass

The English pass keeps the reservation clock, bath sequence, meal service,
room fit, and departure margin explicit. It removes clever or atmospheric
conclusions, does not copy Chinese or Japanese syntax, and uses the historical
section only to explain why district name, private access, and natural-onsen
status must be checked separately.

## Validation

- Chapter 7: ten aligned blocks and nine distinct citation records.
- Chapter 7 Chinese: `1,261` reviewed tokens.
- Chapter 7 Japanese: `1,563` reviewed tokens.
- Combined Chapters 1-7: `7,700` Chinese tokens and `9,562` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- The complete project suite passes `93` tests, including the Hakone ryokan
  contextual reading cases.
- Strict `scripts/validate_readings.py` passes with no candidate layer, missing
  Han reading, invalid pinyin, or missing kanji reading.
