# Chapter 1 Orientation Map Specification

Status: locked for first render on `2026-08-21`.

## Reader Question

Before choosing transport, where is the next stop relative to the river,
east-west direction, and the three arrival gates?

## Visible Hierarchy

1. Yellow River, west-to-east arrow, north bank, and south bank.
2. White Pagoda hill band to the north and Gaolan/Lanshan hill band to the
   south, both explicitly marked as schematic orientation bands.
3. Seven large anchors: Lanzhou West, Gansu Provincial Museum, Xiguan,
   Zhongshan Bridge/White Pagoda approach, Dongfanghong Square, Lanzhou
   University, and Lanzhou Railway Station.
4. Current Line 1 corridor and Line 2 connection as schematic links using the
   operator's station names.
5. A separate northward airport inset labelled “not to central-map scale.”

No restaurants, hotels, minor streets, prices, times, attraction ratings, or
anonymous people appear. The map contains no guide characters.

## Data Boundary

- Extent: first-visit core from Lanzhou West through the Lanzhou
  University/Railway Station side, not the whole municipality.
- River: OpenStreetMap way `166825103`, clipped and rounded to six decimals.
- Anchors: pinned OpenStreetMap object IDs and coordinates in the committed
  configuration.
- Metro station sequence: Lanzhou Rail Transit `serve.js`, checked
  `2026-08-21`; lines are generalized between selected nodes.
- Hill bands: disclosed editorial symbols derived from the official
  river-between-two-hills description, not topographic data.
- Airport: directional inset only. The central panel and inset use different
  scales.

## Print And Mobile Contract

- Landscape `7 x 4.95 in` source composition, exported as SVG, vector PDF, and
  `2100 x 1485 px` PNG.
- White base with vermilion, jade, cobalt, and coral; river remains cobalt and
  the hill bands use two distinct restrained greens.
- Primary labels at least `8 pt` in the source composition; no translucent text
  over a busy layer.
- Mobile proof at `390 px` must retain all primary labels without collisions.
- B6 print proof at `300 ppi` must retain the river arrow, bank labels, legend,
  scale warning, and airport inset.
