# Chapter 10 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-21`. This is a
Chapters 1-10 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `50154ec40d8cd77850e44f25ccf6c3cc376d114909f85d6d6d10c7b06dca7d30`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `193` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `223,095` characters
- Chapters 1-10 contact:
  `build/qa/hakone/ch10-pocket-release/contact.jpg`, SHA-256
  `5bd4966482b8cf1d0260b69ef651acaa193909ae41d6b36de69a462d5e844537`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 158 | Chapter 10 opener | Pass: the three titles and itinerary/transport/attractions/food/hotels/practical/maps deck fit without collision. |
| 159 | `ch10-b001` | Pass: capacity, fixed commitment, removable branch, and usable exit remain one planning rule with reviewed ruby. |
| 160 | Portrait itinerary map | Pass: one-day, one-night, and two-night lanes, pinyin, furigana, weather states, and cut order fill the B6 page without collision. |
| 161 | `ch10-b002` | Pass: the clear one-day crossing protects an early entry, one lake stop, and a working exit without promising a complete loop. |
| 162 | Ropeway figure | Pass: valley, fumaroles, operating-state caveat, and all four guides remain readable. |
| 163 | `ch10-b003` callout | Pass: wind, fog, suspension, and warning responses fit inside the highlight border. |
| 164 | `ch10-b004` | Pass: luggage, arrival, dinner, bath, breakfast, checkout, and departure remain in the correct one-night order. |
| 165 | Ryokan-arrival figure | Pass: the entrance and final transport decision remain dominant over cast staging. |
| 166 | `ch10-b005` | Pass: one museum anchors the day; outdoor and indoor facilities are not combined into a rushed checklist. |
| 167 | Open-Air Museum figure | Pass: the landscape and walking scale remain legible at B6. |
| 168 | `ch10-b006` | Pass: three days exchange whole weather windows and do not restore deleted stops. |
| 169 | Lake Ashi figure | Pass: the crossing illustrates a route choice without promising weather or visibility. |
| 170-171 | `ch10-b007` | Pass: Chinese, Japanese, and English reduced-transfer guidance remains natural and distinguishes each access segment. |
| 172 | Pola rainy-arrival figure | Pass: exactly Aya-chan, Lala Xia, Sasa-kun, and the Zhuangzi robot; museum, forest, canopy, slope, and handrail remain clear. |
| 173-174 | `ch10-b008` | Pass: luggage, lunch, check-in, dinner, rest, and the last useful connection share one practical timeline. |
| 175 | Hakone-Yumoto figure | Pass: arrival threshold, luggage, railway, and onward decisions remain clear. |
| 176-177 | `ch10-b009` | Pass: forecast/warnings, live transport, and booking checks remain three separate decision points. |
| 178 | `ch10-b010` callout | Pass: the cut order remains complete, cited, and inside the highlight border. |
| 179-192 | Sources | Pass: all active Chapters 1-10 entries, dates, locators, links, and rights notes remain legible. |
| 193 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull
  box, error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- The portrait map and Pola figure match approved provenance and their recorded
  B6/mobile evidence.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
