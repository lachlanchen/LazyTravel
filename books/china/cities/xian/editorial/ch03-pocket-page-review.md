# Xi'an Chapters 1-3 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-14`.
Chapter 3 remains part of a review edition until the complete Xi'an book is
approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `f88890d9a85288acb9f49007f0b9e737bc7abf96bdde4a040312a42c807e0f58`
- Manifest SHA-256: `7273f5a575db247e0c6d71755fe6a80a4c02f186f1bc9c3c2d46f31d0f2a64eb`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `44` pages
- Searchable text: `49,046` non-whitespace characters
- Fonts: `10` embedded font records
- Chapter 3 contact-sheet SHA-256:
  `70c75bd97c4e3c29578e644fbe6c12950258dfb7348d57b8bb3336f57fc345eb`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 1-26 | Cover, contents, Chapters 1-2 | Pass: prior reviewed material remains intact; Chapter 1 and 2 openers were inspected again after the shared title adjustment. |
| 27 | Chapter 3 opener | Pass after revision: the full English title remains on one line without forced hyphenation; trilingual hierarchy and coverage line fit. |
| 28 | `ch03-b001` | Pass: burial mound, warrior pits, and wider mausoleum landscape remain distinct in all three languages. |
| 29 | `ch03-b002` | Pass: the 1974 discovery and subsequent archaeological work fit with readable ruby and source markers. |
| 30 | `ch03-b003` | Pass: pit construction, collapse, and fire evidence retain cautious wording and bottom clearance. |
| 31 | `ch03-b004` | Pass: the two map scales and their limitations are established before the visual. |
| 32 | Qin mausoleum and pits map | Pass: landscape rotation, east-west relation, common-scale pit plans, labels, captions, and schematic warning are legible at B6. |
| 33 | `ch03-b005` | Pass: Pit 1 formation is clearly presented as a funerary representation rather than a battlefield photograph. |
| 34 | `ch03-b006` | Pass: Pit 2 unit groups and unexposed areas fit without compressing the reading layers. |
| 35 | `ch03-b007` | Pass: Pit 3's command or ceremonial reading remains explicitly qualified in Chinese, Japanese, and English. |
| 36 | `ch03-b008` | Pass: organized production and controlled variation are explained without portrait or single-mould claims. |
| 37 | `ch03-b009` | Pass: polychromy and conservation lead naturally into the generated editorial figure. |
| 38 | Conservation-work figure | Pass: realistic image and all three AI-generated, non-documentary captions occupy one landscape page without cropping or spill. |
| 39 | `ch03-b010` | Pass after revision: the dated two-area Lintong visit fits on one page and preserves reservation, shuttle, timing, and Chapter 7 cross-reference. |
| 40-43 | Sources | Pass: `29` first-use records are legible, complete, and unclipped; the final four-entry page retains useful breathing room. |
| 44 | Closing brand page | Pass: restrained lazying.art, LazyTravel, and repository close. |

## Automated Gates

- Destination and source-catalog schemas pass.
- All Chinese and Japanese reading arrays reconstruct canonical prose exactly.
- XeLaTeX completes twice with no overfull boxes, underfull boxes, missing
  glyphs, or accepted warning exceptions.
- `qpdf --check`, embedded-font inspection, physical trim inspection, page-count
  inspection, and searchable-text inspection pass.
- Repeated map generation produces stable SVG and provenance checksums.
- The first Chapter 3 opener was rejected because the English title hyphenated
  `Formation`; the accepted title profile keeps it on one line.
- The first practical-page draft was rejected because its English continuation
  spilled onto a source page; the accepted block fits page 39 without dropping
  operational cautions.
