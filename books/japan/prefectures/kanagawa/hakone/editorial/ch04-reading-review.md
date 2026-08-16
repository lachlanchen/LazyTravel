# Chapter 4 Reading Review

Status: reviewed on `2026-08-17`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation, kana-only spans, and literal whitespace remain unannotated.
- Concatenating token text reproduces each canonical paragraph exactly.
- The B6 PDF and website consume the same reviewed token arrays.

## Language Passes

The Chinese pass checked the route and geosite forms `强罗`, `早云山`,
`大涌谷`, `姥子`, `桃源台`, `芦之湖`, `神山`, `冠岳`, `大地狱`,
`自然研究路`, `延命地藏`, and `极乐茶屋`. It preserves digit-by-digit
readings for written historical dates and separates `现场` from the following
modal verb so ruby does not create a false compound.

The Japanese pass checked `強羅（ごうら）`, `早雲山（そううんざん）`,
`大涌谷（おおわくだに）`, `姥子（うばこ）`,
`桃源台（とうげんだい）`, `芦ノ湖（あしのこ）`,
`神山（かみやま）`, `冠ヶ岳（かんむりがたけ）`,
`大地獄（おおじごく）`, and `行幸啓（ぎょうこうけい）`. Counters,
dates, opening times, `臭い（におい）`, and the two contextual readings of
`次` were reviewed. Literal whitespace in `OWAKUDANI KITCHEN` is preserved by
the deterministic tokenizer.

The English pass was edited independently. It distinguishes a same-day trail
slot from public access, a black egg from lunch, and a conditional Fuji view
from the value of the crossing itself. Safety language follows the operator's
different levels of prohibition and caution.

## Validation

- Chapter 4 Chinese: `1,153` tokens across nine aligned blocks.
- Chapter 4 Japanese: `1,422` tokens across nine aligned blocks.
- Chapter 4 browser rendering: `1,599` visible ruby nodes.
- Combined Chapters 1-4: `4,070` Chinese tokens and `4,976` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- No candidate status, missing Han reading, invalid numeric-tone pinyin, or
  missing kanji reading is accepted by `scripts/validate_readings.py`.
