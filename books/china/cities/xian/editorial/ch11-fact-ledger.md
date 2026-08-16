# Chapter 11 Fact Ledger: Leave With the Right Evidence

Ledger date: `2026-08-16`. Destination gate: `china/cities/xian`.

This is the final Xi'an chapter. It does not add another destination. It turns
the route already chosen into a small set of things that can be checked: a
successful order, the identity document used for it, the correct station or
terminal, the current warning, the hotel's Chinese address, and a fallback
that stays in the same part of the city. The supplied family guide and the
pinned Chinese and English open guides remain useful records of what travelers
have needed to know, but their prices, opening hours, route numbers, booking
methods, and broad safety claims are dated evidence rather than current
instructions.

## Locked Block Architecture

| Block | Function | Required content |
| --- | --- | --- |
| `ch11-b001` | Opening figure and decision | On the evening before departure, the four guides reduce a table of plans to four kinds of evidence: identity, confirmed entry, live conditions, and the hotel/return address. The scene is practical and calm, not a product display. |
| `ch11-b002` | Fix the immovable parts first | Put successful timed entries and rail/flight departures on one line, then attach only same-area stops. A screenshot of a search result or completed prefill is not a confirmed order. |
| `ch11-b003` | Current booking check | Dated comparison of the Shaanxi History Museum main site and the Qin museum: official channel, accepted identity document, successful-order test, and document required at entry. Exact mechanisms are visibly checked on `2026-08-16`. |
| `ch11-b004` | Failure and cancellation | When a booking fails, replace the anchor rather than adding a second geography. Read cancellation and no-show rules and release an unused booking through the official order page. |
| `ch11-b005` | Closures and holidays | Do not infer one closure day for every museum. Check each official notice and the annual State Council holiday calendar; holiday opening and crowd patterns can override the ordinary week. |
| `ch11-b006` | Weather changes the route | Check the city and the actual excursion destination separately. Rain, heat, wind, ice, and official warnings change the wall and mountain days differently. Use a 72-hour check and a same-morning check without printing a forecast in the book. |
| `ch11-b007` | Air quality and physical margin | Use the official city air-quality report as a live input. Move or shorten exposed sections when conditions or the travelers' health require it; the book does not diagnose or prescribe. |
| `ch11-b008` | Transport evidence | Match the exact station/terminal, passenger name, identity document, and departure date. Carry the original document used for a real-name rail ticket and keep power, route address, and an arrival margin. |
| `ch11-b009` | Hotel and bags | Keep the hotel's Chinese name, address, telephone, entrance, check-in date, and guest names offline. Confirm early arrival, late arrival, and luggage storage instead of assuming them. Hotels register foreign guests; non-hotel stays require the statutory local registration process. |
| `ch11-b010` | On-site rules | Security, bag, photography, tripod, food, route, and worship rules are venue-specific. Follow current notices, signs, barriers, and staff. At religious sites, protect worship before photographs. |
| `ch11-b011` | Food allergy card | A translated card names the exact allergen and asks whether the dish contains it; it is not proof of a safe kitchen. Severe-allergy travelers keep prescribed medicine and their action plan accessible and make the companion part of the plan. |
| `ch11-b012` | Emergency location | `110` police, `119` fire and rescue, and `120` medical emergency are the three numbers to retain. Give the location first: Chinese venue/hotel name, gate or platform, nearby landmark, and callback number. |
| `ch11-b013` | Final pocket check | Seven checks: confirmed order, matching original identity, live warning, exact station/terminal, hotel address and entrance, return margin, and personal medicine/allergy plan. If one fails, change the day before adding another stop. |

The block count is fixed at `13`. The chapter has one place-aware preparation
figure and no map. A map would imply that the final risk is spatial; the actual
task is matching current evidence to the route maps already printed in
Chapters 1-10.

## Accepted Claims

