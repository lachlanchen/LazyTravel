# Xi'an Chapters 1-5 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-15`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 5 URL:
  `http://127.0.0.1:4173/?chapter=ch05-inside-the-wall`
- Canonical JSON SHA-256:
  `edbbc5b03fa08645865b9355d2bd3599427f89e6a10b0223c696079568eabede`
- Site manifest SHA-256:
  `7c0886c0cfc57993571bb79acea9b1cd15f37ad9a5286f324e7fe36f43c7ba4a`

The static payload is the public projection of the exact canonical JSON used
by the B6 book. Workstation-only citation and provenance paths are removed;
aligned prose, reviewed readings, source IDs, checked dates, captions, and
public provenance remain in parity.

## Parity And Interaction

- `50` aligned blocks render: `8` in Chapter 1, `10` each in Chapters 2-4,
  and `12` in Chapter 5.
- Payload parity passes for `5,026` Chinese and `6,381` Japanese tokens.
- Chapter 5 renders `1,787` ruby nodes, one map, one figure, and `13` unique
  source records.
- The Chapter 5 map loads as the committed `1344`-pixel SVG. On mobile it stays
  at readable scale inside a pannable viewport instead of shrinking labels;
  the focused QA capture reaches the street-scale route panel.
- The lane-to-courtyard figure loads at full source resolution with all three
  captions. Production-method metadata remains in provenance and is not
  repeated in the reading flow.
- Stable vermilion block bubbles, jade and cobalt language markers, and the
  ruby switch do not resize the header or text columns.
- Parallel, Chinese, Japanese, and English modes, the ruby switch, direct query
  loading, chapter switching, and section navigation all pass.
- No console errors, failed requests, workstation paths, page-level horizontal
  overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: three aligned columns, rail navigation, maps, figures, sources, highlight bubbles, and branding remain clear. |
| Mobile `390 x 844` | Pass: chapter and section selects replace the rail; prose stacks by language and pinyin/furigana remain readable. |
| Chapter 5 map | Pass: wall comparison, street-scale route, numbered stops, optional branches, legend, and disclaimer remain legible while panning. |
| Chapter 5 figure | Pass: image, trilingual captions, and editorial label remain visible without crop or reader-facing production note. |
| Source list | Pass: titles, locators, checked dates, and links wrap without horizontal spill. |

## Evidence

- Chapter 5 desktop screenshot SHA-256:
  `056b381b59137ad0bb857732e47277b0c4ce84f81f64bd9502b06edd5a43ec37`
- Chapter 5 mobile screenshot SHA-256:
  `8b13a85ffd4093b9e5c45af56be88faa57f923843bf12037d08f7c75b71b2dcb`
- Chapter 5 mobile map screenshot SHA-256:
  `63cd5c221fd1fd2e01f7fc4313525562b34b537f2b28bfa827621d249369ed43`
- Chapter 5 mobile figure screenshot SHA-256:
  `61067d4c273d4d56737cc26b9427f45a41d633a3f4831b46ac588e68bb1d3a18`
- Browser report SHA-256:
  `b6d08a276da8604c30b6f042d0749dd583bccc3a7f210616cd282ac21e097e27`

Screenshots and the generated `site/` tree remain ignored build evidence. The
renderer, canonical JSON, validation scripts, and this review record are
tracked.
