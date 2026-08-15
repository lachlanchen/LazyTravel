# Chapter 6 Reading Review

Status: reviewed on `2026-08-15`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses hiragana furigana on kanji-bearing tokens; kana, Latin text,
  and punctuation remain unannotated.
- Concatenating token text reproduces the final Chinese or Japanese prose
  exactly.
- The B6 pocket PDF, highlighted ordering block, and website all consume the
  same arrays in `data/china/cities/xian/book.json`.

## Editorial Audit

The Chinese pass corrected food-specific and contextual readings including
`饦饦馍 (tuōtuōmó)`, `腊汁肉夹馍 (làzhīròujiāmó)`, `泡馍
(pàomó)`, `口汤 (kǒutāng)`, `干泡 (gānpào)`, `水围城
(shuǐwéichéng)`, `凉皮 (liángpí)`, `擀面皮 (gǎnmiànpí)`,
`嚼劲 (jiáojìn)`, `臊子 (sàozi)`, `甑糕 (zènggāo)`, and
`见长 (jiàncháng)`. The pass also corrected `干湿`, `干拌`, and the
adverbial particle in `一摊接一摊地` rather than preserving automatic
polyphonic guesses.

The Japanese pass treats retained Chinese dish names as names, not as ordinary
Japanese compounds. It reviewed `飥飥饃（とぅおとぅおもー）`,
`臘汁肉夾饃（らーじーろうじゃーもー）`, `牛羊肉泡饃
（にゅうやんろうぱおもー）`, `涼皮（りゃんぴー）`, `擀面皮
（がんみぇんぴー）`, `油潑（ようぽー）`, `臊子（さおず）`,
`肉丸胡辣湯（ろうわんふーらーたん）`, `甑糕（ずんがお）`, and
the place names used in the food map. Ordinary Japanese contextual readings
such as `辛さ（からさ）`, `餃子（ぎょうざ）`, `一品（いっぴん）`,
and `一か所（いっかしょ）` received a separate pass.

## Validation

- Chapter 6 Chinese: `1,177` tokens, including `967` ruby-bearing tokens.
- Chapter 6 Japanese: `1,465` tokens, including `602` ruby-bearing tokens.
- Full canonical book after Chapter 6: `6,203` Chinese tokens and `7,846`
  Japanese tokens.
- All `12` Chapter 6 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` passes reconstruction, Han coverage, reading
  status, and tone-mark checks.
