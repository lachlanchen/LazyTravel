# Lanzhou Research Source Ledger

Ledger opened: `2026-08-21`. Destination gate: `china/cities/lanzhou`.

This ledger defines the evidence boundary for the Lanzhou book. It is not book
prose. The three supplied Lanzhou and Gansu books are used for leads, historical
context, food vocabulary, and questions worth checking. Official or
institutional sources establish publishable durable claims. Operators and
venue owners establish volatile travel details. No source's chapter order or
sentences determine the LazyTravel structure.

The project catalog contains all six supplied books. The three Xi'an-specific
books were used for the completed Xi'an volume and are not forced into this
Lanzhou book. This ledger covers the three sources that contain relevant
Lanzhou or Gansu evidence, the two pinned Lanzhou open-guide snapshots, the
external reference ledger, and current authoritative sources.

No external guide PDF, source archive, website snapshot, or LALACHAN reference
is copied into this repository. Raw and intermediate extraction remains under
ignored `build/research/lanzhou/`. Committed work is limited to original prose,
aligned JSON, derived maps, approved project-owned figures, source locators,
and reproducible production code.

## Evidence Order

1. A national agency, municipality, museum, heritage institution, transport
   operator, or site operator is primary for facts within its remit.
2. `甘肃简史` is a secondary historical survey. Its chronology is checked
   against institutional or local-chronicle evidence before publication.
3. The 2014 guide and the two open-guide snapshots provide orientation and
   questions. They never establish a current fare, route, opening hour,
   business, hotel, safety condition, or recommended itinerary.
4. `陇味儿` provides food vocabulary and lived context. Memoir-like scenes do
   not establish an origin date, health effect, universal recipe, or city-wide
   practice.
5. Commercial pages and search snippets may identify an official page to open;
   neither is cited as final evidence when a responsible authority exists.

## Read-only Source Index

| ID | Source and locator | Pinned evidence | Use and constraint |
| --- | --- | --- | --- |
| `LZH-GUIDE-2014` | `Sources/甘肃和宁夏（2014年版）.pdf`, printed pp. 50-76 / PDF pp. 53-79 | SHA-256 `44c6c6492c308f4b9b144d94b9d6659519dbfe9756e0d0b25bd851b44bf5df9b`; derived OCR at ignored `build/research/lanzhou/source-extraction/gansu-ningxia-guide-2014/` | Useful old city-section sequence, place leads, district questions, food names, and nearby-trip leads. Every price, route, timetable, hotel, restaurant, phone number, opening hour, and safety statement is obsolete until independently rechecked. Source figures are not publishable. |
| `LZH-HISTORY-2020` | `Sources/甘肃简史.pdf`; sections on Qin/Han Jincheng, Sui/Tang administration, `陕甘分省及兰州的崛起` around printed p. 255, and the iron bridge around printed pp. 279-280 | SHA-256 `d4e621e7045c1671c74d7d87e5a271e8b8fe3aed0f9191f01f3e0e9ac98d7cdf`; text-layer extraction at ignored `build/research/lanzhou/source-extraction/gansu-brief-history/source.raw.txt` | Secondary chronology for the crossing, provincial administration, bridge, railway, and industry. Avoid collapsing changing administrative units into one continuous modern city. Reconcile exact bridge dimensions, cost, and dates with local records before using them. |
| `LZH-FOOD-2020` | `Sources/陇味儿.pdf`, PDF pp. 120-155 | SHA-256 `0fd379920b9e78480ba8d0ca890a1040f2bbca2899d63b30e218d6726ab7b248`; derived OCR at ignored `build/research/lanzhou/source-extraction/gansu-food/` | Leads for morning beef-noodle practice, noodle widths, niangpizi, huidouzi, tianpeizi, and Lanzhou lily. Original phrasing, nostalgia, origin stories, and health claims are not reused. Source figures are not publishable. |
| `LZH-OPEN-ZH` | `/home/lachlan/ProjectsLFS/Books/resources/curated-books/travel-guides/xian-gansu-open-guides/gansu/zh/source-pages/02-gansu-zh.json` | MediaWiki page `兰州`, page ID `5154`, revision `205577`, SHA-256 `c7d6b4ec04107a7dff2612d26d3926058be9b4e67ef5ed4055e7b3f85c717e07`, CC BY-SA 4.0 | Sparse orientation, coordinates, station and attraction leads. Treat the sweeping history paragraph, taxi prices, airport transfer, venue hours, food generalizations, and listings as unverified leads. Attribute any retained CC BY-SA expression, although the book normally replaces it with independently written, independently sourced prose. |
| `LZH-OPEN-EN` | `/home/lachlan/ProjectsLFS/Books/resources/curated-books/travel-guides/xian-gansu-open-guides/gansu/en/source-pages/02-gansu-en.json` | MediaWiki page `Lanzhou`, page ID `19080`, revision `5243430`, SHA-256 `3b5d603314ca3fbbe07256dae23b586beb15bddf53170d91e04d978f243a2c45`, CC BY-SA 4.0 | Leads for station roles, metro questions, central attractions, food, lodging areas, and Bingling Temple. Reject prices, named recommendations, unsupported historical assertions, exact journey times, and editorial judgments until independently verified. |
| `LZH-REFERENCE-LEDGER` | `/home/lachlan/ProjectsLFS/Books/references/XIAN_GANSU_TRAVEL_GUIDES_2026-08-14.md` | External read-only reference ledger | Confirms guide provenance, revisions, hashes, licensing, and intended research roles. It is not a factual source for Lanzhou itself. |
| `LZH-PDF2TEX-TOOLING` | `/home/lachlan/ProjectsLFS/ZhJpBook/pdf2tex` | External read-only extraction tooling inspected before destination production | Reuse page-aware extraction, immutable source hashes, figure manifests, OCR routing, and missing-figure checks. Do not copy its queues, archives, or unrelated book output into LazyTravel. |

