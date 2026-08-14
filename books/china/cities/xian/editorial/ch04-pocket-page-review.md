# Xi'an Chapters 1-4 B6 Pocket Page Review

Status: technical, editorial, and visual review passed on `2026-08-15`.
Chapter 4 remains part of a review edition until the complete Xi'an book is
approved.

## Reviewed Artifact

- Build: `python3 scripts/build_xian_review.py`
- Output: `dist/books/xian/xian-pocket-review.pdf`
- SHA-256: `1fe85277c8cea071dc59d1fb2026a50e038c3c383fe7beda08ebaed021c78887`
- Manifest SHA-256:
  `6eaae2bce0a55787b640c8f80cfaa4be116c0cbef43e32df9e6af0430784232d`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `59` pages
- Searchable text: `69,635` non-whitespace characters
- Fonts: `10` embedded font records
- Chapter 4 contact-sheet SHA-256:
  `ced8db70709f9fd40f21070d3b48dc15fff1a012145fb75153195d4a81370bfd`
- Accepted contents-page SHA-256:
  `fcf7fc3bd84442fd8f231ea32cfabdcfe0f1249f79d162047f01626458edee14`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 1-39 | Cover, contents, Chapters 1-3 | Pass: prior reviewed material remains intact; the edition date is current and long contents entries wrap without broken English words or stretched Chinese. |
| 40 | Chapter 4 opener | Pass: all three titles, chapter number, and coverage line fit with a clear B6 hierarchy. |
| 41 | `ch04-b001` | Pass: the translation-inscription-circulation sequence is concrete and the ruby/source lines remain clear. |
| 42 | `ch04-b002` | Pass: Xuanzang's collaborative translation institution fits without turning the role list into clutter. |
| 43 | `ch04-b003` | Pass: authorship, calligraphy, and stone carving remain distinct in all three languages. |
| 44 | `ch04-b004` | Pass: Small Pagoda form, damage, repair, and the rejected foundation story fit with adequate bottom clearance. |
| 45 | `ch04-b005` | Pass: map scope and the half-day/full-day choice are established before the visual. |
| 46 | Written-word route map | Pass: one scale, three numbered sites, present wall, generalized Tang field, scale bar, and route disclaimer are legible in landscape B6. |
| 47 | `ch04-b006` | Pass: Beilin's relocation and preservation history remains readable with reviewed proper-name ruby. |
| 48 | `ch04-b007` | Pass: Kaicheng Classics counts and the one-stone inspection method fit without promotional superlatives. |
| 49 | `ch04-b008` | Pass: rubbing process, conservation limit, replica boundary, and generated-image disclosure remain on one page. |
| 50 | Replica-rubbing figure | Pass: realistic hands, tools, paper, modern replica, and all three disclosure captions are clear without crop or pseudo-text. |
| 51 | `ch04-b009` | Pass: Chinese and Syriac evidence is separated from an unsupported claim of universal Tang tolerance. |
| 52 | `ch04-b010` | Pass: dated booking advice, the Beilin-hours conflict, separate access checks, and rest margins fit on one page. |
| 53-58 | Sources | Pass: `46` first-use records carry their own checked dates; URLs, titles, and locators remain legible and unclipped. |
| 59 | Closing brand page | Pass: restrained LazyTravel, lazying.art, and repository close. |

## Visual Provenance

- Written-word map SVG SHA-256:
  `7b747d7bf35e0aec5fcba2fb42aa354268d8d7bb9aacf22f19ba4606f89e4d41`.
  A second render reproduced the same SVG, PDF, PNG, and provenance hashes.
- Replica-rubbing image SHA-256:
  `bacbb717d597c05b047090e1f0ad5be7a08ec1506f09640b5086d2d6c9a1d6f1`.
  It is a built-in OpenAI-generated editorial figure of a modern resin replica,
  not evidence for a real object or museum activity.

## Automated Gates

- Destination and source-catalog schemas pass.
- All Chinese and Japanese reading arrays reconstruct canonical prose exactly
  and are marked `reviewed`.
- XeLaTeX completes twice with no overfull boxes, underfull boxes, missing
  glyphs, or warning exceptions.
- `qpdf --check`, embedded-font inspection, physical trim inspection,
  page-count inspection, and searchable-text inspection pass.
- All `36` repository tests and Ruff checks pass.
