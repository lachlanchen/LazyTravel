# Chapter 10 Reading Review

Status: semantic reading audit, compiled B6 inspection, and responsive ruby
inspection accepted on `2026-08-23`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over its matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

The final audit checks route and regional terms across all ten blocks,
including `张掖（zhāngyè）`, `河西走廊（héxī zǒuláng）`,
`祁连山（qíliánshān）`, `出发点（chūfādiǎn）`, and
`中川机场东（zhōngchuān jīchǎng dōng）`. Context-sensitive counters retain
`一行（yī háng）` and `六行（liù háng）`; neither is read as the verb
`xíng`.

## Japanese Pass

The Japanese audit checks complete travel terms rather than isolated
characters: `張掖（ちょうえき）`, `河西回廊（かせいかいろう）`,
`祁連山（きれんざん）`, `蘭州西駅（らんしゅうにしえき）`,
`蘭州駅（らんしゅうえき）`, `中川空港（ちゅうせんくうこう）`, and
`空港行き（くうこうゆき）`. The airport compound and directional suffix
were corrected before acceptance.

## Validation

- Chapter 10 Chinese: `1,648` tokens across ten aligned blocks.
- Chapter 10 Japanese: `2,027` tokens across ten aligned blocks.
- Combined Chapters 1-10: `11,804` Chinese tokens and `15,024` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
- Physical pages 151-174 of the `187`-page B6 artifact preserve attached
  pinyin and furigana without clipping, detached ruby, or line collisions.
- Desktop and `390 px` release QA render all `2,251` Chapter 10 ruby nodes from
  the canonical arrays; the website contains no substitute reading layer.
