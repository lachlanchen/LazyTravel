# Chapter 11 B6 Pocket Page Review

Status: technical, editorial, visual, synchronization, and responsive review
passed on `2026-08-23`. This closes all 11 Lanzhou chapters.

## Reviewed Artifact

- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `a6b70500bbe599b636786f4c5bd012c26fb8a3f2a5715909f729f1bc2e8a7dee`
- Trim and extent: `125 x 176 mm`, `216` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `245,973` characters
- Release manifest:
  `dist/books/lanzhou/lanzhou-pocket-review.manifest.json`, SHA-256
  `6c16b07f42f37389633bf30abf5cfc0eaf56ab04932b400f1c8ada61dfa85036`
- Chapter contact proof:
  `build/qa/books/lanzhou/ch11-release-pages/contact-sheet.png`, SHA-256
  `a4fb5e0e573204916ea4184d70efdda3526acfc46c730e8c6b13dc8da7c46012`
- Source and closing proof:
  `build/qa/books/lanzhou/ch11-release-sources/contact-sheet.png`, SHA-256
  `571c7f174d76b758043b369aa588c922b5602e01daf8a6f987f29f3a9756e535`
- Responsive release QA:
  `build/qa/website/lanzhou-ch11-release/qa.json`, SHA-256
  `e966da9759f6fb32d664fcd7c26dab6e1baa5dea8c3d96bc0fefa011bef377a5`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 175 | Chapter 11 opener | Pass: the title and history/attractions/itineraries/transport/practical/map scope establish one nearby-day decision without suggesting a regional loop. |
| 176-178 | Choose one complete return and opening figure | Pass: the latest acceptable lodging return governs the day; three blank cards remain alternatives, and exactly four guides are distinct without false travel text. |
| 179-181 | Decision order and nearby-day map | Pass: the map shows three exclusive complete-return branches, keeps the confluence subordinate to Bingling-Liujiaxia, marks Xinglong provisional, and remains legible at B6. |
| 182-184 | Bingling access and attraction figure | Pass: Liujiaxia and the grotto entrance remain separate decisions; water and road are not improvised into a hybrid, and the cliff and giant Buddha dominate the plate. |
| 185-186 | Cave 169 and the `420 CE` anchor | Pass: the dated inscription changes how the visitor reads a multi-period site without promising special-cave access or turning `420` into a founding date. |
| 187-189 | Yellow-Tao confluence and figure | Pass: the platform remains a separately checked road branch; variable sediment, flow, light, and weather replace any fixed blue-and-yellow promise. |
| 190-192 | Xinglong provisional route and figure | Pass: the `2026-08-23` evidence gap is explicit, the five direct checks remain intact, and the landscape image is not presented as reopening evidence. |
| 193-195 | Ink Danxia managed geology route and figure | Pass: bands, gullies, depth, open sections, internal movement, weather, and return form one useful line; color and access are not promised. |
| 196-197 | Whole-branch cancellation | Pass: weather, operation, mobility, or return failure removes the entire branch and sends the reader to a checked city fallback rather than a second unverified outing. |
| 198-199 | Return-led day bag, food, and turn-back time | Pass: water, medicine, layers, documents, signal, meals, toilets, and food remain practical protections; no concession or restaurant is assumed open. |
| 200 | Six-line nearby-day card | Pass: the final trilingual callout fits on one page with attached pinyin and furigana and closes on one place seen properly and one protected next day. |
| 201-215 | Sources | Pass: all `85` destination sources retain readable titles, dates, locators, URLs, and evidence boundaries without clipping or footer collisions. |
| 216 | Closing brand page | Pass: LazyTravel, lazying.art, and the repository address remain clear and uncluttered. |

## Automated And Responsive Gates

- Canonical JSON contains all `105` Lanzhou blocks and exactly 11 final
  chapters; Chapters 1-10 remain structurally unchanged by the Chapter 11
  promotion.
- Chapter 11 contributes `1,605` reviewed Chinese tokens, `1,973` reviewed
  Japanese tokens, `2,211` website ruby nodes, `18` cited sources, one map,
  and five new exact-four-guide figures.
- All `184` repository tests and all `25` external-source checks pass.
- The deterministic release builder ran twice from the final JSON and produced
  the same PDF SHA-256 both times.
- The nearby-day map reproduces its SVG, vector PDF, and `1620 x 2280` PNG;
  all five figure variants match approved provenance hashes.
- At `390 px`, the `760 px` map stage pans independently; zoom and reset work,
  all five figures load, and no console, request, ruby, source, or layout
  failure occurs.
- XeLaTeX, `qpdf`, embedded-font, trim, searchable-text, reading, citation,
  asset, parity, desktop, and mobile gates pass.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
