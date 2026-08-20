# Chapter 9 Website Review

Status: responsive build and browser review passed on `2026-08-20`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-9: `87` aligned blocks.
- Chinese reading layer: `10,770` tokens.
- Japanese reading layer: `13,380` tokens.
- Browser rendering: `14,771` ruby nodes, including `2,180` in Chapter 9.
- Chapter 9 source list: `25` entries.
- Chapter 9 figure count: `2`; map count: `1`; trilingual headings: `3`.

The website and B6 pocket consume the same final JSON and the same concise
Chinese chapter title. Chapter 9 follows one lodging decision: match tonight's
arrival and dinner to tomorrow's first leg, choose the district, then verify
the exact entrance, room, bath, meal, shuttle, and fallback.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns with the
  complete pinyin and furigana layers.
- Mobile navigation exposes all ten blocks, two figures, the five-zone map,
  final callout, sources, and captions without page-level horizontal overflow.
- The map remains legible on a `760 px` pannable stage inside the `390 px`
  viewport. Left, centre, and right positions at `0`, `185`, and `370 px`, plus
  zoom and reset, pass inspection.
- The room scene retains exactly Aya-chan, Lala Xia, Sasa-kun, and the
  Zhuangzi robot while the room threshold, bed, luggage, chair, and washroom
  route remain readable.
- The final itinerary callout retains its checked date, citations, pinyin,
  furigana, and full trilingual text without clipping.
- No browser console error, failed request, content mismatch, missing ruby, or
  clipped callout was observed.

## Evidence

- Browser report: `build/qa/hakone-ch09-website-release/qa.json`, SHA-256
  `23e90cb9e20779d23cbc7e88a7eacebb33e4a630a703363a0085e953022a7b37`.
- Full Chapter 9 desktop capture:
  `build/qa/hakone-ch09-website-release/desktop-09.png`, SHA-256
  `32d318a56914385d82fcb0b56323af986652deaf63136c120a1871d1321c7d20`.
- Full Chapter 9 mobile capture:
  `build/qa/hakone-ch09-website-release/mobile-09.png`, SHA-256
  `cb1fa95e5947939a1f8692ede6fce19e0050c060a255e42b310a1dc40707b9ac`.
- Three-position mobile map contact:
  `build/qa/hakone-ch09-website-release/mobile-09-map-contact.jpg`, SHA-256
  `37b7530a2b269a83b438a3c775dd2a1c4b5f5166affe3c2bae79329929c2abd0`.
- Mobile room-check figure:
  `build/qa/hakone-ch09-website-release/mobile-09-figure-02.png`, SHA-256
  `60365aa4470f98cd27b50a8b0781dafa5d8db9cd850965fd22d92e980a894f33`.
- Mobile final callout:
  `build/qa/hakone-ch09-website-release/mobile-09-callout-01.png`, SHA-256
  `99f4b6e0bd95109f5c8023ad056066611a890d488b27300018e7f4efb437776e`.
