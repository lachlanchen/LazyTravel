# Chapter 7 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-20`. This is a
Chapters 1-7 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --skip-map --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `b7eee7beed367ef7382ef79d0d7a8f9fe072573c92029b82a001c7e47f715995`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `122` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `146,085` characters
- Chapter 7 evidence: `build/qa/hakone/ch07-pocket-release/contact.jpg`,
  SHA-256
  `a71e47550b67d67167e24e31b4897e77beb94fdf786f72cd2237969332396664`.

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 94 | Chapter 7 opener | Pass: the title names the onsen-ryokan night and the subtitle sets one arrival-to-departure sequence without promising luxury or uniform house rules. |
| 95 | `ch07-b001` | Pass: the dinner deadline leads arrival, pickup, bath, breakfast, checkout, and delay choices in one practical opening. |
| 96 | Ryokan-arrival figure | Pass: the mountain entrance remains recognizable; exactly four guides arrive before dark with no reflected or anonymous fifth person. |
| 97 | `ch07-b002` | Pass: the ordinary sequence and late-arrival branch remain separate from property-specific clock times. |
| 98 | One-night sequence map | Pass: arrival, check-in, bath, dinner, sleep, breakfast, and departure remain legible at B6 size, including the contact-the-property branch. |
| 99 | `ch07-b003` history callout | Pass: seven springs, one-night and longer stays, seventeen districts, and the 1965 supply history lead to a present-day verification decision. |
| 100 | `ch07-b004` | Pass: the dry-threshold preparation protects privacy and distinguishes public, private, and in-room bath questions. |
| 101 | Onsen-threshold figure | Pass: all four guides remain fully clothed in a dry corridor; the separate entrances and empty wash area illustrate sequence without nudity. |
| 102 | `ch07-b005` bath callout | Pass: wash, rinse, `kakeyu`, towel, hair, phone, photography, noise, heat, and alcohol cautions remain direct and readable. |
| 103-104 | `ch07-b006` six questions | Pass: public/private access, tattoos, natural water, reservation, showers, steps, and cleaning closures fit across two pages without clipping. |
| 105 | `ch07-b007` | Pass: the booked meal is treated as an appointment, while service place, menu form, and property variation remain qualified. |
| 106 | Ryokan-dinner figure | Pass: exactly four guides and four place settings remain distinct; the camera-headed robot and meal setting reproduce the approved cast and avoid fake writing. |
| 107 | `ch07-b008` meal callout | Pass: advance dietary contact, ingredient limits, contamination risk, delay, and the multilingual card fit without an oversized callout. |
| 108-109 | `ch07-b009` room choice | Pass: futon, bed, chair, stairs, toilet, shower, and nighttime movement are presented as valid comfort and access decisions. |
| 110 | `ch07-b010` morning callout | Pass: bath cleaning, breakfast, checkout, payment, luggage, pickup, weather, and onward departure close the stay without a universal timetable. |
| 111-121 | Sources | Pass: all active Chapters 1-7 entries, dates, locators, links, and rights notes remain legible. |
| 122 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- All three Chapter 7 figures and the sequence map match their recorded output
  hashes and approved B6/mobile visual evidence.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
