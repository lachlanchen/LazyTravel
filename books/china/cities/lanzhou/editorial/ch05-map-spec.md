# Chapter 5 Map Specification

Map IDs: `lanzhou-museum-route`, `lanzhou-museum-findspots`
Format: two portrait schematics, character-free
Decision: follow one downward museum route, then keep each selected object's
findspot distinct from its Lanzhou display and planning context.

## Museum Route

The route map must answer four questions at a glance:

1. What must be checked at the entrance?
2. Which two third-floor galleries form the beginning of the route?
3. Which second-floor gallery completes the core visit?
4. Where can the traveler stop without adding another gallery for completeness?

The page is a flow diagram, not a copied floor plan. It begins on the first
floor, rises once to the third floor, moves through Painted Pottery and
Buddhist Art, descends once to the second-floor Silk Road Civilization gallery,
then returns to the first-floor exit. Paleontology and Red Gansu appear only as
one optional post-route choice. Lift operation, room entrances, queues,
walking times, accessibility, and one-way controls are excluded.

## Findspot Map

The findspot map must make one correction visible: the museum is in Lanzhou,
but the selected objects come from other parts of Gansu. It plots the museum
and six county or city anchors:

- Qin'an for the Dadiwan human-head-mouth painted pottery vessel.
- Gangu for the Xiping salamander-design painted pottery vessel.
- Jingchuan for the Dayun Temple fivefold reliquary.
- Wuwei for the Leitai bronze galloping horse.
- Jiayuguan for the messenger mural brick.
- Dunhuang for the Library Cave silk painting.

The province outline is simplified from OSM relation `153314`. The points are
orientation anchors, not excavation coordinates. No route line, travel time,
or archaeological-site access is implied.

## Language And Type

- Chinese is the largest label, Japanese is secondary, and English is a short
  uppercase locator.
- Main route and legend labels target at least `8 pt` in the print raster;
  supporting lines target at least `6.2 pt`.
- Pinyin and furigana remain in the canonical block text rather than crowding
  either map.
- Both maps must remain readable on a compiled B6 page and in a `390 px`
  website viewport without browser-level zoom.

## Palette

Use white paper, dark neutral text, cobalt for the museum/current check,
vermilion for painted pottery, coral for Buddhist material, and jade for
movement and the Silk Road gallery. Shapes, numbers, and line styles must keep
the categories distinguishable without relying on color alone. No yellow wash,
gradient, or decorative map texture is permitted.

## QA Gate

- Deterministic SVG, PDF, and `1620 x 2280` PNG outputs for both maps.
- No clipped labels or collisions.
- Floor order and the single downward sweep are visually unambiguous.
- Museum and findspot symbols are visually distinct.
- The point legend reconstructs all six object-place relationships without
  implying an onward itinerary.
- Adjacent provenance records source locators, source/config/output hashes,
  generalization, and B6/mobile review evidence.

## QA Result

Passed on `2026-08-22`. Both maps rebuild deterministically as SVG, PDF, and
`1620 x 2280` PNG. The compiled B6 pages preserve every stop and key without a
collision. On the website, portrait maps no longer sit inside a vertically
clipped viewport: the full height remains visible while the `760 px` stage pans
left, centre, and right inside a `390 px` viewport. Desktop, mobile, source,
output, and evidence hashes are recorded in each config and adjacent provenance
file.
