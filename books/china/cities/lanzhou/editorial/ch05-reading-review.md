# Chapter 5 Reading Review

Status: reviewed on `2026-08-22`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

Museum, place, and object forms were checked as complete units, including
`甘肃省博物馆（gānsù shěng bówùguǎn）`, `西津西路（xījīn xīlù）`,
`仰韶文化（yǎngsháo wénhuà）`, `庙底沟类型（miàodǐgōu lèixíng）`,
`石岭下类型（shílǐngxià lèixíng）`, `人头形器口彩陶瓶（réntóuxíng qìkǒu
cǎitáopíng）`, `鲵鱼纹彩陶瓶（níyúwén cǎitáopíng）`, and
`棨传（qǐ chuán）`. Context-sensitive forms include `长尾（chángwěi）`; the
reading layer does not inherit the wrong pronunciation of `长` from unrelated
contexts.

## Japanese Pass

The retained names use stable guide readings: `甘粛省博物館（かんしゅくしょうはくぶつかん）`,
`甘粛彩陶展（かんしゅくさいとうてん）`, `人頭形器口彩陶瓶（じんとうけいきこうさいとうへい）`,
`鯢魚文彩陶瓶（げいぎょもんさいとうへい）`, `涇川（けいせん）`,
`銅奔馬（どうほんば）`, and `嘉峪関（かよくかん）`. Final context checks
corrected `三本（さんぼん）`, `四段階（よんだんかい）`, `一組（ひとくみ）`,
`黒彩（こくさい）`, `石函（せきかん）`, `古生物（こせいぶつ）`, and the
suffix reading in `博物館（はくぶつかん）`.

## Validation

- Chapter 5 Chinese: `1,427` tokens across ten aligned blocks.
- Chapter 5 Japanese: `1,781` tokens across ten aligned blocks.
- Combined Chapters 1-5: `4,876` Chinese tokens and `6,323` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
