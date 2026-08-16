# Chapter 10 Fact Ledger: Add One Coherent Day

Ledger date: `2026-08-16`. Destination gate: `china/cities/xian`.

This chapter turns the preceding place, food, transport, and lodging chapters
into usable two-, three-, and five-day routes. The supplied family guide and
the pinned Chinese and English open guides provide older itinerary examples
and useful attraction groupings, but their compressed days, old route numbers,
opening hours, prices, and booking assumptions are not reused. In particular,
an old plan that combines the wall, Bell and Drum Towers, Hui lanes, Beilin,
Shaanxi History Museum, and the Big Wild Goose Pagoda in one day is evidence of
what must be corrected, not a template. LazyTravel uses a nested plan with one
geography and one principal reservation per day.

## Locked Block Architecture

| Block | Function | Required content |
| --- | --- | --- |
| `ch10-b001` | Opening figure and decision | The four guides pause at the Small Wild Goose Pagoda with one route notebook. The missing upper section and dense eaves reward time to look; the day begins with a place, not an attraction count. |
| `ch10-b002` | Nested itinerary map | Two days are Days 1-2; three days add Day 3; five days add Days 4-5. Day 4 shows four mutually exclusive nearby choices. |
| `ch10-b003` | One day, one geography | Each day needs one geographic argument, one booked anchor, one nearby sequence, one proper meal, and protected return/rest time. |
| `ch10-b004` | Day 1: old core | South Gate/wall, then Shuyuanmen or Beilin, then Bell/Drum Tower and mosque-and-lane area. Beilin is cut first when arrival is late. |
| `ch10-b005` | Day 2: Qin archaeology | Reserve the Qin museum day, leave for the booked entry, view Pits 1-3 with the museum sequence explained in Chapter 3, and preserve the return rather than adding unrelated eastern stops. |
| `ch10-b006` | Day 3: museum and pagoda | One substantial southern museum, lunch/rest, then the Big Wild Goose Pagoda and an evening nearby. Shaanxi History Museum's basic display supplies the historical breadth. |
| `ch10-b007` | Booking fallback | If Shaanxi History Museum cannot be booked, replace it with the Small Wild Goose Pagoda plus Xi'an Museum or another single coherent museum anchor. Do not bolt extra sites onto the original day. |
| `ch10-b008` | Day 4: one nearby place | Choose one among Huashan, Han Yangling, Cuihuashan, or Qianling by weather, physical demand, subject, and return burden. Chapter 7 controls the detailed choice. |
| `ch10-b009` | Day 5: depth and recovery | Return to one missed place or follow one new city thread such as Daming Palace. No second long excursion. Keep an unscheduled block for laundry, weather, sleep, or a longer meal. |
| `ch10-b010` | Five route emphases | First visit, history-heavy, food-led, family, and reduced-mobility variants change emphasis and cuts without multiplying sites. |
| `ch10-b011` | Meals belong to the route | Plan breakfast near the start, one seated midday or evening meal, and one food area that fits the day's geography. A food list does not justify crossing the city. |
| `ch10-b012` | Keep one hotel base | Two- to five-day routes normally keep one city room. Split only for a genuine two-day eastern sequence or a rail-led final night. |
| `ch10-b013` | Cut in the correct order | When late, tired, hot, wet, or overbooked: keep the reservation and return; cut optional interiors, secondary stops, and detours in that order. Never recover a missed stop by stealing the next day's return margin. |
| `ch10-b014` | Pocket summary | Five-day nested plan with one anchor, one sequence, one meal, and one protected margin each day; operational details are rechecked before departure. |

The block count is fixed at `14`. The chapter does not duplicate attraction
descriptions from Chapters 3-7, hotel listings from Chapter 9, or the volatile
departure checklist reserved for Chapter 11.

## Accepted Claims

