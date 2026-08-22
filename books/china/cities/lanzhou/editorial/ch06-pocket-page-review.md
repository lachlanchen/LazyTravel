# Chapter 6 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-22`. This is a Chapters
1-6 milestone, not the finished Lanzhou destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_lanzhou_review.py --sync-nutstore`
- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `c85bee576db09f7e1cd40a5f783dec53beb043bc916044aa66bebbd05cb56061`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `101` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `115,221` characters
- Chapter 6 contact proof:
  `build/qa/books/lanzhou/ch06-final-pages/ch06-contact.png`, SHA-256
  `0a307985bbcfb2889b6bd8002feda09411b88bee4fb80f594e7d56633c746306`
- Source/closing contact proof:
  `build/qa/books/lanzhou/ch06-final-pages/sources-contact.png`, SHA-256
  `68b3c31ee17c42c78ecf1082a7e1384c650e1ce303b23f6a561727bfa5ea36cb`
- Responsive release-site QA:
  `build/qa/website/lanzhou-ch06-release/qa.json`, SHA-256
  `4282c81b970d89a80c2e16d3040adfaa6764989a2c2d157261b85ff5940f07cf`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 77 | Chapter 6 opener | Pass: the title establishes one usable day rhythm, with a morning bowl and a limited afternoon choice rather than a food checklist. |
| 78 | `ch06-b001` | Pass: the ordinary morning service sequence, regular portion, bowl components, optional beef and egg, and stop on authenticity hunting read naturally in all three languages. |
| 79 | Beef-noodle morning figure | Pass: one recognisable bowl and a readable shop process lead the scene; exactly four guides are present, with no anonymous diner or fictitious documentary detail. |
| 80 | `ch06-b002` | Pass: same-day opening and payment checks are separated from allergy, vegetarian, halal, ingredient, and shared-equipment questions without inferring answers from a district or shop name. |
| 81 | `ch06-b003` | Pass: the five ordering moves and indicative noodle-name groups remain practical while live shop signs explicitly override the diagram. |
| 82 | Noodle-order diagram | Pass: payment, noodle shape, optional additions, bowl collection, seasoning, and seating remain legible at B6; the width panel is clearly not an exact gauge. |
| 83 | `ch06-b004` | Pass: texture and craft explain what changes in the bowl without ranking one noodle shape as more authentic or turning a founder story into evidence. |
| 84 | `ch06-b005` | Pass: the day rhythm protects the attraction route, omits false exact hours, requires same-day availability checks, and rejects cross-city backtracking for a missed breakfast. |
| 85 | Food-clock diagram | Pass: morning, midday, afternoon, and evening decisions read in one scan; the one-snack branch and stop rule remain prominent and uncrowded. |
| 86 | `ch06-b006` | Pass: *niangpizi*, *huidouzi*, and *tianpeizi* are distinguished by visible form and eating choice, with one portion first rather than three compulsory bowls. |
| 87 | Afternoon-snack figure | Pass: the three foods remain visually distinct, the exact four-guide cast is complete, and the scene supports comparison without suggesting a one-person tasting challenge. |
| 88 | `ch06-b007` | Pass: variable condiments, sweetness, fermentation, allergies, and shared equipment are framed as questions for the actual serving rather than citywide guarantees. |
| 89 | `ch06-b008` | Pass: lily scales, cooking-dependent texture, covered-bowl tea, variable ingredients, and a seated-rest decision remain concrete and free of health folklore. |
| 90 | Lily and *sanpaotai* figure | Pass: the white bulb scales and lidded tea bowl are recognisable; exactly four guides share one dish and one tea setting without extra people or clutter. |
| 91 | `ch06-b009` | Pass: geographical indication, menu name, origin, sugar, caffeine, and ingredients remain separate claims, with clear questions when those distinctions matter. |
| 92 | `ch06-b010` | Pass: the final callout gives a realistic stopping rule, permits sharing, avoids waste and backtracking, and returns dinner to the hotel or onward route. |
| 93-100 | Sources | Pass: all 46 milestone entries retain dates, locators, URLs, licenses where needed, and evidence boundaries without overflow; the final Chapter 6 entries fit cleanly on page 100. |
| 101 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass; all 25 external-source checks
  pass without copying source archives into the repository.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
  Chapters 1-6 contain `6,134` Chinese and `7,878` Japanese reviewed tokens;
  Chapter 6 contributes `1,258` and `1,555` respectively.
- All `145` repository tests pass, including deterministic diagram builds,
  approved evidence hashes, exact four-guide continuity, and the Chapter 7
  production gate.
- XeLaTeX completes twice with no rejected warning, overflow, underflow, error,
  or missing-glyph diagnostic; `qpdf --check`, fonts, searchable text, page
  count, and physical B6 size pass.
- All three generated figures and both deterministic diagrams match approved
  provenance with compiled B6 and actual desktop/`390 px` website evidence.
- Release-site QA passes with `55` aligned blocks, `8,486` ruby nodes, and `51`
  chapter-source entries. Chapter 6 contributes ten blocks, three figures, two
  independently checked maps, nine source entries, and `1,684` ruby nodes; no
  console error, failed request, vertical map clipping, or map-control ambiguity
  remains.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
