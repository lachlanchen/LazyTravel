# Chapter 2 Reading Review

Status: reviewed on `2026-08-16`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation and kana-only spans remain unannotated.
- Concatenating token text reproduces the canonical paragraph exactly.
- The B6 PDF and responsive website consume the same reviewed token arrays.

## Language Passes

The Chinese pass checked the transport and place forms used in this chapter,
including `小田原`, `箱根汤本`, `箱根登山线`, `小田急`, `浪漫特快`,
`周游券`, `汤坂路`, `畑宿`, and `三岛`. It also corrected context-dependent
readings such as `同行（tóngxíng）` and retained Arabic numerals for dated,
time-sensitive information so the pocket page remains legible.

The Japanese pass checked local names and operator usage, including
`小田原（おだわら）`, `箱根湯本（はこねゆもと）`,
`箱根登山線（はこねとざんせん）`, `小田急（おだきゅう）`,
`湯坂路（ゆさかみち）`, `畑宿（はたじゅく）`, and `三島（みしま）`.
The audit separately corrected counters and compounds such as
`一階（いっかい）`, `三階（さんがい）`, `八十分（はちじゅっぷん）`,
and `乗車日（じょうしゃび）`.

The English pass was edited independently. It distinguishes a rail gateway
from the mountain threshold, separates durable route history from dated fare
and luggage details, and keeps late-arrival advice direct rather than dramatic.

## Validation

- Chapter 2 Chinese: `990` tokens across nine aligned blocks.
- Chapter 2 Japanese: `1,184` tokens across nine aligned blocks.
- Chapter 2 browser rendering: `1,327` visible ruby nodes across both reading
  languages.
- Combined Chapters 1-2: `1,838` Chinese tokens and `2,282` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- No missing Han reading, invalid numeric-tone pinyin, or missing kanji reading
  is accepted by `scripts/validate_readings.py`.
