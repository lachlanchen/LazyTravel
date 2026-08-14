# Xi'an Chapters 1-3 Website Review

Status: data parity, interaction, and responsive visual review passed on
`2026-08-14`.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Chapter 3 URL:
  `http://127.0.0.1:4173/?chapter=ch03-army-under-earth`
- Site manifest SHA-256:
  `f2c938c1d8e588f353776b31678f3931470efe6ed556a931dbdf5578551e1185`

The static payload is the public projection of the same canonical JSON used by
the B6 book. Only workstation-local citation paths are removed. Chapter order,
aligned prose, readings, citation IDs, visual references, captions, and
provenance remain unchanged.

## Parity And Interaction

- `28` aligned blocks render: `8` in Chapter 1 and `10` each in Chapters 2 and
  3.
- Payload parity passes for `2,698` Chinese and `3,476` Japanese tokens.
- Chapter 3 renders `1,358` ruby nodes, one map, one figure, and `14` unique
  source records.
- All three completed chapters are selectable from the desktop rail and mobile
  chapter menu; the eight outlined chapters remain visibly unavailable.
- Parallel, Chinese, Japanese, and English modes update chapter and section
  labels without stale content.
- The ruby switch hides and restores pinyin and furigana without removing base
  text.
- The Chapter 3 SVG map loads, pans, zooms, and resets. Its `1344`-pixel natural
  width is retained on mobile so labels remain readable through horizontal
  panning.
- The conservation-work figure loads from its tracked project asset and carries
  trilingual AI-generated, non-documentary disclosure.
- The direct Chapter 3 query URL, browser history, chapter switching, and
  section jumps work.
- No console errors, failed requests, workstation paths, page-level horizontal
  overflow, or header-control overlap were detected.

## Responsive Review

| Surface | Result |
| --- | --- |
| Desktop `1440 x 1000` | Pass: three aligned columns, chapter rail, map controls, figure, sources, and branding remain clear. |
| Mobile `390 x 844` | Pass: navigation becomes chapter and section selects; prose stacks by language and ruby remains legible. |
| Chapter 3 map | Pass: both landscape and pit-plan scales remain legible and pannable without pretending to be a navigation map. |
| Chapter 3 figure | Pass: tools, fragments, hands, and work surface remain visible without crop; the disclosure captions remain attached. |
| Navigation | Pass: direct query loading, in-page switching, browser back/forward state, and section jumps preserve Chapter 3. |

## Evidence

- Chapter 3 desktop screenshot SHA-256:
  `0034f8e30a5d43161509c60705521acceb34d20fa55e93f40e9a51cb55e60a92`
- Chapter 3 mobile screenshot SHA-256:
  `a2b0b218a2e3f64ac9aecf21968b7b607cb37689d99024b067c6416dc0917072`
- Chapter 3 mobile map screenshot SHA-256:
  `a48d85463193be0af715e895d8e35ac0fa367ba0466d9c96932b6e3557fbf40a`
- Chapter 3 mobile figure screenshot SHA-256:
  `fec38740db44e5806e15e09a7bcc92ee87a03cfde0362a58dcd665ff67aed80a`

Screenshots and the generated `site/` tree remain ignored build evidence. The
renderer, canonical JSON, validation scripts, and this review record are
tracked.
