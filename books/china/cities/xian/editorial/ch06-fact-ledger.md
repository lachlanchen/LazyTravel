# Chapter 6 Fact Ledger: Eat Xi'an, Beginning With Mo

Ledger date: `2026-08-15`. Destination gate: `china/cities/xian`.

This chapter explains how to choose and order a meal, not how to collect famous
shop names. *Living in Xian* supplies a deliberately fictional day structured
around breakfast soup, roujiamo, liangpi, and an evening bowl of paomo. It is
useful evidence of a popular city-story frame, not evidence for sales volumes,
recipes, opening times, or the claim that one family shop represents the whole
Hui neighborhood. The 2013 family guide and the two open guides identify
familiar dish names and visitor habits, but their rankings, prices, restaurant
lists, origin stories, and operational details are not reused. Provincial food
standards, gazetteers, heritage lists, current municipal records, and clearly
identified editorial judgment control the publishable claims.

## Locked Block Architecture

| Block | Function | Required content |
| --- | --- | --- |
| `ch06-b001` | Opening cultural context | Wheat in Guanzhong; `馍` as a family of breads rather than one object; begin with handling and texture, not a dynasty claim. |
| `ch06-b002` | Map | Four eating contexts inside the wall: Sajinqiao, Hui-lane core, Xiaonanmen/Baoensi Street, and Yongxingfang; no restaurant pins. |
| `ch06-b003` | Paomo | Tuo-tuo mo, breaking the bread, kitchen finish, beef/lamb choice, soup amount, and how to eat without performing expertise. |
| `ch06-b004` | Figure | A realistic table-scale view of two travelers breaking mo before the bowl returns to the kitchen. |
| `ch06-b005` | Roujiamo | White-ji bread and lazhirou; pork is normal in the Han version, while beef/lamb sandwiches belong to different kitchens; ask rather than infer. |
| `ch06-b006` | Liangpi | Wheat and rice families, texture before ranking, sesame and chilli choices, and why `liangpi` is not one standard dish. |
| `ch06-b007` | Noodles | Wide pulled noodles, biangbiang as one member of a larger noodle field, and rejection of a single settled character-origin story. |
| `ch06-b008` | Breakfast | Meatball pepper soup, oil-tea with mahua, zenggao, and the practical value of eating before attraction queues; no fixed vendor hours. |
| `ch06-b009` | Kitchen context | Hui and Han food traditions share the city but are not interchangeable kitchens; halal conduct and the pork boundary for hulutou and lazhirou. |
| `ch06-b010` | Table composition | Dumplings, one substantial starch, vegetables, and sharing choices for two people; avoid an all-starch checklist. |
| `ch06-b011` | Ordering and allergies | Meat, stock, lard, chilli, wheat, sesame, peanut, and soy questions; a translated allergy card for severe allergies. |
| `ch06-b012` | Practical itinerary | One food-led day, queue judgment, rest, and dated checks; districts and dish specialists rather than old-shop rankings. |

The block count is fixed at `12`. A split is allowed only at a real editorial
boundary and must not increase the count; padding, summary repetition, and
source-only continuation pages are prohibited.

## Accepted Claims

