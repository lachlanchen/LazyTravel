# Chapter 7 Reading Review

Status: accepted on `2026-08-22`; exact reconstruction, compiled B6 ruby, and
responsive-website ruby inspection pass.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

Route and place forms were checked as complete units, including
`白塔山（báitǎshān）`, `中山桥（zhōngshānqiáo）`,
`皋兰山（gāolánshān）`, `兰山（lánshān）`,
`三台阁（sāntáigé）`, and `五泉山（wǔquánshān）`.
The five spring names retain sign-oriented readings:
`甘露（gānlù）`, `掬月（jūyuè）`, `摸子（mōzǐ）`,
`惠（huì）`, and `蒙（méng）`. Context checks also preserve
`重建（chóngjiàn）`, `不适（bùshì）`, and the directional
`东西（dōngxī）`.

## Japanese Pass

Core place names use stable Japanese guide readings:
`白塔山（はくとうざん）`, `中山橋（ちゅうざんきょう）`,
`皋蘭山（こうらんざん）`, `蘭山（らんざん）`,
`三台閣（さんたいかく）`, and `五泉山（ごせんざん）`.
The Chinese spring names use Mandarin-approximation furigana for sign
recognition: `甘露（がんるー）`, `掬月（じゅーゆえ）`,
`摸子（もーず）`, `惠（ふい）`, and `蒙（もん）`.

The final audit corrected `上方` from the place-name reading `かみがた` to
`じょうほう`. It also removed single-character dynasty overrides that made
the `明` in `説明` read as Ming, then locked `明代（みんだい）`,
`清代（しんだい）`, `説明（せつめい）`, and
`明瞭（めいりょう）` in context.

## Validation

- Chapter 7 Chinese: `1,206` tokens across ten aligned blocks.
- Chapter 7 Japanese: `1,570` tokens across ten aligned blocks.
- Combined Chapters 1-7: `7,340` Chinese tokens and `9,448` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
- Compiled pages `94`, `96`, `98-99`, `101-103`, and `105-107` preserve ruby
  above its own token without collision, clipping, or detached punctuation.
- The release website renders `1,652` Chapter 7 ruby nodes at desktop and
  `390 px`; canonical block text and token reconstruction remain identical.
