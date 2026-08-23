# Lanzhou Chapter 10 Onward Map Specification

Asset ID: `asset-lanzhou-onward-gates-map`

State: editorial structure and deterministic render locked on `2026-08-23`;
B6/mobile QA pending.

## Reader Job

At B6 size, the reader must be able to answer five questions:

1. Which exact station or terminal is printed on the live booking?
2. In which city will the reader sleep next?
3. Where are the bags, and when must checkout finish?
4. Which station or terminal margin still has to be protected?
5. What is removed first when that margin shrinks?

## Composition

- Portrait `5.4 x 7.6 in` master, with SVG and vector PDF plus a
  `1620 x 2280` PNG at `300 ppi`.
- White ground with vermilion, jade, cobalt, and coral. No yellow cast, route
  tile, dense legend, or small gray paragraph text.
- Header: Chinese, pinyin, Japanese, furigana, and compact English title.
- Top rule band: choose the next overnight city, then read the departure point
  on the live booking.
- Three mutually exclusive lanes selected by that booking:
  - **Lanzhou West:** next overnight city -> bags and checkout -> printed
    station -> inside-station margin.
  - **Lanzhou Station:** the same four decisions, kept separate so the eastern
    station cannot be substituted for Lanzhou West.
  - **Zhongchuan T3:** next overnight city -> city or airport-area night ->
    confirmed T3 transfer -> terminal margin.
- No destination branches, timetable, rail direction, or implied direct
  service. Wuwei, Zhangye, Jiayuguan, and Dunhuang belong in the prose as
  separate overnight decisions.
- Bottom pair: what must remain and what is cut first. The valid booking,
  documents, bags, checks, and rest remain; the final sight, shopping detour,
  or tight dinner goes first.

## Factual Limits

- The map is an original editorial decision diagram. It does not show railway
  geometry, roads, metro service, airport-rail timing, distance, duration,
  fares, train classes, flight routes, platforms, or boarding gates.
- It prints no destination list and makes no direct-service claim.
- Lanzhou West, Lanzhou Station, and Zhongchuan T3 are alternatives selected by
  the live booking. Direction and vehicle type never override the printed
  station or terminal.
- Warnings, cancellations, schedule changes, station notices, and operator
  instructions override the diagram.

## Source Inputs

- `data/maps/lanzhou/lanzhou-valley-orientation.config.json`
- `data/maps/lanzhou/lanzhou-arrival-gates.config.json`
- `data/maps/lanzhou/lanzhou-stay-segment.config.json`
- `data/maps/lanzhou/lanzhou-itinerary-days.config.json`
- China Railway 12306 live booking and boarding guidance, checked `2026-08-23`
- Lanzhou Railway Bureau 2026 summer-operation report, checked `2026-08-23`
- T3 and integrated-transport sources already accepted in Chapter 2
- Accepted Chapters 2, 8, and 9 and their source ledgers

The config records immutable hashes for every accepted map input. No source
map tile, operator diagram, source-guide page, or character reference appears
in the output.

## Acceptance Checks

- every Chinese and Japanese map label has a reading line;
- the three departure points cannot be mistaken for one another;
- no lane reads as a continuous multi-city itinerary or promised service;
- no text collision or clipping in SVG, PNG, vector PDF, B6, or the independently
  panned `390 px` website stage;
- the decision remains clear without color;
- provenance hashes match every deterministic output;
- reader-facing caption explains use, while technical limits remain in
  provenance.
