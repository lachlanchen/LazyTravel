# Chapter 2 Arrival Gate Map Specification

Status: built and visually accepted on `2026-08-21` in B6 print and at a
`390 px` website viewport.

## Reader Question

Which exact gate is printed on the booking, which city segment comes next, and
where is a change of mode required?

## Visible Hierarchy

1. Three large, non-interchangeable gate cards: Zhongchuan Airport T3 with
   Zhongchuan Airport East Railway Station, Lanzhou West Railway Station with
   Lanzhou West Station North Square metro, and Lanzhou Railway Station with
   Lanzhou Railway Station metro.
2. One west-centre-east city spine using Gansu Provincial Museum, Xiguan and the
   central bridge approach, Dongfanghong Square, and Lanzhou University as
   segment anchors.
3. Airport branches labelled rail, airport coach, and road pickup. Every branch
   says to check live operation; none carries a time or fare.
4. Line 1 and Line 2 shown only as schematic city links. The airport remains in
   a separate panel explicitly marked as not to city scale.
5. A three-step footer: read the ticket, place the first stop, keep a fallback.

No hotel, restaurant, train number, platform, terminal door, exact exit,
frequency, fare, journey time, anonymous person, or guide character appears.

## Data Boundary

- Central-city relationships reuse the accepted Chapter 1 map configuration
  and current Lanzhou Rail Transit station sequence.
- Airport/GTC relationships use `LZH-NDRC-AIRPORT-2025` and
  `LZH-AIRPORT-RAIL-2026`; the airport panel is schematic and not drawn to the
  same scale as the city spine.
- National-rail service is represented as a booked gate, not by route lines.
  The exact service remains a 12306 check.
- Metro colors follow the existing LazyTravel Lanzhou map, not an attempt to
  reproduce every element of the operator diagram.

## Print And Mobile Contract

- Portrait composition sized for a full B6 page, exported as SVG, vector PDF,
  and at least `1800 px` on the long raster edge.
- Gate names use at least `9 pt` source type; secondary branch labels use at
  least `7 pt`.
- White base with vermilion, jade, cobalt, and coral. Each gate has a distinct
  shape as well as color, so the decision survives grayscale and small screens.
- A `390 px` proof must show all three gate names and the footer without zoom.
  Optional zoom may reveal secondary labels but must not be required for the
  primary decision.
- The B6 proof must preserve the airport scale warning, the two different metro
  station names, and the no-timetable language.
