# Chapter 3 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-21`. This is a
Chapters 1-3 milestone, not the finished Lanzhou destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_lanzhou_review.py --sync-nutstore`
- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `ae98bbb715d6cf245820bc826a96b3aadc8fc9e81619fa6c57012234c744aaa5`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `45` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `47,438` characters
- Chapter 3 contact proof:
  `build/qa/books/lanzhou/ch03-final-contact.png`, SHA-256
  `b862a893f3a8e145b5bca0ea323a5d915846e159aeb0041a5c3bc24f45e1c62b`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 29 | Chapter 3 opener | Pass: one question and one present-centre walk lead the chapter; the title and three-language hierarchy are clear. |
| 30 | `ch03-b001` | Pass: the present temple, later old-city layer, current access check, and historical limit fit without crowding. |
| 31 | City God Temple figure | Pass: the courtyard and dense current city dominate; exactly four guides remain distinct and the three captions are legible. |
| 32 | `ch03-b002` | Pass: the walking sequence and the difference between approximate gates and current access are explicit before the map. |
| 33 | Historical-walk map | Pass: the route, uncertainty marks, 581/583/619/1081 sequence, Qing chronology, and bridge/rail layer remain readable at B6. |
| 34 | `ch03-b003` Jincheng callout | Pass: regional commandery, changing county seat, and scholarly uncertainty are separated without a false ancient footprint. |
| 35 | `ch03-b004` | Pass: `五泉`, Sui/Tang administration, Song crossing, and the present Chengguan core connect in one bounded sequence. |
| 36 | `ch03-b005` route callout | Pass: Zhangye Road, Xiguan, approximate gate positions, and the turn to the river form usable walking guidance. |
| 37 | `ch03-b006` | Pass: the four Qing institutional dates read as a sequence rather than one invented capital-founding year. |
| 38 | `ch03-b007` | Pass: the 1909 fixed crossing changes movement and hands the detailed bridge visit cleanly to Chapter 4. |
| 39 | `ch03-b008` | Pass: the 1952 railway and 1954 planning evidence explain valley length without claiming that every plan was built. |
| 40 | `ch03-b009` handoff | Pass: four retained layers place the reader at the bridge; White Pagoda Hill remains the next chapter rather than an extra stop. |
| 41-44 | Sources | Pass: all Chapters 1-3 entries, dates, locators, URLs, and evidence boundaries remain legible. |
| 45 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overflow, underflow,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- The current temple figure and historical-walk map match their provenance
  hashes and approved B6 and `390 px` evidence.
- Website QA passes at desktop and mobile widths with `26` aligned blocks,
  `3,226` ruby nodes, no console errors, and no failed requests.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
