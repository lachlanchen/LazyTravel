# Xi'an Chapters 1-8 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-16`.
Chapter 8 remains part of a review edition until the complete 11-chapter Xi'an
book is approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `c9450bd72402861c018757c73f2d715c6e08811f71a36c01b9bef1e13a305080`
- Manifest SHA-256:
  `ae9579c20e574683c1543034665ed1569186ff40da65cdea6b0ab923709a9467`
- Trim: `125 x 176 mm` B6
- Extent: `134` pages
- Searchable text: `162,824` non-whitespace characters
- Fonts: `10` embedded font records
- Canonical content: `86` aligned blocks, `8` maps, `12` figures, and `107`
  citation records; `105` records are cited in Chapters 1-8.

The final page renders were made from this exact PDF. Chapter 8 occupies
physical pages `105-119`; sources occupy pages `120-133`, followed by the
closing brand page on `134`.

## Chapter 8 Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 105 | Chapter opener | Pass: exact station and terminal choice is the chapter's visible subject; the opener does not drift into a generic transport essay. |
| 106 | `ch08-b001` | Pass: all three station names, terminal check, hotel entrance, and reviewed ruby fit on one page. |
| 107 | Xi'an North figure | Pass: Xi'an North remains the dominant place signal; Aya, Lala, Sasa, Zhuangzi, their luggage, and all three captions remain distinct. |
| 108 | `ch08-b002` | Pass: the prose states the map's schematic limit before the visual page. |
| 109 | Four-hub map | Pass: four hubs, four line numbers, wall and river anchors, three language layers, and four decision cards remain readable at B6 size. |
| 110 | `ch08-b003` | Pass: T5 and T2/T3 paths, current flight assignment, and on-site station names remain separate. |
| 111 | `ch08-b004` | Pass: Line 2 versus Line 4 is a hotel-side decision, with no promise based on scheduled landing time. |
| 112 | `ch08-b005` | Pass: Xi'an North's plaza, mode, luggage, and pickup-level choices fit without an abstract station overview. |
| 113 | `ch08-b006` | Pass: Xi'an Station and Xi'an North remain unmistakably different; wall and Daming orientation is concrete. |
| 114 | `ch08-b007` | Pass: the 2026 Xi'an East opening, Line 5 walk, and changing new-station circulation are dated and sourced. |
| 115 | `ch08-b008` | Pass: metro, bus, car, and walking choices are tied to luggage, service, and a known hotel entrance. |
| 116 | `ch08-b009` | Pass: the luggage band is the densest page but retains clear pinyin, furigana, English, lift advice, and current-rule boundary. |
| 117 | `ch08-b010` | Pass: the payment fallback is operational, compact, and does not promise universal foreign-card acceptance. |
| 118 | `ch08-b011` | Pass: late arrival uses the post-gate clock and a signed pickup fallback without a forced last-train plan. |
| 119 | `ch08-b012` | Pass: the six-check coral callout closes on one page with no clipped border, citation, or language layer. |
| 120-133 | Sources | Pass: all cited titles, locators, checked dates, and URLs wrap without rejected TeX diagnostics. |
| 134 | Closing brand page | Pass: LazyTravel, lazying.art, and the repository close remain restrained. |

## Visual Evidence

- Pages 105-109 sheet SHA-256:
  `5706f4eddc1fc703f8b1a4f4a27e01a0ece08ccb19ead7ef7d820e6ba5324d68`.
- Pages 110-114 sheet SHA-256:
  `ffa23992c678ad24d49598f9c5cd9d70efa441e5e3f8e7ac3527ce906666fe38`.
- Pages 115-119 sheet SHA-256:
  `572d6a5464eb82230bdb4ddeb92563d8e8ff5c4f45267cd91d87dc991308a83f`.
- Station-figure B6 proof SHA-256:
  `9f4d0eda0a7b77995c4dc07e902437afa36b5516b83f537e0f452c894e7dac06`.
- Arrival-map B6 proof SHA-256:
  `9be921eb5d68c28d580e1c0248deb0e56914b61705ae641d6679e960b6f7814c`.

## Automated Gates

- Source catalog and destination JSON schemas pass.
- Reading validation passes for `8,606` Chinese and `10,938` Japanese tokens.
- All `61` repository tests pass, including the new four-hub map contract.
- All `23` read-only source-manifest checks pass.
- All eight maps regenerate before XeLaTeX completes twice without rejected
  diagnostics; the arrival-map outputs and final PDF match the reviewed probe
  byte for byte.
- `qpdf`, B6 trim, page count, embedded fonts, searchable text, and clean-log
  checks pass.
