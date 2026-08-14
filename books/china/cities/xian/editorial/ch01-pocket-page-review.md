# Chapter 1 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-14`; chapter content remains
an editorial review edition, not a finished destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-ch01-pocket-review.pdf`
- SHA-256: `0e77de8b36af4c1ce0e952befe5239102c52d30a9f40cbda37c51369cc64a1e4`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `16` pages
- Raster review: all pages at `200 dpi`, with ruby-heavy pages and the map checked
  at full resolution

## Page Review

| Page | Content | Result |
| ---: | --- | --- |
| 1 | Trilingual cover and branding | Pass: hierarchy, trim, repository line, and edition label are clear. |
| 2 | Review-edition note | Pass: three languages remain legible without crowding. |
| 3 | Contents | Pass: destinations and page references align. |
| 4 | Chapter opener | Pass: title hierarchy is balanced at B6. |
| 5 | `ch01-b001` | Pass after repair: pinyin and furigana are readable; no punctuation begins a line. |
| 6 | `ch01-b002` | Pass: aligned language order and citations are intact. |
| 7 | `ch01-b003` | Pass: map introduction fits without compression. |
| 8 | Orientation map | Pass: landscape rotation, river labels, scale, north arrow, and provenance line are legible. |
| 9 | `ch01-b004` | Pass: no overlap, clipping, or detached citation marker. |
| 10 | `ch01-b005` | Pass: dense place-name readings remain distinguishable. |
| 11 | `ch01-b006` | Pass: dated conservation material remains visually separate and readable. |
| 12 | `ch01-b007` | Pass: longest practical block retains bottom clearance. |
| 13 | `ch01-b008` | Pass: dynasty sequence and conclusion fit without a forced type reduction. |
| 14 | Sources, first page | Pass: titles, locators, licences, and links are readable. |
| 15 | Sources, second page | Pass: continuation and final entries are not stranded or clipped. |
| 16 | Closing brand page | Pass: restrained close with consistent branding. |

## Automated Gates

- Both JSON schemas pass.
- Chinese and Japanese token layers reconstruct their canonical paragraphs exactly.
- All Han-bearing Chinese and kanji-bearing Japanese tokens have reviewed readings.
- XeLaTeX completes twice with no rejected warnings, overfull boxes, underfull boxes,
  or missing glyphs.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page-count
  inspection, and physical B6-size inspection pass.

The warning and visual gates are complementary. The first technically valid draft
still allowed Chinese and Japanese closing punctuation at line starts; the renderer
was repaired and this report describes the rebuilt artifact.