| ID | Claim allowed in original prose | Evidence and locator | Durability | Editorial constraint |
| --- | --- | --- | --- | --- |
| `READY-01` | A confirmed order must be distinguished from a search result, prefilled form, wait state, or payment attempt. | Shaanxi History Museum current guide; Qin museum current guide. | Decision rule durable; interface volatile | Do not reproduce an app screen or imply every venue uses the same status words. |
| `READY-02` | On `2026-08-16`, the Shaanxi History Museum main site states that its basic-display tickets are released five days ahead at 17:00, supports information prefill, and requires the official successful-order record plus the matching original identity document for timed entry. | Official visitor guide, lines 91-117, checked `2026-08-16`. | Time-sensitive | Print the check date beside the block and tell readers to recheck; do not treat the five-day window as permanent. |
| `READY-03` | The Qin museum currently uses real-name reservation through its official website or official WeChat channels, accepts passport details, and checks the original valid identity document at entry; free-entry categories also reserve. | Qin museum official guide, checked `2026-08-16`. | Time-sensitive | Do not name a third-party seller, promise availability, or freeze hours and prices in durable prose. |
| `READY-04` | Booking failure should replace the day's anchor, and an unused timed booking should be cancelled under the venue's current rules. | Current museum guides; Chapter 10 replacement logic. | Durable rule; cancellation rules volatile | Do not promise a refund or quote one universal penalty. |
| `READY-05` | China's public-holiday dates and adjusted working days are published annually; a venue may publish separate holiday opening notices. | State Council 2026 holiday notice; current museum guide directs holiday visitors to latest announcements. | Annual/time-sensitive | Do not generalize the 2026 calendar to another year or equate an adjusted working day with normal museum operations. |
| `READY-06` | Weather must be checked for the specific city or mountain route shortly before travel, and an official warning overrides the printed itinerary. | China Meteorological Administration weather and warning services; official Huashan/Cuihuashan route constraints from Chapter 7. | Live/time-sensitive | No forecast, temperature promise, or universal best-season claim. |
| `READY-07` | China National Environmental Monitoring Centre publishes city air-quality daily/hourly data and national forecasts. | CNEMC real-time data page checked `2026-08-16`. | Live/time-sensitive | Use the reading as a route input; do not turn AQI into individual medical advice. |
| `READY-08` | China Railway real-name travel requires the passenger, ticket information, and the identity document used for purchase to match; travelers using other accepted documents may use a staffed channel. | China Railway 12306 real-name ticket FAQ and trip reminder, checked `2026-08-16`. | Time-sensitive operations; identity principle durable | Avoid unsupported advice about a specific gate, queue, or amount of advance time. |
| `READY-09` | Hotels register foreign guests with public security; foreigners staying outside hotels complete local accommodation registration within 24 hours. | National Immigration Administration accommodation-registration guidance. | Legal requirement; recheck before travel | State the rule plainly without implying a hotel may lawfully reject a guest because of nationality. |
| `READY-10` | Venue security, restricted-item, photography, and route rules can differ and change. | Current Shaanxi History Museum guide and restricted-item notice; Qin museum guide; reviewed mosque and heritage sources. | Time-sensitive | Signs and staff control the visit. Do not invent a universal camera or bag rule. |
| `READY-11` | Travelers with serious allergies should carry prescribed medicine, a translated allergy/medical card, and an emergency plan; companions should know the plan and medicine location. | CDC Travelers' Health allergy page and 2026 Yellow Book chapter, checked `2026-08-16`. | Health guidance; recheck with clinician | No diagnosis, dosage, promise of cross-contact control, or suggestion that a card guarantees safety. |
| `READY-12` | `110`, `119`, and `120` are the police, fire/rescue, and medical-emergency numbers. | Beijing Communications Administration public-service number notice under MIIT, checked `2026-08-16`; corroborated by current government English service pages. | Durable but checked | Keep the list to genuine emergencies; `12345` is not presented as an emergency substitute. |
| `READY-13` | A two-person trip is more resilient when both travelers can retrieve confirmed orders, the Chinese hotel address, and emergency information if one phone fails. | Original operational judgment; supplied family-guide practical framing; Chapters 8-10. | Durable | Do not recommend unsafe duplication of identity documents or storing sensitive data publicly. |

