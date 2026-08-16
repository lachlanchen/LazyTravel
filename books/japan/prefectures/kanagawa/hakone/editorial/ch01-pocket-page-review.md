# Chapter 1 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-16`. This is a Chapter 1
milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- SHA-256: `5c684439a22475f810b57bcb1ef0b2f629356b7bae057961f8cd581cd9cfc310`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `19` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `17,199` characters
- Visual evidence: `build/qa/books/hakone/ch01-milestone/contact-sheet.png`

## Page Review

| Page | Content | Result |
| ---: | --- | --- |
| 1 | Text-free cover underlay with live trilingual type and four guides | Pass: title field, guide group, review gate, branding, and repository footer are distinct and readable. |
| 2 | How to use the guide | Pass: the mountain-route premise is clear in all three languages without a dense introduction. |
| 3 | Contents | Pass: the active chapter and page reference are aligned. |
| 4 | Chapter opener | Pass: title and coverage line fit cleanly at B6. |
| 5 | `ch01-b001` | Pass: opening route judgment and ruby remain readable. |
| 6 | Lake Ashi figure and caption | Pass: lake and ridges dominate; all four guides remain distinct; the three captions fit below the image. |
| 7 | `ch01-b002` | Pass: map explanation distinguishes height samples from schematic links. |
| 8 | Hakone orientation map | Pass: landscape map, labels, legend, north arrow, caveat, and elevation profile remain legible. |
| 9 | `ch01-b003` | Pass: the multi-phase volcano explanation fits without reducing type. |
| 10 | `ch01-b004` | Pass: approximate chronology and place relationships remain together. |
| 11 | `ch01-b005` | Pass: Lake Ashi elevation and planning consequence fit with bottom clearance. |
| 12 | `ch01-b006` | Pass: transfer callout is prominent but not crowded. |
| 13 | `ch01-b007` | Pass: volcanic safety advice, ruby, and citations remain readable. |
| 14 | `ch01-b008` | Pass: the Fuji judgment fills one restrained highlight without overflow. |
| 15 | `ch01-b009` | Pass: four morning checks remain a usable sequence. |
| 16 | `ch01-b010` | Pass: the gateway bridge leads into Chapter 2 without a padded summary. |
| 17 | Sources, first page | Pass: seven entries and direct links remain legible. |
| 18 | Sources, second page | Pass: the final safety source is not stranded or clipped. |
| 19 | Closing brand page | Pass: restrained close with consistent LazyTravel branding. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- The accepted figure and map variants match their recorded hashes and approved
  provenance.
