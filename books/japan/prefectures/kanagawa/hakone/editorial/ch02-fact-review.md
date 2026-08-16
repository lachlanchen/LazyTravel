# Hakone Chapter 2 Fact Review

Chapter: `ch02-odawara-yumoto`

Checked: `2026-08-16`

State: reviewed and accepted for the Chapter 2 milestone

## Chapter Question

The chapter answers one practical question: **what must be decided between the
intercity train and the first mountain journey?** The answer proceeds in this
order: gateway, interchange, ticket, luggage, first direction, fallback. It
does not attempt to preview every attraction on the full Hakone circuit.

## Supported Claims

| ID | Claim permitted in original prose | Source IDs | Treatment |
| --- | --- | --- | --- |
| `C2-01` | Hakone's road threshold predates the railways: the Yusaka route linked Yumoto and Mishima in the Kamakura period, and the early-Edo Tokaido crossed from Yumoto through Hatajuku. | `HKN-TOWN-HISTORY` | Durable context. One paragraph only; Chapter 6 handles the old road in detail. |
| `C2-02` | The mountain railway opened from Yumoto to Gora in the Taisho era, and Odakyu through-running between Odawara and Hakone-Yumoto began in 1950. | `HKN-TOWN-HISTORY` | Durable chronology. It explains why Yumoto remains the threshold between gateway rail and mountain transport. |
| `C2-03` | Odawara is the practical rail gateway from Tokyo and from the Tokaido Shinkansen corridor. | `HKN-NAVI-ODAWARA`; `HKN-NAVI-ACCESS-TOKYO`; `HKN-NAVI-ACCESS-WEST` | Durable role. Do not call it the only gateway to the whole region. |
| `C2-04` | At the checked station layout, the JR Tokaido Shinkansen gate is by the west exit on level 1; the shared Odakyu/Hakone Tozan gate is on level 3. Platforms 7 and 11 are signed towards Hakone-Yumoto. | `HKN-NAVI-ODAWARA-STATION` | Time-sensitive. Publish with `checked_at`; advise following current signs, not memorizing a platform. |
| `C2-05` | Current direct Romancecar travel from Shinjuku to Hakone-Yumoto takes about 80 minutes, is all reserved, and requires a limited-express ticket plus the base fare or a covering pass/IC payment. | `ODKY-ROMANCECAR` | Time-sensitive. "About" is required. Recheck schedule and fare before release. |
| `C2-06` | The current adult limited-express surcharge from Shinjuku to Hakone-Yumoto is JPY 1,200 at the station, with an online discount stated by the operator; tickets go on sale at 10:00 JST one month before travel. | `ODKY-ROMANCECAR` | Time-sensitive. Keep in one dated ticket block, not in durable narrative. |
| `C2-07` | From 2025-10-01, the adult Hakone Freepass costs JPY 6,000/6,400 for two/three days from Odawara and JPY 7,100/7,500 from Shinjuku. The Shinjuku version includes one Odakyu return journey to Odawara; the pass covers unlimited rides on the named Hakone-area modes, but Romancecar needs an extra limited-express fee. | `HKN-NAVI-FREEPASS` | Time-sensitive. State date and compare against the actual intended rides; do not declare the pass universally cheapest. |
| `C2-08` | Current station-to-lodging luggage acceptance is 08:30-12:00 for delivery after 15:00. Return luggage must be handed to a participating lodging by 10:00 for collection at Yumoto from 13:30-18:30. Current one-way prices are JPY 1,500 up to 140 cm/15 kg and JPY 2,500 up to 200 cm/30 kg. | `HKN-LUGGAGE` | Time-sensitive. Participating lodging, excluded contents, weather limits, and current cutoff control. |
| `C2-09` | Hakone-Yumoto currently connects the Odawara train, the mountain train for Gora, and bus routes towards Miyanoshita, Sengokuhara, the old road, and Lake Ashi. | `HKN-NAVI-YUMOTO-STATION`; `HKN-NAVI-AROUND` | Durable branch logic; platform and timetable details are time-sensitive. |
| `C2-10` | JR Central's published timetable is basic and does not list every extra train. | `JRCT-TIMETABLE` | Time-sensitive operational warning. Use it to require a current Odawara-stopping train search, not to reproduce a timetable. |

## Rejected Shortcuts

- "The Romancecar is always best from Tokyo." Rejected. Shinjuku location,
  onward travel, reserved-seat availability, and luggage alter the decision.
- "Buy the Freepass automatically." Rejected. Value depends on the actual
  route and whether the intercity leg is included.
- "Always travel clockwise." Rejected. The first attraction, lodging district,
  weather, and final destination determine direction.
- "Send every suitcase ahead." Rejected. The service reaches participating
  lodgings only and has cutoffs, size rules, excluded items, and weather limits.
- Exact walking minutes inside Odawara Station. Rejected without a controlled
  timed accessibility survey.
- Memorized platforms or a reproduced daily timetable. Rejected as brittle.

## Block Spine

1. See the four guides make the Odawara interchange without rushing past the signs.
2. Read the gateway map as a set of decisions, not as a timetable.
3. Understand why Yumoto remains Hakone's working threshold.
4. Choose a Shinjuku through train or an Odawara interchange, then buy the right fare and pass combination.
5. Arrive at Yumoto and decide what happens to the luggage before choosing a branch.
6. Use the checked luggage service only when its cutoff, size rules, and lodging coverage fit the day.
7. Choose the Gora side or the old-road/lake side from the first real destination and lodging district.
8. Protect check-in and dinner with a simple late-arrival fallback.
9. Leave Yumoto on the mountain train and hand the route to Chapter 3.

## Release Recheck

- Odakyu and JR stopping patterns and reservation rules;
- Romancecar surcharge and Freepass prices/inclusions;
- Odawara and Hakone-Yumoto gate, floor, platform, and facility arrangement;
- luggage-service times, prices, size limits, excluded contents, and eligible
  lodgings;
- live Hakone transport status on publication day.
