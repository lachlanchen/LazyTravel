# Chapter 9 Reading Review

Status: semantic reading audit, compiled B6 inspection, and responsive ruby
inspection accepted on `2026-08-23`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over its matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

Route and context forms were checked across all ten blocks, including
`四行（sì háng）`, `不为（bù wèi）`, `为准（wéi zhǔn）`,
`出土地（chūtǔdì）`, `重走（chóngzǒu）`, `能见度（néngjiàndù）`,
`白塔山（báitǎshān）`, and `兰山（lánshān）`. Context checks preserve
`长（cháng）`, `差（chà）`, `还（hái）`, `着（zhe）`, and the neutral
particle `得（de）`.

## Japanese Pass

The final audit corrected compounds that a general tokenizer split with the
wrong contextual reading: `開館日（かいかんび）`, `開館（かいかん）`,
`館内（かんない）`, `三泊（さんぱく）`, and `二本目（にほんめ）`.
It also checks `甘粛省博物館（かんしゅくしょうはくぶつかん）`,
`蘭州西駅（らんしゅうにしえき）`, `中山橋（ちゅうざんきょう）`,
`白塔山（はくとうざん）`, `三台閣（さんたいかく）`,
`蘭州府城隍廟（らんしゅうふじょうこうびょう）`, and
`保安検査（ほあんけんさ）` as complete travel terms.

## Validation

- Chapter 9 Chinese: `1,347` tokens across ten aligned blocks.
- Chapter 9 Japanese: `1,756` tokens across ten aligned blocks.
- Combined Chapters 1-9: `10,156` Chinese tokens and `12,997` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
- Pages 131-150 of the `163`-page B6 proof preserve attached pinyin and
  furigana without clipping, detached ruby, or line collisions.
- Desktop and `390 px` release QA render all `1,916` Chapter 9 ruby nodes from
  the canonical arrays; the website contains no substitute reading layer.
