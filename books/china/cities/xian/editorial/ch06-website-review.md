# Xi'an Chapters 1-6 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-15`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 6 URL:
  `http://127.0.0.1:4173/?chapter=ch06-beginning-with-bread`
- Canonical JSON SHA-256:
  `061690550d90147c659642beca4f6dce385783d1515e3dd054742620d9cf6b3a`
- Site manifest SHA-256:
  `0e14dca679a094e99264118fd05878353851efce5ed582a6e4f5f80d1677ac20`

The site payload is the public projection of the same canonical JSON used by
the B6 book. Local source and visual-reference paths are stripped while prose,
readings, citations, captions, checked dates, assets, and public provenance
remain aligned.

## Parity And Interaction

- `62` aligned blocks render: `8` in Chapter 1, `10` each in Chapters 2-4,
  and `12` each in Chapters 5-6.
- Payload parity passes for `6,203` Chinese and `7,846` Japanese tokens.
- Chapter 6 renders `1,569` ruby nodes, one vector map, one figure, one
  highlighted callout, and `21` unique source records.
- The Chapter 6 map loads as the committed `1344`-pixel SVG and stays at a
  readable scale in the mobile pan viewport.
- All five non-map figures load at `1536 x 1024`; dedicated mobile captures
  confirm Aya-chan and Lala Xia in Chapters 2-6.
- Parallel and single-language modes, ruby toggle, direct chapter URLs, chapter
  switching, section navigation, map zoom/reset, and mobile selection pass.
- No console errors, failed requests, local-path leakage, page-level horizontal
  overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: aligned columns, chapter rail, maps, figures, sources, callout, and branding remain clear. |
| Mobile `390 x 844` | Pass: select controls replace the rail; prose stacks by language and ruby remains readable. |
| Chapter 6 map | Pass: enlarged labels, context fields, four-key legend, and disclaimer remain legible while panning. |
| Chapter 6 figure | Pass: all four guides, travel tools, food sequence, and three captions fit without crop. |
| Chapter 6 callout | Pass: coral frame, command title, allergy language, pinyin, and furigana fit without collision. |
| Source list | Pass: titles, locators, checked dates, and links wrap without horizontal spill. |

## Evidence

- Chapter 6 desktop screenshot SHA-256:
  `0cc672a1ebd4705d0f3f744bc746dbef9640a63c3ff27dfc652474a879d012d6`
- Chapter 6 mobile screenshot SHA-256:
  `f941499bd4e36b2006bead31d0e7181bb20ce7f0cc9b3209db65c1bb84ca6d2f`
- Chapter 6 mobile map SHA-256:
  `6a584ded4488ac705b0ecb8e95c4e83eb9f52a15063f794efae313f2a5cad1c7`
- Chapter 6 mobile figure SHA-256:
  `053b262d2714b356139b3a42ad7692586eb7fe3b92c04860d98d9f82c484ea01`
- Chapter 6 mobile callout SHA-256:
  `3331ce80a593e932dcee64f61b506699ad31efe5d053dc177016081d631b256b`
- Browser report SHA-256:
  `2438f585251dfb0c7fc28d6d35690a3b86b34e33417bbafa5aa4e2d64e7e1aaf`

Screenshots and the generated `site/` tree remain ignored build evidence. The
canonical JSON, renderer, validation scripts, and review record are tracked.