| ID | Claim allowed in original prose | Evidence and locator | Durability | Editorial constraint |
| --- | --- | --- | --- | --- |
| `FOOD-01` | Wheat flour is a central staple in Guanzhong and a practical key to reading Xi'an food, but wheat dominance has a history rather than being timeless. | *Shaanxi Provincial Gazetteer: Grain and Oil Industry*, flour-processing section; *Shaanxi Provincial Gazetteer: Agriculture*, crop-history section. | Durable regional pattern | Do not claim every Xi'an meal is wheat-based or turn climate into culinary destiny. Rice, pulses, vegetables, and meat remain visible. |
| `FOOD-02` | `馍` names a field of breads. Paomo uses a firm tuo-tuo mo designed to be broken and cooked; lazhirou roujiamo commonly uses white-ji mo; other breads should not be treated as interchangeable props. | Shaanxi paomo food-standard drafting note; Ministry of Commerce old-brand record for Fanji roujiamo; official local-chronicle paomo process description. | Durable broad distinction | Describe texture and use. Avoid unsupported claims that one present bread is unchanged from Han or Tang recipes. |
| `FOOD-03` | In a conventional beef/lamb paomo meal, the diner breaks the bread before the kitchen finishes it with broth and meat. Terms such as `单走`, `口汤`, `干泡`, and `水围城` describe different bread-and-soup relationships, but usage can vary by shop. | Shaanxi Local Chronicles Office, "Origins of Beef and Lamb Paomo," process section; Shaanxi food-standard drafting note; 2025 heritage-event account showing hand-broken pieces. | Durable process; terminology varies | State the Song-emperor story only as a legend if mentioned at all. Do not grade a visitor's crumb size or imply that hand breaking proves authenticity. |
| `FOOD-04` | A standard lazhirou roujiamo combines white-ji bread with braised pork. Beef or lamb versions are different choices common in halal contexts. The name `肉夹馍` alone does not establish the meat or halal status. | Ministry of Commerce Old-Brand Digital Museum, Fanji, direct history and production sections; Lianhu District Gazetteer, halal foods section. | Durable ingredient distinction | Never translate every roujiamo as a pork sandwich or every shop version as halal. Tell the reader to ask what meat is used. |
| `FOOD-05` | Shaanxi liangpi includes wheat and rice families. The 2025 provincial standard drafting note distinguishes mianpi, ganmianpi, and mipi by grain and process; texture and seasoning differ across them. | *Food Safety Local Standard: Liangpi* DBS61/0011-2025 revision explanation, sections 1.1-1.2; Shaanxi Archives account of sesame liangpi. | Durable category; recipes vary | Do not repeat Qin-dynasty invention stories or describe chilli as compulsory. Sesame, peanut, soy, and gluten questions belong in the order block. |
| `FOOD-06` | Biangbiang mian is a broad, hand-pulled noodle form associated with Guanzhong and represented in the provincial intangible-heritage list. The written `biang` character and its origin stories are not needed to explain the bowl. | Shaanxi Government notice publishing the third provincial ICH list, item VIII-103; Shaanxi Local Chronicles Office, "Eight Oddities," noodle description; open-guide dish lead. | Durable broad form; naming stories unstable | Describe width, chew, sauce, and serving choice. Do not print a definitive stroke count, character etymology, or emperor legend. |
| `FOOD-07` | Breakfast offers a different city rhythm from the evening snack streets. Meatball pepper soup, oil-tea with mahua, zenggao, and simple filled breads are plausible categories, but individual stalls and hours change. | Chinese and English open-guide food sections; *Living in Xian*, sections 4-7, used only as narrative evidence; current municipal coverage naming Xiaonanmen and Sajinqiao as active food areas. | Durable meal pattern; stalls and hours volatile | Avoid calling one combination "the Xi'an breakfast." Do not publish a vendor time unless checked directly near travel. |
| `FOOD-08` | Hui and Han kitchens overlap geographically but keep meaningful ingredient and religious boundaries. Halal beef/lamb paomo and Hui sweets should not be collapsed with pork lazhirou or pork-intestine hulutou. | Lianhu District Gazetteer, mosque and halal-food sections; Xi'an historic-city protection regulations; Ministry of Commerce roujiamo record; Shaanxi Archives hulutou record. | Durable broad boundary | `清真` is a religious food practice, not a visual style or synonym for vegetarian. Do not carry pork food or alcohol into a halal dining room. |
| `FOOD-09` | Dumplings appear in everyday, halal, and banquet settings with different fillings and purposes. A "dumpling banquet" is a designed restaurant format, not proof that every decorative dumpling reproduces ancient court food. | Lianhu District Gazetteer, halal dumpling-banquet section; Chinese and English open guides, dumpling leads. | Durable broad presence; menus volatile | Use dumplings to explain table composition and filling questions, not to construct an ancient origin story. |
| `FOOD-10` | Sajinqiao, the Hui-lane core, Xiaonanmen/Baoensi Street, and Yongxingfang offer four different eating contexts. Yongxingfang is a current curated scenic/food venue; the other areas are mixed urban streets and markets. | Xi'an 2026 A-level scenic-site list; current municipal food-area coverage; pinned OSM positions and present wall geometry; Chapter 5 verified district evidence. | Area identity durable; vendors and operating times volatile | The map is a choice diagram, not a route to complete in one day. Do not pin restaurants, imply every vendor is local, or present a curated venue as an ancient market. |
| `FOOD-11` | A traveler with a severe food allergy should carry a translated allergy card, ask about ingredients, keep prescribed emergency medication accessible, and decline food when the kitchen cannot answer safely. | CDC Travelers' Health, "Allergies and Travel," reviewed 19 August 2022 and checked 15 August 2026; CDC Yellow Book 2026, severely allergic travelers. | Durable health guidance | This is safety guidance, not a guarantee. `少辣`, `不吃猪肉`, `素`, and `清真` do not communicate a severe allergy. Street food is not recommended for a traveler who cannot verify ingredients or cross-contact. |
| `FOOD-12` | A queue proves demand at that moment, not quality, age, hygiene, or suitability. Useful observations are a focused menu, visible turnover, food arriving at the right temperature, and whether the meal fits the day's route. | Original traveler judgment; CDC dining-out guidance for hot/cold holding; stale shop rankings in the family/open guides used as counterexamples. | Durable judgment; venue conditions change | Do not award "best" status, repeat influencer rankings, or turn queue length into evidence of authenticity. |

