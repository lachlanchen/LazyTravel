# Chapter 10 Pocket Page Review

Status: passed on `2026-08-16`.

Artifact: `dist/books/xian/xian-pocket-review.pdf`

Chapter 10 occupies physical PDF pages `137-155` in the 172-page B6 review
edition. All 19 pages were rendered at 180 dpi. The landscape figure and map
were inspected at full size in addition to the portrait-page contact review.

## Cover Audit

Physical PDF page `1` uses the text-free
`assets/images/xian/xian-cover-underlay.png` beneath live LaTeX typography.
The 1476 x 2079 raster is embedded at 300 ppi. Exactly four guides occupy the
lower-right city-wall scene; the broad bright title area remains clear, the
pagoda and roofline do not cross the title, and the footer clears the wall,
luggage, and figures. Chinese, Japanese, English, LazyTravel, lazying.art, the
chapter gate, and the GitHub repository all remain selectable text.

## Page Audit

| PDF page | Content | Result |
| ---: | --- | --- |
| 137 | Trilingual Chapter 10 opener | Pass: clear two-, three-, and five-day promise |
| 138 | Small Wild Goose morning opening | Pass: ZH/JA/EN and ruby remain legible |
| 139 | Small Wild Goose Pagoda figure | Pass: attraction dominant; all four guides and caption clear |
| 140 | Nested itinerary explanation | Pass: map caveat stays with the route rule |
| 141 | Two-, three-, and five-day map | Pass: large landscape labels; Day 4 choices remain separate |
| 142 | Five-line day-building rule | Pass: one-page aligned block with sources |
| 143 | Day 1 old core | Pass: route, worship-space note, meal, and sources stay together |
| 144-145 | Day 2 Qin archaeology | Pass: deliberate English continuation, not an orphan |
| 146 | Day 3 southern corridor | Pass: museum facts and pagoda sequence remain on one page |
| 147-148 | Booking fallback | Pass: replacement rule continues cleanly into English |
| 149 | Day 4 choose one nearby place | Pass: four alternatives and return test stay together |
| 150 | Day 5 depth and recovery | Pass: city-depth option and recovery margin fit cleanly |
| 151 | Route emphases | Pass: first visit, history, food, family, and mobility variants fit |
| 152 | Meals on the route | Pass: practical band, all languages, ruby, and sources fit |
| 153 | Keep one hotel base | Pass: concise two-exception rule; no citation-only page |
| 154 | Cut order when delayed | Pass: safety priorities and sources remain on the same page |
| 155 | Five-day pocket plan | Pass: callout border, ruby, sources, footer, and page number clear |

The first layout build exposed four citation-only pages after Blocks 10-13.
The final layout keeps each source row with its block and removes all four
blank pages without reducing the main reading size.

## Build Checks

- PDF SHA-256: `9be7fe32bdf8e9f0540a9e6ebd5389e97c41b27db423f64195babf1709b76d6f`.
- Trim: `125 x 176 mm`; total pages: `172`; file size: `47,245,345` bytes.
- Embedded fonts: `10`; searchable characters: `217,198`.
- `qpdf --check`, schema validation, reading reconstruction, cover/asset QA,
  and strict TeX-log validation pass.
- No overfull/underfull box, missing-character, LaTeX-warning, or package-warning
  diagnostic remains.

## Evidence

- `build/qa/books/xian/cover/xian-cover-text-overlay.png`
- `build/qa/books/xian/ch10/final-139.png`
- `build/qa/books/xian/ch10/final-141.png`
- `build/qa/books/xian/ch10/contact-final-151-155.png`