## Rejected Or Deferred Claims

| Claim | Decision |
| --- | --- |
| Every museum is closed on Monday. | Rejected. Closure and holiday arrangements vary by venue and current notice. |
| A booking is complete once names are prefilled or a payment page appears. | Rejected. The official successful-order record and matching entry document control the visit. |
| Five days ahead at 17:00 is the permanent Shaanxi History Museum booking rule. | Rejected as durable advice. It may appear only in the dated `2026-08-16` block. |
| Good weather in central Xi'an means Huashan or Cuihuashan is also suitable. | Rejected. The destination forecast, warning, terrain operation, and return chain require their own check. |
| One air-quality number determines whether every traveler should remain indoors. | Rejected. The reading informs route exposure; personal decisions depend on health and professional advice. |
| A translated allergy card makes a dish safe. | Rejected. It improves communication but cannot prove ingredients, shared oil, utensils, or cross-contact control. |
| A hotel listing proves early check-in, late arrival handling, luggage storage, room view, or foreign-guest procedure. | Rejected. Confirm each operational need with the property and retain the reply. |
| Screenshots replace original identity documents. | Rejected for real-name rail and venue entry where the official rule requires the original document. |
| The guide should print current prices, complete opening hours, and a live weather forecast. | Rejected. These would age before the trip and crowd the pocket pages. |
| The final chapter needs another city map. | Rejected. Chapters 1-10 already provide the spatial tools; this chapter verifies the evidence that activates them. |

## Language Pass Briefs

- **Chinese:** use ordinary verbs: `确认成功订单`, `核对证件`, `看最新公告`,
  `换掉预约锚点`, `保留返程`. Avoid bureaucratic filler, platform slang, and
  alarmist language.
- **Japanese:** distinguish `入力済み`, `予約成立`, and `原本の身分証明書`.
  Keep the prose as a calm departure routine, not a literal checklist
  translation.
- **English:** prefer “successful order,” “matching original document,”
  “replace the anchor,” “current notice,” and “state the location first.” Avoid
  “travel hack,” “stress-free,” “guaranteed,” “better safe than sorry,” and
  generic safety reassurance.

## Visual Evidence Rules

- `asset-xian-before-departure-four-guides` shows Aya-chan, Lala Xia, Sasa-kun,
  and the Zhuangzi robot as four travelers at a Xi'an hotel table on the
  evening before departure. The view includes restrained city-wall context;
  identity details and screens are unreadable, and no text is baked into the
  image.
- The figure must include all four guides, with Aya-chan and Lala Xia clearly
  recognizable from their supplied references. Travel preparation remains the
  subject; notebook, cards, and devices are supporting objects rather than
  advertisements.
- Reader-facing captions describe the decision. Generation method, reference
  hashes, limitations, and visual QA remain in technical provenance only.

## Citation URLs

- Shaanxi History Museum current visitor guide:
  <https://www.sxhm.com/guide.html>
- Qin museum current visitor guide:
  <https://www.bmy.com.cn/guide/>
- State Council 2026 public-holiday notice:
  <https://www.gov.cn/zhengce/zhengceku/202511/content_7047091.htm>
- China Meteorological Administration weather service:
  <https://weather.cma.cn/>
- China National Environmental Monitoring Centre real-time data:
  <https://www.cnemc.cn/sssj/>
- China Railway real-name ticket guide:
  <https://kyfw.12306.cn/otn/gonggao/realNameTicket.html>
- National Immigration Administration accommodation registration:
  <https://en.nia.gov.cn/n147423/n147478/n147715/c158241/content.html>
- CDC allergies and travel:
  <https://wwwnc.cdc.gov/travel/page/allergies>
- CDC Yellow Book, severely allergic travelers:
  <https://www.cdc.gov/yellow-book/hcp/travelers-with-additional-considerations/severely-allergic-travelers.html>
- Emergency and public-service numbers:
  <https://bjca.miit.gov.cn/zwgk/tzgg/art/2022/art_8d4eb93ee3424f30826c97ee400e8937.html>
