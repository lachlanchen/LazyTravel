# Xi'an Chapters 1-7 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-16`.
Chapter 7 remains part of a review edition until the complete 11-chapter Xi'an
book is approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `b6699a28134b7401686c508337252731fa2a6959567ed5c0360b63276b8496f8`
- Manifest SHA-256:
  `6525405f85bea313adfc5057a4e85f460fd3680c02bafd1883946f73dc2bb9f7`
- Trim: `125 x 176 mm` B6
- Extent: `117` pages
- Searchable text: `141,536` non-whitespace characters
- Fonts: `10` embedded font records
- Canonical content: `74` aligned blocks, `7` maps, `11` figures, and `94`
  bibliography records
- Nutstore pocket mirror:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Xian-ZH-JA-EN-B6-Pocket.pdf`
  matches the reviewed PDF SHA-256.

The final page renders were made from this exact PDF. Chapter 7 occupies
physical pages `89-104`; sources begin on physical page `105`.

All subject headings are rendered from canonical JSON. The test suite rejects
missing block-specific headings, and the current page review found no generic
fallback heading. The seven maps use the enlarged landscape width without
clipping; eleven figures each retain one complete trilingual caption page.

## Chapter 7 Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 89 | Chapter opener | Pass: the one-place-per-day argument and three titles remain clear without a marketing-style opener. |
| 90 | `ch07-b001` | Pass: the chapter begins with transport stages and return time rather than straight-line distance. |
| 91 | `ch07-b002` | Pass: all five choices are introduced as decisions, not a checklist or ranking. |
| 92 | Nearby-choice map | Pass: five markers, directional joins, terrain context, large place labels, transport cards, and the non-navigation note remain readable. |
| 93 | `ch07-b003` | Pass: the choice key distinguishes archaeology, mountain walking, geology, and imperial landscape. |
| 94 | `ch07-b004` | Pass: the two Qin museum areas, reservation slot, shuttle, queues, and Huaqing cut rule form one usable Lintong plan. |
| 95 | `ch07-b005` | Pass: Huaqing's Tang and 1936 layers remain separate from the Qin visit; the prose does not present today's site as an intact Tang palace. |
| 96 | `ch07-b006` | Pass: the data-driven `ROUTE FIRST` heading remains specific; all three route options fit. |
| 97 | `ch07-b007` | Pass: the `FOUR CONDITIONS` callout fits within its coral frame; `不适` has the corrected pinyin grouping. |
| 98 | `ch07-b008` | Pass: Han Yangling's external pits, controlled glass-walkway environment, road access, and flight-margin warning remain concrete. |
| 99 | `ch07-b009` | Pass: Cuihuashan is presented as a managed geological field day with explicit weather and boundary limits. |
| 100 | `ch07-b010` Chinese/Japanese | Pass: Qianling's surface evidence, associated tomb choice, and dated conservation notice fit without an orphaned English label. |
| 101 | `ch07-b010` English | Pass: the English label stays with its paragraph; no line, citation, or footer is clipped. |
| 102 | `ch07-b011` | Pass: cableway limits, stone steps, weather, photography etiquette, and safe-return rule lead directly to the figure. |
| 103 | Managed mountain figure | Pass: Aya, Lala, Sasa, and the Zhuangzi robot, managed railings, path surface, and all three captions remain on one landscape page. |
| 104 | `ch07-b012` | Pass: the `SIX CHECKS` callout closes the chapter on one page with reviewed pinyin and furigana. |
| 105-116 | Sources | Pass: all citations, locators, checked dates, and URLs wrap without clipping. |
| 117 | Closing brand page | Pass: LazyTravel, lazying.art, and the repository close remain restrained. |

## Visual Evidence

- Pages 89-92 sheet SHA-256:
  `5ff225759fd9aa63764ce3410c00e76ec94f4d88627f4012d61aee7c6b9fc183`
- Pages 93-96 sheet SHA-256:
  `0a09470630cbf5d4cc1b86d4c69853c440e5464a74f7bd62900a46c271ba30fa`
- Pages 97-100 sheet SHA-256:
  `8803cd5a7fa06ea9e7c0a7344981901a83661347e8de489eb380bc63ab4a6fc9`
- Pages 101-104 sheet SHA-256:
  `bfce99506fd4f899222fe5ed874bbd4dc05bb50821917f0e8edf605018352266`
- All seven landscape map pages sheet SHA-256:
  `39872b31f0088290909acf900e3f0182d3b61e23f60545dbfc04689e521dfc9e`
- All eleven landscape figure pages sheet SHA-256:
  `2dd2af94bc86a99f1664d7bc3edf1923dbebb739de263288795cfc02d78c17ec`

## Automated Gates

- Source catalog and destination JSON schemas pass.
- Reading validation passes for `7,463` Chinese and `9,476` Japanese tokens.
- All `57` repository tests pass, including the non-map Aya/Lala cast gate,
  block-specific heading checks, and the five-choice map contract.
- All `23` read-only source-manifest checks pass.
- All seven maps regenerate before XeLaTeX completes twice without rejected
  diagnostics; `qpdf`, trim, page count, embedded fonts, and searchable-text
  checks pass.
