# Chapter 4 Reading Review

Status: reviewed on `2026-08-21`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

The route and engineering forms were checked as complete units, including
`中山桥（zhōngshānqiáo）`, `白塔山（báitǎshān）`,
`将军铁柱（jiāngjūn tiězhù）`, `镇远浮桥（zhènyuǎn fúqiáo）`,
`钢桁架（gāng héngjià）`, `弧形钢梁（húxíng gāngliáng）`, and
`铆接构件（mǎojiē gòujiàn）`. Context errors from mechanical segmentation
were corrected to `系在（jìzài）` and `背着（bēizhe）`.

## Japanese Pass

The retained Chinese names use stable guide readings:
`中山橋（ちゅうざんきょう）`, `城関（じょうかん）`,
`将軍鉄柱（しょうぐんてっちゅう）`, `鎮遠浮橋（ちんえんふきょう）`,
`白塔山（はくとうざん）`, and `白塔寺（はくとうじ）`. Directional forms
such as `南詰（みなみづめ）`, `北詰（きたづめ）`, and
`橋詰（はしづめ）` were checked in their final sentences.

## Validation

- Chapter 4 Chinese: `1,152` tokens across nine aligned blocks.
- Chapter 4 Japanese: `1,571` tokens across nine aligned blocks.
- Combined Chapters 1-4: `3,449` Chinese tokens and `4,542` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
