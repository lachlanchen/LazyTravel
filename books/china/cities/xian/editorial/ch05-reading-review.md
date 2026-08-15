# Chapter 5 Reading Review

Status: reviewed on `2026-08-15`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses furigana on kanji-bearing tokens; kana and punctuation remain
  unannotated.
- Concatenating token text reproduces the canonical Chinese or Japanese prose
  exactly.
- The B6 pocket PDF and website consume the same reviewed arrays in
  `data/china/cities/xian/book.json`.

## Editorial Audit

Chapter 5 was reviewed token by token after the three language editions were
line-edited. The Chinese pass checked the route and place names `钟楼
(zhōnglóu)`, `鼓楼 (gǔlóu)`, `永宁门 (yǒngníngmén)`, `北院门
(běiyuànmén)`, `化觉巷 (huàjuéxiàng)`, `回坊 (huífāng)`, `清真大寺
(qīngzhēn dàsì)`, and `书院门 (shūyuànmén)`. It also reviewed contextual
forms including `周长为 (zhōucháng wéi)`, `全圈 (quánquān)`, `征得
(zhēngdé)`, the decimal `十三点七四 (shísān diǎn qī sì)`, and four-digit
years containing `〇`.

The Japanese pass checked `永寧門（えいねいもん）`,
`北院門（ほくいんもん）`, `化覚巷清真大寺（かかくこうせいしんだいじ）`,
`回族街区（かいぞくがいく）`, `鼓楼（ころう）`,
`書院門（しょいんもん）`, `礼拝大殿（れいはいだいでん）`, and the
complete readings of all dates and measurements. Independent Japanese editing
kept route instructions idiomatic and removed phrasing that read as a literal
transfer from Chinese or English.

The validator and candidate generator now recognize `〇` as a Han-bearing
year character. Regression review also covered the earlier contextual readings
`四年（よねん）` and `甲片（こうへん）` rather than preserving known candidate
errors outside the new chapter.

## Validation

- Chapter 5 Chinese: `1,313` tokens, including `1,098` ruby-bearing tokens.
- Chapter 5 Japanese: `1,581` tokens, including `689` ruby-bearing tokens.
- Full canonical book after Chapter 5: `5,026` Chinese tokens and `6,381`
  Japanese tokens.
- All `12` Chapter 5 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` passes reconstruction, Han coverage, reading
  status, and tone-mark checks; the destination-book schema also passes.
