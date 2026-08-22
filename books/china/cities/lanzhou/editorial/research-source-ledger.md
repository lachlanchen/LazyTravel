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

All web sources below were opened or rechecked on `2026-08-21` or
`2026-08-22`. A check date
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
| `LZH-AIRPORT-RAIL-2026` | Lanzhou New Area government, first year of the airport loop railway | <https://www.lzxq.gov.cn/system/2026/03/23/031341573.shtml> | Confirms current operation and physical connection of Zhongchuan Airport East Railway Station with T3. The article's peak frequencies, journey-time examples, demand figures, and promotional claims are not treated as a timetable or promise. |
| `LZH-METRO-HUBS-2026` | Lanzhou Rail Transit, 2026 holiday hub service | <https://www.lzgdjt.com/lzgd/detail.jsp?contentId=53037> | Confirms current passenger-service presence at Lanzhou West Station North Square and Lanzhou Railway Station metro stations. Holiday staffing and ridership are dated context, not a permanent service guarantee. |
| `CR-12306-LIVE` | China Railway 12306 official booking service | <https://www.12306.cn/> | Live authority for the train-specific departure/arrival station and bookable service. The book records the checking method, not a result, train number, fare, or timetable. |
| `LZH-STAY-SEGMENT-MAP` | Original LazyTravel lodging-segment diagram | `data/maps/lanzhou/lanzhou-stay-segment.config.json` | Reproducible west-centre-east decision bands and a separate not-to-scale airport panel. It contains no hotel pins, transfer line, timetable, fare, or administrative boundary. |
| `LZH-MERCURE-ZHENGNING-2026` | Accor, Mercure Lanzhou Zhengning Road | <https://all.accor.com/hotel/B7D6/index.en.shtml> | Rechecked `2026-08-22`; supports No. 11 South Yongchang Road, Chengguan, Zhengning Road night-market adjacency, and a direct contact route. It does not establish room quietness, view, exact entrance, cleanliness, or accessibility. |
| `LZH-HIEX-JIANLAN-2026` | IHG, Holiday Inn Express Lanzhou Jianlan | <https://www.ihg.com/holidayinnexpress/hotels/us/en/lanzhou/lhwlj/hoteldetail> | Rechecked `2026-08-22`; supports the Qilihe relationship to Gansu Provincial Museum, Xizhanshizi on Line 1, and Lanzhou West. Operator distances are locating clues, not fixed journey times. |
| `LZH-HILTON-CENTRE-2026` | Hilton, Hilton Lanzhou City Center | <https://www.hilton.com/en/hotels/lhwtrhi-hilton-lanzhou-city-center/> | Rechecked `2026-08-22`; supports 3 Mid Tianshui Road, Chengguan, the office-and-shopping-complex setting, and operator wording that a metro station is walkable. The English property name and city-view wording do not establish bridge proximity or the room sold. |
| `LZH-IBIS-AIRPORT-2026` | Accor, Ibis Lanzhou Zhongchuan Airport | <https://all.accor.com/hotel/B496/index.zh.shtml> | Rechecked `2026-08-22`; supports the operator's approximate ten-minute road estimate and advertised complimentary 24-hour transfer. T3 pickup, reservation, waiting, luggage capacity, and earliest drop-off remain direct checks. |
| `CN-FOREIGN-LODGING-CIRCULAR-2024` | State Council, seven-department foreign-guest accommodation circular | <https://english.www.gov.cn/news/202407/26/content_WS66a2d827c6d0868f4e8e975c.html> | Current policy evidence against qualification-based reception restrictions and illegal refusal notices. It makes old guidebook refusal lists unusable as current evidence, but does not guarantee error-free handling at every desk or shift. |
| `CN-HOTEL-REGISTRATION-2025` | State Council, 2025 guide for business expatriates in China | <https://english.www.gov.cn/2025special/bizexpatsinchina2025> | Supports presentation of a passport or other valid document at a hotel and registration by the hotel. It does not replace the property's booking and late-arrival confirmation. |
| `CN-NIA-REGISTRATION-2026` | National Immigration Administration, foreigner accommodation registration | <https://www.nia.gov.cn/n741440/n741577/c1771556/content.html> | Rechecked `2026-08-22`; corroborates hotel registration and keeps non-hotel online registration outside the scope of this city-hotel chapter. |
| `LZH-MUSEUM` | Gansu Provincial Museum | <https://www.gansumuseum.com/> | Current institutional entry point for visitor information, galleries, floor guidance, collection records, and notices. The narrower records below are cited for Chapter 5 claims. |
| `LZH-MUSEUM-VISIT-2026` | Gansu Provincial Museum, individual appointment and visitor guide | <https://www.gansumuseum.com/visitAppointment?nav=1-0> | Rechecked `2026-08-22`: opening days and cutoffs, free individual appointment up to three days ahead, accepted original identity documents, luggage storage, manual-wheelchair/stroller loans, photography restrictions, and first-floor guide desk. The record conflicts internally on daily ticket-release time (`17:00` in the summary, `09:00` in the body), so no release time is published. The homepage and detailed guide also disagree on a metro exit, so the book names Line 1 but requires a live exit check. |
| `LZH-MUSEUM-GALLERIES-2026` | Gansu Provincial Museum, current long-term exhibition index | <https://www.gansumuseum.com/regularExhibitions?nav=2-0> | Rechecked `2026-08-22`; entries updated `2026-08-21` list Painted Pottery and Buddhist Art on the third floor and Silk Road Civilization, Paleontology, and Red Gansu on the second floor. Long-term status is not a guarantee that a room or named object is open or displayed on a particular day. |
| `LZH-MUSEUM-FLOOR-2026` | Gansu Provincial Museum, official floor guide | <https://www.gansumuseum.com/navMap?nav=1-1> | Current floor relationship and service-area lead for an original schematic. Do not copy the museum diagram or infer lift operation, walking time, accessibility, one-way controls, or current room access. |
| `LZH-MUSEUM-OBJECTS-POTTERY-2026` | Gansu Provincial Museum collection catalogue, human-head-mouth and salamander-design painted pottery vessels | <https://www.gansumuseum.com/collectionDetail?id=1675&nav=3-0> | Rechecked `2026-08-22`; catalogue records establish Yangshao type, approximate age, form, motif, and the Qin'an Dadiwan and Gangu Xiping findspots. Catalogue presence is not display confirmation; speculative belief, totem, or origin claims are excluded. |
| `LZH-MUSEUM-OBJECTS-BUDDHIST-2026` | Gansu Provincial Museum collection catalogue, Dayun Temple reliquary and *Repaying Parents Sutra* transformation painting | <https://www.gansumuseum.com/collectionDetail?id=1356&nav=3-0> | Rechecked `2026-08-22`; establishes the `694` nested reliquary from Jingchuan and the Song silk painting from Dunhuang's Library Cave. Each findspot remains explicit, and neither record guarantees current display. |
| `LZH-MUSEUM-OBJECTS-SILK-2026` | Gansu Provincial Museum collection catalogue, bronze galloping horse and messenger mural brick | <https://www.gansumuseum.com/collectionDetail?id=f74b96843aec46c9ae14039adbd9666c&nav=3-0> | Rechecked `2026-08-22`; establishes the Han bronze horse from Wuwei Leitai and the Wei-Jin messenger brick from Jiayuguan Tomb 5. Use the official horse title, avoid identifying the support as a swallow, and never treat collection listing as current display status. |
| `LZH-LANZHOU-CHRONICLE` | Gansu Local Chronicles, Lanzhou city chronicle | <https://www.gsdfszw.org.cn/gssz_58/del_70/lzs_238/202006/P020200623624402422154.pdf> | Institutional chronology for the 1738 move and renaming of Lanzhou Prefecture and the 1764 concentration of the Shaan-Gan governor-general in Lanzhou. The large general chronicle is used by locator, not copied into project storage. |
| `LZH-CHENGGUAN-HISTORY` | Gansu Local Chronicles, Chengguan district gazetteer | <https://www.gsdfszw.org.cn/gsxz/lzs_266/cgq/201708/P020170814555511254018.pdf> | Administrative and city-site sequence from Han-era regional geography through Wuquan, the Song river-facing city, and Ming enlargement. It does not settle every disputed identification of early Jincheng County. |
| `LZH-JINCHENG-DEBATE` | Gansu Local Chronicles historical journal, early Jincheng location debate | <https://www.gsdfszw.org.cn/gssz_64/szxq/201910/P020191011364011343764.pdf> | Evidence that the locations, identifications, and movements of early Jincheng County remain disputed. Supports explicit uncertainty, not a new preferred site claim. |
| `LZH-OLD-CITY-STREETS` | Gansu Local Chronicles, Lanzhou land and street-name gazetteer | <https://www.gsdfszw.org.cn/gssz_58/dyl_69/lzs_224/dssqjsfz/201707/P020170705319152749529.pdf> | Documents Qing street names and the old east-west main street corresponding to present Zhangye Road. It does not prove an ancient street line beneath the current paving. |
| `LZH-OLD-CITY-GATES` | Gansu Local Chronicles, Lanzhou construction gazetteer | <https://www.gsdfszw.org.cn/gssz_58/dyl_69/lzs_224/dsbjjzyz/201707/P020171108368971422997.pdf> | Approximate former inner-city gate relationships around Zhangye Road, Nanguan, and the north bridge gate. Most points are interpretive locators, not surviving entrances. |
| `LZH-CITY-GOD-TEMPLE` | Gansu Local Chronicles, Lanzhou culture and heritage gazetteer | <https://www.gsdfszw.org.cn/gssz_58/dyl_69/lzs_224/dwsyjwwz/201707/P020170705314130708607.pdf> | Heritage history, present Zhangye Road location, current First Workers' Club use, and surviving courtyard/building sequence. Current public access must be checked separately. |
| `LZH-CITY-GOD-CURRENT-2026` | Gansu media portal, current cultural use of Lanzhou Prefecture City God Temple | <https://gansu.gscn.com.cn/system/2026/01/27/013448439.shtml> | Dated confirmation that the temple/First Workers' Club remains an active civic-cultural venue. The event, access arrangement, and any opening information are not treated as permanent. |
| `LZH-RAILWAY-HISTORY` | Gansu Local Chronicles, Gansu railway gazetteer | <https://gsdfszw.org.cn/gssz/dyl/dsjjszs/201612/P020170214612523218022.pdf> | Completion of the Tian-Lan railway in 1952 and the later Bao-Lan, Lan-Xin, and Lan-Qing network sequence. No historic timetable or promotional traffic total is needed. |
| `LZH-1954-PLAN` | Gansu Local Chronicles, Lanzhou planning gazetteer | <https://www.gsdfszw.org.cn/gssz_58/dyl_69/lzs_224/dwjtdz/201711/P020171115374652928666.pdf> | The 1954 plan's old centre, Xigu, Qilihe/rail, and eastern industrial-district logic. A planning document is not proof that every proposal was built as drawn. |
| `LZH-BRIDGE-HISTORY` | Lanzhou local chronicles, Zhongshan Bridge | <https://dfzb.lanzhou.gov.cn/art/2017/10/16/art_9606_518474.html> | Floating-bridge sequence, iron-bridge construction, `1909` opening, and `1942` renaming. The page also contains stale tourism logistics that are not used. |
| `LZH-BRIDGE-DETAIL` | Gansu Local Chronicles, Yellow River Iron Bridge record | <https://www.gsdfszw.org.cn/tp/201703/t20170327_523.html> | Surviving south-bank General Pillar, the repeated winter dismantling of the floating bridge, the five through-truss spans, transported materials, and completion on `1909-08-19`. Exact dimensions, cost, heroic rhetoric, and dramatized construction prose are not reused. |
| `LZH-BRIDGE-PEDESTRIAN-2026` | Chinese Lanzhou, current Zhongshan Bridge use | <https://news.lanzhou.cn/system/2026/03/30/012596111.shtml> | Dated confirmation that vehicle use ended in `2013` and the bridge now functions as a permanent pedestrian crossing. Temporary restrictions still require a same-day check. |
| `LZH-RIVER-CORE-2024` | Lanzhou municipal portal, Zhongshan Bridge and White Pagoda core-area work | <https://www.lanzhou.cn/ztpd/system/2024/08/30/012496958.shtml> | Place relationship and dated public-space work. Completion and access are checked on current official notices. |
| `LZH-TOURISM-2026` | Gansu culture and tourism department, current Lanzhou visitor overview | <https://www.gswbj.gov.cn/a/2026/06/10/28550.html> | Current lead for the pedestrian bridge, riverfront relationship, foods, and central visitor sequence. Promotional language and broad quality claims are not reused. |
| `LZH-BAITA-GAZETTEER` | Gansu Local Chronicles, Lanzhou garden and greening gazetteer, printed pp. 139-151 | <https://www.gsdfszw.org.cn/gssz_58/dyl_69/lzs_224/dsjyllhz/201707/P020170705353409423046.pdf> | Documents pre-`1448` temple ruins, reconstruction during `1448-1452`, later Ming/Qing additions, the `1958-1959` terrace complex, full park opening in `1960`, and the bridge-park-temple axis. It does not settle the first foundation date or prove current access to every path or building. |
| `LZH-BAITA-CURRENT-2025` | Lanzhou municipal English portal, White Pagoda Hill Park | <https://english.lanzhou.cn/system/2025/09/16/012564390.shtml> | Current institutional confirmation of the park's north-bank setting, terraced ascent, and central-city viewpoint. Promotional descriptions and permanent-access implications are excluded. |
| `LZH-HEIGHTS-GEOGRAPHY-2025` | Gansu culture and tourism department, Lanzhou's three southern and northern height choices | <https://www.gswbj.gov.cn/a/2025/07/17/25374.html> | Current institutional lead for White Pagoda Hill, Lanshan, and Wuquan in the valley landscape. Promotional superlatives, clear-view promises, and permanent route implications are excluded. |
| `LZH-LANSHAN-RECORD-2025` | Gansu Daily, local record of Lanshan and Santai Pavilion | <https://szb.gansudaily.com.cn/gsrb/pc/con/202501/08/c202436.html> | Records the Santai high point at `2129.6 m`, repeated loss and rebuilding, and the present `26 m` pavilion rebuilt in `1983-1984`. The accompanying image is an unredistributed massing reference, not a publishable source figure. |
| `LZH-HEIGHTS-ACCESS-2026` | Gansu culture and tourism department, dated Lanzhou height itinerary | <https://www.gswbj.gov.cn/a/2026/06/11/28565.html> | Dated evidence that taxi or cableway and a Wuquan-Lanshan connection were promoted in June 2026. It does not prove current operation, step-free access, one-way versus return service, or an open through-route. |
| `LZH-LANSHAN-HOLIDAY-BUS-2026` | Gansu Daily, Lanzhou bus `750` holiday service notice | <https://lz.gansudaily.com.cn/system/2026/04/29/031360676.shtml> | Shows intensified service only for `2026-05-01` through `2026-05-05`. It is evidence against presenting route `750` as a permanent daily service. |
| `LZH-WUQUAN-HERITAGE-2023` | Xinhua, Wuquan Mountain conservation and reopening | <https://www.news.cn/culture/2023-04/02/c_1129487481.htm> | Establishes the five named springs, layered Yuan-to-later construction, `24` protected buildings or groups, national-level protection in `2013`, and nine reopened after conservation in `2023`. That reopening does not prove every doorway is open today. The images are unredistributed visual references only. |
| `LZH-WUQUAN-HERITAGE-2021` | Gansu culture and tourism department, Wuquan Mountain heritage overview | <https://www.gswbj.gov.cn/a/2021/02/26/7922.html> | Corroborating institutional context for the named springs and layered park-and-building landscape. The Huo Qubing spring story is treated as tradition, not historical proof. |
| `LZH-WUQUAN-FLOOD-2026` | Gansu Daily, Wuquan flood-season operation | <https://gansu.gansudaily.com.cn/system/2026/08/11/031415145.shtml> | Dated evidence for monitoring, broadcast clearance, and temporary closure procedures during the 2026 flood season. It supports a weather-triggered cancellation rule, not a current closure claim. |
| `ICH-WATERWHEEL` | China Intangible Cultural Heritage, Lanzhou Yellow River waterwheel | <https://www.ihchina.cn/project_details/14355/> | Protected-heritage record, `2006` listing, technology, and historical practice. A heritage description does not establish the operating condition of a present display. |
| `ICH-BEEF-NOODLE` | China Intangible Cultural Heritage, Lanzhou beef-noodle craft | <https://www.ihchina.cn/project_details/23794.html> | `2021` national-list record, noodle forms, craft sequence, and the established color formula. Treat origin narrative as recorded tradition unless corroborated; do not convert it into a health or authenticity ranking. |
| `LZH-FOOD-2026` | Gansu culture and tourism department, Lanzhou food context | <https://www.gswbj.gov.cn/a/2026/03/16/27730.html> | Contemporary cultural context for beef noodles and their social rhythm. Promotional claims require separate support. |
| `LZH-NOODLE-ORDER-2022` | Gansu Belt and Road portal, beef-noodle ordering guide | <https://ydyl.gansu.gov.cn/gsydyl/news/gsdt/202209/t20220907_9265.html> | Common counter sequence, menu-recognition terms, and separate beef or egg additions. Old prices and any implication of one universal shop layout are excluded. |
| `LZH-SUMMER-FOODS-2023` | Gansu Belt and Road portal, niangpizi and tianpeizi | <https://ydyl.gansu.gov.cn/gsydyl/gjjl/whsl/202306/t20230605_10588.html> | Institutional descriptions of cut niangpizi with variable condiments and fermented-grain tianpeizi with liquid. Seasonal absolutes, alcohol assumptions, and health claims are excluded. |
| `CNIPA-LANZHOU-LILY-2025` | CNIPA geographical-indication compendium, Lanzhou lily, pp. 3973-3974 | <https://www.cnipa.gov.cn/attach/0/20250826010509.pdf> | Protected edible bulb, thick white scales, and fresh sweet-crisp character. A restaurant menu name does not authenticate GI origin. |
| `GS-SANPAOTAI-2022` | Gansu market-regulator consumer guidance, sanpaotai covered-bowl tea | <https://www.bypc.gov.cn/zfxxgk/bmdwxzjd/bmdw/qscjdglj/fdzdgknr/xfzwq/art/2023/art_42448a8b696a4a02ae540a100978554a.html> | Covered-bowl format and variable tea, dried-fruit, flower, sugar, and goji combinations. It does not establish one recipe or therapeutic effect. |
| `SAMR-NOODLE-STANDARD` | National standard-information platform, Lanzhou beef-noodle collective-mark standard | <https://std.samr.gov.cn/db/search/stdDBDetailed?id=2E7984F54EA9E867E06397BE0A0AE106> | Evidence that a `2024` local standard exists and defines a protected business context. It is not proof that every shop follows it. |
| `LZH-LILY` | Lanzhou municipal investment material, lily production | <https://tzcjj.lanzhou.gov.cn/module/download/downfile.jsp?classid=0&filename=82794439d83d401c9a877f8a44207d7a.pdf> | Qilihe/Xiguoyuan production context. Do not infer the origin or quality of a restaurant dish from its name alone. |
| `CMA-LANZHOU-CLIMATE` | China Meteorological Administration city-climate page | <https://www.weather.com.cn/cityintro/101160101.shtml> | Long-term dry climate and large daily/seasonal temperature variation. It is not a trip-date forecast; current warnings and forecasts override it. |
| `LZH-ROUTES-2024` | Gansu culture and tourism department, Lanzhou route leads | <https://www.gswbj.gov.cn/a/2024/04/17/20156.html> | Place combinations to investigate. LazyTravel derives its own timings and removes overpacked sequences. |
| `LZH-ROUTES-2026` | Gansu culture and tourism department, current regional route overview | <https://www.gswbj.gov.cn/a/2026/04/27/28105.html> | Current lead for city and surrounding-area relationships. It does not replace site or operator access checks. |
| `UNESCO-SILK-ROADS` | UNESCO World Heritage Centre, Silk Roads: Chang'an-Tianshan Corridor | <https://whc.unesco.org/en/list/1442/> | World Heritage framework for the corridor and component sites. Do not label an unlisted Lanzhou place as a World Heritage component. |
| `DHA-BINGLING` | Dunhuang Academy, Bingling Temple Grottoes | <https://www.dha.ac.cn/skxl/blssk.htm> | Institutional history and visitor-information entry point. Reservoir crossings, boats, road access, hours, and closures remain volatile. |
| `YJ-BINGLING-CLOSURE-2025` | Yongjing County government, temporary Bingling closure example | <https://www.gsyongjing.gov.cn/yjx/wtgdhlyj/fdzdgknr/GSGG/art/2025/art_754e69206c1f4e8f9cbac5eca89409b5.html> | Evidence that weather can suspend access. It is not evidence of a current closure or reopening. |
| `LZH-XINGLONG-2024` | Lanzhou municipal investment portal, Xinglong Mountain | <https://tzcjj.lanzhou.gov.cn/art/2024/3/13/art_220_1332695.html> | Landscape and location lead. Current gates, trails, vehicles, and closures require site-level confirmation. |
| `LZH-INK-DANXIA-2026` | Gansu culture and tourism department, Lanzhou Ink Danxia | <https://www.gswbj.gov.cn/a/2026/07/07/28814.html> | Current place and visitor-experience lead for a geology-led nearby day. New activities, transport, hours, ticketing, and construction claims are volatile and require direct site confirmation. Promotional rankings and investment language are not reused. |
| `YJ-YELLOW-TAO-2025` | Yongjing County government, Yellow River-Tao River confluence viewpoint | <https://www.gsyongjing.gov.cn/yjx/zwdt/MTGZ/art/2025/art_6d769761186241bb8c73859dd1dcc83b.html> | Confirms the viewpoint near Longhuishan by Liujiaxia and a dated ticket-and-shuttle operation. River colors, shuttle arrangements, road access, crowding, and opening status require a same-day check. |
| `LZH-REGIONAL-ROUTE-2026` | Gansu culture and tourism department, 2026 travel route | <https://www.gswbj.gov.cn/a/2026/06/17/28621.html> | Current lead for nearby and onward route questions. The book does not copy its itinerary or assume each segment runs daily. |