## Current Authoritative Source Index

All web sources below were opened or rechecked on `2026-08-21`. A check date
does not make a volatile observation durable. Operational facts are checked
again during their chapter gate and close to release.

| ID | Authority and subject | URL | Use and constraint |
| --- | --- | --- | --- |
| `LZH-GEO-2026` | Gansu Belt and Road portal, Lanzhou geography | <https://ydyl.gansu.gov.cn/gsydyl/zjgs/202605/t20260511_36214.html> | Main-city relationship among the west-east Yellow River, Gaolan/White Pagoda hill systems, and the long narrow valley. Do not repeat promotional uniqueness claims. |
| `LZH-CITY-PLAN` | Lanzhou territorial spatial plan | <https://szfjrb.lanzhou.gov.cn/module/download/downfile.jsp?classid=0&filename=5a959a8c6d014f02abc1baabb7cbee44.pdf> | Broad river-and-two-hills urban form and planning geography. It is not a pedestrian map or evidence that every mapped project is complete. |
| `LZH-METRO-SERVICE` | Lanzhou Rail Transit, passenger service and station index | <https://www.lzgdjt.com/lzgd/serve.jsp> | Current line and station relationships, including the West Station, Xiguan, provincial government, Dongfanghong Square, Lanzhou University, Lanzhou Railway Station, and Wulipu. Exact hours, exits, and temporary conditions remain volatile. |
| `LZH-METRO-NETWORK-2026` | Lanzhou Rail Transit, current two-line network summary | <https://www.lzgdjt.com/lzgd/detail.jsp?contentId=53151> | Line 1 opening in 2019, Line 2 first-phase opening in 2023, and current network scale. Future lines and construction are not presented as operating service. |
| `LZH-AIRPORT-T3-2025` | Lanzhou New Area government, T3 opening | <https://www.lzxq.gov.cn/system/2025/03/06/031148351.shtml> | T3 operation from `2025-03-20` and transfer of passenger flights from T1/T2. Recheck terminal use before release and before travel. |
| `LZH-NDRC-AIRPORT-2025` | National Development and Reform Commission, T3 and integrated transport hub | <https://www.ndrc.gov.cn/xwdt/ztzl/dtfzgz/202504/t20250403_1397004.html> | Institutional confirmation of the new terminal and transport hub. It does not supply a current timetable. |
| `LZH-AIRPORT-BUS-2025` | Lanzhou New Area government, bus arrangements at T3 opening | <https://www.lzxq.gov.cn/system/2025/03/20/031155931.shtml> | Dated lead for city transfer branches. Never preserve the opening-day route, frequency, or fare as current advice without a fresh operator check. |
| `LZH-AIRPORT-CONNECTIONS-2026` | Lanzhou Investment and Trade Fair visitor transport page | <https://www.lanzhoufair.cn/services/transport/transport-airport> | Current orientation to airport rail and road connections. Exact departures and station naming require operator confirmation. |
| `LZH-MUSEUM` | Gansu Provincial Museum | <https://gansumuseum.com/> | Current visitor guide, reservation route, transport guidance, permanent-exhibition index, and venue notices. Opening days, entry cutoff, display status, and special exhibitions are volatile. |
| `LZH-BRIDGE-HISTORY` | Lanzhou local chronicles, Zhongshan Bridge | <https://dfzb.lanzhou.gov.cn/art/2017/10/16/art_9606_518474.html> | Floating-bridge sequence, iron-bridge construction, `1909` opening, and `1942` renaming. The page also contains stale tourism logistics that are not used. |
| `LZH-RIVER-CORE-2024` | Lanzhou municipal portal, Zhongshan Bridge and White Pagoda core-area work | <https://www.lanzhou.cn/ztpd/system/2024/08/30/012496958.shtml> | Place relationship and dated public-space work. Completion and access are checked on current official notices. |
| `LZH-TOURISM-2026` | Gansu culture and tourism department, current Lanzhou visitor overview | <https://www.gswbj.gov.cn/a/2026/06/10/28550.html> | Current lead for the pedestrian bridge, riverfront relationship, foods, and central visitor sequence. Promotional language and broad quality claims are not reused. |
| `ICH-WATERWHEEL` | China Intangible Cultural Heritage, Lanzhou Yellow River waterwheel | <https://www.ihchina.cn/project_details/14355/> | Protected-heritage record, `2006` listing, technology, and historical practice. A heritage description does not establish the operating condition of a present display. |
| `ICH-BEEF-NOODLE` | China Intangible Cultural Heritage, Lanzhou beef-noodle craft | <https://www.ihchina.cn/project_details/23794.html> | `2021` national-list record, noodle forms, craft sequence, and the established color formula. Treat origin narrative as recorded tradition unless corroborated; do not convert it into a health or authenticity ranking. |
| `LZH-FOOD-2026` | Gansu culture and tourism department, Lanzhou food context | <https://www.gswbj.gov.cn/a/2026/03/16/27730.html> | Contemporary cultural context for beef noodles and their social rhythm. Promotional claims require separate support. |
| `SAMR-NOODLE-STANDARD` | National standard-information platform, Lanzhou beef-noodle collective-mark standard | <https://std.samr.gov.cn/db/search/stdDBDetailed?id=2E7984F54EA9E867E06397BE0A0AE106> | Evidence that a `2024` local standard exists and defines a protected business context. It is not proof that every shop follows it. |
| `LZH-LILY` | Lanzhou municipal investment material, lily production | <https://tzcjj.lanzhou.gov.cn/module/download/downfile.jsp?classid=0&filename=82794439d83d401c9a877f8a44207d7a.pdf> | Qilihe/Xiguoyuan production context. Do not infer the origin or quality of a restaurant dish from its name alone. |
| `CMA-LANZHOU-CLIMATE` | China Meteorological Administration city-climate page | <https://www.weather.com.cn/cityintro/101160101.shtml> | Long-term dry climate and large daily/seasonal temperature variation. It is not a trip-date forecast; current warnings and forecasts override it. |
| `LZH-ROUTES-2024` | Gansu culture and tourism department, Lanzhou route leads | <https://www.gswbj.gov.cn/a/2024/04/17/20156.html> | Place combinations to investigate. LazyTravel derives its own timings and removes overpacked sequences. |
| `LZH-ROUTES-2026` | Gansu culture and tourism department, current regional route overview | <https://www.gswbj.gov.cn/a/2026/04/27/28105.html> | Current lead for city and surrounding-area relationships. It does not replace site or operator access checks. |
| `UNESCO-SILK-ROADS` | UNESCO World Heritage Centre, Silk Roads: Chang'an-Tianshan Corridor | <https://whc.unesco.org/en/list/1442/> | World Heritage framework for the corridor and component sites. Do not label an unlisted Lanzhou place as a World Heritage component. |
| `DHA-BINGLING` | Dunhuang Academy, Bingling Temple Grottoes | <https://www.dha.ac.cn/skxl/blssk.htm> | Institutional history and visitor-information entry point. Reservoir crossings, boats, road access, hours, and closures remain volatile. |
| `YJ-BINGLING-CLOSURE-2025` | Yongjing County government, temporary Bingling closure example | <https://www.gsyongjing.gov.cn/yjx/wtgdhlyj/fdzdgknr/GSGG/art/2025/art_754e69206c1f4e8f9cbac5eca89409b5.html> | Evidence that weather can suspend access. It is not evidence of a current closure or reopening. |
| `LZH-XINGLONG-2024` | Lanzhou municipal investment portal, Xinglong Mountain | <https://tzcjj.lanzhou.gov.cn/art/2024/3/13/art_220_1332695.html> | Landscape and location lead. Current gates, trails, vehicles, and closures require site-level confirmation. |
| `LZH-REGIONAL-ROUTE-2026` | Gansu culture and tourism department, 2026 travel route | <https://www.gswbj.gov.cn/a/2026/06/17/28621.html> | Current lead for nearby and onward route questions. The book does not copy its itinerary or assume each segment runs daily. |

