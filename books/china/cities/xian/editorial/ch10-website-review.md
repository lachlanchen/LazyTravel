# Chapter 10 Website Review

Status: passed on `2026-08-16`.

URL: `http://127.0.0.1:4173/?chapter=ch10-itineraries-with-room`

## Data Parity

- Website payload is rebuilt from `data/china/cities/xian/book.json`.
- Public projection parity passes for `112` total blocks, `11,800` Chinese
  tokens, and `15,134` Japanese tokens.
- Chapter 10 renders `14` blocks, `2,465` ruby nodes, `40` unique sources, one
  SVG map, one figure, and five trilingual block headings.
- Website payload SHA-256:
  `8aae5c28c659048b086c6ddad790c55404b4174ce62cec83bf87b35043f196b5`.

## Browser QA

- Desktop: Chromium at `1440 x 1000`; the chapter rail remains visible and
  Chinese, Japanese, and English remain distinct in the parallel reader.
- Mobile: Chromium at `390 x 844`, device scale factor `2`; chapter selection,
  responsive controls, ruby, figure captions, and callout text remain legible.
- The itinerary map loads from its SVG variant at natural width `960`, opens in
  a wide scroll viewport, and passes zoom-in and reset checks.
- The Small Wild Goose Pagoda figure loads above 1,200 natural pixels, keeps
  the destination dominant, and shows Aya, Lala, Sasa, and Zhuangzi clearly.
- The final five-day callout retains Chinese pinyin and Japanese furigana and
  captures without clipping at mobile width.
- No browser console error, failed request, page-level horizontal overflow, or
  sticky-header overlap was detected.

## Evidence

- `build/qa/site/xian/desktop-ch10.png`
- `build/qa/site/xian/mobile-ch10-map.png`
- `build/qa/site/xian/mobile-ch10-figure.png`
- `build/qa/site/xian/mobile-ch10-highlight.png`
- Browser QA JSON SHA-256:
  `ad5e338312ae479881b5a4a50b469d461804abe198b37149d71b8cfddeb28105`.
