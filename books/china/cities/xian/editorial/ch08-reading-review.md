# Chapter 8 Reading Review

Status: reviewed on `2026-08-16`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses hiragana furigana on kanji-bearing tokens; kana, Latin text,
  numerals, and punctuation remain unannotated.
- Concatenating token text reproduces the final Chinese or Japanese prose
  exactly.
- The B6 pocket PDF, practical bands, callout, and website consume the same
  arrays in `data/china/cities/xian/book.json`.

## Editorial Audit

The Chinese pass checked the exact hub and transport vocabulary, including
`西安北站 (xī'ān běizhàn)`, `西安站 (xī'ānzhàn)`, `西安东站
(xī'ān dōngzhàn)`, `咸阳机场 (xiányáng jīchǎng)`, `航站楼
(hángzhànlóu)`, `乘车区 (chéngchēqū)`, and `直梯 (zhítī)`.
`同行人` is explicitly read `tóngxíngrén`, not the business-context reading
of `同行`, and the route sentence now uses unambiguous `重新 (chóngxīn)`.

The Japanese pass checked station names, numbered lines, and arrival terms
independently. `四人` is `よにん`, standalone floor `階` is `かい`, and
`到着口` is `とうちゃくぐち`. The Chinese station signs `机场` and
`机场西` remain in their on-site forms and carry the guide readings
`くうこう` and `くうこうにし`; they are not silently rewritten into
Japanese display text.

## Validation

- Chapter 8 Chinese: `1,143` tokens, including `921` ruby-bearing tokens.
- Chapter 8 Japanese: `1,462` tokens, including `612` ruby-bearing tokens.
- Full canonical book after Chapter 8: `8,606` Chinese tokens and `10,938`
  Japanese tokens.
- All `12` Chapter 8 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` passes reconstruction, Han coverage, review
  status, and tone-mark checks.
