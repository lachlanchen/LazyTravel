# Chapter 11 B6 Pocket Page Review

Status: technical, page-by-page, and whole-book visual review passed on
`2026-08-21`. This completes the 11-chapter Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `9d9e45fa6150e740d335c10da932bea96283f6c90fa01fb1a33d6b1fa596eaa0`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `218` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `253,365` characters
- Whole-book contact: `build/qa/hakone/pocket-release/contact.jpg`, SHA-256
  `8b7b11a2f245959e5ac1fde227946d878f0cdc444fe75504353b07c6b47403c6`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 179 | Chapter 11 opener | Pass: all three short titles fit, and the chapter deck states the travel decision without crowding. |
| 180-181 | `ch11-b001` route rule | Pass: next ticket, actual exit, luggage, one stop, and boarding margin remain one coherent rule with reviewed ruby. |
| 182 | Onward-choice map | Pass: Odawara, Mishima, and Gotemba remain three alternatives; pinyin, furigana, constraints, and the cut rule are legible at B6. |
| 183-184 | Odawara branch | Pass: east-side descent, bag decision, castle approach, and reserved train remain in practical order. |
| 185 | Odawara Castle figure | Pass: the present keep dominates; exactly the four recurring guides remain distinct at pocket size. |
| 186-187 | Odawara history | Pass: present reconstruction, honmaru, Hojo enclosure, 1590 siege, and later dismantling are not collapsed into one era. |
| 188-189 | Mishima branch | Pass: Moto-Hakone bus, station transfer, bag, and one-stop limit remain clear. |
| 190 | Mishima Taisha figure | Pass: the present sanctuary is recognizable and all four guides remain secondary to the place. |
| 191-192 | Shrine or river | Pass: Taisha and Genbe River are alternatives under a tight connection, with wet-surface and bus-delay cuts visible. |
| 193-194 | Mishima history | Pass: unknown foundation, route record, Yoritomo tradition, earthquake, and 1866 buildings remain separate layers. |
| 195-196 | Gotemba branch | Pass: the northern exit, actual bus, Gotemba Line, bag, and onward route are not presented as a Shinkansen transfer. |
| 197 | Niihashi Sengen figure | Pass: the modest station-side shrine is recognizable; the image does not promise Fuji visibility or drinking water. |
| 198-199 | Niihashi context | Pass: ceremony and spring are attributed to local sources and kept apart from current operating conditions. |
| 200-201 | Departure clock | Pass: the text works backwards from boarding and keeps the removable local stop distinct from essential margins. |
| 202 | Final check | Pass: five dated checks fit inside the highlight border with complete ruby and citations. |
| 203-217 | Sources | Pass: all active destination sources, dates, locators, links, and rights notes remain legible. |
| 218 | Closing brand page | Pass: LazyTravel, lazying.art, and the project repository remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull
  box, error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- The Chapter 11 map and three figures match approved provenance and recorded
  B6/mobile evidence.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
