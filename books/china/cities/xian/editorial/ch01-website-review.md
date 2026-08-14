# Chapter 1 Website Review

Status: parity, interaction, and visual review passed on `2026-08-14`; Chapter 1
remains a review edition pending destination-book approval.

## Reviewed Build

- Build: `python3 scripts/build_website.py`
- Parity: `python3 scripts/validate_site_parity.py`
- Browser QA: `python3 scripts/qa_website.py --url http://127.0.0.1:4173/`
- Local review URL: `http://127.0.0.1:4173/`
- Generated manifest SHA-256:
  `64950769691eb9d1a3517b8dc664deea2e3a28164e745dfcabbc757ebaac36ee`

The browser payload is a deterministic public projection of
`data/china/cities/xian/book.json`. It removes workstation-only citation paths
but preserves the book metadata, chapter order, every ZH/JA/EN paragraph,
all reading tokens, citation IDs, asset references, captions, and provenance.

## Parity And Interaction

- `8` aligned Chapter 1 blocks rendered in canonical order.
- `696` Chinese and `886` Japanese source tokens passed payload parity.
- `954` reading-bearing tokens rendered as HTML ruby elements.
- `11` first-use citations matched the pocket-book citation sequence.
- Parallel, Chinese, Japanese, and English modes switched without stale panels.
- The ruby switch hid and restored pinyin and furigana without changing base text.
- Map zoom and reset worked; the small-screen reset returns to the Xi'an marker.
- No console errors, failed requests, leaked `/home/...` paths, or page-level
  horizontal overflow were found.

## Visual Review

| Surface | Result |
| --- | --- |
| Header and controls | Pass at `1440 x 1000` and `390 x 844`; labels fit and controls do not overlap. |
| Desktop navigation | Pass: current Chapter 1 sections appear before the future book outline. |
| Mobile navigation | Pass: the rail becomes one section menu without obscuring the chapter. |
| Chapter masthead | Pass: Xi'an and the chapter are first-viewport signals; the first reading block remains visible below. |
| Blocks 01-02 | Pass: three-column desktop alignment and stacked mobile ruby remain legible. |
| Block 03 and map | Pass: vector map loads; desktop fits cleanly; mobile keeps a legible-width pannable view centred on Xi'an. |
| Blocks 04-06 | Pass: dense names and the dated `CHECKED 2026-08-14` label remain distinct. |
| Blocks 07-08 | Pass: practical orientation and chapter transition retain readable measure and spacing. |
| Sources and footer | Pass: all cited locators fit, external links wrap, and branding is consistent. |

## Evidence

- Desktop full-page screenshot SHA-256:
  `efdda6e541a5627facf1c962b6aa0ec72d5076554e256d808689cb2f2f8ca4d8`
- Mobile full-page screenshot SHA-256:
  `2b94eb4415fb30666fc00e9afab5f63d6846699ffcc1f9db56fdb353ae32faaf`
- Mobile map screenshot SHA-256:
  `bc329f07ef3c60d4e2df96bde24a8f2f55aaac711a43a98d12a1e44674ebfce9`

The screenshots and `site/` output are generated evidence under ignored build
paths. Their source, validation code, and review record are tracked.
