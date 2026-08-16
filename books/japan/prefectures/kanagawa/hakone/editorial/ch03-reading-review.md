# Chapter 3 Reading Review

Status: reviewed on `2026-08-17`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation and kana-only spans remain unannotated.
- Concatenating token text reproduces the canonical paragraph exactly.
- The B6 PDF and responsive website consume the same reviewed token arrays.

## Language Passes

The Chinese pass checked the railway and place forms used in this chapter,
including `大平台`, `上大平台`, `出山`, `宫之下`, `小涌谷`, `雕刻之森`,
`强罗`, and `早云山`. It corrected the context readings for
`黏着力（niánzhuólì）` and `长椅（chángyǐ）`, and keeps the digit-by-digit
reading of `一九一九年` explicit.

The Japanese pass checked operator usage and local readings, including
`出山（でやま）`, `大平台（おおひらだい）`,
`上大平台（かみおおひらだい）`, `小涌谷（こわきだに）`,
`彫刻の森（ちょうこくのもり）`, `強羅（ごうら）`, and
`早雲山（そううんざん）`. The audit also corrected `欧米（おうべい）` and
the minute counters in `二十分`, `三十分`, `六十分`, and `九十分`.

The English pass was edited independently. It keeps railway engineering tied
to what the traveler sees, distinguishes a short cafe stop from a full meal,
and does not present generic refreshments as traditional Hakone food.

## Validation

- Chapter 3 Chinese: `1,079` tokens across nine aligned blocks.
- Chapter 3 Japanese: `1,272` tokens across nine aligned blocks.
- Chapter 3 browser rendering: `1,402` visible ruby nodes.
- Combined Chapters 1-3: `2,917` Chinese tokens and `3,554` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- No missing Han reading, invalid numeric-tone pinyin, or missing kanji reading
  is accepted by `scripts/validate_readings.py`.
