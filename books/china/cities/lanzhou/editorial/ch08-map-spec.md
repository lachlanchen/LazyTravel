# Lanzhou Chapter 8 Map Specification

Asset: `asset-lanzhou-stay-segment-map`
Snapshot date: `2026-08-22`

## Reader Task

The reader must be able to choose a lodging segment at B6 size without treating
the diagram as navigation or a hotel ranking. The diagram answers:

1. Which city segment contains the arrival gate or first fixed stop?
2. Is the night in the west, centre, east, or airport area?
3. Which cross-city movement disappears when that segment is chosen?

## Composition

- Draw Lanzhou as one long east-west city band below a simple Yellow River
  line. Use three large, equally legible segments: west, centre, and east.
- Put the airport in a separate northern inset with a broken connector and an
  explicit `not to scale` label.
- Give each city segment only two recognition anchors:
  - west: Lanzhou West and Gansu Provincial Museum;
  - centre: Xiguan and Zhongshan Bridge;
  - east: Dongfanghong Square and Lanzhou Station.
- Put four decision cards below the orientation band. Each card gives one
  arrival or morning reason and one boundary.
- End with the same rule in all three languages: choose the segment first, then
  verify the property.

## Exclusions

- No hotel pin, logo, rate, ranking, review score, star category, or room image.
- No road, metro line, airport rail path, exit number, travel time, walking
  distance, or claim of a direct connection.
- No exact district boundary. The colored spans are editorial route segments.
- No cast. Maps remain character-free.
- No implication that the airport inset shares the city band's scale.

## Visual Gate

- `1620 x 2280` PNG for 300 dpi B6 review, plus SVG and PDF.
- Large Chinese, Japanese, and English labels with no collision or clipped text.
- Vivid vermilion, jade, cobalt, and coral accents on white; no yellow wash.
- At `390 px`, the independently pannable map stage must retain readable
  anchors, all four choices, the not-to-scale note, and the final rule.
- Approval requires compiled B6 and real mobile-page evidence; config status
  remains unapproved until those screenshots have been inspected.

## Acceptance

Accepted on `2026-08-22`. The final B6 proof is physical page `113`; the
responsive proof uses an independently pannable `760 px` stage inside a
`390 px` viewport. Both preserve the four choices, large trilingual labels,
not-to-scale airport boundary, and arrival-to-first-stop rule without a false
route, hotel pin, collision, or clipping. Exact evidence paths and hashes are
recorded in the map config and adjacent provenance file.
