# Chapter 3 Reading Review

Status: reviewed on `2026-08-14`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses furigana on kanji-bearing tokens; kana and punctuation remain
  unannotated.
- Concatenating token text reproduces the canonical Chinese or Japanese prose
  exactly.
- The pocket PDF and website consume the same reviewed arrays in
  `data/china/cities/xian/book.json`.

## Editorial Audit

Machine-assisted candidates received a chapter-specific proper-name,
polyphone, number, archaeological-term, and travel-term pass. Chinese checks
included `兵马俑 (bīngmǎyǒng)`, `秦始皇帝陵 (qín shǐhuángdìlíng)`,
`一号坑 (yīhàokēng)`, `二号坑 (èrhàokēng)`, `三号坑
(sānhàokēng)`, `丽山园 (lìshānyuán)`, `弩兵 (nǔbīng)`, and the
measurement use of `长 (cháng)`.

The Japanese pass checked `兵馬俑（へいばよう）`,
`兵馬俑坑（へいばようこう）`, `秦始皇帝陵（しんしこうていりょう）`,
`一号坑（いちごうこう）`, `二号坑（にごうこう）`,
`三号坑（さんごうこう）`, `麗山園（れいざんえん）`,
`歩兵（ほへい）`, and `凹字形（おうじけい）`. The audit corrected a
Chinese length polyphone and an incorrect machine reading for Japanese
`歩兵`; ambiguous `何が`, `何も`, and `何を` tokenization was also
resolved before approval.

## Validation

- Chapter 3 Chinese: `1,003` tokens, including `814` ruby-bearing tokens.
- Chapter 3 Japanese: `1,253` tokens, including `544` ruby-bearing tokens.
- Chapter 3 website total: `1,358` rendered ruby nodes.
- Full canonical book after Chapter 3: `2,698` Chinese tokens and `3,476`
  Japanese tokens.
- `scripts/validate_readings.py` passes complete reconstruction, coverage,
  reviewed status, and tone-mark checks.
