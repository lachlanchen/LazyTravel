# Chapter 10 Website Review

Status: responsive build and browser review passed on `2026-08-21`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-10: `97` aligned blocks.
- Chinese reading layer: `12,205` tokens.
- Japanese reading layer: `15,120` tokens.
- Browser rendering: `16,770` ruby nodes, including `1,999` in Chapter 10.
- Chapter 10 source list: `27` entries.
- Chapter 10 figure count: `6`; map count: `1`; trilingual headings: `3`.

The website and B6 pocket consume the same final JSON, readings, citations,
captions, and asset choices. Chapter 10 keeps one itinerary rule visible:
choose one anchor, protect one fixed commitment and one exit, then remove or
exchange a complete branch when weather or operation changes.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns with the
  complete pinyin and furigana layers.
- Mobile navigation exposes all ten blocks, six figures, the portrait map,
  both callouts, sources, and captions without page-level horizontal overflow.
- The map uses a `760 px` pannable vector stage inside the `390 px` viewport.
  Left, centre, and right positions at `0`, `185`, and `370 px`, plus zoom and
  reset, pass inspection.
- The rainy Pola Museum figure retains exactly Aya-chan, Lala Xia, Sasa-kun,
  and the Zhuangzi robot while the museum, forest, entrance slope, handrail,
  and wet approach remain readable.
- Reader-facing visual headers identify the itinerary map and rainy-arrival
  plate; no internal asset ID is exposed.
- No browser console error, failed request, content mismatch, missing ruby,
  clipped callout, or incoherent overlap was observed.

## Evidence

- Browser report: `build/qa/hakone-ch10-website-release/qa.json`, SHA-256
  `1bae0c54c4a6781a281d36c17564669e659374f0d12a3e2889a5dc1793bbd7df`.
- Full Chapter 10 desktop capture:
  `build/qa/hakone-ch10-website-release/desktop-10.png`, SHA-256
  `842fc8c03234a51056ebb369371193455a61a20a691dbb9dec86a8a56f63703f`.
- Full Chapter 10 mobile capture:
  `build/qa/hakone-ch10-website-release/mobile-10.png`, SHA-256
  `de674b4fa3877574e079524a65f0abc5e339576a398c71904194524e3eab6b50`.
- Three-position mobile map contact:
  `build/qa/hakone-ch10-website-release/mobile-10-map-contact.jpg`, SHA-256
  `16b674f90f8d81547552e807f18fa522f28ebf35d31b96b3b715920f3ede7061`.
- Mobile Pola rainy-arrival figure:
  `build/qa/hakone-ch10-website-release/mobile-10-figure-05.png`, SHA-256
  `b1c835876d79e851e1ac51423e54e2f8bdb8979edb2cf744d9e77153e5c7cd1d`.
- Mobile fallback and cut-order callouts:
  `build/qa/hakone-ch10-website-release/mobile-10-callout-01.png`, SHA-256
  `30a790b7911770ec2e63da67ebd7e0b8bd5a30dd5fa1b7603e17f41d75bac793`;
  `build/qa/hakone-ch10-website-release/mobile-10-callout-02.png`, SHA-256
  `fdf17bb030d94525efe7e01a5727ac0d4c9195ac4b9a03eddefda88fb3cf9e03`.
