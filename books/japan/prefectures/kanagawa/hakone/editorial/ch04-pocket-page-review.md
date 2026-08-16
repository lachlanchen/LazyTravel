# Chapter 4 B6 Pocket Page Review

Status: technical and visual review passed on `2026-08-17`. This is a
Chapters 1-4 milestone, not the finished Hakone destination book.

## Reviewed Artifact

- Build: `python3 scripts/build_hakone_review.py --sync-nutstore`
- Output: `dist/books/hakone/hakone-pocket-review.pdf`
- Nutstore copy:
  `/home/lachlan/Nutstore Files/Share/LazyTravel/LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf`
- SHA-256 of both copies:
  `73ec6fb6a93f8b786762e116d1fc7ba3f727cf0c3c1115742538c3d7af6ed5cd`
- Trim: `125 x 176 mm` B6 pocket format
- Extent: `67` pages
- Embedded font sets: `10`
- Searchable non-whitespace text: `76,812` characters
- Chapter 4 evidence:
  `build/qa/hakone-ch04-proof-final/contact-sheet.png`, SHA-256
  `55ec2ac78d397b5bfe62107122f123437e9cc0db7a75387184af01ced0f8a5da`

## Page Review

| Physical page | Content | Result |
| ---: | --- | --- |
| 44 | Chapter 4 opener | Pass: the route question leads; the long coverage deck wraps in three intact rows without a broken word. |
| 45 | `ch04-b001` | Pass: Sounzan transfer, visible terrain, `130 m` scale, and compulsory Owakudani change fit together. |
| 46 | Ropeway-approach figure | Pass: the actual valley and cabin view dominate; all four guides and all three captions remain clear. |
| 47 | `ch04-b002` | Pass: operator approximations, three editorial stop ranges, and closure response remain distinct. |
| 48 | Owakudani decision map | Pass: station order, cabin change, stop choices, access rules, and reroute note are legible without collisions. |
| 49 | `ch04-b003` | Pass: visible landform, gas limits, naming history, heat use, and management infrastructure form one place-led account. |
| 50 | Public-overlook figure | Pass: fumarole terrain and barriers dominate; the four-guide group does not obscure the site. |
| 51 | `ch04-b004` safety callout | Pass: prohibited riders, caution groups, separate trail rules, monitoring, and official rechecks fit inside the bubble without overflow. |
| 52 | `ch04-b005` | Pass: preparation chemistry, longevity folklore, four-egg sales unit, price, and availability remain clearly separated. |
| 53 | Black-egg figure | Pass: exactly four eggs and four guides are visible; the peeled egg and place context remain readable at B6. |
| 54 | `ch04-b006` | Pass: snack, seated meal, quick food, trail rule, and ryokan-dinner constraint fit on one aligned trilingual page. |
| 55 | `ch04-b007`, Chinese and Japanese | Pass: reopening context, route profile, sessions, check-in, and exclusions remain readable with reviewed ruby. |
| 56 | `ch04-b007`, English | Pass: the safety-critical English pass remains intact rather than being compressed below the standard type size. |
| 57 | Nature-trail figure | Pass: steps, barriers, shelter, helmets, and all four guides remain clear; no unsafe access is depicted. |
| 58 | `ch04-b008` itinerary callout | Pass: public stop, booked stop, food choice, cloud fallback, and disruption rule fit without clipping. |
| 59 | `ch04-b009` | Pass: the descent uses wind, cloud, lake, pier, bus, and lodging direction to hand the route to Chapter 5. |
| 60 | Lake-descent figure | Pass: Lake Ashi remains dominant; the fixed crop contains exactly four guides and does not promise Fuji. |
| 61-66 | Sources | Pass: all Chapters 1-4 entries, dates, locators, direct links, and rights notes remain legible. |
| 67 | Closing brand page | Pass: LazyTravel, lazying.art, and repository branding remain clear. |

## Automated Gates

- Destination and source-catalog schemas pass.
- Chinese and Japanese reading layers reconstruct the exact canonical text.
- XeLaTeX completes twice with no rejected warning, overfull box, underfull box,
  error, or missing-glyph diagnostic.
- `qpdf --check`, embedded-font inspection, searchable-text inspection, page
  count, and physical B6-size checks pass.
- All five figures and the map match their recorded output hashes and exact B6
  and mobile proof records.
- The distributed PDF and Nutstore pocket copy are byte-for-byte identical.
