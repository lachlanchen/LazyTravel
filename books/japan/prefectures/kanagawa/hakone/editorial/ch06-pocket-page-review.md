# Chapter 6 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-20`. This is a
Chapters 1-6 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `8a0858f10ef16ec18b447404f68b9c06519dffd446dd7343b1b93d16be16614d`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `103` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `123,623` characters
- Chapter 6 evidence: `build/qa/hakone/ch06-pocket-release/contact.jpg`,
  SHA-256
  `60bbc37f10ecf3e1c0d46a40fd5acabd6e17e558a19aa7b0442701a6615842c2`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 79 | Chapter 6 opener | Pass: the title names the old road and checkpoint while the subtitle states the walk-and-system spine without becoming a synopsis. |
| 80 | `ch06-b001` | Pass: uneven paving, drainage, footwear, weather, and the stop decision form one route-led opening. |
| 81 | Old-road figure | Pass: wet stone and drainage dominate; exactly four guides remain distinct at B6 size. |
| 82 | `ch06-b002` | Pass: the short history visit and longer stone section have separate endings; closure and bus caveats remain dated. |
| 83 | Old Tokaido choice map | Pass: six route nodes, two choices, three bus exits, and the closed lower section remain legible without label collisions. |
| 84 | `ch06-b003` conservation callout | Pass: surviving fabric is kept distinct from repair, drainage, and later care. |
| 85 | `ch06-b004` closure callout | Pass: dates, unavailable section, road detour, footwear, luggage, and safe-exit judgment fit without clipping. |
| 86 | `ch06-b005` | Pass: site geometry leads into the qualified 1619, 1865, and 2007 chronology. |
| 87 | Checkpoint figure | Pass: gate, palisade, reconstructed buildings, hillside, and lake remain recognizable; exactly four guides establish scale. |
| 88 | `ch06-b006` rules callout | Pass: all five 1711 rules and the Hakone-specific correction remain readable with pinyin and furigana. |
| 89 | `ch06-b007` visit sequence | Pass: the forty-five-minute route, optional hillside climb, seasonal hours, last entry, and port access remain distinct. |
| 90 | `ch06-b008` | Pass: amazake ingredients, three mochi choices, portion judgment, and old-road context share one coherent stop. |
| 91 | Amasake Chaya figure | Pass: the tea-house setting and modest food rest dominate; exactly four guides are present without crowding the table. |
| 92 | `ch06-b009` bus callout | Pass: live departure, direction, destination, food order, and ingredient check fit with reviewed whole-name pinyin. |
| 93 | `ch06-b010` itinerary callout | Pass: full-morning and late-arrival plans end at a realistic bus or lodging commitment. |
| 94-102 | Sources | Pass: all active Chapters 1-6 entries, dates, locators, links, and rights notes remain legible. |
| 103 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- All three Chapter 6 figures and the route map match their recorded output
  hashes and approved B6/mobile visual evidence.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
