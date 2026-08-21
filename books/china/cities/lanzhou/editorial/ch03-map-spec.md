# Chapter 3 Map Specification

Status: accepted in B6 print and responsive web on `2026-08-21`.

## Reader Question

How can a visitor read Lanzhou's history while moving through the present
centre without mistaking several changing administrative places for one
unchanged ancient city?

## Composition

Build one portrait, character-free map with two visually distinct parts:

1. **Current walk:** a simplified west-east old-city axis from Xiguan through
   Zhangye Road and the City God Temple, with the south approach to Zhongshan
   Bridge shown as the handoff. Former inner gate positions are approximate
   historical anchors, not surviving entrances.
2. **Four layers:** a short vertical key for (a) Han regional administration
   and disputed seat geography, (b) Sui/Tang/Song movement into the later
   Chengguan core, (c) Qing institutional concentration, and (d) bridge and
   railway-era east-west expansion.

The Han layer uses an uncertainty band or separated locator, never an ancient
wall polygon under the current centre. The current route remains the dominant
graphic.

## Required Labels

- 西关 / Xiguan
- 张掖路 / Zhangye Road
- 兰州府城隍庙 / Lanzhou Prefecture City God Temple
- later old-city core / 后来城址
- former east and west gate positions / 旧东、西城门位置
- 中山桥南端 / south bridge approach
- 黄河 / Yellow River
- westward railway/industrial expansion and eastward expansion, shown only as
  broad directional arrows

Chinese labels are primary, with compact Japanese or English support only
where the label remains readable at B6. The four-layer key carries all three
languages in short lines.

## Visual Rules

- Use white, vermilion, jade, cobalt, and coral with dark neutral text.
- Minimum primary-label size must remain readable on a `125 x 176 mm` page and
  within a pannable `390 px` website stage.
- No decorative textures, tiny dynasty lists, pseudo-antique parchment, or
  dense road network.
- No cast, reconstructed historical people, or fake documentary imagery.
- Distinguish current place markers, approximate former gate positions,
  uncertainty, and directional expansion by shape as well as color.
- Include a north arrow and explicit “schematic, not navigation” note. Do not
  include a scale bar unless the route geometry is based on measured current
  coordinates.

## Evidence And Limits

The config records every current coordinate, official/local-gazetteer source,
OpenStreetMap object if used, declared generalisation, output hash, and visual
QA evidence. The map must explicitly state that:

- early Jincheng seat identifications are disputed;
- former gate points are approximate locators derived from the cited
  gazetteer, not surviving structures;
- street and route access are current conditions to verify on site;
- broad expansion arrows are historical interpretation, not administrative
  boundaries or a complete industrial map.

## Acceptance

Pass only after the map is legible in the compiled B6 page and at a `390 px`
viewport, including left, centre, and right pan positions if the website stage
is wider than the viewport. All labels must remain collision-free, and the
uncertainty symbol must be understandable without reading the chapter prose.

Result: pass. The `1620 x 2280` print map is clear on physical page 33. The
website uses a `760 px` stage inside the `390 px` viewport, with reviewed left,
centre, and right captures. The current route, approximate former gates,
disputed Han locator, and all four dated cards remain readable without a label
collision.
