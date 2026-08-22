# Chapter 7 Height-choice Map Specification

Status: accepted at B6 and `390 px` on `2026-08-22`.

Map ID: `lanzhou-height-choice`
Format: portrait schematic, character-free
Decision: choose one height by the view or place needed, then lock the return.

## Spatial Spine

The map keeps only the relationships needed for the choice:

- the Yellow River crosses the upper-middle of the map from west to east;
- Zhongshan Bridge marks the central crossing;
- White Pagoda Hill rises directly from the north-bank bridge route;
- the central city occupies the narrow band south of the river;
- Wuquan Mountain Park sits at the north foot of the southern height;
- Lanshan and Santai Pavilion sit higher and farther south.

This is not a turn-by-turn path map. It must not draw an open through-route
from Wuquan to Lanshan, a step-free path, a guaranteed cableway, a bus line, or
an exact climb. The north-south spacing is generalized so labels remain
legible at B6.

## Three Choices

Each branch has one purpose, one on-site decision, and one stopping point:

1. **White Pagoda Hill:** read the bridge and both banks; decide at the park
   entrance between a lower-terrace turnaround and the pagoda precinct.
2. **Lanshan / Santai Pavilion:** read the long river valley; choose the ascent
   and confirmed return together, then stop after the high viewpoint.
3. **Wuquan Mountain:** read a park-and-heritage landscape; follow only open
   courtyards and spring paths, then return from the park instead of assuming a
   through-climb.

The branch cards use short Chinese, Japanese, and English labels. Full pinyin
and furigana remain in the canonical text rather than being squeezed into the
map.

## Decision Strip

The lower strip asks four questions in order:

`visibility -> weather and surface -> steps or boarding -> confirmed descent`

Any failed check points to `skip the climb / keep the city-level route`. The
diagram never converts rain or poor visibility into a demand to try another
hill.

## Source And Generalization

- White Pagoda Hill and Wuquan Mountain Park use OpenStreetMap park features
  and the official place relationship.
- The Lanshan/Santai anchor uses the read-only open-guide coordinate only as a
  plotting lead, checked against the current Gaolan Mountain and access
  records. It is not a trailhead or entrance coordinate.
- `Tianditu Lanzhou` is the responsible municipal geospatial entry point for a
  live map check. The printed schematic remains independent artwork and does
  not redistribute basemap tiles.
- The config records source URLs, feature IDs or source hashes, coordinate
  roles, retrieval dates, and declared generalization.

## Language And Type

- Chinese is the primary label, Japanese is secondary, and English is a short
  locator.
- Main choice labels target at least `8 pt` in the print raster; warnings and
  support labels target at least `6.4 pt`.
- `白塔山 / 白塔山 / WHITE PAGODA`, `兰山·三台阁 / 蘭山・三台閣 /
  LANSHAN`, and `五泉山 / 五泉山 / WUQUAN` remain visually distinct.
- No label may depend on colour alone, and no label may cross a route line or
  crop edge.

## Palette

Use white paper, dark neutral text, cobalt for the river and route baseline,
vermilion for White Pagoda Hill, jade for Wuquan, and coral for Lanshan. Avoid
yellow wash, gradients, simulated parchment, contour clutter, tiny legends,
and decorative icons unrelated to movement.

## QA Gate

- Deterministic SVG, PDF, and `1620 x 2280` PNG outputs.
- Character-free, sparse, and readable on one B6 page and in the website's
  `390 px` scrollable map stage.
- All three purposes, stops, and the city-level fallback remain visible.
- No exact time, fare, distance, gradient, operation, accessibility, or
  skyline claim is encoded.
- Adjacent provenance records config/source/output hashes, declared
  generalization, and final B6/mobile review evidence.
