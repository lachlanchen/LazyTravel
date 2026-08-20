# Chapter 9 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-20`. This is a
Chapters 1-9 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `0cac4d2fda8e163d638f06396ed8bbb7673be2c8acefcc6b6b78df5410875e77`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `170` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `198,073` characters
- Chapter 9 evidence: `build/qa/hakone/ch09-pocket-release/contact.jpg`,
  SHA-256
  `a335d593aaccd4c1b666b50c9fbd72a1c695460ade802293f260235a572a2da0`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 135 | Chapter 9 opener | Pass: the concise Chinese title is shared with canonical JSON and fits one line; Japanese, English, and the hotel/transport/practical/map deck remain balanced. |
| 136 | `ch09-b001` Chinese/Japanese | Pass: five districts are introduced as travel decisions, with arrival, dinner, next morning, entrance, and bad-weather exit kept together. |
| 137 | `ch09-b001` English | Pass: the district-before-room rule and all eight sources fit without crowding. |
| 138 | Five-zone stay map | Pass: all five zones, readings, arrival/dinner/morning sequence, and decision strip remain legible at 300 dpi with no label collision. |
| 139 | `ch09-b002` Chinese/Japanese | Pass: Yumoto and Tonosawa serve the eastern arrival without turning older onsen history into a room-feature promise. |
| 140 | `ch09-b002` English | Pass: bridge, slope, steps, entrance, luggage, and reserved pickup remain concrete. |
| 141 | Ryokan-arrival figure | Pass: the approved four-guide scene supports the final-transport decision; the property confirmation, not the image, controls arrival. |
| 142 | `ch09-b003` Chinese/Japanese | Pass: Miyanoshita and Kowakudani stay distinct, and the revised Japanese walking-route sentence reads naturally. |
| 143 | `ch09-b003` English | Pass: railway sequence, slopes, exact side of the road, and luggage test remain one corridor decision. |
| 144 | `ch09-b004` Chinese/Japanese | Pass: Gora's upper-route gain and eastbound cost are stated without calling it universally central. |
| 145 | `ch09-b004` English | Pass: the higher start and interchange reduce backtracking only when tomorrow genuinely begins uphill. |
| 146 | `ch09-b005` Chinese/Japanese | Pass: Sengokuhara is a broad highland; the property stop, evening return, walking space, and disruption exit remain explicit. |
| 147 | `ch09-b005` English | Pass: museums and grassland justify the base only when the matching bus stop shortens the evening journey. |
| 148 | `ch09-b006` Chinese/Japanese | Pass: the lake shore is split into real northern, southern, Hakone-en, and upland approaches. |
| 149 | `ch09-b006` English | Pass: a lake or Fuji view remains weather-dependent and cannot replace a bus fallback or included dinner. |
| 150 | `ch09-b007` Chinese/Japanese | Pass: room, bedding, bathroom, steps, bath, meals, tattoo policy, arrival, and checkout are checked separately with readable ruby. |
| 151 | `ch09-b007` English | Pass: written answers replace assumptions about what a ryokan normally provides. |
| 152 | Room-check figure | Pass: exactly four established guides, one coherent room, threshold, bed height, suitcase space, chair, and washroom route remain clear; no property or accessibility claim appears. |
| 153 | `ch09-b008` Chinese/Japanese | Pass: luggage delivery, partner status, shuttle details, and the most uncertain final section fit cleanly. |
| 154 | `ch09-b008` English | Pass: volatile luggage and transport conditions are dated and left for current recheck. |
| 155 | `ch09-b009` Chinese/Japanese | Pass: official filters create only a shortlist; the exact room and written enquiry still control. |
| 156 | `ch09-b009` English | Pass: whole-night usability and route cost replace a headline room-rate comparison. |
| 157 | `ch09-b010` itinerary callout | Pass: four realistic district fits, ruby, sources, and the poor-weather rule remain inside the highlight border and above the footer. |
| 158-169 | Sources | Pass: all active Chapters 1-9 entries, dates, locators, links, and rights notes remain legible. |
| 170 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- The new map and room figure match their recorded outputs and approved
  B6/mobile visual evidence; the reused arrival figure retains approved
  provenance.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
