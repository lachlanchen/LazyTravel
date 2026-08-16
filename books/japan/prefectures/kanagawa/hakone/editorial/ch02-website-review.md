# Chapter 2 Website Review

Status: responsive build and browser review passed on `2026-08-16`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-2: `19` aligned blocks.
- Chinese reading layer: `1,838` tokens.
- Japanese reading layer: `2,282` tokens.
- Browser rendering: `2,502` ruby nodes.
- Chapter 2 source list: `13` entries.
- Chapter 2 figure count: `2`; map count: `1`; trilingual headings: `4`.

The website is generated from the same JSON as the B6 book. The Chapter 2
projection preserves prose, readings, citations, captions, asset selection,
and dated operational qualifiers while removing private local source paths.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop keeps three aligned language columns and the chapter rail.
- Mobile replaces the rail with chapter and section navigation.
- Chinese pinyin and Japanese furigana render without clipping.
- Both place figures load from `1920 x 1080` web crops, retain all four guides,
  and leave Odawara Station and Hakone-Yumoto visually dominant.
- The gateway map opens on the Odawara-Yumoto decision at mobile width. Its
  `390 px` viewport pans over a readable `760 px` stage; zoom and reset work.
- The late-arrival food and lodging fallback remains a single legible callout.
- No page-level horizontal overflow, header overlap, browser console error, or
  failed request was observed.

## Evidence

- Browser report: `build/qa/site/hakone-ch02/browser/qa.json`, SHA-256
  `8fd2756cf28b637ec778f0f5b759c3ccb00cc08a2a286f7b642ced4fd6f6b88a`.
- Odawara mobile figure: `build/qa/site/hakone-ch02/browser/mobile-02-figure.png`,
  SHA-256 `58d1534c9bdb819f3894aaf42735b792259c31b0b7cca7f15f78fd5438994865`.
- Yumoto mobile figure:
  `build/qa/site/hakone-ch02/browser/mobile-02-figure-02.png`, SHA-256
  `b89174349a2570492999e605a7d3431998a0100af629303b52b745b7879410b8`.
- Mobile map: `build/qa/site/hakone-ch02/browser/mobile-02-map.png`, SHA-256
  `2f951f0e666feec9a9d525915acf10aafd810c967d7b15345672f0a44cc2540a`.
- Mobile food fallback:
  `build/qa/site/hakone-ch02/browser/mobile-02-callout-01.png`, SHA-256
  `84d49d47b0b7e92436d723b7cc65247b5361c6bd85e36df689fb85eb758edcae`.
