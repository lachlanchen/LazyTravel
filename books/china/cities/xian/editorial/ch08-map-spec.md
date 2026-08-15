# Chapter 8 Map Specification: Four Arrival Hubs

Status: rendered and visually approved on `2026-08-16`.

## Editorial Purpose

The map answers the first arrival question: which hub is this, and which line
or signed pickup area matters next? It does not replace the current official
metro diagram, a timetable, a road map, or live navigation.

## Composition

- Regional extent: `108.72-109.09 E`, `34.16-34.48 N`.
- Four numbered hubs: Xi'an Xianyang International Airport, Xi'an North,
  Xi'an Station, and Xi'an East.
- Only Lines `14`, `2`, `4`, and `5` appear, because they alter the first
  cityward decision described in the chapter.
- The walled core and Wei River are orientation anchors, not route geometry.
- Four trilingual cards state one decision at each hub.
- Maps remain character-free.

## Data And Generalization

- Hub and central-anchor positions are pinned to named OpenStreetMap objects
  in `data/maps/xian/xian-arrival-hubs.config.json`, under ODbL 1.0.
- Line relationships are controlled by the current official Xi'an metro
  diagram; line strokes are declared schematic coordinates.
- Airport terminal paths, Xi'an North plaza choice, Xi'an Station's wall-side
  orientation, and Xi'an East's 2026 Line 5 connection are controlled by the
  cited airport, municipal, railway, and transport guidance.
- No line length encodes journey time, fare, service frequency, or an exact
  walking route.

## Visual And Technical Gate

- Coral, cobalt, vermilion, and jade separate the four hubs and first-transfer
  spines while keeping the page legible rather than decorative.
- The `5600 x 5040` sRGB PNG master, selectable-text SVG, and vector PDF
  regenerate byte for byte.
- B6 300 dpi, `390 px` mobile zoom, and label-collision checks pass.
- PNG SHA-256:
  `0bfb8bd74db2ba426df8a7a94a3060e740821ff0cc0ba8d6b21f0e218cecd1a3`.
- B6 proof SHA-256:
  `9be921eb5d68c28d580e1c0248deb0e56914b61705ae641d6679e960b6f7814c`.
- Mobile zoom proof SHA-256:
  `8fe51c3193921225b7c1fc75d771ca73746f5f5490068f2fbbf27814b08e1d48`.
- Rebuild command: `python3 scripts/build_xian_arrival_hubs_map.py`.
- Provenance: `assets/maps/xian/xian-arrival-hubs.provenance.json`.
