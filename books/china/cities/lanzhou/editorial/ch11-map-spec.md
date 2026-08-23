# Lanzhou Chapter 11 Nearby-day Map Specification

Asset ID: `asset-lanzhou-nearby-day-map`

State: accepted on `2026-08-23` after deterministic-render, B6, desktop, and
independently panned `390 px` review.

## Reader Job

At B6 size, the reader must be able to answer six questions:

1. Which one of the three nearby branches is being considered?
2. Is one complete outward and return method confirmed?
3. Is the attraction entrance and internal movement confirmed for that day?
4. Does the return still have a named operator and protected margin?
5. Is the Yellow-Tao confluence only a separately confirmed road branch?
6. Which failure cancels the whole branch and sends the reader back to a
   checked Lanzhou city fallback?

## Composition

- Portrait `5.4 x 7.6 in` master, with SVG and vector PDF plus a
  `1620 x 2280` PNG at `300 ppi`.
- White ground with vermilion, jade, cobalt, and coral. No yellow cast, basemap,
  dense legend, road geometry, or small gray paragraph text.
- Header: Chinese, pinyin, Japanese, furigana, and compact English title.
- Top rule band: protect the return, then choose one of three branches.
- Three mutually exclusive horizontal lanes:
  - **Bingling-Liujiaxia:** choose one water or road return, confirm entry and
    the caves open that day, then retain a named return operator and time.
    A separate coral strip nests the Yellow-Tao viewpoint under this lane only
    when road access, platform operation, and the return all fit.
  - **Xinglong:** mark the whole lane as `DIRECT REOPENING CHECK`. Confirm the
    open entrance, usable S104 section, visitor route, ascent, descent, and
    return before it can become an itinerary.
  - **Ink Danxia:** confirm the day's opening and weather response, open
    boardwalk or internal transport, exit route, and return to Lanzhou.
- Bottom band: one broken link removes the entire branch; use a previously
  checked Lanzhou city fallback instead of another nearby branch.

## Factual Limits

- The map is an original editorial decision diagram. It is not a road,
  topographic, boating, shuttle, attraction, or accessibility map.
- Arrows show verification order, not distance, duration, direction, elevation,
  boarding sequence, or a guaranteed connection.
- No timetable, fare, ticket, phone number, opening time, boat, road, shuttle,
  trail, platform, vehicle, weather, or capacity is preserved.
- The confluence platform is not shown as part of a Bingling boat ticket.
- Xinglong's lane is not an open-status claim. It remains conditional until a
  complete reopening and return are confirmed directly.
- Current site, transport, public-safety, weather, and road notices override the
  diagram.

## Source Inputs

- `books/china/cities/lanzhou/editorial/ch11-fact-review.md`
- `data/maps/lanzhou/lanzhou-valley-orientation.config.json`
- `data/maps/lanzhou/lanzhou-itinerary-days.config.json`
- Dunhuang Academy and current Linxia Bingling route and safety channels
- Yongjing County's dated confluence operating report
- current Lanzhou, Gansu transport, and tourism recovery sources for Xinglong
- current Gansu culture and tourism and weather-closure sources for Ink Danxia

The config records immutable hashes for accepted local inputs. No map tile,
operator diagram, source-guide page, official photograph, or character
reference appears in the output.

## Acceptance Checks

- every Chinese and Japanese map label has a reading line;
- the three branches cannot be read as a circuit or same-day chain;
- the confluence strip is visibly subordinate to Bingling-Liujiaxia;
- Xinglong cannot be mistaken for a current reopening recommendation;
- no text collision or clipping in SVG, PNG, vector PDF, B6, or the independently
  panned `390 px` website stage;
- the decision remains clear without color;
- provenance hashes match every deterministic output;
- reader-facing caption explains use, while technical limits remain in
  provenance.

## Acceptance Evidence

- SVG SHA-256: `4115e162602011776251ec7bb6ccd0cb04af27ec7e2d7cdc5ae9ba9c3ad81a22`.
- Vector PDF SHA-256: `9dc179c127f7d09ee7e6c9608e3df4ffb9291b87d34955cbdf3ee02ce144ab7b`.
- `1620 x 2280` PNG SHA-256:
  `1ecbd5420c3308135c61c8160baab5fabfaba06f402bae6a259437fae6b63cba`.
- The compiled `300 ppi` B6 map on physical page `181` has SHA-256
  `692d79ec5973d1a3d10f2e690d5dedfd960eae22fed32c6d50687de14d0cee6b`.
- Desktop plus left, centre, and right `390 px` inspections preserve all three
  complete-return branches, the subordinate confluence condition, the
  Xinglong reopening guard, and the cancellation band without clipping.
