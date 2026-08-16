# Chapter 9 Pocket Page Review

Status: passed on `2026-08-16`.

Artifact: `dist/books/xian/xian-pocket-review.pdf`

Chapter 9 occupies physical PDF pages `120-136` in the 153-page B6 review
edition. Pages were rendered at 120 dpi for contact-sheet review; the map and
figure also retain their separate higher-resolution proofs.

## Page Audit

| PDF page | Content | Result |
| ---: | --- | --- |
| 120 | Trilingual Chapter 9 opener | Pass: clear hierarchy and chapter categories |
| 121 | Arrival-at-the-door opening in ZH/JA/EN | Pass: ruby clear; sources remain with text |
| 122 | South Gate hotel-arrival figure and trilingual caption | Pass: all four guides visible; gate, luggage and entrance legible |
| 123 | Five-area map introduction in ZH/JA/EN | Pass: balanced text page |
| 124 | Five itinerary anchors map | Pass: no label collision; B6 and mobile proofs approved |
| 125 | Inside the wall | Pass: address caveat and room-direction checks readable |
| 126 | South Gate | Pass: official-address example and tradeoff stay together |
| 127 | Yanta/Qujiang | Pass: citations remain on the same page; no orphan page |
| 128 | Xi'an North corridor | Pass: station-access warning and no-shuttle example intact |
| 129 | Lintong overnight decision | Pass: two-day test and moving cost remain together |
| 130 | Five current properties, Chinese and Japanese | Pass: dense list remains legible |
| 131 | Five current properties, English continuation | Pass: deliberate language continuation, not an orphan |
| 132 | Ten checks before payment, Chinese and Japanese | Pass: practical band, ruby and policy note fit cleanly |
| 133 | Ten checks before payment, English continuation | Pass: citations remain with the block |
| 134 | A room that works for two | Pass: all three languages and sources fit without reduced type |
| 135 | One base or a split stay | Pass: complete ZH/JA/EN decision rule on one page |
| 136 | Six final booking checks | Pass: callout border clears footer and page number |

## Build Checks

- PDF SHA-256: `7703a3273523c3fa414947a9fc06fbdb10aab56600ec0099b33b40108415f7bd`.
- Trim: `125 x 176 mm`; total pages: `153`.
- Embedded fonts: `10`; searchable characters: `189,100`.
- `qpdf --check`, schema validation, reading reconstruction, and strict TeX log
  validation pass.
- No `Overfull`, `Underfull`, missing-character, LaTeX-warning, or package-warning
  diagnostics remain.
