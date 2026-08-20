# Chapter 8 Website Review

Status: responsive build and browser review passed on `2026-08-20`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-8: `77` aligned blocks.
- Chinese reading layer: `9,181` tokens.
- Japanese reading layer: `11,401` tokens.
- Browser rendering: `12,588` ruby nodes, including `2,050` in Chapter 8.
- Chapter 8 source list: `23` entries.
- Chapter 8 figure count: `5`; map count: `1`; trilingual headings: `4`.

The website and B6 pocket consume the same final JSON. Chapter 8 follows one
food clock: choose a real lunch, add only route-sized snacks and rests, keep
Odawara kamaboko at the gateway, and protect the booked ryokan dinner.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns with the
  complete pinyin and furigana layers.
- Mobile navigation exposes all ten blocks, five figures, the food-clock map,
  two callouts, sources, and captions without page-level horizontal overflow.
- The map remains legible on a `760 px` pannable stage inside the `390 px`
  viewport. Left, centre, and right positions at `0`, `185`, and `370 px`, plus
  zoom and reset, pass inspection.
- The new kamaboko scene retains exactly Aya-chan, Lala Xia, Sasa-kun, and the
  Zhuangzi robot while the board-steamed food process remains dominant.
- Allergy and three-plan callouts retain headings, checked dates, citations,
  and ruby without clipping.
- No browser console error, failed request, content mismatch, missing ruby, or
  clipped callout was observed.

## Evidence

- Browser report: `build/qa/hakone-ch08-website-release/qa.json`, SHA-256
  `dfa105e7105a674d49ec271250e875bcd1702d8358abedf899593f6c1d028657`.
- Full Chapter 8 desktop capture:
  `build/qa/hakone-ch08-website-release/desktop-08.png`, SHA-256
  `0e28db7e0b49ab2590bf91f0bd1a7a74195d04e4bfc988d730fd9ec0be054dbb`.
- Full Chapter 8 mobile capture:
  `build/qa/hakone-ch08-website-release/mobile-08.png`, SHA-256
  `e8dfce6be0537ba73f93001dca36ea0d237ba48e37dbd246c5ed756ece07f4fb`.
- Three-position mobile map contact:
  `build/qa/hakone-ch08-website-release/mobile-08-map-contact.jpg`, SHA-256
  `37dd7d72997fc8440e681087c29c5cb6c1552806896669546a04e1afc9b38389`.
- Mobile kamaboko figure:
  `build/qa/hakone-ch08-website-release/mobile-08-figure-04.png`, SHA-256
  `40ce3da34fc959f4dcee7aa2b404b7ae35e0dea63874c4f4339bd30a70ee870c`.
- Mobile allergy and three-plan callouts have SHA-256 values
  `67b72164c28ecaa8519e13010384190743ce39498bcd7df53db0e88a477088ce`
  and `5eb4dc9eb766e8aec23f96731013b8aa674283f42d53f7dee309814317d395c1`.
