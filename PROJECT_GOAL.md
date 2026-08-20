# LazyTravel Project Goal

## Product

Publish an original, professional multilingual travel series under LazyTravel
and lazying.art, with the project repository at
<https://github.com/lachlanchen/LazyTravel>. Each destination has one canonical
aligned Chinese, Japanese, and English JSON source that produces both a clean
B6 pocket book and a polished responsive website.

The series is organized as:

```text
china/cities/<city>
japan/prefectures/<prefecture>
japan/prefectures/<prefecture>/<city-or-area>
world/countries/<country>
```

Xi'an and Lanzhou are China Cities books. Hakone is a Kanagawa destination at
`japan/prefectures/kanagawa/hakone`. Build one destination at a time in this
order: Xi'an, Hakone, then Lanzhou. Xi'an has passed its complete gate; do not
begin Lanzhou until Hakone has passed the same gate.

## Xi'an Structure

The Xi'an guide has exactly 11 chapters. This is the complete scope: neither
fewer nor more chapters are needed.

1. Start with the Map: Qinling, the Wei, and the Wall
2. The Capitals Moved: Choosing Which Sites to Visit
3. A Half Day at the Terracotta Army: Excavation Before Formation
4. Pagodas to Beilin: Follow the Written Word
5. Half a Day Inside the Wall: Towers, Hui Lanes, and Side Streets
6. How to Eat in Xi'an: Begin with Mo
7. Around Xi'an: Give One Place a Day
8. Arriving in Xi'an: Airport, Stations and Transfers
9. Where to Stay: Choose the District First
10. Xi'an in Two, Three or Five Days
11. Before Departure: Bookings, Weather, and On-site Rules

Chapter 7 is the single nearby-area plan, covering realistic choices among
Huashan, Lintong, Han Yangling, selected Qinling foothills, and western
imperial landscapes. It must help the reader choose one coherent day rather
than present a checklist.

Together the 11 chapters must substantially cover history, food, attractions,
transport, hotels, practical itineraries, cultural context, nearby trips, and
clean legible maps without padding or duplicated chapters.

## Hakone Structure

The Hakone guide also has exactly 11 chapters. Its route is one mountain
crossing rather than a catalogue of sights:

1. Read the Mountain First: Caldera, Lake, and Elevation
2. Odawara to Yumoto: Make Transfers Part of the Day
3. Climb to Gora: Grade, Art, and Time to Stop
4. Cross Owakudani: See the Volcano Before Fuji
5. Lake Ashi: Shrine, Wakasagi, and Shore
6. Old Tokaido and the Checkpoint: Walk the Road, Read the System
7. One Night in an Onsen Ryokan: Bathing, Dinner, and Quiet
8. Eat Along the Route: Black Eggs, Amazake, and the Dinner Clock
9. Where to Stay: Choose a District Before a Property
10. One, Two, or Three Days: Leave Room for Weather
11. One Stop Beyond Hakone: Odawara, Mishima, or Gotemba

Together they cover terrain, volcanic and road history, current attractions,
transport, food, onsen culture, hotels, practical itineraries, and one nearby
continuation chapter. The detailed trilingual spine and boundaries are locked
in `books/japan/prefectures/kanagawa/hakone/editorial/outline.md`.

## Editorial Standard

- Use all six supplied books, the external Xi'an and Gansu open guides, and
  `XIAN_GANSU_TRAVEL_GUIDES_2026-08-14.md` as research evidence.
- Reuse inspected `../ZhJpBook/pdf2tex` extraction and figure-manifest patterns
  safely, without copying source archives or publishing raw extraction.
- Give the book its own structure, observation, traveler judgment, and voice.
  Do not copy or closely paraphrase source prose.
- Fact-check claims, record locators, distinguish durable history from
  time-sensitive advice, and attribute maps and images.
- Perform separate Chinese, Japanese, and English editorial passes so each
  language reads naturally. Avoid embarrassing, strange, formulaic, or
  conspicuously generated phrasing.
- Keep Chinese pinyin and Japanese furigana as reviewed ruby throughout the
  pocket book and website.
- Favor useful detail, narrative continuity, cultural nuance, and realistic
  decisions for ordinary travelers. Write efficiently, but do not skip factual,
  language, visual, or page-level review.
