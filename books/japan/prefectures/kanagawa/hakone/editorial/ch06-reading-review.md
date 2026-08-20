# Chapter 6 Reading Review

Status: reviewed on `2026-08-20`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation, kana-only spans, Latin route letters, Arabic digits, and literal
  whitespace remain unannotated.
- Concatenating token text reproduces each canonical paragraph exactly.
- The B6 PDF and website consume the same reviewed token arrays.

## Language Passes

The Chinese pass checked `元箱根`, `箱根町`, `东海道`, `箱根八里`,
`旧街道口`, `畑宿`, `箱根关所`, `江户口御门`, `大番所`, `上番休息所`,
`远见番所`, and `甘酒茶屋`. Contextual corrections include
`倒木（dǎomù）` and the paving verb `补铺（bǔpū）`. The historical years
`一六一九年`, `一七一一年`, `一八六五年`, and `二〇〇七年` use
digit-by-digit year readings instead of accidental word segmentation.

The Japanese pass checked `元箱根（もとはこね）`,
`杉並木（すぎなみき）`, `箱根八里（はこねはちり）`,
`旧街道口（きゅうかいどうぐち）`, `一里塚（いちりづか）`,
`甘酒茶屋（あまざけちゃや）`, `江戸口御門（えどぐちごもん）`,
`大番所（おおばんしょ）`,
`上番休息所（かみばんきゅうそくじょ）`, and
`遠見番所（とおみばんしょ）`. The contextual forms
`入り鉄砲（いりでっぽう）` and `山道（やまみち）` replace the
tokenizer's compound defaults.

The English pass was edited independently. It keeps the footing decision,
closure, checkpoint evidence, inspection practice, food stop, and bus exit
clear without following Chinese or Japanese syntax sentence by sentence.

## Validation

- Chapter 6 Chinese: `1,122` tokens across ten aligned blocks.
- Chapter 6 Japanese: `1,443` tokens across ten aligned blocks.
- Combined Chapters 1-6: `6,439` Chinese tokens and `7,999` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- No candidate status, missing Han reading, invalid numeric-tone pinyin, or
  missing kanji reading is accepted by `scripts/validate_readings.py`.
- The Chapter 6 browser proof renders `1,561` ruby nodes; the active Chapters
  1-6 render `8,803`, with no missing or clipped reading layer.
