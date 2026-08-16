# Chapter 4 Website Review

Status: responsive build and browser review passed on `2026-08-17`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-4: `37` aligned blocks.
- Chinese reading layer: `4,070` tokens.
- Japanese reading layer: `4,976` tokens.
- Browser rendering: `5,503` ruby nodes.
- Chapter 4 source list: `18` entries.
- Chapter 4 figure count: `5`; map count: `1`; trilingual headings: `3`.

The website is generated from the same JSON as the B6 book. It preserves the
reviewed prose, ruby arrays, citations, captions, asset choices, and dated
operational qualifiers while removing private local source paths.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop keeps three aligned language columns, a chapter rail, and large
  place and food figures.
- Mobile replaces the rail with chapter and section navigation; no content is
  hidden behind the fixed controls.
- Chinese pinyin and Japanese furigana render without clipping.
- The five figures retain exactly four guides while the ropeway, fumarole
  field, black eggs, reserved trail, or lake remains the main subject.
- The Owakudani map uses a readable `760 px` stage inside the `390 px`
  scrollable viewport; pan, zoom, and reset work.
- Both highlighted safety and itinerary blocks remain unclipped on mobile.
- No page-level horizontal overflow, browser console error, failed request, or
  book/site parity mismatch was observed.

## Evidence

- Browser report: `build/qa/hakone-ch04-website/qa.json`, SHA-256
  `7e538c7cb3d81d2ef1f4b88020fa49a8312991c7a2da1457e2ebedbc00501b5b`.
- Full Chapter 4 desktop capture:
  `build/qa/hakone-ch04-website/desktop-04.png`, SHA-256
  `fe1a65169a5d9a4de8915d8e9436a644a0532f5255ebe1d01d48b3bfcc84c614`.
- Mobile map: `build/qa/hakone-ch04-website/mobile-04-map.png`, SHA-256
  `f007f05eb0269a0990da6d4078e0bd8ee379c74b27123baa32a1f7846edbf14f`.
- Mobile safety callout:
  `build/qa/hakone-ch04-website/mobile-04-callout-01.png`, SHA-256
  `9205aa85bdf04e1f7e6cdb5977cba51e37d1b86a0cf87f8a4d9fca8869050769`.
- Mobile food figure:
  `build/qa/hakone-ch04-website/mobile-04-figure-03.png`, SHA-256
  `c233a14f263a800f22a9d7e42eefb2fbd73d4c6f6738748773c9f1cb2f18ffa8`.
- Mobile nature-trail figure:
  `build/qa/hakone-ch04-website/mobile-04-figure-04.png`, SHA-256
  `50bca66cdd01b4d884743eada1e98fce998db3ac5c546df7cc146d9b4c490daf`.
- Mobile lake-descent figure:
  `build/qa/hakone-ch04-website/mobile-04-figure-05.png`, SHA-256
  `910d8690d812a75c2cc447accf5483d4697a60c99ed4bc1e3114cc412ed3bc70`.
