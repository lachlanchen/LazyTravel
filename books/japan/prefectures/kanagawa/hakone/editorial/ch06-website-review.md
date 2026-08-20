# Chapter 6 Website Review

Status: responsive build and browser review passed on `2026-08-20`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-6: `57` aligned blocks.
- Chinese reading layer: `6,439` tokens.
- Japanese reading layer: `7,999` tokens.
- Browser rendering: `8,803` ruby nodes, including `1,561` in Chapter 6.
- Chapter 6 source list: `16` entries.
- Chapter 6 figure count: `3`; map count: `1`; trilingual headings: `6`.

The website and B6 pocket consume the same reviewed JSON. Chapter 6 keeps one
route spine: decide how much stone paving is suitable, read the checkpoint in
its actual landscape, take a proportionate rest at Amasake Chaya, and leave by
bus before the walk compromises lodging or dinner.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns with the
  complete pinyin and furigana layers.
- Mobile navigation exposes every block, figure, callout, source, and caption
  without page-level horizontal overflow.
- The map remains legible on a `760 px` pannable stage inside the `390 px`
  viewport; both halves, pan, zoom, and reset pass inspection.
- Three place and food figures retain exactly four guides while stone paving,
  the checkpoint, or the tea-house rest remains dominant.
- Five mobile callouts retain their headings, dated checks, citations, and
  ruby without clipping.
- Reader-facing map and figure bars use editorial labels rather than internal
  asset filenames.
- No browser console error, failed request, content mismatch, missing ruby, or
  clipped callout was observed.

## Evidence

- Browser report: `build/qa/hakone-ch06-website-release/qa.json`, SHA-256
  `856cf7a18514499ecf9ed1d7797d02f064a5cf8594ee42f37cb23d6ab5cc5059`.
- Full Chapter 6 desktop capture:
  `build/qa/hakone-ch06-website-release/desktop-06.png`, SHA-256
  `ed6fc10e180e5c757308f8f6c43620044565fd689e8dc32d493ae116a87d192e`.
- Mobile map:
  `build/qa/hakone-ch06-website-release/mobile-06-map.png`, SHA-256
  `da26a6fdc434db89f974bd84a562b1cac62b65398ae9ae7ed8fe7f933c5cd070`.
- Three-figure mobile contact sheet:
  `build/qa/hakone-ch06-assets/mobile-figures-contact.jpg`, SHA-256
  `5a71e2f0aca9479fb9c99661d0cf3799130dc793e8594665a9cd7894657fd450`.
