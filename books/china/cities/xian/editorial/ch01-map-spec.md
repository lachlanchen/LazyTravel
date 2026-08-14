# Chapter 1 Map Specification: Xi'an Before the Walls

Status: approved for first render on `2026-08-14`.

## Editorial Purpose

The opening map must make one argument at a glance: the walled historic core
is a small part of a broader landscape between the Qinling Mountains and the
Wei River system. It is an orientation map, not a route map and not a claim
that every historical capital occupied the same footprint.

## Composition

- Landscape page or full-width spread, designed first for the book's 170 x
  240 mm trim and then reused responsively on the website.
- North at top; no rotated tourist-map perspective.
- Extent approximately `108.35-109.35 E`, `33.78-34.62 N`.
- Show a restrained Qinling foothill band, the Wei River, the seven named
  tributary corridors in the traditional Eight Waters set, the present wall as
  a small outline, and a single current-city label.
- Label rivers in Chinese first, with compact Japanese/English readings in the
  key rather than repeating three labels on every line.
- Use line weight and whitespace, not saturated color, to establish hierarchy.
- Add a visible `SCHEMATIC / NOT FOR NAVIGATION` note in all three languages.

## Data and Generalization

- River names and topology: Shaanxi Provincial Local Gazetteer Office's Eight
  Waters article and Xi'an planning nomenclature.
- River centerlines where mapped: OpenStreetMap contributors, fetched by a
  reproducible script and clipped to the declared extent, ODbL 1.0.
- Minor channels missing or discontinuous in the source data may be shown only
  as generalized corridors. The legend must identify them as generalized;
  their geometry must not be used for navigation or distance measurement.
- The Qinling band is a terrain symbol, not a surveyed ridgeline. It must be
  labelled as such in provenance.
- No basemap tiles, road clutter, business markers, administrative fills, or
  source-book scans.

## Visual System

- Paper: warm white `#F5F2EA`.
- Land/terrain: muted forest `#315347` and soft grey-green `#DDE3DA`.
- Water: clear blue `#237FA3`; Wei River 1.8 pt, tributaries 0.9-1.2 pt.
- Historic-core outline: vermilion `#B44736`, no fill.
- Text: near-black `#202522`; secondary text `#5C625E`.
- No gradients, drop shadows, decorative icons, or pseudo-antique texture.

## Acceptance Gate

1. Chinese river names survive at print size without collisions.
2. The wall remains visibly subordinate to the mountain-river frame.
3. No label crosses another label, line, scale, key, or caption.
4. The SVG has a viewBox and selectable text; the PDF is vector; the PNG is at
   least 2400 px wide for website fallbacks.
5. A 300 dpi print raster and 390 px mobile rendering both pass visual review.
6. Asset metadata records query, snapshot date, ODbL attribution, generalized
   features, dimensions, checksums, and QA decisions.
