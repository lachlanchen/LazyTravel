# Chapter 2 Reading Review

Status: reviewed on `2026-08-14`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses furigana on kanji-bearing tokens; kana and punctuation remain
  unannotated.
- Concatenating token text reproduces the canonical Chinese or Japanese
  paragraph exactly.
- The pocket PDF and website consume the same reviewed arrays in
  `data/china/cities/xian/book.json`.

## Editorial Audit

Machine-assisted segmentation was followed by a proper-name, polyphone,
counter, and historical-term pass. Chinese checks included `丰京
(fēngjīng)`, `镐京 (hàojīng)`, `秦咸阳 (qín xiányáng)`, `阿房宫
(ēpánggōng)`, `汉长安城 (hàn cháng'ānchéng)`, `未央宫
(wèiyānggōng)`, `大明宫 (dàmínggōng)`, `奉元路 (fèngyuánlù)`, and
`南大街 (nándàjiē)`.

The Japanese pass checked `豊京（ほうけい）`, `鎬京（こうけい）`,
`秦咸陽（しんかんよう）`, `咸陽宮（かんようきゅう）`,
`漢長安城（かんちょうあんじょう）`, `未央宮（びおうきゅう）`,
`大明宮（だいめいきゅう）`, `韓建（かんけん）`,
`南大街（なんだいがい）`, and `一日（いちにち）`. Each language was
read as independent prose after the base text was revised; the reading layer
was then regenerated and audited rather than patched around stale tokens.

## Validation

- Chinese: `999` tokens, including `853` ruby-bearing tokens.
- Japanese: `1,337` tokens, including `579` ruby-bearing tokens.
- Chapter total: `1,432` rendered ruby nodes on the website.
- `scripts/validate_readings.py` passes complete reconstruction, coverage,
  status, and tone-mark checks.
- Full canonical book total after Chapter 2: `1,695` Chinese tokens and `2,223`
  Japanese tokens.
