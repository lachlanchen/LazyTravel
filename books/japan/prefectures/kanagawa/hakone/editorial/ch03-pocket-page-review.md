# Chapter 3 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-17`. This is a
Chapters 1-3 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `e1660937579401259f9324ed42469b115d3e194e7f66585c8209549a99365814`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `48` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `54,479` characters
- Chapter 3 and source-page evidence:
  `build/qa/books/hakone/ch03-milestone/contact-sheet.png`, SHA-256
  `0883be9ecbbca3ff591d92d6413b20ff67259fdcd8fabb1a7056979bd0a577de`

## Page Review

| Page | Content | Result |
| ---: | --- | --- |
| 30 | Chapter 3 opener | Pass: the railway, art, and stopping question fits clearly with the chapter coverage. |
| 31 | `ch03-b001` | Pass: Ohiradai reversal, crew movement, and signal-station restriction remain together. |
| 32 | Ohiradai figure | Pass: railway and branching track dominate; all four guides and captions remain clear. |
| 33 | `ch03-b002` | Pass: station order, elevation, duration, and schematic limits are distinguished. |
| 34 | Gora slope map | Pass: station labels, three reversals, museum stop, Gora change, metrics, and caveats are legible without collisions. |
| 35 | `ch03-b003` | Pass: 1919 engineering history explains the visible ride without becoming a chronology dump. |
| 36 | `ch03-b004` | Pass: the best-side shortcut is rejected and three observable actions remain prominent. |
| 37 | `ch03-b005` | Pass: the museum arrival and `90-120` minute judgment stay route-led. |
| 38 | Museum landscape | Pass: terrain and walking scale dominate; no identifiable artwork is reproduced. |
| 39 | `ch03-b006` | Pass: dated hours, prices, visit ranges, lockers, and mobility services fit on one page. |
| 40 | `ch03-b007` | Pass: quick food, full lunch, and brought-food rules remain distinct and readable. |
| 41 | Museum food figure | Pass: four guides, food, and the shortened trilingual caption fit on one landscape page. |
| 42 | `ch03-b008` | Pass: the Gora continue-or-stop decision protects luggage, lodging, dinner, and return margin. |
| 43 | `ch03-b009` | Pass: the cable-car handoff leads into Chapter 4 without summary padding. |
| 44-47 | Sources | Pass: all Chapters 1-3 entries, dates, locators, and direct links remain legible. |
| 48 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- All accepted figure and map variants match their recorded hashes and approved
  B6/mobile provenance.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
