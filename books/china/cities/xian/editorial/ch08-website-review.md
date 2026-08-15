# Xi'an Chapters 1-8 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-16`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 8 URL:
  `http://127.0.0.1:4173/?chapter=ch08-arrive-and-move`
- Canonical JSON SHA-256:
  `8b297ab3296e65c0c268a0b041c7405235952c1f737bac6310caacfdf81f4176`
- Site manifest SHA-256:
  `cad711df4f53eeefb4e6b3a923db4f0d66248d935c38a227e58201783368d4a6`

The site payload is the public projection of the same canonical JSON used by
the B6 book. Local source and visual-reference paths are stripped while prose,
readings, headings, citations, captions, checked dates, assets, and public
provenance remain aligned.

## Parity And Interaction

- `86` aligned blocks render across Chapters 1-8.
- Payload parity passes for `8,606` Chinese and `10,938` Japanese tokens.
- Eight maps and twelve figures render from the same asset records as the
  pocket book. Figure counts by chapter are `1, 1, 2, 2, 3, 1, 1, 1`.
- Chapter 8 renders `12` blocks, `1,533` ruby nodes, one selectable SVG map,
  one figure, four trilingual block headings, one callout, and `15` unique
  source records.
- Parallel and single-language modes, ruby toggle, direct chapter URLs,
  chapter switching, section navigation, map zoom/reset, and mobile selection
  pass.
- Browser QA opens all eight reviewed chapters at desktop and mobile sizes and
  captures every figure automatically.
- The map zoom implementation now scales both percentage width and minimum
  width, so the first mobile `+` tap visibly enlarges the map instead of being
  absorbed by the legibility floor.
- No console errors, failed requests, local-path leakage, page-level horizontal
  overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: three aligned language columns, chapter rail, arrival map, guide figure, practical bands, callout, sources, and branding remain clear. |
| Mobile `390 x 844` | Pass: selectors replace the rail; prose stacks by language, ruby remains readable, and the complete chapter scrolls without page-level overflow. |
| Chapter 8 map | Pass: the wide SVG opens in a pannable viewport with large hub labels and working first-step zoom; captions and ODbL credit remain below it. |
| Chapter 8 figure | Pass: Aya, Lala, Sasa, Zhuangzi, luggage, Xi'an North, and all three captions fit at full mobile width. |
| Chapter 8 callout | Pass: coral frame, trilingual heading, pinyin, furigana, English, checked date, and citations remain separated. |
| Source list | Pass: all 15 Chapter 8 source entries wrap without horizontal spill. |

## Evidence

- Chapter 8 desktop screenshot SHA-256:
  `d56a2ab6fa696f88cc297b3fb8580d37dcc86076b55043509ef2a60a9375e182`.
- Chapter 8 mobile screenshot SHA-256:
  `d3f542488a4cb8be5fb701672a0e056c529306e99c5d7ce08facfc00a06a64ec`.
- Chapter 8 mobile map viewport SHA-256:
  `89d616b3d081b905ab7e9888a86466574bbc2e88b7320495e11177ea54de9099`.
- Chapter 8 mobile figure SHA-256:
  `3d8084713dda355fd13c69f7ccb54a2d6c4a1552d91424e8762e11160fa8ced4`.
- Chapter 8 mobile callout SHA-256:
  `341aa9eef4fbb853d7b232ff7688fa955c83ee892d803c85ade14641879d73db`.
- Combined twelve-figure mobile sheet SHA-256:
  `b311344af2359307e3eccaa99b2b72c119e1a180eb2678f95f97d35351f682cb`.
- Browser report SHA-256:
  `744203740f5c57b0d1830319efe334b21901efcbd749328dccec5992df963a9c`.

Screenshots and the generated `site/` tree remain ignored build evidence. The
canonical JSON, renderer, validation scripts, and review record are tracked.
