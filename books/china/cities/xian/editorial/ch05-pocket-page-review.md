# Xi'an Chapters 1-5 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-15`.
Chapter 5 remains part of a review edition until the complete Xi'an book is
approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `75cba1ae1628e04d20e6d8f58476961b73c81b8655380e1f3ea7a1ecc989de16`
- Manifest SHA-256:
  `662fb5d3d3a8691bfe5d54d2aa12d1ee6537e4f20c32fafedb40c992dc5be7e3`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `76` pages
- Searchable text: `93,024` non-whitespace characters
- Fonts: `10` embedded font records
- Chapter 5 contact-sheet SHA-256:
  `3b949b33cb9f1d24fb5849aba59c3e00972faa741c83271ba1e151dd787b6ad2`

The page-by-page preview and final distributable PDF have the same SHA-256, so
the visual review applies to the exact milestone artifact.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 1-52 | Cover, contents, Chapters 1-4 | Pass: prior reviewed material remains intact in the revised vivid palette; ruby geometry and body sizes are unchanged. |
| 53 | Chapter 5 opener | Pass: three titles, coverage line, and vermilion chapter bubble fit with a clear pocket hierarchy. |
| 54 | `ch05-b001` | Pass: the crossroads-to-lanes route logic is concrete and all three language columns finish with their sources. |
| 55 | `ch05-b002` | Pass: Ming wall history, circuit scale, and safe return judgment fit without a continuation page. |
| 56 | `ch05-b003` | Pass: the Bell Tower relocation argument and pedestrian-underpass advice remain distinct and legible. |
| 57 | `ch05-b004` | Pass: Bell and Drum Tower comparison leads naturally from avenue scale to lane scale. |
| 58 | `ch05-b005` | Pass: both map scales, optional branches, and route limitations are established before the visual. |
| 59 | Inside-wall route map | Pass: full-wall comparison, street-scale route, optional branches, numbered stops, labels, legend, and scale bar are legible in landscape B6. |
| 60 | `ch05-b006` | Pass: the spatial meaning of Huifang is explained without treating a living neighborhood as a spectacle. |
| 61 | `ch05-b007` | Pass: conflicting official foundation dates are stated carefully; architecture and active worship remain the usable focus. |
| 62 | `ch05-b008` | Pass: threshold, courtyard sequence, and visitor limits introduce the figure without production commentary. |
| 63 | Lane-to-courtyard figure | Pass: gate depth, raised threshold, tree shade, and two travelers remain clear at B6 size; captions identify it as an editorial scene rather than a specific entrance. |
| 64 | `ch05-b009` | Pass: lane flow, queue clearance, and photographic consent form one coherent practical unit. |
| 65 | `ch05-b010` | Pass: public street, worship-space, and residential thresholds are stated without vague warnings or clutter. |
| 66 | `ch05-b011` | Pass: half-day and full-day choices retain a seated meal and realistic optional interiors. |
| 67 | `ch05-b012` | Pass: dated access checks and the full-circuit time buffer fit on one page. |
| 68-75 | Sources | Pass: `57` first-use records for Chapters 1-5 remain legible, dated individually, and unclipped. |
| 76 | Closing brand page | Pass: restrained LazyTravel, lazying.art, and repository close. |

## Visual System And Provenance

- The revised white, vermilion, jade, cobalt, and coral palette remains vivid
  without reducing text contrast. Small numbered and information bubbles have
  stable dimensions and do not disturb pinyin or furigana leading.
- Inside-wall route SVG SHA-256:
  `e493607176bb61e7d169a5cc005b64a5cbfc8c45169ce7d9691f5ec9bb2a7fa7`.
  Clean-build regeneration reproduced the accepted map and retained passing
  print, mobile, and label-collision QA.
- Lane-to-courtyard image SHA-256:
  `5c98064961de0ce60a013c4dcd7b137f2435e7a5940877557837df08df6709c1`.
  Technical provenance records the generation method and prompt; the image is
  used only for spatial orientation and is not factual evidence for a site.

## Automated Gates

- Destination and source-catalog schemas pass.
- All Chinese and Japanese reading arrays reconstruct canonical prose exactly
  and are marked `reviewed`.
- XeLaTeX completes twice with no overfull boxes, underfull boxes, missing
  glyphs, or warning exceptions.
- `qpdf --check`, embedded-font inspection, physical trim inspection,
  page-count inspection, searchable-text inspection, and page-occupancy review
  pass.
- All `41` repository tests and Ruff checks pass.
