# Chapter 5 Reading Review

Status: reviewed on `2026-08-17`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation, kana-only spans, and literal whitespace remain unannotated.
- Concatenating token text reproduces each canonical paragraph exactly.
- The B6 PDF and website consume the same reviewed token arrays.

## Language Passes

The Chinese pass checked the route and place forms `桃源台`, `元箱根`,
`箱根町`, `芦之湖`, `箱根神社`, and `恩赐箱根公园`. The history and food
pass checked `筥根山缘起并序`, `万卷上人`, `源赖朝`, `二所诣`, `霞浦`,
`刺网渔`, `南蛮渍`, `甘露煮`, `佃煮`, and `湖畔展望馆`. Contextual
readings for `行`, `重`, `为`, `藏`, and `系` were reviewed rather than
accepted from the tokenizer without inspection.

The Japanese pass checked `桃源台（とうげんだい）`,
`元箱根（もとはこね）`, `箱根町（はこねまち）`,
`芦ノ湖（あしのこ）`, `箱根神社（はこねじんじゃ）`,
`恩賜箱根公園（おんしはこねこうえん）`, and
`湖畔展望館（こはんてんぼうかん）`. It also checked
`万巻上人（まんがんしょうにん）`,
`筥根山縁起并序（はこねさんえんぎならびにじょ）`,
`二所詣（にしょもうで）`, `霞ヶ浦（かすみがうら）`,
`刺網漁（さしあみりょう）`, and `白御影石（しろみかげいし）`.
The automatic errors `老杉（おいすぎ）` and `行先（いきさき）` were
replaced with the reviewed forms `ろうさん` and `ゆきさき`.

The English pass was edited independently. It keeps the port decision,
weather fallback, shrine chronology, food provenance, and former-villa site
clear without copying Japanese sentence structure or turning the chapter into
a detached history survey.

## Validation

- Chapter 5 Chinese: `1,247` tokens across ten aligned blocks.
- Chapter 5 Japanese: `1,580` tokens across ten aligned blocks.
- Combined Chapters 1-5: `5,317` Chinese tokens and `6,556` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- No candidate status, missing Han reading, invalid numeric-tone pinyin, or
  missing kanji reading is accepted by `scripts/validate_readings.py`.
- Browser proof renders `1,739` ruby nodes in Chapter 5 and `7,242` across the
  active Chapters 1-5, with no clipped or missing reading layer.