- Keep one explicit travel-guide line: first help the reader choose and move;
  then use the history and food behind actual places to make the visit richer.
  Do not mix eras to manufacture a story or let contextual history take over
  the trip.
- Spend review time on facts, language, route usefulness, and visible layout
  faults. Do not loop on micro-details that do not change accuracy, legibility,
  reproducibility, or the reader's decision.

## Visual Standard

- Use vivid, balanced white, vermilion, jade, cobalt, and coral rather than a
  dull yellow or one-note palette. Use restrained highlight bubbles while
  preserving ruby clarity.
- Maps must use large readable labels, clear scale and orientation, minimal
  clutter, accurate provenance, and separate B6/mobile visual checks.
- Reuse source images only after rights and editorial review. Otherwise create
  original high-resolution realistic figures with captions and provenance.
- For Hakone and later books, use the AgInTi image-generation route for new
  raster figures when available. Codex remains responsible for the visual
  brief, factual boundaries, provenance, selection, and B6/mobile QA.
- Attraction-led chapters must include an attraction-dominant view at a useful
  scale. Aya-chan and Lala Xia may establish traveler scale in the foreground,
  but the destination remains the main subject; instructional scenes do not
  count as substitutes for showing the place.
- The recurring guide team is Aya-chan, Lala Xia, Sasa-kun, and the Zhuangzi
  robot. They are four friends and the visual guides shared with the LALACHAN
  travel-video series. The robot has equal narrative status.
- Every new non-map figure includes exactly Aya-chan, Lala Xia, Sasa-kun, and
  the Zhuangzi robot, even when an instructional composition might otherwise
  show only hands, partial people, or distant anonymous visitors. Maps do not
  include the cast.
- Distribute substantial location views through the guide so major places are
  recognizable before the reader arrives. The destination must still dominate,
  and repeated views must not clutter the pocket edition.
- The patchwork notebook, LightMind glasses, and word-card device are recurring
  travel tools. Use cast and props smoothly, only where they strengthen the
  guide content; never turn the book into a character catalogue or product ad.
- Do not burden reader-facing captions with generation notes. Keep production
  method, reference hashes, rights, limitations, and visual QA in technical
  provenance.

## Acceptance Gate

A destination milestone is accepted only when:

- canonical JSON and schemas validate;
- Chinese pinyin and Japanese furigana reconstruct the source text and have
  passed human review;
- every claim is cited or tracked in a fact ledger, with volatile facts dated;
- all maps and figures have approved provenance and B6/mobile visual QA;
- the B6 LaTeX PDF builds reproducibly with correct trim, embedded fonts,
  searchable text, clean logs, and page-by-page review;
- the website builds from the same JSON, passes content parity, responsive
  navigation, ruby, map/figure, citation, and desktop/mobile checks;
- only the verified pocket PDF is hash-synced to Nutstore; and
- the coherent milestone is committed and pushed to GitHub.

A destination is complete only after every planned chapter, the synchronized
website, cover and branding, maps, figures, citations, language passes, final
artifact QA, repository publication, and pocket-PDF sync have passed this
gate. A chapter milestone does not complete a destination, and completing one
destination does not open work on two later books at once.

## Current Gate

As of `2026-08-21`, all 11 Xi'an chapters have passed editorial, reading, page,
and public website review and build reproducibly as one `195`-page B6
pocket PDF from `125` aligned blocks, with ten maps and fifteen chapter
figures. The text-free four-guide cover sits beneath selectable LaTeX text, and
the synchronized website passes the same JSON, ruby, asset, citation, desktop,
and mobile gates. The public guide is available at
<https://lachlanchen.github.io/LazyTravel/>. Hakone is the next active book;
Lanzhou remains queued behind it.

Hakone has a locked 11-chapter structure. Chapters 1 through 10 have passed the
editorial, reading, PDF-page, website, Nutstore, and GitHub milestone gates.
The current pocket review has `193` B6 pages and SHA-256
`50154ec40d8cd77850e44f25ccf6c3cc376d114909f85d6d6d10c7b06dca7d30`.
It contains `97` aligned blocks, ten maps, thirty-five figure placements, and
the website renders `16,770` reviewed ruby nodes from the same JSON. Hakone
remains incomplete; Chapter 11, **One Stop Beyond Hakone**, is the only next
production gate.
