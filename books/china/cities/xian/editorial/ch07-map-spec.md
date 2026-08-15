# Chapter 7 Map Specification: Five One-Day Choices

Status: rendered and visually approved on `2026-08-15`.

## Editorial Purpose

The map answers one decision: which single place deserves the day. It compares
five transport chains around Xi'an without pretending that direction lines are
railways, roads, measured journey times, or live navigation.

## Composition

- Regional extent: `108.05-110.20 E`, `33.86-34.70 N`.
- Central orientation point: Xi'an Bell Tower, not a universal departure point.
- Five numbered choices: Lintong, Huashan, Han Yangling, Cuihuashan, and
  Qianling.
- Each choice has one trilingual focus and one trilingual transport-chain card.
- The Wei River and Qinling band provide regional orientation only.
- Dashed joins indicate direction only; the map contains no live route.
- Maps remain character-free.

## Data And Generalization

- Named-place positions are hash-pinned in
  `data/maps/xian/xian-nearby-day-choices.config.json` from OpenStreetMap,
  ODbL 1.0.
- The Lintong marker is a declared midpoint between the Huaqing Palace and
  Terracotta Army source positions. It is not an entrance or station.
- The Huashan marker uses South Peak for regional orientation; Han Yangling
  uses the museum complex; Cuihuashan uses the named peak; Qianling uses the
  main attraction point.
- Wei River geometry and the Qinling band are explicit schematic features.
- Transport chains are supported by current official attraction or government
  guidance, but times, fares, openings, and bookings stay outside the map.

## Visual And Technical Gate

- Vivid coral, vermilion, cobalt, jade, and magenta distinguish the five
  choices without turning the page into a route-planning dashboard.
- All labels and cards passed inspection at the `5600 x 5040` sRGB master,
  a `1476 px` B6 300 dpi proof, and a `900 px` pannable mobile proof.
- SVG contains selectable text; PDF remains vector; PNG is `5600 x 5040`.
- Label-collision, B6, and `390 px` mobile checks pass.
- Rebuild command:
  `python3 scripts/build_xian_nearby_day_choices_map.py`.
- Provenance:
  `assets/maps/xian/xian-nearby-day-choices.provenance.json`.
