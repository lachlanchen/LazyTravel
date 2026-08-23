# Chapter 11 Reading Review

Status: semantic reading audit, compiled B6 inspection, and responsive ruby
inspection accepted on `2026-08-23`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

The final audit checks the route and historical terms across all ten blocks,
including `炳灵寺（bǐnglíngsì）`, `刘家峡（liújiāxiá）`,
`黄洮交汇（huáng-táo jiāohuì）`, `兴隆山（xīnglóngshān）`,
`水墨丹霞（shuǐmò dānxiá）`, `建弘元年（jiànhóng yuánnián）`,
`西秦（xīqín）`, and `去程（qùchéng）`.

## Japanese Pass

The Japanese audit checks complete place and context terms, including
`炳霊寺（へいれいじ）`, `劉家峡（りゅうかきょう）`,
`興隆山（こうりゅうざん）`, `水墨丹霞（すいぼくたんか）`,
`建弘元年（けんこうがんねん）`, `西秦（せいしん）`,
`石窟（せっくつ）`, `水況（すいきょう）`, and `市内（しない）`.
The context-sensitive `水況` and travel-use `市内` readings were explicitly
reviewed before acceptance.

## Validation

- Chapter 11 Chinese: `1,605` tokens across ten aligned blocks.
- Chapter 11 Japanese: `1,973` tokens across ten aligned blocks.
- Complete Lanzhou book: `13,409` Chinese tokens and `16,997` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
- Physical pages `175-200` preserve attached pinyin and furigana without
  clipping, detached ruby, or line collisions.
- Desktop and `390 px` QA render all `2,211` Chapter 11 ruby nodes from the
  canonical arrays; the website contains no substitute reading layer.
