# Chapter 4 Map Specification

Map ID: `lanzhou-bridge-hill-route`
Format: portrait schematic, character-free
Decision: cross Zhongshan Bridge once, then choose the depth of the White
Pagoda Hill visit and one exit.

## Reader Task

The map must answer four questions without pretending to be live navigation:

1. Which bank does the walk begin on?
2. Where does the bridge hand directly into White Pagoda Hill Park?
3. Can the traveler stop at the lower terraces instead of completing the
   climb?
4. Where should one optional riverfront segment branch from the core route?

## Spatial Structure

- North is at the top; the south-bank approach is at the bottom.
- The Yellow River is a strong horizontal cobalt band.
- Zhongshan Bridge crosses it vertically and is the only mandatory crossing.
- White Pagoda Hill rises above the north-bank entry in three stages: entry,
  lower terraces, and pagoda precinct/viewpoint.
- The optional riverfront branch leaves the north-bank entry laterally. It does
  not imply that Waterwheel Park, a boat, or another attraction is included.
- The route is schematic. OSM provides orientation checks for the bridge,
  park boundary, and pagoda position; no road-level turn, exact gradient,
  duration, or accessible route is encoded.

## Numbered Stops

1. South-bank bridge approach and same-day check.
2. Zhongshan Bridge pedestrian crossing.
3. North-bank park entrance and route confirmation.
4. Lower terraces: river-and-bridge reading and a valid turnaround.
5. White Pagoda precinct/viewpoint: full-climb branch only.

## Decision Labels

- `LOWER TERRACES`: shorter visit; still includes the designed bridge-park
  axis; never labelled step-free.
- `FULL CLIMB`: current open path, steps, weather, visibility, and daylight
  must suit the traveler.
- `ONE RIVERFRONT SEGMENT`: optional after the bridge or descent; same-day path
  and river conditions apply.
- `RETURN`: a complete route, not a failure to add another sight.

## Language And Type

- Chinese is the largest route label, Japanese is secondary, and English is a
  compact uppercase locator.
- Main stop labels target at least `8 pt` in the print raster; supporting lines
  target at least `6.3 pt`.
- The title, river, five stop numbers, both hill branches, and the schematic
  disclaimer must remain readable on a compiled B6 page.
- No pinyin or furigana is printed inside the map; the canonical block text and
  caption provide ruby readings without crowding the geography.

## Palette

Use the existing vivid LazyTravel palette: white paper, cobalt river, jade
park, vermilion mandatory route, coral optional branch, and dark neutral text.
No yellow wash, decorative gradients, or low-contrast pastel labels.

## Sources And Generalization

- Bridge way `W223253546`, checked from OSM on `2026-08-21`.
- White Pagoda Hill Park way `W409963603`, checked through Nominatim/OSM on
  `2026-08-21`.
- White Pagoda Temple node `N13318861354`, checked through Nominatim/OSM on
  `2026-08-21`.
- `LZH-BAITA-GAZETTEER` for the bridge-entry-terrace-temple axis.
- `LZH-RIVER-CORE-2024` for dated route and public-space work.
- `LZH-BRIDGE-PEDESTRIAN-2026` for the current pedestrian crossing.

The OSM data is a coordinate check, not a copied basemap. The rendered map is
an original LazyTravel decision diagram. Current gates, route closures,
construction, river conditions, and assisted ascent are deliberately excluded
and must be checked on the day.

## QA Gate

- Deterministic SVG, PDF, and `1620 x 2280` PNG outputs.
- No label collisions or clipped text.
- The mandatory route and optional branch remain visually distinct without
  relying on color alone.
- All five stops and both route-depth choices are readable in B6 print.
- The website map uses a pannable stage at `390 px`; left, center, and right
  captures expose every label without browser-level zoom.
- Adjacent provenance records source locators, output hashes, declared
  generalization, and print/mobile review evidence.
