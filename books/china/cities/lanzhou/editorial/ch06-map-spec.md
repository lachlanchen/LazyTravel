# Chapter 6 Diagram Specification

Diagram IDs: `lanzhou-noodle-order`, `lanzhou-food-clock`
Format: two portrait decision diagrams, character-free
Decision: make one confident morning order, then let appetite and the day's
route choose a single afternoon branch.

## Noodle Order

The first diagram answers five questions at a glance:

1. Where does the traveler begin if the shop uses a ticket or counter?
2. Which noodle-width words are useful to recognise?
3. Which additions are separate decisions?
4. Where is the bowl collected?
5. Which part of the sequence may differ in the actual shop?

It is a service-flow diagram, not a shop plan. The main sequence is
`pay or collect ticket -> state noodle shape -> request optional additions ->
collect bowl -> season and sit as directed`. A side panel groups sample signs
from fine to broad: `毛细 / 细 / 三细 / 二细`, then `韭叶`, `宽 / 大宽`.
No millimetre scale, price, queue time, mandatory condiment, or promise that
all names appear in every shop is encoded.

## Food Clock

The second diagram uses four broad phases rather than exact hours:

- **Morning:** eat the beef-noodle bowl while the shop is in its natural
  breakfast rhythm.
- **Midday:** reset with water, walking, or the day's main attraction instead
  of ordering another item immediately.
- **Afternoon:** choose either one snack among `酿皮子`, `灰豆子`, and
  `甜醅子`, or a quiet lily and `三炮台` stop when the setting suits.
- **Evening:** stop the list and eat according to appetite, location, and
  verified dietary needs.

The clock is not an opening-hours chart. It must not imply that all products
are available in every phase, that every traveler should eat them, or that one
precise schedule applies throughout the year.

## Language And Type

- Chinese is the largest label, Japanese is secondary, and English is a short
  uppercase locator.
- Main decisions target at least `8 pt` in the print raster; supporting notes
  target at least `6.4 pt`.
- Pinyin and furigana remain in the canonical block text instead of crowding
  either diagram.
- Both diagrams must remain readable on a compiled B6 page and in a `390 px`
  website viewport without browser-level zoom.

## Palette

Use white paper, dark neutral text, vermilion for the morning bowl, cobalt for
service actions, jade for pause or choice, and coral for tea and the stopping
rule. Use line style, numbering, and shape as well as colour. No yellow wash,
gradient, simulated paper texture, or decorative food icon field is allowed.

## QA Gate

- Deterministic SVG, PDF, and `1620 x 2280` PNG outputs for both diagrams.
- No clipped labels, collisions, tiny legends, or text rendered as raster
  decoration.
- The five counter decisions remain unambiguous while the variation warning is
  visually prominent.
- The day clock shows broad phases, one afternoon branch, and a visible stop;
  it cannot read as an exact timetable or completion challenge.
- Adjacent provenance records source locators, source/config/output hashes,
  generalisation, and B6/mobile review evidence.

## QA Result

Both diagrams passed on `2026-08-22`. Their SVG, PDF, and `1620 x 2280` PNG
outputs rebuild deterministically. The compiled pocket pages are physical pages
`82` and `85`; all primary labels, warnings, and branches remain legible at B6.
The responsive site uses a `760 px` scrollable stage at a `390 px` viewport;
left, centre, and right captures preserve the full service flow, noodle-shape
panel, afternoon alternatives, and missed-morning fallback without collisions.
