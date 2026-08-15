# Chapter 8 Fact Ledger: Arrive and Move

Ledger date: `2026-08-16`. Destination gate: `china/cities/xian`.

This chapter begins with the name printed on the ticket or flight display. It
does not treat “Xi'an station” as a generic point: Xi'an North, Xi'an Station,
Xi'an East, and the airport are different arrival systems. The supplied 2013
family guide and the pinned Chinese and English open guides remain useful for
showing which details age badly. Their three-terminal airport description,
old bus routes, old station circulation, fares, travel times, and incomplete
rail-hub list are rejected as current advice. Official airport, municipal,
railway, metro, and station sources control operational claims.

## Locked Block Architecture

| Block | Function | Required content |
| --- | --- | --- |
| `ch08-b001` | Opening figure and decision | The four guides stop before the first escalator, match the exact hub and terminal to the hotel address, and choose one onward mode. |
| `ch08-b002` | Four-hub map | Airport, Xi'an North, Xi'an Station, Xi'an East, and the walled-city core. Lines are decision spines, not the complete metro or live navigation. |
| `ch08-b003` | Airport terminal | T5 and T2/T3 have different arrival paths and Line 14 station names. Read the current flight display before following a remembered route. |
| `ch08-b004` | Airport to city | Line 14 reaches Xi'an North, where Lines 2 and 4 provide cityward choices. Use the current operating window; never promise a last train. |
| `ch08-b005` | Xi'an North | Lines 2, 4, and 14 serve the hub. Choose by destination and follow the signed north/south plaza or official pickup zone. |
| `ch08-b006` | Xi'an Station | The station beside the north wall is not Xi'an North. It has north, south, and underground access and connects with Line 4. |
| `ch08-b007` | Xi'an East | The new station opened on 30 June 2026. Line 5 is within a short signed walk; bus, taxi, and ride-hailing zones are separated. Recheck because the hub is new. |
| `ch08-b008` | Mode choice | Metro for the long cross-city leg, bus only when the live route is clear, and official taxi/ride-hailing for a difficult final leg or late arrival. |
| `ch08-b009` | Luggage and access | Keep documents and small electronics reachable, leave hands free, allow for security, use lift signs, and arrange assistance instead of assuming a step-free path. |
| `ch08-b010` | Payment and communication | A single ticket or staffed service point is the fallback when a phone payment fails. Keep the hotel's Chinese name, address, entrance, and phone number offline. |
| `ch08-b011` | Late-arrival protocol | Recalculate after baggage claim or train exit. When the rail window no longer works, use the signed official pickup area and send the exact hotel entrance. |
| `ch08-b012` | Six checks | Exact hub, terminal, arrival time, operating window, hotel address, and pickup/exit. Do these once before departure and once after arrival. |

The block count is fixed at `12`. Additional station inventories, full metro
instructions, airport shopping, and unsupported “fastest route” comparisons
belong outside this chapter.

## Accepted Claims

