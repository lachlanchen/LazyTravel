# Chapter 3 Website Review

Status: responsive build and browser review passed on `2026-08-17`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-3: `28` aligned blocks.
- Chinese reading layer: `2,917` tokens.
- Japanese reading layer: `3,554` tokens.
- Browser rendering: `3,904` ruby nodes.
- Chapter 3 source list: `11` entries.
- Chapter 3 figure count: `3`; map count: `1`; trilingual headings: `4`.

The website is generated from the same JSON as the B6 book. Its public
projection preserves prose, readings, citations, captions, asset selection,
and dated operational qualifiers while removing private local source paths.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop keeps three aligned language columns and the chapter rail.
- Mobile replaces the rail with chapter and section navigation.
- Chinese pinyin and Japanese furigana render without clipping.
- The Ohiradai, museum landscape, and food figures use the reviewed web crops,
  retain exactly four guides, and keep the place or food visually dominant.
- The slope map opens in a `390 px` viewport over a readable `760 px` stage;
  pan, zoom, and reset work.
- Food is presented as a quick cafe choice, a full meal, or brought food rather
  than a generic list of local dishes.
- No page-level horizontal overflow, header overlap, browser console error, or
  failed request was observed.

## Evidence

- Browser report: `build/qa/site/hakone-ch03/qa.json`, SHA-256
  `16bac2ae958209edd53871e5854a48ea4748b66703ed48f082cfcb626dc8a5a0`.
- Ohiradai mobile figure:
  `build/qa/site/hakone-ch03/mobile-03-figure.png`, SHA-256
  `a283f8e5450f01c5c4026e5eadc2a76fe5b4f79943f8181f43964538022c21ea`.
- Museum mobile figure:
  `build/qa/site/hakone-ch03/mobile-03-figure-02.png`, SHA-256
  `97e3a1d5856660a79b61980cc3d158783d64aa537f25dc143c06b11a8d79d3c7`.
- Food mobile figure:
  `build/qa/site/hakone-ch03/mobile-03-figure-03.png`, SHA-256
  `039d619919f1307fd40bec003e731f06905c028c2a5495ba6b0d93ff63bb7018`.
- Mobile map: `build/qa/site/hakone-ch03/mobile-03-map.png`, SHA-256
  `57db0f4ebdc91e569f70a01cbb33df68baea3aaa4a5771e7b667c963d1cb69f2`.