## Initial Claim Plan

| Chapter | Publishable question | Evidence required before prose is final |
| --- | --- | --- |
| 1 | How does the valley shape ordinary movement? | `LZH-GEO-2026`, `LZH-CITY-PLAN`, current metro geography, and map-coordinate checks. Avoid a precise valley length unless two compatible official definitions agree. |
| 2 | Which arrival gate fits the booked service and hotel district? | `LZH-AIRPORT-T3-2025`, `LZH-NDRC-AIRPORT-2025`, `LZH-METRO-SERVICE`, railway/airport operator checks, and dated booking evidence. |
| 3 | Which changes in crossing and administration are still visible? | `LZH-HISTORY-2020` plus `LZH-BRIDGE-HISTORY`; reconcile names, administrative levels, bridge dates, and urban continuity. |
| 4 | What is a realistic central bridge-and-banks walk? | Current public-space and bridge sources, map measurements, same-day river/access guidance, and field-readable landmarks. |
| 5 | Which museum route gives useful context for a later Gansu trip? | `LZH-MUSEUM`, object-level institutional records, current gallery status, and explicit distinction between findspot and display location. |
| 6 | How does a traveler order and pace meals without turning food into folklore? | `ICH-BEEF-NOODLE`, `LZH-FOOD-2020`, `LZH-FOOD-2026`, food-safety and dietary confirmation where needed, and direct menu terminology. |
| 7 | Which one height fits weather, mobility, and daylight? | Separate official access sources for White Pagoda Hill, Lanshan, and Wuquan Mountain, current route checks, map gradients, and no guaranteed-view language. This is an open research gate. |
| 8 | Which district minimizes the traveler's actual transfers? | Current station/metro geography, official lodging directories or direct property pages, and dated verification for every named property or feature. |
| 9 | Can each itinerary be completed with meals, rest, and a usable exit? | Accepted Chapters 1-8, measured map distances, current venue days, and a whole-day fallback rather than added stops. |
| 10 | How much buffer does the next Gansu leg require? | Current railway and airline booking results, station/terminal confirmation, and dated operator notices. No preserved timetable. |
| 11 | Which single nearby day is operationally realistic? | `DHA-BINGLING`, current Bingling/Liujiaxia operator notices, site-level Xinglong and Ink Danxia access, weather/closure checks, and conservative return margins. |

