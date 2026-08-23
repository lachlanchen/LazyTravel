# Lanzhou Chapter 9 Itinerary Map Specification

Asset ID: `asset-lanzhou-itinerary-days-map`

State: accepted on `2026-08-23` after deterministic regeneration, compiled B6
inspection, and desktop plus independently panned `390 px` website QA.

## Reader Job

At B6 size, the reader must be able to answer four questions without reading
the chapter body:

1. Is the available time one full day, two full days, or three full days?
2. Which single anchor controls each day?
3. Which complete day can move when the museum, weather, or visibility changes?
4. What must remain protected when the route is shortened?

## Composition

- Portrait `5.4 x 7.6 in` master, with vector PDF and SVG plus a `1620 x 2280`
  PNG at `300 ppi`.
- White ground with vermilion, jade, cobalt, and coral route lanes. Avoid a
  yellow cast and avoid thin gray type.
- Header: Chinese title, Japanese title, and compact English title.
- Rule band: `BAGS -> ONE ANCHOR -> SEATED MEAL -> RELIABLE RETURN`, with Chinese
  pinyin and Japanese furigana lines directly below their source labels.
- Three full-width lanes:
  - **One day:** bags and breakfast -> river **or** museum -> one meal -> hotel
    or departure.
  - **Two days:** Day 1 museum west-to-centre -> Day 2 bridge and one hill ->
    exit.
  - **Three days:** preserve Days 1-2 -> Day 3 one hill **or** slow city ->
    exit.
- Each lane includes one dashed fallback band. The fallback replaces a whole
  branch; it is never drawn as an extra stop.
- Bottom decision row distinguishes: suitable outdoor window; heat or cold;
  rain or poor visibility; closure or fixed departure.
- Final cut-order band protects bags, booking, meal/rest, and exit while
  removing optional food, a second street, and the exposed height first.

## Factual Limits

- The diagram is an original editorial decision map. It does not show street
  geometry, walking distance, metro lines, roads, entrances, or journey times.
- “River” means the accepted Zhongshan Bridge-to-White-Pagoda route. “Museum”
  means the accepted Gansu Provincial Museum visit flow. “One hill” means one
  option from the accepted Chapter 7 choice, with a complete checked descent.
- The one-day river and museum branches are alternatives. The `OR` must remain
  visually stronger than their arrows.
- A climate background never stands in for a travel-date forecast. A warning,
  closure, unsafe condition, or operator instruction overrides the map.
- The current museum and transport sources provide check routes, not permanent
  hours or departures.

## Source Inputs

- `data/maps/lanzhou/lanzhou-valley-orientation.config.json`
- `data/maps/lanzhou/lanzhou-arrival-gates.config.json`
- `data/maps/lanzhou/lanzhou-bridge-hill-route.config.json`
- `data/maps/lanzhou/lanzhou-museum-route.config.json`
- `data/maps/lanzhou/lanzhou-food-clock.config.json`
- `data/maps/lanzhou/lanzhou-height-choice.config.json`
- `data/maps/lanzhou/lanzhou-stay-segment.config.json`
- Gansu Provincial Museum visitor guide, checked `2026-08-23`
- China Meteorological Administration Lanzhou climate background, checked
  `2026-08-23`
- Accepted Chapters 1-8 and their source ledgers

The config records immutable hashes for all accepted map inputs. No map tile,
source-guide page, operator diagram, or character reference appears in the
output.

## Acceptance Checks

- every Chinese and Japanese map label has a reading line;
- no text collision or clipping in SVG, PNG, vector PDF, B6 proof, or the
  `390 px` map stage;
- the `OR`, whole-day swap, and cut-order logic remain clear without color;
- the minimum body label remains readable at physical B6 size;
- the website map can be panned without hiding its lower rows;
- provenance hashes match all deterministic outputs;
- all technical detail stays in provenance, while the reader caption explains
  only how to use the map.