| ID | Claim allowed in original prose | Evidence and locator | Durability | Editorial constraint |
| --- | --- | --- | --- | --- |
| `ARRIVE-01` | The first reliable route decision is the exact arrival hub and terminal printed by the carrier or China Railway 12306. Xi'an North, Xi'an Station, and Xi'an East are not interchangeable names. | China Railway 12306 station service and ticket data; Xi'an municipal transport pages; current airport arrival guide. | Decision rule durable; assignment volatile | Never shorten all railway arrivals to “Xi'an station.” Repeat the exact Chinese station name where it prevents a mistake. |
| `ARRIVE-02` | Xi'an Xianyang International Airport T5 opened on 20 February 2025. T5 and T2/T3 use different paths to metro, taxi, and airport-bus facilities. | Xi'an municipal T5 opening report; airport domestic-arrival guide; Xixian New Area T5 guide and operating notice. | Terminal geography durable; airline assignment and operations volatile | Tell readers to trust the current boarding pass and airport display. Do not preserve the old guide's T1/T2/T3-only model. |
| `ARRIVE-03` | The Line 14 station for T5 is `机场（T5）`; the station for T1/T2/T3 is `机场西（T1、T2、T3）`. T5 arrivals reach its station through the integrated transport centre. | Xixian New Area Line 14 T5 opening guide; airport domestic-arrival page, “离开机场.” | Station names durable; access route may change | Print station names, not a minute-by-minute walk. Airport signs and staff override the book. |
| `ARRIVE-04` | Line 14 links the airport with Xi'an North. Xi'an North is served by Lines 2, 4, and 14, allowing a cityward transfer chosen by destination. | Xi'an North official public-transport guide; Xixian New Area Line 14 through-operation notice; Xi'an municipal 2025 network diagram. | Network spine durable; service hours volatile | Omit fares and first/last train times. Check the current network and service notice after the actual arrival time is known. |
| `ARRIVE-05` | Xi'an North has north and south public-transport areas and separate taxi/ride-hailing pickup arrangements. A traveler should follow the exit-specific official signs rather than walk toward a generic pin. | Xi'an Economic and Technological Development Zone public-transport guide, taxi and ride-hailing sections. | Spatial organisation moderately durable | Do not print every exit number, walking estimate, route number, or parking fee. The signed zone chosen on the day is authoritative. |
| `ARRIVE-06` | Xi'an Station sits by the north side of the Ming wall and is connected to Metro Line 4. Its expansion produced north, south, and underground access. | Xinhua, 27 December 2024, station expansion account; Xi'an planning bureau Line 4 connection notice; Xi'an transport station page. | Durable until reconstruction | Keep the historical-spatial observation useful: south is the wall, north is Daming Palace. Do not imply that every train uses this station. |
| `ARRIVE-07` | Xi'an East began operation on 30 June 2026. Passengers can reach Line 5 within a five-minute signed walk, and buses, taxis, and ride-hailing use separate zones. | Xi'an municipal English news report updated 1 July 2026. | Highly time-sensitive because the hub is new | State the check date. Do not infer all train services, exits, or hotel transfer times from the opening report. |
| `ARRIVE-08` | A simplified arrival map may show the airport, three principal railway hubs, the walled core, and only the metro spines that explain first transfers. | Official 2025 metro network diagram; official hub pages; pinned OpenStreetMap positions; original schematic synthesis. | Geography durable; network volatile | Label it as a decision schematic. No full network, timetable, fare, street navigation, or universal hotel route. |
| `ARRIVE-09` | At Airport T5 station, current official guidance lists single tickets, transport cards, QR, cash, digital RMB, face recognition, and smart POS support for foreign cards. A staffed service point is the prudent fallback. | Xixian New Area Line 14 T5 station opening guide, payment section. | Time-sensitive | Do not imply every payment method works for every foreign phone, card, or station. Do not require a proprietary app. |
| `ARRIVE-10` | T5 passengers pass metro security before ticketing. Railway passengers and luggage are subject to security checks and current prohibited/restricted-item rules. | T5 station opening guide; Railway Safety Management Regulations; China Railway 12306 prohibited/restricted-item notice. | Security requirement durable; item rules can change | Advise accessible packing, not a long prohibited-item list. Readers must check the current carrier and 12306 rules. |
| `ARRIVE-11` | China Railway 12306 provides a special-priority passenger reservation service and station assistance; T5 Line 14 guidance also describes advance assistance and handoff service. | China Railway 12306 priority-passenger service instructions; Xixian New Area T5 station service section. | Service concept durable; eligibility and timing volatile | Do not promise a universal step-free route. Ask for assistance in advance and confirm each travel segment. |
| `ARRIVE-12` | When the planned metro or bus connection no longer fits after the actual arrival, the safe practical response is to use the signed official taxi or ride-hailing zone and send the hotel's exact Chinese entrance details. | Official airport and Xi'an North pickup-zone guidance; original traveler judgment. | Decision rule durable; pickup zones volatile | No scare language, unofficial-car anecdotes, or promised fare. Confirm the vehicle and destination in the app or official queue. |

## Rejected Or Deferred Claims

| Claim | Decision |
| --- | --- |
| The airport still consists only of T1, T2, and T3. | Rejected. T5 opened in February 2025 and has its own Line 14 station and transport path. |
| Xi'an North, Xi'an Station, Xi'an East, and the former Xi'an South can be treated as one “Xi'an railway station.” | Rejected. The ticket's exact Chinese station name controls the route. |
| Xi'an East remains under construction. | Rejected after the official 30 June 2026 opening report. |
| Line 2 is always the best cityward transfer from Xi'an North. | Rejected. Lines 2 and 4 serve different corridors; the hotel side and final entrance determine the useful line. |
| Printed first/last trains, airport-bus route lists, bus numbers, fixed fares, and taxi prices remain reliable for the life of the book. | Rejected. These are live checks and the older references demonstrate how quickly they age. |
| A map pin for a station or hotel is enough to find the correct pickup point. | Rejected. Large hubs separate plazas, levels, taxi zones, and ride-hailing zones. |
| Every metro or rail route is step-free without advance planning. | Rejected. Use current lift signs and assistance services; confirm the actual segment. |
| A late arrival should still attempt the planned metro because the last published departure has not passed. | Rejected. Baggage, walking, security, transfer, and platform access consume the remaining window. |
| The full Xi'an metro network belongs in a B6 arrival map. | Rejected. Chapter 8 shows only the first-transfer spines and directs readers to the dated official network. |
| Named hotels or a universal “best” station area. | Deferred to Chapter 9, where neighborhoods and current hotel verification are the main subject. |

