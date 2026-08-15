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
world/countries/<country>
```

Xi'an and Lanzhou are China Cities books. Build one destination at a time,
starting with Xi'an; do not begin Lanzhou until Xi'an passes its complete
editorial and reproducibility gate.

## Xi'an Structure

The Xi'an guide has exactly 11 chapters. This is the complete scope: neither
fewer nor more chapters are needed.

1. First the Land, Then the Dynasties
2. Successive Capitals, Different Sites
3. The Terracotta Army: From Excavation to Formation
4. From the Pagodas to the Forest of Steles: Follow the Written Word
5. Inside the Wall: Four Main Streets and Many Lanes
6. At the Xi'an Table: Begin with Mo
7. Around Xi'an: Give One Place a Day
8. Arriving in Xi'an: Airport, Stations and Transfers
9. Where to Stay: Choose the District First
10. Xi'an in Two, Three or Five Days
11. Before Departure

Chapter 7 is the single nearby-area plan, covering realistic choices among
Huashan, Lintong, Han Yangling, selected Qinling foothills, and western
imperial landscapes. It must help the reader choose one coherent day rather
than present a checklist.

Together the 11 chapters must substantially cover history, food, attractions,
transport, hotels, practical itineraries, cultural context, nearby trips, and
clean legible maps without padding or duplicated chapters.

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

## Visual Standard

- Use vivid, balanced white, vermilion, jade, cobalt, and coral rather than a
  dull yellow or one-note palette. Use restrained highlight bubbles while
  preserving ruby clarity.
- Maps must use large readable labels, clear scale and orientation, minimal
  clutter, accurate provenance, and separate B6/mobile visual checks.
- Reuse source images only after rights and editorial review. Otherwise create
  original high-resolution realistic figures with captions and provenance.
- The recurring guide team is Aya-chan, Lala Xia, Sasa-kun, and the Zhuangzi
  robot. They are four friends and the visual guides shared with the LALACHAN
  travel-video series. The robot has equal narrative status.
- Every non-map figure includes at least Aya-chan and Lala Xia, even when an
  instructional composition might otherwise show only hands, partial people,
  or distant anonymous visitors. Maps do not include the cast.
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

The goal is complete only after all 11 Xi'an chapters, the synchronized website,
cover/branding, maps, figures, citations, language passes, final artifact QA,
repository publication, and pocket-PDF sync have passed this gate.
