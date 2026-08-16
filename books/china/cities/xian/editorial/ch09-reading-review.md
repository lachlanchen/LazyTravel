# Chapter 9 Reading Review

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

The Chinese pass checked lodging-area names and the practical vocabulary that
is easy to misread in isolation: `曲江 (qǔjiāng)`, `粉巷 (fěnxiàng)`,
`巷道 (xiàngdào)`, `凤城九路 (fèngchéng jiǔlù)`, `悦椿东路
(yuèchūn dōnglù)`, `芷阳广场站 (zhǐyáng guǎngchǎngzhàn)`, and
`涉外资质 (shèwài zīzhì)`. Phrase overrides preserve `理解为 (lǐjiě
wéi)` and `当保证 (dàng bǎozhèng)` without changing unrelated uses of
`为` or `当`.

The Japanese pass was edited independently before pronunciation review. It
replaces literal hotel-language calques with ordinary travel-book Japanese,
then checks `城壁内 (じょうへきない)`, `西安北駅
(せいあんきたえき)`, `西安南門城壁 (せいあんなんもんじょうへき)`,
`芷陽広場駅 (しようひろばえき)`, `階下 (かいか)`, `棟 (とう)`,
`宿替え (やどがえ)`, and `四人 (よにん)`. Latin hotel
names and the letters `C` and `D` remain visible rather than being rewritten.

## Validation

- Chapter 9 Chinese: `1,487` tokens, including `1,213` ruby-bearing tokens.
- Chapter 9 Japanese: `1,953` tokens, including `837` ruby-bearing tokens.
- Full canonical book after Chapter 9: `10,093` Chinese tokens and `12,891`
  Japanese tokens.
- All `12` Chapter 9 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` passes reconstruction, Han coverage, review
  status, and tone-mark checks.
