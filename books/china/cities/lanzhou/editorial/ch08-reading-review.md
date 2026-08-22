# Chapter 8 Reading Review

Status: accepted on `2026-08-22`; exact reconstruction, compiled B6 ruby, and
responsive-website ruby inspection pass.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

Booking and place forms were checked as complete units, including
`正宁路（zhèngníng lù）`, `永昌南路（yǒngchāng nánlù）`,
`七里河（qīlǐhé）`, `西站十字（xīzhàn shízì）`,
`建兰（jiànlán）`, `天水中路（tiānshuǐ zhōnglù）`, and
`中川机场（zhōngchuān jīchǎng）`. Context checks preserve
`朝（cháo）` for room orientation, `为例（wéi lì）`, and
`不为（bù wèi）` in the airport stop rule.

## Japanese Pass

Core lodging names now use reviewed guide readings:
`正寧路（せいねいろ）`, `永昌南路（えいしょうなんろ）`,
`七里河（しちりが）`, `天水中路（てんすいちゅうろ）`, and
`中川空港（ちゅうせんくうこう）`. The final audit corrected the automatic
personal-name reading of `正寧`, the route reading of `天水中路`, and the
counter/date forms `深夜着（しんやちゃく）`, `一泊（いっぱく）`,
`二十四時間（にじゅうよじかん）`, `二〇二四年（にせんにじゅうよねん）`,
and `二〇二六年八月二十二日（にせんにじゅうろくねんはちがつにじゅうににち）`.

## Validation

- Chapter 8 Chinese: `1,469` tokens across ten aligned blocks.
- Chapter 8 Japanese: `1,793` tokens across ten aligned blocks.
- Combined Chapters 1-8: `8,809` Chinese tokens and `11,241` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
- The compiled Chapter 8 prose and callout pages preserve ruby above their own
  tokens without collision, clipping, or detached punctuation.
- The responsive website renders `2,023` Chapter 8 ruby nodes at desktop and
  `390 px`; canonical text and token reconstruction remain identical.
