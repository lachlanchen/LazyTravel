# Xi'an Chapters 1-4 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-15`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 4 URL:
  `http://127.0.0.1:4173/?chapter=ch04-let-text-lead`
- Canonical JSON SHA-256:
  `4a4b521b33deb14ca3d3584b9f94e18fd371999220bf5c68544ff1d67c27e4d5`
- Site manifest SHA-256:
  `48fe89fae99ba3b02c9e4aa442efa5212bce1f5a29cb13dbfc1dcd2bf72bd548`

The static payload is the public projection of the exact canonical JSON used
by the B6 book. Workstation-only citation and provenance paths are removed;
aligned prose, reviewed readings, source IDs, checked dates, captions, rights,
and public provenance remain in parity.

## Parity And Interaction

- `38` aligned blocks render: `8` in Chapter 1 and `10` each in Chapters 2-4.
- Payload parity passes for `3,734` Chinese and `4,807` Japanese tokens.
- Chapter 4 renders `1,418` ruby nodes, one map, one figure, and `22` unique
  source records.
- The Chapter 4 map loads as the committed `1344`-pixel SVG, remains wider than
  the mobile viewport, and supports pan, zoom, and reset without page overflow.
- The realistic replica-rubbing figure loads at full source resolution with
  trilingual AI-generated, non-documentary disclosure and a human-readable
  editorial label.
- Every source entry shows its own checked date; no blanket stale date or
  internal asset slug is exposed.
- Parallel, Chinese, Japanese, and English modes, the ruby switch, direct query
  loading, chapter switching, and section navigation all pass.
- No console errors, failed requests, workstation paths, page-level horizontal
  overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: three aligned columns, rail navigation, map controls, figure, sources, and branding remain clear. |
| Mobile `390 x 844` | Pass: chapter and section selects replace the rail; prose stacks by language and ruby remains readable. |
| Chapter 4 map | Pass: numbered sites, wall, generalized Tang field, scale, and route disclaimer remain legible in the pannable viewport. |
| Chapter 4 figure | Pass: hands, tamping pad, paper, resin replica, tools, captions, and rights remain visible without crop. |
| Source list | Pass: titles, locators, checked dates, and links wrap without horizontal spill. |

## Evidence

- Chapter 4 desktop screenshot SHA-256:
  `a7f20e546b6e17da01201bf95eb52916d5759c21ef3419d3663a92d2f980a067`
- Chapter 4 mobile screenshot SHA-256:
  `a0a1019061f380615765996d131a933a9558d3c8874926c696e34ae50511e7aa`
- Chapter 4 mobile map screenshot SHA-256:
  `2e877d644968071f53bfd65320c0c753d46a3f641a164bced994c0613593bcf3`
- Chapter 4 mobile figure screenshot SHA-256:
  `f6e83b7f78dfd0b9603905b42372d2aa98cbc70c557f2d70e93fed6e954e2bd0`
- Browser report SHA-256:
  `91ec3195aa875219a615658c827f29a373109a07480260af588df09422b417f0`

Screenshots and the generated `site/` tree remain ignored build evidence. The
renderer, canonical JSON, validation scripts, and this review record are
tracked.
