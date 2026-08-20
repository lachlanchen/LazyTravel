# Chapter 8 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-20`. This is a
Chapters 1-8 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `85eeb1e47cc65564cbe0894fd1b0e19598d3b1555e8f3c69d0eee8dbab186670`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `146` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `171,312` characters
- Chapter 8 evidence: `build/qa/hakone/ch08-pocket-release/contact.jpg`,
  SHA-256
  `bd5c5d7d306497fe9b59541d2944c8485740c71f2b87f6d923d9d6911f941c3f`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 111 | Chapter 8 opener | Pass: the title names the actual food route and the subtitle keeps the chapter tied to black eggs, amazake, and the dinner clock rather than a restaurant ranking. |
| 112 | `ch08-b001` Chinese/Japanese | Pass: food roles are introduced in route order, with one proper meal and optional stops clearly separated. |
| 113 | `ch08-b001` English | Pass: gateway taste, snack, lunch, old-road rest, and booked dinner remain one coherent decision sequence. |
| 114 | Food-clock map | Pass: all six roles, trilingual labels, readings, optional-node note, and one-lunch rule remain legible at B6 size without collisions. |
| 115 | `ch08-b002` Chinese/Japanese | Pass: the lunch anchor is chosen before climbing without falsely requiring lunch in Odawara. |
| 116 | `ch08-b002` English | Pass: museum, Owakudani, and Lake Ashi remain alternatives; reserve food is not presented as a normal meal. |
| 117 | `ch08-b003` Chinese/Japanese | Pass: the black egg stays a route-sized snack and the local longevity saying is identified as legend. |
| 118 | `ch08-b003` English and sources | Pass: sell-out, ordinary egg, volcanic process, safety, and citations fit without crowding. |
| 119 | Black-egg figure | Pass: the established four guides share one ordinary snack while Owakudani remains recognizable. |
| 120 | `ch08-b004` Chinese/Japanese | Pass: one substantial lunch is selected and Lake Ashi origin is a question, not an unsupported guarantee. |
| 121 | `ch08-b004` English | Pass: museum service levels and wakasagi history remain concrete and qualified. |
| 122 | Lake Ashi wakasagi figure | Pass: the four-guide meal plate shows the lunch scale and keeps origin verification in the caption. |
| 123 | `ch08-b005` | Pass: Amasake Chaya remains an old-road or route-K rest governed by the next bus or walking finish, not a mandatory lunch detour. |
| 124 | Amasake Chaya figure | Pass: the real road-rest setting, four guides, amazake, and mochi remain clear without menu or health claims. |
| 125 | `ch08-b006` Chinese/Japanese | Pass: board-steamed kamaboko, qualified Tenmei-era history, and the transfer-versus-production choice read naturally. |
| 126 | `ch08-b006` English | Pass: the gateway craft is connected to Odawara without claiming all current fish is locally landed. |
| 127 | Kamaboko workshop figure | Pass: exactly four guides, board shaping, steamed form, and sliced texture remain distinct at B6 size; no company, staff, copied mark, or fifth traveler appears. |
| 128 | `ch08-b007` Chinese/Japanese | Pass: a meal-inclusive booking sets the end of the food day and room-only stays receive a separate evening decision. |
| 129 | `ch08-b007` English | Pass: arrival, meal inclusion, delay contact, and kitchen limits remain property-specific. |
| 130 | Ryokan-dinner figure | Pass: the reused approved four-guide scene supports the booked dinner decision without promising a fixed Hakone menu. |
| 131 | `ch08-b008` allergy callout | Pass: ingredient labels, batter, oil, sauce, cross-contact, written confirmation, and the multilingual card fit with readable ruby. |
| 132 | `ch08-b009` Chinese/Japanese | Pass: a closure or transport change leads first to the next connection and last useful food hub. |
| 133 | `ch08-b009` English | Pass: the fallback does not chase a dish, replace lunch with snacks, or make the ryokan wait. |
| 134 | `ch08-b010` route-plan callout | Pass: day trip, ryokan night, and old-road day each contain a real meal, optional snacks, transport margin, and the correct endpoint. |
| 135-145 | Sources | Pass: all active Chapters 1-8 entries, dates, locators, links, and rights notes remain legible. |
| 146 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- The Chapter 8 map and kamaboko figure match their recorded output hashes and
  approved B6/mobile visual evidence; four reused figures retain approved
  provenance.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