## Language Pass Briefs

- **Chinese:** preserve the exact forms `西安北站`, `西安站`, `西安东站`,
  `机场（T5）站`, and `机场西（T1、T2、T3）站`. Use `出租车乘车区`
  and `网约车乘车区` only when the official source distinguishes them. Avoid
  `无缝丝滑`, `秒到市区`, `闭眼冲`, and route-app marketing language.
- **Japanese:** distinguish `西安北駅`, `西安駅`, and `西安東駅` throughout.
  Use ordinary travel terms such as `到着ロビー`, `乗り換え`, `配車アプリの
  乗車場所`, and `エレベーター`. Do not carry Chinese promotional compounds
  into Japanese.
- **English:** use “Xi'an North,” “Xi'an Station,” and “Xi'an East” as proper
  hub names. Prefer “signed pickup zone,” “actual arrival time,” and “final
  entrance.” Avoid “seamless,” “hassle-free,” “gateway,” “smart hub,” and
  claims that one transfer is always fastest.

## Visual Evidence Rules

- `asset-xian-arrival-hubs-map` is character-free. It shows four arrival hubs,
  the walled core, and the Line 14/2/4/5 decision spines at large B6-readable
  scale. It is not a complete metro map or a street-navigation layer.
- `asset-xian-north-interchange` includes Aya-chan, Lala Xia, Sasa-kun, and the
  Zhuangzi robot as the four guide travelers. Xi'an North's broad station form
  and forecourt remain dominant. Their luggage is compact and controlled; no
  character blocks a path.
- Generated signage must use only simple transport pictograms and arrows. It
  must not invent readable Chinese station directions, platform numbers,
  timetables, fares, or commercial marks.
- Reader-facing captions explain the transfer decision. Generator, prompt,
  reference paths, checksums, factual limitations, and production QA remain
  in technical provenance.

## Citation URLs

- Xi'an East opening report:
  <https://en.xa.gov.cn/MediaCenter/News/2072253459180654594.html>
- Xi'an North public-transport guide:
  <https://xetdz.xa.gov.cn/xwzx/jkdt/1831494658425413633.html>
- Xi'an airport domestic-arrival guide:
  <https://www.xxia.com.cn/cjzn/gndd.htm>
- T5 opening report and terminal notice:
  <https://en.xa.gov.cn/ztzl/XI%27ANLEADSHIGH-LEVELOPENING-UP/BuildingtheAirSilkRoad/1892494226718523393.html>
  and <https://www.xixianxinqu.gov.cn/xwzx/tzgg/1889306024130240514.html>
- T5 and Line 14 transfer guides:
  <https://www.xixianxinqu.gov.cn/xwzx/ztzl/yjhj/jt/1891134067765170178.html>
  and <https://www.xixianxinqu.gov.cn/zwgk/zcwd/jycy/1892481399452139521.html>
- Xi'an municipal metro network diagram, 29 December 2025:
  <https://jtj.xa.gov.cn/zmhd/xxcx/dtxl/1.html>
- Xi'an Station expansion account and Line 4 connection:
  <https://www.news.cn/politics/20241227/ce5be5bf3dce4038b0ad73cd13c7c376/c.html>
  and <https://zygh.xa.gov.cn/ywpd/cxghgsgb/ghglpqgs/62ff3d4cf8fd1c4c211205d8.html>
- China Railway 12306 station and service material:
  <https://kyfw.12306.cn/index/view/station/hand.html>,
  <https://kyfw.12306.cn/otn/view/icentre_qxyyInfo.html>, and
  <https://kyfw.12306.cn/otn/gonggao/saleTicketMeans.html>
- OpenStreetMap copyright and data license:
  <https://www.openstreetmap.org/copyright>
