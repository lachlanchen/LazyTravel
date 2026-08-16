# Chapter 11 Pocket Page Review

Status: passed on `2026-08-16`.

Artifact: `dist/books/xian/xian-pocket-review.pdf`

Chapter 11 occupies physical PDF pages `156-177` in the 195-page B6 review
edition. All 22 pages were rendered at 150 dpi for continuous review; the
corrected emergency block and final checklist on pages `175-177` were rendered
again at 180 dpi and inspected at full size.

## Page Audit

| PDF page | Content | Result |
| ---: | --- | --- |
| 156 | Trilingual Chapter 11 opener | Pass: booking, conditions, and local rules establish the departure gate |
| 157 | Arrival-night evidence check | Pass: four-document rule remains a narrative opening, not a generic checklist |
| 158 | Four guides at the hotel table | Pass: Aya, Lala, Sasa, and Zhuangzi are clear; wall view and travel tools remain legible |
| 159 | Fixed points before optional stops | Pass: booking, transport, fallback, and offline-record fields fit together |
| 160-161 | Dated booking snapshot | Pass: museum-specific rules, passport handling, change warning, and sources remain explicit |
| 162-163 | Failed-booking replacement | Pass: replacement day and cancellation discipline continue without an orphan |
| 164 | Opening-day verification | Pass: rejects the false universal Monday rule and keeps the same-day check concise |
| 165-166 | Weather checked twice | Pass: origin/destination checks and the outdoor fallback remain together |
| 167 | Air quality as a current condition | Pass: temporary conditions are clearly separated from durable city description |
| 168-169 | Ticket, document, traveler, station | Pass: complete station names and identity checks remain readable across the continuation |
| 170-171 | Hotel as a reachable address | Pass: Chinese address, entrance, telephone, and late-arrival procedure stay actionable |
| 172 | Venue and worship-space conduct | Pass: current signs and staff correctly outrank the printed guide |
| 173-174 | Food-allergy card | Pass: exact allergen, cross-contact uncertainty, medicine, and companion roles stay together |
| 175-176 | Emergency location script | Pass: `110`, `119`, and `120` are distinct; the English heading now wraps without hyphenating a key word |
| 177 | Seven checks before departure | Pass: border, ruby, sources, footer, and final narrative close fit on one page |

The first strict build exposed an overfull final callout and an unwanted blank
page. The renderer now keeps the callout marker inside its unbreakable box, and
the reduced internal spacing fits the complete trilingual checklist without
shrinking body text. A later visual pass caught the English heading split as
`Emer-gency`; the final wording removes that defect.

## Build Checks

- PDF SHA-256: `ae2872703174ea523b051ccba21e34eeaa2182aba323bc68a23e5cf558af83c5`.
- Trim: `125 x 176 mm`; total pages: `195`; file size: `49,536,558` bytes.
- Embedded fonts: `10`; searchable text is present across the complete book.
- `qpdf --check`, both JSON schemas, reading reconstruction, image provenance,
  cover/asset QA, and strict TeX-log validation pass.
- No rejected overfull/underfull box, missing-character, LaTeX-warning, or
  package-warning diagnostic remains.

## Evidence

- `build/qa/books/xian/ch11-final-pages/contact-156-159.png`
- `build/qa/books/xian/ch11-final-pages/contact-160-163.png`
- `build/qa/books/xian/ch11-final-pages/contact-164-167.png`
- `build/qa/books/xian/ch11-final-pages/contact-168-171.png`
- `build/qa/books/xian/ch11-final-pages/contact-172-175.png`
- `build/qa/books/xian/ch11-final-pages/contact-176-177.png`
- `build/qa/books/xian/ch11-final-rebuild/page-175.png`
- `build/qa/books/xian/ch11-final-rebuild/page-177.png`