## Initial Claim Plan

| Chapter | Publishable question | Evidence required before prose is final |
| --- | --- | --- |
| 1 | How does the valley shape ordinary movement? | `LZH-GEO-2026`, `LZH-CITY-PLAN`, current metro geography, and map-coordinate checks. Avoid a precise valley length unless two compatible official definitions agree. |
| 2 | Which arrival gate fits the booked service and hotel district? | `LZH-AIRPORT-T3-2025`, `LZH-NDRC-AIRPORT-2025`, `LZH-METRO-SERVICE`, railway/airport operator checks, and dated booking evidence. |
| 3 | Which changes in crossing and administration are still visible? | `LZH-HISTORY-2020`, local gazetteers for the Chengguan core, streets, gates, Qing administration, railway, and planning, plus `LZH-BRIDGE-HISTORY`. Keep early Jincheng geography explicitly uncertain and stop at the bridge approach. |
| 4 | What is a realistic Yellow River Iron Bridge-White Pagoda Hill Park walk? | `LZH-BRIDGE-HISTORY`, `LZH-RIVER-CORE-2024`, current public-space sources, map measurements, same-day river/access guidance, and field-readable landmarks. |
| 5 | Which museum route gives useful context for a later Gansu trip? | `LZH-MUSEUM`, object-level institutional records, current gallery status, and explicit distinction between findspot and display location. |
| 6 | How does a traveler order and pace meals without turning food into folklore? | `ICH-BEEF-NOODLE`, `LZH-FOOD-2020`, `LZH-FOOD-2026`, `LZH-NOODLE-ORDER-2022`, `LZH-SUMMER-FOODS-2023`, `CNIPA-LANZHOU-LILY-2025`, `GS-SANPAOTAI-2022`, and direct shop confirmation for dietary needs. Chapter accepted on `2026-08-22`. |
| 7 | Which one height fits weather, mobility, and daylight? | `LZH-BAITA-GAZETTEER`, `LZH-BAITA-CURRENT-2025`, `LZH-LANSHAN-RECORD-2025`, `LZH-HEIGHTS-ACCESS-2026`, `LZH-LANSHAN-HOLIDAY-BUS-2026`, `LZH-WUQUAN-HERITAGE-2023`, `LZH-WUQUAN-FLOOD-2026`, current route checks, and no guaranteed-view language. Factual, language, reading, figure, map, B6, and responsive-site gates accepted on `2026-08-22`. |
| 8 | Which district minimizes the traveler's actual transfers? | Current station/metro geography, four dated direct property pages, current foreign-guest registration policy, an original no-hotel-pin segment map, and exact booking boundaries. Factual, language, reading, figure, map, B6, and responsive-site gates accepted on `2026-08-22`. |
| 9 | Can each itinerary be completed with meals, rest, and a usable exit? | Accepted Chapters 1-8, measured map distances, current venue days, and a whole-day fallback rather than added stops. |
| 10 | How much buffer does the next Gansu leg require? | Current railway and airline booking results, station/terminal confirmation, and dated operator notices. No preserved timetable. |
| 11 | Which single nearby day is operationally realistic? | `DHA-BINGLING`, `YJ-YELLOW-TAO-2025`, current Bingling/Liujiaxia operator notices, `LZH-XINGLONG-2024`, `LZH-INK-DANXIA-2026`, weather/closure checks, and conservative return margins. The confluence platform is a Liujiaxia route branch, not a fourth day-trip chain. |