| ID | Claim allowed in original prose | Evidence and locator | Durability | Editorial constraint |
| --- | --- | --- | --- | --- |
| `PLAN-01` | A first Xi'an route works better when each day stays in one geography and has one principal reservation or physical demand. | Original route judgment tested against the supplied family guide and open-guide itineraries; reviewed Chapters 3-9. | Decision rule durable | Do not invent universal travel times or say the route is effortless. |
| `PLAN-02` | The two-, three-, and five-day plans are nested: Days 1-2 remain stable, Day 3 adds the southern museum/pagoda corridor, and Days 4-5 add one excursion plus city depth. | Original book structure; reviewed route and nearby maps. | Durable | Do not present five separate itineraries that drift out of sync. |
| `PLAN-03` | South Gate, Beilin/Shuyuanmen, Bell/Drum Tower, the Great Mosque, and adjacent lanes can form one old-core sequence because they share a compact geography. | Chapter 5 official city-wall, mosque, Beilin, and reviewed route-map evidence. | Geography durable; entry rules volatile | Beilin is optional, not a promise that every interior fits after a late arrival. |
| `PLAN-04` | The Qin museum deserves its own principal day. The three pits differ in archaeological function and should be read in sequence rather than used as a backdrop for a crowded east-Xi'an checklist. | Qin museum official home, pit pages, and excavation history; Chapter 3 fact ledger. | Archaeological interpretation durable; entry/transport volatile | Do not add Huaqing Palace by default or print an unsupported transfer time. |
| `PLAN-05` | Shaanxi History Museum's basic display spans three halls and seven chronological sections, with material from prehistoric Shaanxi through later periods and strong Zhou, Qin, Han, and Tang holdings. | Official basic-display page checked 16 August 2026. | Display concept durable; gallery access volatile | Describe the intellectual scope, not a guaranteed room order or opening hour. |
| `PLAN-06` | The current official museum guide uses timed real-name reservation and lists wheelchairs, strollers, accessible paths/lifts/toilets, rest areas, and visitor services. | Official visitor guide and current official homepage checked 16 August 2026. | Time-sensitive | Chapter 10 says to reserve and verify; Chapter 11 will carry the current operational checklist. |
| `PLAN-07` | The Small Wild Goose Pagoda, Xi'an Museum, and Jianfu Temple precinct form a coherent replacement morning when the primary museum cannot be booked. | Xi'an Museum visitor page; official Shaanxi pagoda material; Chapter 4 ledger. | Place relationship durable; entry rules volatile | It replaces the first anchor. It is not an extra stop after a failed booking. |
| `PLAN-08` | Day 4 should contain one of Huashan, Han Yangling, Cuihuashan, or Qianling because each has a distinct transport chain, physical demand, and return burden. | Chapter 7 official route/access sources and nearby-choice map. | Decision rule durable; operations volatile | Never suggest combining two because their map markers look close. |
| `PLAN-09` | Daming Palace can anchor a fifth-day city-depth thread that reconnects visible geography to the Tang palace site's position on Longshouyuan. | Shaanxi heritage Daming Palace source; Chapter 2 city-layer ledger. | Historical geography durable; site operations volatile | It is one example, not a compulsory final-day attraction. |
| `PLAN-10` | A family route benefits from fewer interiors, reliable toilets/rest, and a fixed return; a reduced-mobility route must verify each entrance, lift, distance, and assistance segment rather than infer accessibility from one venue. | Current museum service guides; Chapters 3, 4, 7, and 8 accessibility findings. | Decision rule durable; facilities volatile | Do not label the entire route accessible or promise that all surfaces are step-free. |
| `PLAN-11` | Meals should follow the day's geography: breakfast near the start, one seated meal, and only one food area that does not force a cross-city detour. | Chapter 6 source-backed food contexts; original itinerary judgment. | Food context durable; shop hours volatile | No restaurant ranking, queue promise, or “eat everything” list. |
| `PLAN-12` | One city base normally reduces packing and transfer friction for a two- to five-day visit. | Chapter 9 verified stay-area geography and decision ledger. | Decision rule durable | Preserve Chapter 9's two narrow split-stay exceptions; do not calculate invented minutes saved. |
| `PLAN-13` | When a day slips, protect the booked anchor and the return first, then remove optional interiors, secondary stops, and detours. | Original operational rule derived from current booking and transfer constraints. | Decision rule durable | The rule does not override safety, weather closure, or official instructions. |
| `PLAN-14` | The itinerary map is orientation and editorial sequence only. | `data/maps/xian/xian-itinerary-days.config.json` and its explicit generalizations. | Snapshot dated | No line may be described as a live route, walking path, complete metro, or journey time. |