## Rejected Or Deferred Claims

| Claim or pattern | Decision |
| --- | --- |
| “Lanzhou is the only provincial capital through which the Yellow River passes.” | Reject. It is a promotional and definition-dependent uniqueness claim that does not improve a travel decision. |
| One uninterrupted Lanzhou city from Qin or Han administration to the present | Reject. Administrative names, jurisdictions, settlements, and urban footprints changed. Use dated layers tied to visible places. |
| Every important Silk Road route crossed the river at the same Lanzhou point | Reject unless a route-specific historical source proves it. The corridor is not one timeless line. |
| “Jincheng” simply proves an impregnable golden city or one named founding episode | Defer. Present etymology or founding stories only with a responsible historical source and uncertainty label. |
| Huo Qubing crossed the Yellow River at Lanzhou twice on the stated campaigns | Defer. The open guide is not enough, and the claim is unnecessary unless a reliable locator changes an on-site reading. |
| Exact iron-bridge dimensions, imported components, cost, or payment terms | Defer pending reconciliation between `LZH-HISTORY-2020`, local chronicles, and engineering records. The `1909` opening and visible role are enough for the first draft. |
| All Lanzhou beef-noodle shops are halal, use one recipe, or share one origin | Reject. Verify each shop's practice directly; describe the protected craft without universalizing businesses. |
| A single exact invention date for Lanzhou beef noodles | Treat as recorded tradition unless independent historical evidence supports the date and person. Do not write an origin legend as settled fact. |
| Beef noodles, lily, sanpaotai, or any snack has a medical or longevity effect | Reject without high-quality medical evidence; such claims are irrelevant to the guide. |
| Yellow River carp as an automatic visitor recommendation | Defer. Current legality, sourcing, ecological impact, and restaurant provenance would need reliable evidence. |
| “Lanzhou food is mainly sour and spicy.” | Reject as an unhelpful generalization from a sparse open-guide snapshot. Describe individual dishes and ordering choices. |
| Spring is unsuitable for Lanzhou | Reject. Use long-term climate patterns plus a trip-date forecast, clothing plan, and current warnings. |
| The 2014 airport distance, one-hour transfer, taxi fare, bus route, hotel, restaurant, or venue hours | Reject as current advice. The opening of T3 alone demonstrates why the old logistics cannot be carried forward. |
| A clear skyline, river level, boat service, cableway, or sunset | Never promise. Give a same-day check and a ground-level alternative. |
| A search result or tourism list proves a hotel is open, clean, quiet, accessible, or suitable | Reject. Verify direct property evidence and preserve the check date. |
| Linxia, the Yellow River Stone Forest, or another complex regional destination is an easy add-on to a full Lanzhou day | Reject. A place that requires a long transfer, uncertain operation, or an overnight belongs in a wider Gansu plan. |

