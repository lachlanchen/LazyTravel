# Xi'an Chapters 1-7 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-16`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 7 URL:
  `http://127.0.0.1:4173/?chapter=ch07-beyond-the-center`
- Canonical JSON SHA-256:
  `91afc900be214165a9d8c904d682a59a7e15a283c94dae8abdcbe38a977613e6`
- Site manifest SHA-256:
  `a90dbad379d5dee7c9923c07c4cc1890db8503dd504ac5544588d98981dd5fdb`

The site payload is the public projection of the same canonical JSON used by
the B6 book. Local source and visual-reference paths are stripped while prose,
readings, headings, citations, captions, checked dates, assets, and public
provenance remain aligned.

## Parity And Interaction

- `74` aligned blocks render across Chapters 1-7.
- Payload parity passes for `7,463` Chinese and `9,476` Japanese tokens.
- Seven maps and eleven figures render from the same asset records as the
  pocket book. Figure counts by chapter are `1, 1, 2, 2, 3, 1, 1`.
- Chapter 7 renders `12` blocks, `1,780` ruby nodes, one selectable SVG map,
  one figure, two highlighted callouts, three trilingual block headings, and
  `20` unique source records.
- Parallel and single-language modes, ruby toggle, direct chapter URLs,
  chapter switching, section navigation, map zoom/reset, and mobile selection
  pass.
- Browser QA explicitly opens all seven chapters at desktop and mobile sizes;
  it captures every figure automatically and checks `ROUTE FIRST`, `FOUR
  CONDITIONS`, and `SIX CHECKS` from canonical JSON rather than relying on
  hard-coded LaTeX headings.
- Every practical band and callout in Chapters 1-7 now carries a required
  trilingual heading. Schema and renderer checks reject a missing heading, so
  unrelated fallback text cannot return in the PDF or website.
- Mobile browser scrolling places blocks, maps, and figures below the sticky
  header. No console errors, failed requests, local-path leakage, page-level
  horizontal overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: three aligned columns, chapter rail, map, guide figure, callouts, sources, and branding remain clear. |
| Mobile `390 x 844` | Pass: selectors replace the rail; prose stacks by language, ruby remains readable, and all eleven full trilingual figure captions fit without crop. |
| Chapter 7 map | Pass: the wide SVG opens in a pannable viewport with large place labels and transport cards; its top edge clears the sticky header. |
| Chapter 7 figure | Pass: Aya, Lala, Sasa, and Zhuangzi remain distinct at full width; caption text wraps without crop. |
| Chapter 7 callouts | Pass: coral frame, trilingual headings, pinyin, furigana, checked date, and citations remain separated. |
| Source list | Pass: titles, locators, checked dates, and links wrap without horizontal spill. |

## Evidence

- Chapter 7 desktop screenshot SHA-256:
  `bebc84ad12d179dd78c29c6135c32c4bd3d8f82e489d4e7fd009c61ad34e16a1`
- Chapter 7 mobile screenshot SHA-256:
  `e5b0b7e407833b49c6c298c8a5af1f1337f0b8af2c60627a9b6581973eb0906b`
- Chapter 7 mobile map viewport SHA-256:
  `c5f3081f7574ab3aff5b1b1fe33a05b43eac558de2810fd68b8ee51cda71c18f`
- Chapter 7 mobile figure SHA-256:
  `ece7b8cea339aac9d29a133d7d55108e56b9e25b7097af0a9587c56269dcfafe`
- Chapter 7 mobile callout viewport SHA-256:
  `319f6a87521f74352a3d97582568e12cb4d2126e1f7f02c6c42d865fa111b57c`
- Combined eleven-figure mobile evidence sheet SHA-256:
  `b62f5465f9a1366cf38162b9831cdc8444bf469e9befb7f2919ee70233d31be4`
- Browser report SHA-256:
  `0bb2ee435d69baf353fb729e36650bae09faedad05d7f6bb22f89372687a602a`

Screenshots and the generated `site/` tree remain ignored build evidence. The
canonical JSON, renderer, validation scripts, and review record are tracked.