## Rejected Or Deferred Claims

| Claim | Decision |
| --- | --- |
| Xi'an has eaten the same wheat breads continuously since the Zhou, Han, or Tang. | Rejected. Ancient grain and bread references do not establish continuity with a present recipe. |
| Beef/lamb paomo was invented when Zhao Kuangyin received broth for dry bread. | Rejected as history. It is a named legend in local promotional writing, not a dated origin record. |
| The smaller a visitor breaks the mo, the more authentic or skilled the visitor is. | Rejected. Small pieces affect cooking, but the chapter gives a practical range and follows the shop's instruction. |
| Roujiamo is simply a "Chinese hamburger." | Rejected as the main explanation. It hides the bread, braise, meat question, and distinct local forms. |
| Every roujiamo is pork, or every roujiamo in the Hui neighborhood is halal. | Rejected. Ask the meat and respect the kitchen context. |
| Liangpi is one noodle dish, always wheat-based, always spicy, or invented by Qin Shi Huang's court. | Rejected. Provincial materials distinguish grain and process families; chilli is adjustable. |
| The `biang` character has one official form, exactly one accepted stroke count, or a verified imperial origin story. | Rejected. The chapter needs the noodle, not a calligraphic stunt. |
| "Muslim Street" contains all Xi'an food worth trying. | Rejected. Chapter 5 established a larger living district; Chapter 6 adds other eating contexts without ranking them. |
| A quiet lane is more authentic than a busy street, or an old sign guarantees a better meal. | Rejected. Both are weak proxies and can encourage intrusive behavior. |
| A dumpling banquet recreates Tang court dining. | Rejected unless a specific historical claim is independently documented; the current format is treated as designed restaurant service. |
| A translated allergy sentence makes street food safe. | Rejected. Severe allergy planning requires medication, a card, direct answers, and willingness not to eat. |
| Current restaurant prices, exact market hours, delivery-app rankings, or a list of "best" shops. | Rejected from the durable chapter. Near-travel checks may appear only with a visible date in Chapter 11. |
| Detailed hotel-breakfast or airport/station food advice. | Deferred to Chapters 8-9 because it depends on arrival route and lodging. |

## Language Pass Briefs

