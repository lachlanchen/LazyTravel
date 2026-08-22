# Chapter 6 Reading Review

Status: reviewed on `2026-08-22`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

Food and menu forms were checked as complete units, including
`牛肉面（niúròumiàn）`, `毛细（máoxì）`, `二细（èrxì）`, `韭叶（jiǔyè）`,
`酿皮子（niàngpízi）`, `灰豆子（huīdòuzi）`, `甜醅子（tiánpēizi）`,
`三炮台（sānpàotái）`, and `兰州百合（lánzhōu bǎihé）`. Context checks retain
`不为（bù wèi）` in the food-waste sentence and avoid an incorrect `行` reading
by using unambiguous prose.

## Japanese Pass

Chinese menu terms retain stable Mandarin-approximation readings for sign
recognition: `毛细（まおしー）`, `二细（あるしー）`, `韭叶（じういえ）`,
`酿皮子（にゃんぴーず）`, `灰豆子（ふいどうず）`,
`甜醅子（てぃえんぺいず）`, and `三炮台（さんぱおたい）`.
`蘭州百合（らんしゅうゆり）` uses the natural Japanese place-and-food reading.
The final audit removed contexts in which `開く`, `通`, `細麺`, or `止め時`
could receive an unintended reading.

## Validation

- Chapter 6 Chinese: `1,258` tokens across ten aligned blocks.
- Chapter 6 Japanese: `1,555` tokens across ten aligned blocks.
- Combined Chapters 1-6: `6,134` Chinese tokens and `7,878` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
