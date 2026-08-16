# Chapter 1 Reading Review

Status: reviewed on `2026-08-16`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Punctuation and kana-only spans remain unannotated.
- Concatenating token text reproduces the canonical paragraph exactly.
- The PDF and website consume the same reviewed token arrays.

## Language Passes

The Chinese pass retained ordinary travel-guide syntax and checked the local
forms used in this chapter, including `箱根`, `箱根汤本`, `小田原`, `宫之下`,
`强罗`, `早云山`, `大涌谷`, `桃源台`, `芦之湖`, `仙石原`, `元箱根`,
`箱根町`, `神山`, `驹岳`, `冠岳`, `气象厅`, and `国土地理院`. Pinyin is
attached to the matching Chinese span rather than a detached whole sentence.

The Japanese pass checked operator and place usage, including
`箱根（はこね）`, `箱根湯本（はこねゆもと）`, `小田原（おだわら）`,
`宮ノ下（みやのした）`, `強羅（ごうら）`, `早雲山（そううんざん）`,
`大涌谷（おおわくだに）`, `桃源台（とうげんだい）`,
`芦ノ湖（あしのこ）`, `仙石原（せんごくはら）`, and
`元箱根（もとはこね）`. The audit also corrected compound readings that a
general tokenizer handled poorly: `芦ノ湖畔（あしのこはん）`,
`水蒸気爆発（すいじょうきばくはつ）`, `外輪山（がいりんざん）`,
`富士山（ふじさん）`, and the verb form `開けた（ひらけた）`.

The English pass was edited independently. It uses plain transport language,
keeps uncertain views conditional, and avoids treating a through service as a
single vehicle or a lodging district as a hotel ranking.

## Validation

- Chinese: `848` tokens across ten aligned blocks.
- Japanese: `1,098` tokens across ten aligned blocks.
- Browser rendering: `1,175` visible ruby nodes across both reading languages.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- No missing Han reading, invalid numeric-tone pinyin, or missing kanji reading
  is accepted by `scripts/validate_readings.py`.
