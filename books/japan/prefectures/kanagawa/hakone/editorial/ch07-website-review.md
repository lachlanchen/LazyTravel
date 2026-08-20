# Chapter 7 Website Review

Status: responsive build and browser review passed on `2026-08-20`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-7: `67` aligned blocks.
- Chinese reading layer: `7,700` tokens.
- Japanese reading layer: `9,562` tokens.
- Browser rendering: `10,538` ruby nodes, including `1,735` in Chapter 7.
- Chapter 7 source list: `9` entries.
- Chapter 7 figure count: `3`; map count: `1`; trilingual headings: `6`.

The website and B6 pocket consume the same reviewed JSON. Chapter 7 follows
one stay in order: protect the booked dinner, verify the actual bath, prepare
at the dry threshold, eat at the agreed time, choose a room that fits, and set
the morning departure before sleep.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns with the
  complete pinyin and furigana layers.
- Mobile navigation exposes all ten blocks, three figures, the sequence map,
  callouts, sources, and captions without page-level horizontal overflow.
- The map remains legible on a `760 px` pannable stage inside the `390 px`
  viewport; both halves, pan, zoom, and reset pass inspection.
- Arrival, bath-threshold, and dinner scenes each retain exactly the four
  approved guides without obscuring the travel subject.
- Callouts retain headings, dated checks, citations, and ruby without clipping.
- Reader-facing map and figure bars use editorial labels rather than internal
  asset filenames.
- No browser console error, failed request, content mismatch, missing ruby, or
  clipped callout was observed.

## Evidence

- Browser report: `build/qa/hakone-ch07-website-release/qa.json`, SHA-256
  `3bf29fd6dc02dd7641f777b997ae492fa6664f88a14228cfffde9682d0df2aa1`.
- Full Chapter 7 desktop capture:
  `build/qa/hakone-ch07-website-release/desktop-07.png`, SHA-256
  `2803ad3f0d2dfe9959b8e8bf5f330eb88c2517c78346f89378d68370b0a8c04c`.
- Full Chapter 7 mobile capture:
  `build/qa/hakone-ch07-website-release/mobile-07.png`, SHA-256
  `7de3416e0d92f23cf749249b8633119aadbfbb20d2dea016718a20fa025ddfd1`.
- Both-halves mobile map contact:
  `build/qa/hakone-ch07-website-release/mobile-07-map-contact.jpg`, SHA-256
  `843aef5ae8804bdeb5b21cf54d73a297076024d9ddf1f023a84fd6f2632bd2f8`.
- Mobile arrival, bath, and dinner captures have SHA-256 values
  `24e02ede02b52deae40bacfe0dd46c2d16e784224497725a06f2b3e098ce793b`,
  `4b5e4876ba321953edb4abfee0a6e0c9ec030318dd8a2ad577df88c8d0a1adbf`,
  and `a4173f1ee884a5e70ab71b392a75ad73a6ad2620b1ea17a754061ba2bb9264bf`.
