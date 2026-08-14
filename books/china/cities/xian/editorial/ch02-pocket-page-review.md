# Xi'an Chapters 1-2 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-14`.
Chapter 2 remains part of a review edition until the complete Xi'an book is
approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `35948263bedd9a70edd987c94be8ef248ae0b510188ed495db74fd3c0495643b`
- Manifest SHA-256: `655676326b485001d401f340c300eb898273637aae1dcffa00db5a67ecf983d8`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `30` pages
- Searchable text: `31,540` non-whitespace characters
- Fonts: `10` embedded font records

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 1 | Trilingual cover | Pass: title, China Cities identity, lazying.art, LazyTravel, GitHub, and review range are clear. |
| 2 | Review-edition note | Pass: source-use and aligned-JSON policy fit in all three languages. |
| 3 | Contents | Pass: Chapters 1 and 2 and source page numbers match the built PDF. |
| 4 | Chapter 1 opener | Pass: hierarchy and coverage line remain balanced at B6. |
| 5 | `ch01-b001` | Pass: ruby, punctuation binding, and English measure remain legible. |
| 6 | `ch01-b002` | Pass: terrain sequence fits with bottom clearance. |
| 7 | `ch01-b003` | Pass: map-use warning and citations stay attached to the block. |
| 8 | Chapter 1 orientation map | Pass: landscape rotation, labels, scale, and provenance are legible. |
| 9 | `ch01-b004` | Pass: Guanzhong explanation is not crowded. |
| 10 | `ch01-b005` | Pass: eight water names and readings remain distinguishable. |
| 11 | `ch01-b006` | Pass: dated policy material is visually separated from durable geography. |
| 12 | `ch01-b007` | Pass: field-orientation marker and longest language panels fit. |
| 13 | `ch01-b008` | Pass: transition to successive capitals ends cleanly. |
| 14 | Chapter 2 opener | Pass: new chapter is unmistakable and coverage is concise. |
| 15 | `ch02-b001` | Pass: Ming wall versus Sui-Tang outer city distinction fits without compression. |
| 16 | `ch02-b002` | Pass: schematic-map limitations precede the visual. |
| 17 | Successive-capitals map | Pass after revision: primary labels are readable, Qin is visibly separated from Han, and the Ming wall remains nested inside the Sui-Tang field. |
| 18 | `ch02-b003` | Pass: Feng and Hao stay readable with reviewed proper-name ruby. |
| 19 | `ch02-b004` | Pass: Qin palace and funerary sites remain distinct in all languages. |
| 20 | `ch02-b005` | Pass: Weiyang area figure is clearly described as a precinct. |
| 21 | `ch02-b006` | Pass: palace city, imperial city, outer city, wards, and pagodas fit cleanly. |
| 22 | `ch02-b007` | Pass: Daming date, scale, zone sequence, and visual disclosure remain together. |
| 23 | Daming site-scale figure | Pass after repair: realistic image and all three disclosure captions occupy one landscape page; no spill page remains. |
| 24 | `ch02-b008` | Pass: 904 contraction and limited street continuity fit with no clipped ruby. |
| 25 | `ch02-b009` | Pass: 1369, 1384, and 1582 remain distinct and readable. |
| 26 | `ch02-b010` | Pass: practical sequence and four field questions retain bottom clearance. |
| 27 | Sources, page 1 | Pass: first-use numbering, titles, locators, licences, and links are legible. |
| 28 | Sources, page 2 | Pass: continuation is balanced; no entry is clipped or orphaned. |
| 29 | Sources, page 3 | Pass: Chapter 2 official and open-guide records finish cleanly. |
| 30 | Closing brand page | Pass: restrained LazyTravel and repository close. |

## Automated Gates

- Destination and source-catalog schemas pass.
- All Chinese and Japanese reading arrays reconstruct canonical prose exactly.
- XeLaTeX completes twice with no overfull boxes, underfull boxes, missing
  glyphs, or accepted warning exceptions.
- `qpdf --check`, embedded-font inspection, physical trim inspection, page-count
  inspection, and searchable-text inspection pass.
- The first enlargement attempt was rejected because a figure caption moved to
  a nearly empty second landscape page. The accepted build restores the figure
  and its three captions to one page.