## Volatile Verification Matrix

| Topic | Authoritative check near release and travel | Durable wording allowed now |
| --- | --- | --- |
| Airport | Airport/airline and official terminal notices | T3 became the operating passenger terminal in 2025; recheck terminal and transfer. |
| Rail | Booked ticket and official railway notices | Lanzhou West and Lanzhou Station serve different journeys; use the station printed on the ticket. |
| Metro | Lanzhou Rail Transit service page and station notice | Two operating lines form the current core network; exits and hours can change. |
| Museum | Gansu Provincial Museum reservation and notice pages | The museum is a major regional-context anchor; opening day and displayed objects can change. |
| Riverfront | Municipal/site notices and same-day weather/river conditions | The bridge-and-banks relationship is durable; access and boat operation are not. |
| Food | Direct shop/menu/dietary confirmation | Explain food forms and ordering logic; do not preserve a business recommendation as permanent. |
| Lodging | Direct property page/contact plus booking terms | District-first advice is durable; property operations and facilities are not. |
| Nearby day | Site, county, transport operator, and weather notices | Bingling, Xinglong, and Ink Danxia are alternative planning branches, not guaranteed departures. |

## Map And Figure Evidence

- Maps use current official route diagrams, site coordinates, measured
  distances, and separately recorded map data. They remain schematic and do
  not imply that every drawn path is open or step-free.
- Maps contain no cast. Every new non-map figure contains exactly Aya-chan,
  Lala Xia, Sasa-kun, and the Zhuangzi robot, derived from the hash-pinned
  external references in `data/sources/catalog.json`.
- Historical evidence is shown as maps, objects, structures, or clearly dated
  documentary material. The four guides are never placed inside a historical
  event as witnesses.
- Attraction plates must make the destination recognizable at B6 and mobile
  sizes. Character likeness, geographic cues, crowd count, signage, season,
  and implied access are checked before approval.
- Reader captions identify the place and useful observation. Technical
  generation details remain in asset provenance and adjacent QA records.

## Chapter Gate

A Lanzhou chapter may advance only after its factual ledger, original aligned
Chinese/Japanese/English text, pinyin and furigana reconstruction, assets,
citations, B6 pages, and responsive website views pass. Review stops when
facts, natural language, route usefulness, readings, legibility, and
reproducibility pass. Later chapters do not bypass the active chapter.
