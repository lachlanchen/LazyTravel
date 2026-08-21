# Chapter 2 Reading Review

Status: reviewed on `2026-08-21`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana on kanji-bearing tokens and reviewed readings on
  Chinese station labels retained for sign matching.
- Concatenating token text reproduces each canonical paragraph exactly.
- The B6 PDF and website consume the same reviewed token arrays.

## Chinese Pass

The station forms `中川机场东`, `兰州西站北广场`, and `兰州火车站` were
checked as complete labels. The final checklist uses the noun reading `háng`
in `第一行`, `第二行`, `第三行`, and `三行`, rather than the movement reading
`xíng`. Contextual readings for `可售车次`, `同行人数`, `一号线`, and
`二号线` were also reviewed.

## Japanese Pass

The retained sign labels were reviewed as
`中川机场东（ちゅうせんくうこうひがし）`,
`兰州西站北广场（らんしゅうにしえききたひろば）`, and
`兰州火车站（らんしゅうえき）`. The local place name
`七里河` uses `しちりが` in this Lanzhou context. The surrounding Japanese
was retokenized after the independent language edit and checked against the
final text.

## Validation

- Chapter 2 Chinese: `789` tokens across nine aligned blocks.
- Chapter 2 Japanese: `957` tokens across nine aligned blocks.
- Combined Chapters 1-2: `1,432` Chinese tokens and `1,760` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, numeric-tone pinyin, or unreconstructed text.
- Browser QA renders `1,086` ruby nodes in Chapter 2 and `1,964` across the
  two published chapters without clipping or missing content.
