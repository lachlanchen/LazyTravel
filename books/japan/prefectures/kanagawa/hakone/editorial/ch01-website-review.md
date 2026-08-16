# Chapter 1 Website Review

Status: responsive build and browser review passed on `2026-08-16`. Public
deployment remains gated on the complete Hakone book.

## Parity

- Build: `python3 scripts/build_website.py --book data/japan/prefectures/kanagawa/hakone/book.json --output build/site-hakone`
- Canonical content: `10` aligned blocks
- Chinese reading layer: `848` tokens
- Japanese reading layer: `1,098` tokens
- Browser ruby count: `1,175` nodes
- Chapter source list: `8` entries
- Figure count: `1`; map count: `1`; trilingual block headings: `4`

The website payload is the public projection of the same canonical JSON used
by the B6 book. Local source paths are removed without changing prose,
readings, citations, captions, or asset selection.

## Browser Gate

The generic destination QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop keeps three aligned language columns and the chapter rail.
- Mobile replaces the rail with chapter and section navigation.
- Chinese pinyin and Japanese furigana display and hide correctly with the ruby
  control.
- The Lake Ashi figure loads from the `1920 x 1080` web crop and keeps the
  destination dominant at 390 px.
- The map loads as SVG. Its mobile viewport is `390 px` wide over a `760 px`
  pannable stage, and zoom/reset controls change and restore the map scale.
- Reader-facing headers say `LAKE ASHI · WATER, RIDGES, CLOUD` and
  `HAKONE · HEIGHT AND TRANSFERS`; no internal asset ID is shown.
- No page-level horizontal overflow, header overlap, browser console error, or
  failed request was observed.

## Evidence

- Browser report: `build/qa/site/hakone-ch01/qa.json`, SHA-256
  `415f1d7888ba18588a6a339b8831c4637a1dd55db69bcfc5fc5799f55c5c9720`
- Mobile figure: `build/qa/site/hakone-ch01/mobile-01-figure.png`, SHA-256
  `5a18c2e784e6c461c949ab4dc6463928c6c54fe1481eb7b665afd8dbe822fb06`
- Mobile map: `build/qa/site/hakone-ch01/mobile-01-map.png`, SHA-256
  `e45757f045c966ee0214d467dffeefbe5c3b1c144b4d86546bf71db5c9db586a`
