# Chapter 5 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-22`. This is a Chapters
1-5 milestone, not the finished Lanzhou destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_lanzhou_review.py --skip-map --sync-nutstore`
- Output: `dist/books/lanzhou/lanzhou-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Lanzhou-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `bf238bb246ab1da2c671436c593b67f3372c793ec2552b1b25b34e976fdf8270`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `84` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `92,840` characters
- Chapter 5 contact proof:
  `build/qa/books/lanzhou/ch05-final-contact.png`, SHA-256
  `89a652cb54cc5267ba79513453ee724636ebeadb8c2e059415c5ccf868c8c1e8`
- Source/closing contact proof:
  `build/qa/books/lanzhou/ch05-sources-contact.png`, SHA-256
  `7fa1d351e679c24eb4d5002b0fe70576aa32ffcc331f67b5cdbb6002b2e3d947`
- Responsive website QA:
  `build/qa/website/lanzhou-ch05-release/qa.json`, SHA-256
  `df3463c37e7e46380dad6af0403f4b98865a1d06fd63ce8637a3f5fbea1bc3df`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 58 | Chapter 5 opener | Pass: the title promises one museum route rather than a regional-history survey or object checklist. |
| 59-60 | `ch05-b001` | Pass: the present entrance, half-day commitment, province-wide collection boundary, and three-gallery line read continuously in all three languages. |
| 61 | Museum exterior figure | Pass: the current pale-stone frontage dominates; exactly four guides remain distinct and the caption directs a live display check. |
| 62-63 | `ch05-b002` | Pass: dated opening, appointment, identity-document, luggage, guide-desk, metro, and gallery rules are legible; the conflicting release time is not guessed. |
| 64 | `ch05-b003` | Pass: one ascent, one descent, three central galleries, one optional addition, and live floor-operation limits fit without crowding. |
| 65 | Museum route map | Pass: all five stops, three floor bands, optional-gallery choice, and current-display warning remain readable at B6. |
| 66 | `ch05-b004` | Pass: the four-pass vessel method remains practical and survives absence of the named object. |
| 67 | Painted Pottery figure | Pass: one representative vessel and the exact four-guide cast remain clear; no anonymous visitor, label fiction, or mixed-era tableau appears. |
| 68 | `ch05-b005` | Pass: Qin'an and Gangu vessels stay distinct by type, date, form, and findspot; unsupported symbolism remains a question. |
| 69 | `ch05-b006` | Pass: Jingchuan reliquary and Dunhuang painting are separated by material, date, use, and place instead of compressed into a cultural slogan. |
| 70-71 | `ch05-b007` | Pass: Wuwei speed and Jiayuguan travel administration form one movement comparison; the bird is not fixed as a swallow and display remains conditional. |
| 72 | `ch05-b008` | Pass: Lanzhou is clearly the museum and planning point, while six findspots remain distributed around Gansu without a false onward route. |
| 73 | Gansu findspot map | Pass: museum, six numbered anchors, object keys, and orientation-only warning remain legible without collisions. |
| 74-75 | `ch05-b009` | Pass: label fact and traveler inference stay separate; the missing-object fallback remains usable and avoids repeated gallery searching. |
| 76 | `ch05-b010` | Pass: the highlighted exit decision clears every border and footer, permits one optional gallery, and protects food, hotel rest, or booked transport. |
| 77-83 | Sources | Pass: all 37 milestone entries retain dates, locators, URLs, licenses where needed, and evidence boundaries without overflow. |
| 84 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass; all 25 external-source checks
  pass without copying source archives into the repository.
- Chinese and Japanese reading layers reconstruct the exact canonical text;
  Chapter 5 adds `1,427` Chinese and `1,781` Japanese reviewed tokens.
- All `139` repository tests pass, including Chapter 5 map reproducibility,
  evidence hashes, exact four-guide continuity, and the Chapter 6 gate.
- XeLaTeX completes twice with no rejected warning, overflow, underflow, error,
  or missing-glyph diagnostic; `qpdf --check`, fonts, searchable text, page
  count, and physical B6 size pass.
- Both generated figures and both deterministic maps match approved provenance
  with compiled B6 and actual desktop/`390 px` website evidence.
- Website QA passes with `45` aligned blocks, `6,802` ruby nodes, and `42`
  chapter-source entries. Chapter 5 contributes ten blocks, two figures, two
  independently checked maps, and `1,961` ruby nodes; no console error, failed
  request, vertical map clipping, or map-control ambiguity remains.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
