# Chapter 2 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-21`. This is a
Chapters 1-2 milestone, not the finished Lanzhou destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_lanzhou_review.py --sync-nutstore`
- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `3f1a0577df925899a9515afcc8858a20d53d1b85cc9a1055fe85a5bbed95def1`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `31` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `29,185` characters
- Chapter 2 contact proof:
  `build/qa/books/lanzhou/ch02-final-contact.png`, SHA-256
  `6724810a5fd3b0690970508a0c4a3272996ecb739caceecebd228355463aed1d`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 15 | Chapter 2 opener | Pass: the three arrival gates are named without turning the opener into a transport catalogue. |
| 16 | `ch02-b001` | Pass: airport arrival, T3/GTC, rail label, baggage, lodging, and first-night segment form one decision. |
| 17 | Zhongchuan T3 figure | Pass: the terminal dominates; exactly four guides remain distinct and the caption is legible. |
| 18 | `ch02-b002` | Pass: the schematic scale warning and west-centre-east use are clear before the map. |
| 19 | Arrival-gates map | Pass: three gates, official station-name distinctions, mode branches, scale warning, and footer remain readable without collisions. |
| 20 | `ch02-b003` | Pass: rail, coach, taxi, and ride-hailing are compared without a frozen timetable or universal winner. |
| 21 | `ch02-b004` fallback callout | Pass: the difference between scheduled margin and usable transfer time remains clear with ruby. |
| 22 | `ch02-b005` | Pass: Lanzhou West and Lanzhou West Station North Square are not conflated. |
| 23 | Lanzhou West figure | Pass: the roof and forecourt dominate; exactly four guides remain distinct at B6 size. |
| 24 | `ch02-b006` | Pass: the western first segment is direct, natural in all three languages, and does not backtrack for bags. |
| 25 | `ch02-b007` | Pass: national-rail and metro labels at Lanzhou Station remain distinct. |
| 26 | Lanzhou Station figure | Pass: clock, frontage, hills, and the four-guide group remain recognizable and uncluttered. |
| 27 | `ch02-b008` | Pass: the westbound transfer and final walk replace the vague instruction “into town.” |
| 28 | `ch02-b009` checklist | Pass: ticketed gate, Chinese lodging address, first stop, transport branch, and fallback fit in one callout. |
| 29-30 | Sources | Pass: all Chapters 1-2 entries, dates, locators, links, and evidence boundaries remain legible. |
| 31 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overflow, underflow,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- Three figures and the arrival map match their output hashes and approved B6
  and `390 px` visual evidence.
- Website QA passes at desktop and mobile widths with `17` aligned blocks,
  `1,964` ruby nodes, no console errors, and no failed requests.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
