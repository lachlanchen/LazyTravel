# Chapter 5 Website Review

Status: responsive build and browser review passed on `2026-08-17`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Canonical Chapters 1-5: `47` aligned blocks.
- Chinese reading layer: `5,317` tokens.
- Japanese reading layer: `6,556` tokens.
- Browser rendering: `7,242` ruby nodes, including `1,739` in Chapter 5.
- Chapter 5 source list: `16` entries.
- Chapter 5 figure count: `5`; map count: `1`; trilingual headings: `4`.

The website and B6 pocket consume the same reviewed JSON. Chapter 5 keeps its
places-and-food route intact: choose the southern landing at Togendai, cross
the lake, use the shrine or park as the first stop, fit wakasagi lunch between
them, and retain a bus fallback when the boat changes.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns with the
  complete pinyin and furigana layers.
- Mobile navigation exposes every block, figure, callout, source, and caption
  without page-level horizontal overflow.
- The map remains legible on a `760 px` pannable stage inside the `390 px`
  viewport; pan, zoom, and reset work.
- Five place and food figures retain exactly four guides while Togendai, Lake
  Ashi, the shrine approach, wakasagi meal, or Onshi Park remains dominant.
- Reader-facing map and figure bars use editorial labels rather than internal
  asset filenames.
- No browser console error, failed request, content mismatch, missing ruby, or
  clipped callout was observed.

## Evidence

- Browser report: `build/qa/hakone-ch05-website-final/qa.json`, SHA-256
  `28d8831905fbd5b74db0b2f1a376ac544362f813b886b4dce72150cdb7b35114`.
- Full Chapter 5 desktop capture:
  `build/qa/hakone-ch05-website-final/desktop-05.png`, SHA-256
  `e3e1837d8eff354bdc8c6919d0af16043aba2bc1bd5336e882e3cc642cdac135`.
- Mobile map: `build/qa/hakone-ch05-website-final/mobile-05-map.png`, SHA-256
  `c644f904a7d8889d8d077bcb9eb1b64f42852051103d6155a666fdffa1f96a31`.
- Mobile wakasagi figure:
  `build/qa/hakone-ch05-website-final/mobile-05-figure-04.png`, SHA-256
  `1d4c9fb7ae78c7a7430e21d042813fc890a813260d2f43ba8454ba5b5877aa84`.
- Five-figure mobile contact sheet:
  `build/qa/hakone-ch05-website-final/mobile-05-figures-contact.jpg`, SHA-256
  `bbb4834090374f08c3fb9f2a2743b2e5af95c3ef4d606e6e58bbda206febf437`.