## Rejected Or Deferred Claims

| Claim | Decision |
| --- | --- |
| The wall, Bell and Drum Towers, Hui lanes, Beilin, Shaanxi History Museum, and the Big Wild Goose Pagoda make one efficient first day. | Rejected. This crosses distinct old-core and southern museum geographies and leaves no useful looking, meal, or transfer margin. |
| Huaqing Palace always belongs after the Terracotta Army. | Rejected. Add it only when it is the deliberate second subject and the current entry and return chain still work; it is not the default two-day plan. |
| A missed reservation can be recovered by adding the replacement venue to the same afternoon. | Rejected. Replace the anchor and preserve the day; do not double it. |
| Day 4 can combine Han Yangling with Qianling or Huashan because both lie outside the centre. | Rejected. Their transport and viewing demands are independent full choices. |
| The fifth day should be another long day trip. | Rejected. The final added day protects depth, recovery, and one missed city place. |
| Every family or reduced-mobility traveler can follow one universal special itinerary. | Rejected. The route supplies decision rules; actual entrances, fatigue, mobility aids, and assistance must be checked segment by segment. |
| Exact opening hours, booking windows, prices, train numbers, taxi times, and restaurant hours belong in this durable itinerary chapter. | Deferred to dated checks and Chapter 11. |

## Language Pass Briefs

- **Chinese:** use `一天一条地理主线`, `预约锚点`, `返程余量`, `替换`, and
  `四选一` plainly. Avoid `无脑抄作业`, `特种兵`, `天花板`, `一网打尽`,
  and platform itinerary slang.
- **Japanese:** use ordinary route prose: `一日に一つの地理`, `予約の軸`,
  `帰路の余白`, `差し替える`, and `一か所を選ぶ`. Do not force Chinese
  slogan rhythm into Japanese.
- **English:** prefer “one geography,” “booked anchor,” “protect the return,”
  “replace rather than add,” and “choose one.” Avoid “ultimate itinerary,”
  “jam-packed,” “effortless,” “hidden gem,” and “perfect for everyone.”

## Visual Evidence Rules

- `asset-xian-itinerary-days-map` is character-free and states the nested
  2/3/5-day logic without route-time claims. Day 4's four markers are mutually
  exclusive choices.
- `asset-xian-small-wild-goose-route-morning` shows Aya-chan, Lala Xia,
  Sasa-kun, and the Zhuangzi robot as four guide travelers. The pagoda's dense
  eaves and missing upper section dominate the view; the notebook supports the
  itinerary decision rather than becoming a product display.
- Reader captions explain what to notice and how the scene changes the day.
  Generation method, source-image hashes, limitations, and visual QA stay in
  technical provenance.

## Citation URLs

- Shaanxi History Museum basic display:
  <https://www.sxhm.com/basic_display.html>
- Shaanxi History Museum current visitor guide:
  <https://www.sxhm.com/guide.html>
- Xi'an Museum visitor information:
  <https://www.xabwy.com/visit.html>
- Qin museum visitor information:
  <https://www.bmy.com.cn/guide/>
- OpenStreetMap copyright and data license:
  <https://www.openstreetmap.org/copyright>
