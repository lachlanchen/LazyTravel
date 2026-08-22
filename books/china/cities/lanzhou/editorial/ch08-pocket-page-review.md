# Chapter 8 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-22`. This is
a Chapters 1-8 milestone, not the finished Lanzhou destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_lanzhou_review.py --sync-nutstore`
- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `57245b223cd477534f824a6ff276ff0f5dd05cb53a14262eb3acd06a0da4126a`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `141` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `164,223` characters
- Chapter 8 first contact proof:
  `build/qa/books/lanzhou/ch08-final-pages/contact-108-118.png`, SHA-256
  `b6cbcb1953bbfef353e825aa5c4c6059ea611edc2b16904c92accdd9a8206356`
- Chapter 8 second contact proof:
  `build/qa/books/lanzhou/ch08-final-pages/contact-119-129.png`, SHA-256
  `1156bfcb9697db2404e35704b5581e725f79c34a147f71b3d19365ad618c4528`
- Source and closing contact proof:
  `build/qa/books/lanzhou/ch08-final-pages/contact-130-141.png`, SHA-256
  `4b788ff72e24af9eecd1b6ecf64f5406a4a02e623f1500d20cf1db78867e5a46`
- Chapter responsive release QA:
  `build/qa/website/lanzhou-ch08-release/qa.json`, SHA-256
  `5096e43ad94d52c0eaf9441cb2c5539df12aa99d518006a7815695ba3bc39f9f`
- Full Lanzhou responsive release QA:
  `build/qa/website/lanzhou-ch08-site-release/qa.json`, SHA-256
  `e5b55887838c721433eb78adfabc1c969020ae4e1b6dd7834e4b5f5f7b1b6654`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 108 | Chapter 8 opener | Pass: the title states the decision in all three languages and keeps the chapter visibly about lodging location, not hotel ranking. |
| 109 | `ch08-b001`, Chinese and Japanese | Pass: arrival point and first fixed morning stop lead; ruby remains attached and the route question fits without crowding. |
| 110 | `ch08-b001`, English | Pass: the four lodging alternatives and the boundary on named properties are direct, readable, and free of false room promises. |
| 111 | Central side-street figure | Pass: the entrance is the subject, exactly four guides remain distinct, no anonymous person or usable raster sign appears, and the caption explains what to verify. |
| 112 | `ch08-b002` | Pass: the schematic boundary, east-west relationship, and exact-booking checks are clear before the map. |
| 113 | Stay-segment map | Pass: west, centre, east, and the separate not-to-scale airport buffer remain legible at B6; there are no hotel pins, false transfer lines, or label collisions. |
| 114 | `ch08-b003`, Chinese and Japanese | Pass: the central segment follows the bridge, old centre, and dinner route; the named example remains dated and bounded. |
| 115 | `ch08-b003`, English | Pass: Zhengning Road is not called riverfront, and entrance, street exposure, and room side remain questions for the live booking. |
| 116 | `ch08-b004` | Pass: Lanzhou West is identified by its broad roof and forecourt without treating generated architecture as documentary evidence. |
| 117 | Lanzhou West figure | Pass: the rail gate dominates, the four guides are clear at final size, and the caption preserves the North Square boundary. |
| 118 | `ch08-b005`, Chinese and Japanese | Pass: the western segment joins Lanzhou West to Qilihe and the museum instead of forcing a first cross-city trip. |
| 119 | `ch08-b005`, English | Pass: the current property example is only a locating clue; entrance, address, and return route remain live checks. |
| 120 | `ch08-b006` | Pass: Lanzhou Station is distinguished from Lanzhou West, with luggage and late-arrival decisions stated before transport choice. |
| 121 | Lanzhou Station figure | Pass: the eastern rail gate remains recognizable, exactly four guides are present, and generated station lettering is not used as evidence. |
| 122 | `ch08-b007`, Chinese and Japanese | Pass: the eastern segment follows Lanzhou Station, Dongfanghong Square, the university side, and Tianshui Road without moving a branded hotel toward the bridge. |
| 123 | `ch08-b007`, English | Pass: address, pickup area, station entrance, and east-west return are explicit checks; the page has no overflow. |
| 124 | `ch08-b008`, Chinese and Japanese | Pass: an airport-area night is limited to late landing or early flight, and shuttle details remain dated direct checks. |
| 125 | `ch08-b008`, English | Pass: the operator estimate is bounded and the city hotel remains preferable when the arrival route is already reliable. |
| 126 | Airport buffer figure | Pass: exactly four guides, luggage, an empty unbranded shuttle, and the distant terminal communicate the buffer-night decision without a false pickup promise. |
| 127 | `ch08-b009`, Chinese and Japanese | Pass: full booking details, two-guest registration, and the complete accessibility chain remain together without detached ruby or clipping. |
| 128 | `ch08-b009`, English | Pass: current registration policy is separated from prudent direct confirmation, and one filter icon is not treated as an accessible route. |
| 129 | `ch08-b010` callout | Pass: four lines before payment close the chapter; all three languages, ruby, citations, and coral highlight border fit on one clean page. |
| 130-140 | Sources | Pass: all 62 unique milestone sources retain titles, dates, locators, URLs, and evidence boundaries without overflow. |
| 141 | Closing brand page | Pass: LazyTravel, lazying.art, and the repository address remain clear and uncluttered. |

## Automated Gates

- Destination and source-catalog schemas pass; all 25 external-source checks
  pass without copying source archives into the repository.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
  Chapters 1-8 contain `8,809` Chinese and `11,241` Japanese reviewed tokens;
  Chapter 8 contributes `1,469` and `1,793` respectively.
- All `158` repository tests pass, including deterministic map output, final
  evidence hashes, exact four-guide continuity, dated lodging sources, and the
  Chapter 9 gate.
- XeLaTeX completes twice with no rejected warning, overflow, underflow, error,
  or missing-glyph diagnostic; `qpdf --check`, fonts, searchable text, page
  count, and physical B6 size pass.
- The synchronized release site passes with `75` aligned blocks, `12,161` ruby
  nodes, and 79 chapter-source entries. Chapter 8 contributes ten blocks, one
  map, four figure placements, sixteen sources, and `2,023` ruby nodes.
- The mobile map uses a `760 px` independently pannable stage inside the
  `390 px` viewport so its trilingual labels remain readable.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