- **Chinese:** distinguish `馍`, `饦饦馍`, `白吉馍`, `牛羊肉泡馍`,
  `腊汁肉夹馍`, `凉皮`, `面皮`, `擀面皮`, `米皮`, and `清真`. Avoid
  `碳水天堂`, `舌尖盛宴`, `烟火气拉满`, and copied menu adjectives.
- **Japanese:** use `饃（モー）` once as a category explanation, then retain
  dish names with reviewed readings. Explain ingredients in ordinary Japanese;
  do not replace every item with a misleading familiar Japanese dish name.
- **English:** retain *mo*, *paomo*, *roujiamo*, *liangpi*, and *biangbiang
  mian* after one concrete explanation. Avoid "foodie heaven," "Chinese
  hamburger," "secret recipe," "authentic hole-in-the-wall," and "carb
  overload."

## Visual Evidence Rules

- `asset-xian-food-contexts-map` shows the present wall and four broad eating
  contexts. It contains no restaurant pin, price, opening hour, ranking, or
  route that asks the reader to eat at all four places.
- The map uses pinned OSM coordinates for Sajinqiao road, Dapiyuan/Hui lanes,
  Wumu Gate and Baoensi Street, Yongxingfang, and the Bell Tower. Current
  municipal records support the area labels; the circles remain deliberately
  generalized.
- `asset-xian-breaking-mo-table` shows two ordinary travelers breaking firm mo
  into one shared work bowl before cooking. Hands, crumb size, ceramic bowls,
  whole bread, and table scale must be plausible; no shop identity, ritual,
  waiter, logo, menu text, steam effect, or heritage claim appears.
- Reader-facing captions explain what the action changes in the final bowl.
  Prompt, generation method, checksum, rights, and visual QA remain in project
  provenance rather than interrupting the chapter.

## Citation URLs

- Shaanxi Provincial Gazetteer, grain and oil industry:
  <https://dfz.shaanxi.gov.cn/zslm/fzzlk/xbsxsz/szdylpdf/201404/P020240923622025233209.pdf>
- Shaanxi Provincial Gazetteer, agriculture:
  <https://dfz.shaanxi.gov.cn/zslm/fzzlk/xbsxsz/szdylpdf/201404/P020240923606283686763.pdf>
- Shaanxi food-safety local-standard drafting note, beef/lamb paomo:
  <https://sxwjw.shaanxi.gov.cn/hdjl/dczj/202412/P020241223635101402485.pdf>
- Shaanxi food-safety local standard revision explanation, liangpi:
  <https://sxwjw.shaanxi.gov.cn/hdjl/dczj/202511/P020251103589745415792.pdf>
- Shaanxi Local Chronicles Office, beef/lamb paomo:
  <https://dfz.shaanxi.gov.cn/zslm/zjyd/fzsy/200611/t20061123_2621381.html>
- Ministry of Commerce Old-Brand Digital Museum, Fanji:
  <https://lzhbwg.mofcom.gov.cn/edi_ecms_web_front/thb/detail/f1b29e1774c04ec690cdab178e18f8ba>
- Shaanxi Government, third provincial intangible-heritage list:
  <https://www.shaanxi.gov.cn/zfxxgk/zfgb/2011/d15q_4156/201108/t20110818_1634340.html>
- Shaanxi Archives, sesame liangpi:
  <https://daj.shaanxi.gov.cn/Article/View?id=4474>
- Shaanxi Archives, hulutou paomo:
  <https://daj.shaanxi.gov.cn/Article/View?id=2677>
- Xi'an 2026 A-level scenic-site list:
  <https://www.xa.gov.cn/ztzl/ztzl/lzledc/ywdc/1824366329290301442.html>
- CDC, allergies and travel:
  <https://wwwnc.cdc.gov/travel/page/allergies>
- CDC Yellow Book 2026, severely allergic travelers:
  <https://www.cdc.gov/yellow-book/hcp/travelers-with-additional-considerations/severely-allergic-travelers.html>
