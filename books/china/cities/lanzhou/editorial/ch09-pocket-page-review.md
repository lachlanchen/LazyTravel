# Chapter 9 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-23`. This is
a Chapters 1-9 milestone, not the finished Lanzhou destination book.

## Reviewed Artifact

- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `593784c30e4a85cd30640bc9acfa128eced72c085f7a2f9b30090502cafe4b8f`
- Trim and extent: `125 x 176 mm`, `163` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `187,955` characters
- Chapter contact proof:
  `build/qa/books/lanzhou/ch09-proof-pages-v2/contact-sheet.png`, SHA-256
  `733e0766f63efc023aaeb3fbd9f41a7b9326cd115af5f5f8fccfb6e93aa8ccb7`
- Source and closing proof:
  `build/qa/books/lanzhou/ch09-source-pages/contact-sheet.png`, SHA-256
  `3e0d783920798a96412e7acff4651b4f203a02fbe745bb20d23a71d844808361`
- Responsive release QA:
  `build/qa/website/lanzhou-ch09-release/qa.json`, SHA-256
  `319b31e1592345cd04c15c4bfcf651fc33168aef8d13a1119b40d3ed55b299a8`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 131 | Chapter 9 opener and usable-day rule | Pass: the chapter begins with a concrete planning decision; bags, one anchor, a seated meal, and the return remain together. |
| 132 | River-valley orientation figure | Pass: the valley dominates, exactly four guides remain distinct, and the scene introduces scale without replacing route information. |
| 133 | Itinerary-map introduction | Pass: the one-, two-, and three-day choices and the whole-day swap rule are explicit before the diagram. |
| 134 | Itinerary decision map | Pass: all three lanes, the strong one-day `OR`, weather responses, protected items, and cut order remain legible without collision at B6. |
| 135-136 | One-day river plan and bridge figure | Pass: the route crosses once, makes White Pagoda Hill optional by condition, and keeps Zhongshan Bridge visually dominant. |
| 137-138 | One-day museum plan and museum figure | Pass: reservation and opening checks control the day; the substantial museum visit is not compressed into a checklist. |
| 139-140 | Two-day Day 1 and noodle figure | Pass: the west-to-centre museum day includes a real meal, while food remains part of the route rather than a second itinerary. |
| 141-142 | Two-day Day 2 and White Pagoda figure | Pass: one bridge and one complete hill choice fit together; the attraction stays recognizable behind the four guides. |
| 143-145 | Third-day hill choice and Lanshan figure | Pass: only one hill is added, visibility and full descent are checked, and a previous full White Pagoda climb prevents a second hill. |
| 146-147 | Slow old-city alternative and temple figure | Pass: the no-climb branch is coherent, seated, and conditional on safe city walking rather than presented as an all-weather promise. |
| 148-149 | Weather and disruption response | Pass: heat, cold, poor visibility, closure, and heavy rain remove or swap a whole branch without inventing a denser substitute day. |
| 150 | Final cut-order callout | Pass: baggage, booking, meal/rest, station margin, and the reliable return fit cleanly in all three languages with attached ruby. |
| 151-162 | Sources | Pass: all 64 milestone sources retain readable titles, dates, locators, URLs, and evidence boundaries; no entry clips or crosses the footer. |
| 163 | Closing brand page | Pass: LazyTravel, lazying.art, and the repository address remain clear and uncluttered. |

## Automated And Responsive Gates

- Canonical JSON contains ten final Chapter 9 blocks; Chapters 10-11 remain
  outlined and empty.
- Chapter 9 contributes `1,347` reviewed Chinese tokens, `1,756` reviewed
  Japanese tokens, `1,916` website ruby nodes, 24 source entries, one map, and
  seven accepted four-guide figure placements.
- All `166` repository tests and all `25` external-source checks pass.
- The deterministic map rebuild reproduces its SVG, PDF, and `1620 x 2280` PNG
  and records the final B6, desktop, and mobile evidence hashes.
- At `390 px`, the `760 px` map stage pans independently through reviewed left,
  centre, and right positions without vertical clipping.
- XeLaTeX, `qpdf`, embedded-font, trim, searchable-text, reading, citation,
  asset, parity, and desktop/mobile website checks pass.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
