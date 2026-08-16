# Chapter 11 Website Review

Status: passed on `2026-08-16`.

URL: `http://127.0.0.1:4173/?chapter=ch11-before-departure`

## Data Parity

- Website payload is rebuilt from `data/china/cities/xian/book.json`.
- Public projection parity passes for `125` total blocks, `13,468` Chinese
  tokens, and `17,299` Japanese tokens.
- Chapter 11 renders `13` blocks, `2,313` ruby nodes, `33` unique sources, one
  figure, eight trilingual block headings, and no map by design.
- Website payload SHA-256:
  `0392efb347d4738d4d83f8d89d2caa6bf699b2f6aa44f4523115d873b391536f`.

## Browser QA

- Desktop: Chromium at `1440 x 1000`; the chapter rail stays usable and the
  Chinese, Japanese, and English columns remain aligned through the long
  practical blocks.
- Mobile: Chromium at `390 x 844`, device scale factor `2`; navigation,
  headings, ruby, source links, and the final callout stay inside the viewport.
- The 1448 x 1086 departure figure loads at mobile width with Aya, Lala, Sasa,
  and Zhuangzi identifiable, the hotel-table evidence readable, and the Xi'an
  wall visible through the window.
- The emergency heading uses the final text `Emergency: Give Your Location
  First` on both book and website.
- The seven-check callout retains Chinese pinyin and Japanese furigana and
  captures without clipping or horizontal overflow.
- No browser console error, failed request, page-level horizontal overflow, or
  sticky-header overlap was detected.

## Evidence

- `build/qa/site/xian/desktop-ch11.png`
- `build/qa/site/xian/mobile-ch11.png`
- `build/qa/site/xian/mobile-ch11-figure.png`
- `build/qa/site/xian/mobile-ch11-highlight.png`
- Browser QA JSON SHA-256:
  `795a4085849975bd18f003b51c7406e6323c26192463e8fb12c4ad68901f55c4`.
