# Chapter 5 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-17`. This is a
Chapters 1-5 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --skip-map --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `8c6a0835c9a1195662981b4d5d02ab4b2b6f39d529d0aed2b3108071c159a430`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `86` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `100,947` characters
- Chapter 5 evidence: `build/qa/hakone-ch05-proof-final/contact-01.jpg`,
  `contact-02.jpg`, and `contact-03.jpg`, with SHA-256 values
  `886334abdf5eaa26417336a4a635e6b3464a9c9ee3beab7e0ec59572c0a4a8f9`,
  `e67ccf7939571970be350d6ffb20406f4285889ef060f3f0c6d47d3b2e3d6a01`, and
  `7e92aacb71feb63bad65bf86e12b0bbf4632cef16a7b02c20bd84f1a5dc63fec`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 62 | Chapter 5 opener | Pass: the compact title names the lake, shrine, wakasagi, and shore without wrapping or turning the opener into a synopsis. |
| 63 | `ch05-b001` | Pass: Togendai begins with one useful choice among port, first place, and onward direction. |
| 64 | Togendai figure | Pass: the harbor and boarding decision dominate; exactly four guides remain visible at B6 size. |
| 65 | `ch05-b002` | Pass: the prose explains how to use the diagram and keeps boat time distinct from stop time. |
| 66 | Lake Ashi choice map | Pass: ports, shrine, wakasagi lunch, park, three stop ranges, and the bus fallback remain legible without collisions. |
| 67 | `ch05-b003` | Pass: lake elevation, ridges, visibility, and the value of the crossing form one place-led paragraph. |
| 68 | Lake-crossing figure | Pass: the lake and enclosing ridges dominate, four guides are present, and no Fuji view is promised. |
| 69 | `ch05-b004` weather callout | Pass: rain, wind, fog, route changes, and the bus alternative remain distinct and unclipped. |
| 70 | `ch05-b005` | Pass: the visible shrine approach carries the history; early chronology is explicitly attributed to shrine tradition. |
| 71 | Shrine figure | Pass: the cedar approach and stair remain the subject; exactly four guides establish scale. |
| 72 | `ch05-b006` etiquette callout | Pass: worship, temizu, the modern Heiwa torii, and queue judgment remain readable with ruby. |
| 73 | `ch05-b007` | Pass: the 1918 introduction and current food preparations connect directly to a Lake Ashi lunch choice. |
| 74 | Wakasagi figure | Pass: fried wakasagi and nanbanzuke are recognizable; the meal, lake setting, and four guides remain clear. |
| 75 | `ch05-b008` | Pass: season, stock, origin, preparation, and restaurant confirmation fit on one page without padding. |
| 76 | `ch05-b009` | Pass: surviving foundations and the current observation building are not confused with the vanished imperial villa. |
| 77 | Onshi Park figure | Pass: the corrected current facade, lawn, site trace, and four guides remain legible and uncluttered. |
| 78 | `ch05-b010` itinerary callout | Pass: early and late arrivals, changed landings, onward bus, lodging dinner, and Chapter 6 handoff close one coherent day. |
| 79-85 | Sources | Pass: all Chapters 1-5 entries, dates, locators, links, and rights notes remain legible. |
| 86 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- All five figures and the map match their recorded output hashes and approved
  B6/mobile visual evidence.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
