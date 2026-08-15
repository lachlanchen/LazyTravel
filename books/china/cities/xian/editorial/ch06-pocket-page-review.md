# Xi'an Chapters 1-6 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-15`.
Chapter 6 remains part of a review edition until the complete 11-chapter Xi'an
book is approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `f6b5377a3b179d5ce7fb53fc5d68e2ba86f7a0b6e143ec4ce46f7db957ee9d85`
- Manifest SHA-256:
  `a694d092d3e5ac1a793b0ecef8e9fc2674f99ba1306b3a4349571d7d3a6249ff`
- Trim: `125 x 176 mm` B6
- Extent: `93` pages
- Searchable text: `115,250` non-whitespace characters
- Fonts: `10` embedded font records
- Canonical content: `62` aligned blocks, `6` maps, `5` figures, and `77`
  first-use bibliography entries

The final page renders were made from this exact PDF. Guide-cast replacements
on physical pages 23, 38, 50, 63, and 74 are reviewed separately in
`guide-cast-figure-review.md`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 1 | Cover | Pass: title, three languages, China Cities identity, LazyTravel, lazying.art, GitHub, and Chapters 1-6 review range fit cleanly. |
| 2-67 | Front matter and Chapters 1-5 | Pass: prior reviewed text and maps remain stable; all four changed figure pages have separate current-artifact QA. |
| 68 | Chapter 6 opener | Pass: all three titles fit with a clear hierarchy; the five-topic coverage line remains restrained. |
| 69 | `ch06-b001` | Pass: the chapter starts from how `馍` functions at the table rather than an origin myth; ruby and sources fit. |
| 70 | `ch06-b002` | Pass: four eating contexts are distinguished before the map without becoming a route or ranking. |
| 71 | Food-context map | Pass: four areas, wall orientation, four context keys, disclaimer, and larger bilingual labels remain readable at B6 size. |
| 72 | `ch06-b003` | Pass: paomo ordering, bread handling, cooking sequence, and condiments form one practical unit. |
| 73 | `ch06-b004` | Pass: piece-size judgment, accessibility alternative, and shop-specific limits lead directly to the figure. |
| 74 | Paomo figure | Pass: Aya-chan, Lala Xia, Sasa-kun, and the Zhuangzi robot remain distinct; the dry bowl, whole mo, torn pieces, garlic, chilli, and trilingual caption remain clear. |
| 75 | `ch06-b005` | Pass: roujiamo meat, bread, halal-boundary, fatness, and juice questions are concrete and uncluttered. |
| 76 | `ch06-b006` | Pass: liangpi families are explained through flour, texture, and seasoning rather than colour alone. |
| 77 | `ch06-b007` | Pass: biangbiang noodles stay focused on noodle width, texture, hot oil, and ordering judgment rather than character folklore. |
| 78 | `ch06-b008` | Pass: breakfast categories, sharing logic, market timing, and same-day checks fit without a vendor list. |
| 79 | `ch06-b009` | Pass: Hui, Han, halal, ingredient, and room-boundary distinctions remain careful and readable. |
| 80 | `ch06-b010` | Pass: the two-person ordering plan and dumpling judgment sit inside one compact blue orientation band. |
| 81 | `ch06-b011` | Pass: the coral order/ingredients/allergies callout fits on one page; Chinese pinyin and Japanese furigana remain legible inside the frame. |
| 82 | `ch06-b012` | Pass: the food-led day uses breakfast, one sight, lunch, rest, and dinner without proposing a forced eating checklist. |
| 83 | Sources opener | Pass: scope note and first entries are legible with no clipped URLs. |
| 84 | Sources continuation 1 | Pass: titles, locators, checked dates, and links maintain consistent leading. |
| 85 | Sources continuation 2 | Pass: institutional and source-book records remain visually distinct. |
| 86 | Sources continuation 3 | Pass: long English titles and URLs wrap inside the text block. |
| 87 | Sources continuation 4 | Pass: heritage-source entries remain unclipped. |
| 88 | Sources continuation 5 | Pass: rubbing and access records fit without collisions. |
| 89 | Sources continuation 6 | Pass: current historic-city and open-guide entries remain dated and readable. |
| 90 | Sources continuation 7 | Pass: food standards and district records wrap cleanly. |
| 91 | Sources continuation 8 | Pass: food-map, breakfast, roujiamo, liangpi, and noodle records remain separated. |
| 92 | Sources continuation 9 | Pass: allergy and food-safety records close the bibliography without overflow. |
| 93 | Closing brand page | Pass: LazyTravel, lazying.art, and the repository close remain centered and restrained. |

## Visual Evidence

- Cover render SHA-256:
  `9e87a93e21ba4b9a8da3b18e0192d7c8e51c7246bbf7f6cbeaa33af0254c05da`
- Pages 68-72 sheet SHA-256:
  `e3028f56489c762a1693e3f3b71dac9e9254b4935b1677ed1e46da55998a8f57`
- Pages 73-77 sheet SHA-256:
  `6cd29f4826c4a098bb439fc6d3a9f53d54515cc30466c420f6822829da795859`
- Pages 78-82 sheet SHA-256:
  `9c6f4fa802492fddf9dd5b5c879d5481938d4059ee9c1ab11129d3ed5d12ba11`
- Pages 83-93 sheet SHA-256:
  `66470929a37de63b8c250da6bed2475a560c4a34ce4044bd2e29635080b5bc4f`

## Automated Gates

- Source catalog and destination JSON schemas pass.
- `23` external paths and hashes verify without copying the source archives or
  visual references into the repository.
- Reading validation passes for `6,203` Chinese and `7,846` Japanese tokens.
- All `50` repository tests pass, including the non-map Aya/Lala cast gate.
- XeLaTeX completes twice without rejected diagnostics; `qpdf`, trim, page
  count, embedded fonts, and searchable-text checks pass.
