# Xi'an Chapters 1-2 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-14`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 2 URL:
  `http://127.0.0.1:4173/?chapter=ch02-capitals-on-different-maps`
- Site manifest SHA-256:
  `902e0d656a2b153b949e77a4ad88172bf07ecaf3475f1158608aff0267dd1f03`

The static payload is the public projection of the same canonical JSON used by
the B6 book. Only workstation-local citation paths are removed. Chapter order,
aligned prose, readings, citation IDs, visual references, captions, and
provenance remain unchanged.

## Parity And Interaction

- `18` aligned blocks render: `8` in Chapter 1 and `10` in Chapter 2.
- Payload parity passes for `1,695` Chinese and `2,223` Japanese tokens.
- The browser renders `954` Chapter 1 and `1,432` Chapter 2 ruby nodes.
- Both completed chapters are selectable from the desktop rail and mobile
  chapter menu; the nine outlined chapters remain visibly unavailable.
- Parallel, Chinese, Japanese, and English modes update chapter and section
  labels without stale content.
- The ruby switch hides and restores pinyin and furigana without removing base
  text.
- Both SVG maps load, pan, zoom, and reset. Chapter 2's generated figure loads
  from its tracked project asset and carries trilingual non-documentary
  disclosure.
- No console errors, failed requests, workstation paths, page-level horizontal
  overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: three aligned columns, chapter rail, map controls, figure, sources, and branding remain clear. |
| Mobile `390 x 844` | Pass: rail becomes chapter and section selects; prose stacks by language and ruby remains legible. |
| Chapter 2 map | Pass: a legible-width SVG remains pannable instead of shrinking every label into the viewport. |
| Chapter 2 figure | Pass: realistic site impression uses stable width, does not crop the archaeological ground, and retains all captions. |
| Navigation | Pass: direct Chapter 2 query URL, in-page chapter switching, browser back/forward state, and section jumps work. |

## Evidence

- Chapter 1 desktop screenshot SHA-256:
  `bd73f02c9e9a09a566ae051334d80a16df6547edf13dba3e55306000718ef832`
- Chapter 2 desktop screenshot SHA-256:
  `58452389ded776598a27343512398e16d7b1460fb0699d3d923c4850db0a63cf`
- Chapter 2 mobile screenshot SHA-256:
  `25f0bf7ab2ae83fd2b3ec8a50b0094461ca17582cb3ae11e362c3129d81fac95`
- Chapter 2 mobile map screenshot SHA-256:
  `8bff6791ad0a95273e1694b1a1992f7e5fad32b76ac2fc556bc69b15b025e1a2`

Screenshots and the generated `site/` tree remain ignored build evidence. The
renderer, canonical JSON, validation scripts, and this review record are
tracked.