## Rejected Or Deferred Claims

| Claim or pattern | Decision |
| --- | --- |
| “Lanzhou is the only provincial capital through which the Yellow River passes.” | Reject. It is a promotional and definition-dependent uniqueness claim that does not improve a travel decision. |
| One uninterrupted Lanzhou city from Qin or Han administration to the present | Reject. Administrative names, jurisdictions, settlements, and urban footprints changed. Use dated layers tied to visible places. |
| Every important Silk Road route crossed the river at the same Lanzhou point | Reject unless a route-specific historical source proves it. The corridor is not one timeless line. |
| “Jincheng” simply proves an impregnable golden city or one named founding episode | Defer. Present etymology or founding stories only with a responsible historical source and uncertainty label. |
| Huo Qubing crossed the Yellow River at Lanzhou twice on the stated campaigns | Defer. The open guide is not enough, and the claim is unnecessary unless a reliable locator changes an on-site reading. |
| Exact iron-bridge dimensions, imported components, cost, or payment terms | Defer pending reconciliation between `LZH-HISTORY-2020`, local chronicles, and engineering records. The `1909` opening and visible role are enough for the first draft. |
| The visible bridge is wholly unchanged fabric from `1909` | Reject. The current profile includes the five curved upper members added during the `1954` reinforcement; describe the crossing as layered infrastructure. |
| The present White Pagoda and temple precinct can simply be labelled Yuan-period construction | Reject. The garden gazetteer says the first foundation is uncertain, documents ruins before `1448`, and records reconstruction in `1448-1452` plus later work. Preserve that uncertainty. |
| Every terrace, arcade, and pavilion on White Pagoda Hill is an ancient temple survival | Reject. Much of the present park composition and main terrace complex dates to `1958-1960`, while the temple precinct contains older documented layers. |
| All Lanzhou beef-noodle shops are halal, use one recipe, or share one origin | Reject. Verify each shop's practice directly; describe the protected craft without universalizing businesses. |
| A single exact invention date for Lanzhou beef noodles | Treat as recorded tradition unless independent historical evidence supports the date and person. Do not write an origin legend as settled fact. |
| Beef noodles, lily, sanpaotai, or any snack has a medical or longevity effect | Reject without high-quality medical evidence; such claims are irrelevant to the guide. |
| Yellow River carp as an automatic visitor recommendation | Defer. Current legality, sourcing, ecological impact, and restaurant provenance would need reliable evidence. |
| “Lanzhou food is mainly sour and spicy.” | Reject as an unhelpful generalization from a sparse open-guide snapshot. Describe individual dishes and ordering choices. |
| Spring is unsuitable for Lanzhou | Reject. Use long-term climate patterns plus a trip-date forecast, clothing plan, and current warnings. |
| The 2014 airport distance, one-hour transfer, taxi fare, bus route, hotel, restaurant, or venue hours | Reject as current advice. The opening of T3 alone demonstrates why the old logistics cannot be carried forward. |
| A clear skyline, river level, boat service, cableway, or sunset | Never promise. Give a same-day check and a ground-level alternative. |
| Bus `750`, a cableway, taxi pickup, or a Wuquan-Lanshan link is a permanent route | Reject. The cited examples are dated; verify the full ascent and descent on the travel day. |
| Huo Qubing created the five Wuquan springs as a settled historical event | Reject. It is a local tradition and does not improve route decisions; use the spring names only for sign recognition. |
| White Pagoda Hill, Lanshan, and Wuquan Mountain should be completed in one day | Reject. They answer different travel questions; choose one and stop after the planned descent. |
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
| City heights | Site/transport notices, hourly forecast, current map, and confirmed return | Each height offers a different city reading; visibility, paths, vehicles, devices, and closures remain volatile. |
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
