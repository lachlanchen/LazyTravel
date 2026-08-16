# Chapter 10 Reading Review

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

The Chinese pass checked itinerary terms and context-sensitive readings,
including `华山 (huàshān)`, `乾陵 (qiánlíng)`, `从葬坑
(cóngzàngkēng)`, `写进行程 (xiějìn xíngchéng)`, `丽山园
(lìshānyuán)`, and `化觉巷清真大寺 (huàjuéxiàng qīngzhēn
dàsì)`. The two multiword route phrases are protected from segmentation that
would otherwise assign the wrong reading in context.

The Japanese pass was edited independently before pronunciation review. It
checks the day names `二日 (ふつか)`, `三日 (みっか)`, `四日
(よっか)`, and `五日 (いつか)`, as well as the duration forms
`二日間 (ふつかかん)`, `四日間 (よっかかん)`, and `五日間
(いつかかん)`. Proper-name checks include `秦 (しん)`, `麗山園
(りざんえん)`, `小雁塔 (しょうがんとう)`, `薦福寺
(せんぷくじ)`, `漢陽陵 (かんようりょう)`, `翠華山
(すいかざん)`, and `乾陵 (けんりょう)`.

## Validation

- Chapter 10 Chinese: `1,707` tokens, including `1,416` ruby-bearing tokens.
- Chapter 10 Japanese: `2,243` tokens, including `1,049` ruby-bearing tokens.
- Full canonical book after Chapter 10: `11,800` Chinese tokens and `15,134`
  Japanese tokens.
- All `14` Chapter 10 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` passes reconstruction, Han coverage, review
  status, and tone-mark checks.
