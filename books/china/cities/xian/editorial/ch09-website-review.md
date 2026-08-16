# Chapter 9 Website Review

Status: passed on `2026-08-16`.

URL: `http://127.0.0.1:4173/?chapter=ch09-choose-a-side`

## Data Parity

- Website payload is rebuilt from `data/china/cities/xian/book.json`.
- Public projection parity passes for `98` total blocks, `10,093` Chinese
  tokens, and `12,891` Japanese tokens.
- Chapter 9 renders `12` blocks, `2,050` ruby nodes, `19` unique sources,
  one SVG map, one figure, and three trilingual block headings.
- Website payload SHA-256:
  `1d03f6b9e5c8d9951f04f64db13563f17b4e9b22b97182e6fe46dd72e462a906`.

## Browser QA

- Desktop: Chromium at `1440 x 1000`; the chapter rail remains visible and
  the aligned Chinese, Japanese, and English columns remain distinct.
- Mobile: Chromium at `390 x 844`, device scale factor `2`; chapter selection,
  responsive navigation, ruby, and all visual captions remain readable.
- The stay-area map loads from its SVG variant with natural width `768`, opens
  in a wide scroll viewport for larger labels, and passes zoom-in and reset
  interaction checks.
- The South Gate arrival figure loads at more than `1,200` natural pixels and
  shows Aya, Lala, Sasa, and Zhuangzi with four pieces of luggage, the hotel
  entrance, and Yongning Gate unobstructed.
- The final booking callout retains Chinese pinyin and Japanese furigana and
  captures without clipping at mobile width.
- No browser console error, failed request, page-level horizontal overflow, or
  sticky-header overlap was detected.

## Evidence

- `build/qa/site/xian/desktop-ch09.png`
- `build/qa/site/xian/mobile-ch09-map.png`
- `build/qa/site/xian/mobile-ch09-figure.png`
- `build/qa/site/xian/mobile-ch09-highlight.png`
- Browser QA JSON SHA-256:
  `d9d3d7cf198ae922ad7167cc32944b98ac1300005576a26172f7a7494574e346`.
