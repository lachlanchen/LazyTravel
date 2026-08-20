# Project Memory

This file stores durable production decisions, not chat transcripts, Codex
history, rollout data, or session backups.

## What Has Proven Useful

- Canonical aligned JSON prevents the pocket book and website from drifting.
  Reading arrays must reconstruct the exact Chinese/Japanese text before layout
  review begins.
- A chapter is manageable when it has one factual ledger, one language review,
  one reading review, focused tests, a reproducible build, and page/site QA.
- Source structure and figures can be inventoried safely with the inspected
  ZhJpBook queue, OCR routing, immutable hashes, and figure-manifest patterns.
  Extracted source prose remains evidence, never publishable copy.
- Generalized choice maps are more useful than dense restaurant-pin maps in a
  pocket guide. Primary labels must survive both B6 print and a 390 px viewport.
- A pannable mobile map must scale its CSS minimum width as well as its
  percentage width; otherwise the first zoom step can appear to do nothing.
- Time-sensitive transport, hotel, ticket, opening-hour, and business details
  need a check date and an official confirmation route close to travel.
- The strongest prose explains what to notice, what a distinction changes for
  the traveler, and where uncertainty remains. Empty scene-setting and repeated
  conclusions are removed.
- The book's main line is the traveler's decision sequence. Places and routes
  lead; history and food explain what is visible there. A reader should never
  have to infer that this is a travel guide from historical prose.
- Review effort stops when a detail no longer changes accuracy, naturalness,
  route usefulness, legibility, or reproducibility. Progress to the next
  chapter instead of reopening settled micro-details.

## Stable Visual Identity

- Palette: white base with vermilion, jade, cobalt, and coral accents; no dull
  yellow cast and no single-hue page system.
- Guide team: Aya-chan, Lala Xia, Sasa-kun, and the Zhuangzi robot. They are four
  friends shared with the LALACHAN travel-video series. The robot is a guide,
  not a prop.
- Hard figure rule: every new non-map figure contains exactly Aya-chan, Lala
  Xia, Sasa-kun, and the Zhuangzi robot. No fifth traveler, duplicate guide, or
  anonymous replacement is allowed; maps stay character-free.
- Recurring tools: patchwork notebook, LightMind glasses, and word-card device.
  They support a scene only when useful and must remain visually secondary.
- Character scenes use tactile, realistic editorial miniature photography that
  preserves each supplied design. Historical or archaeological evidence stays
  clearly documentary/schematic and does not use the guides as eyewitnesses.
- Technical provenance records reference paths, hashes, rights, generation
  method, factual limits, and visual QA. Reader captions describe the travel
  subject rather than the production process.
- For Hakone and later destinations, AgInTi is the default raster-figure
  generator. Codex prepares the factual visual brief and performs selection,
  provenance, B6 proof, and mobile proof; generation notes remain technical.
- Attraction-led chapters need attraction-dominant views, with Aya and Lala as
  traveler-scale guides rather than the primary spectacle. Existing
  instructional figures remain useful but do not satisfy that need by
  themselves.
- New location plates use the full four-guide team when B6 legibility allows.
  The complete 11-chapter visual route now includes Yongning Gate, Pit 1, the
  Big Wild Goose Pagoda, the City Wall, the Bell Tower, food practice, a
  managed mountain day, Xi'an North, a South Gate hotel arrival, and a Small
  Wild Goose Pagoda route morning, and the four-guide departure table rather
  than relying on generic character scenes. The cover is a text-free four-guide
  city-wall underlay beneath live LaTeX typography.

## Current Production Decision

Xi'an has exactly 11 chapters, and all 11 have passed the internal editorial,
reading, PDF-page, and responsive-website gate. Chapter 7 is the single
nearby-area decision chapter, Chapter 8 covers exact airport/station arrival
choices, Chapter 9 covers district-first lodging, Chapter 10 provides nested
two-, three-, and five-day routes, and Chapter 11 closes the trip with dated
departure checks. The verified pocket has `195` B6 pages, `125` blocks, ten
maps, fifteen figures, and SHA-256
`ae2872703174ea523b051ccba21e34eeaa2182aba323bc68a23e5cf558af83c5`.
The synchronized website is publicly deployed at
`https://lachlanchen.github.io/LazyTravel/`; all 74 published files match the
manifest and canonical JSON. Xi'an is complete. Hakone is next at
`japan/prefectures/kanagawa/hakone`, followed by Lanzhou.

Hakone has exactly 11 chapters and advances in order. Chapters 1 through 10 are
accepted internal milestones. Together they provide `97` aligned blocks,
`12,205` Chinese reading tokens, `15,120` Japanese reading tokens, ten maps,
and thirty-five destination, transport, museum, food, landscape, lodging, and
itinerary figure placements using all four guides. The reproducible B6 review
has `193` pages and SHA-256
`50154ec40d8cd77850e44f25ccf6c3cc376d114909f85d6d6d10c7b06dca7d30`.
Desktop and `390 px` website QA pass from the same JSON with `16,770` ruby
nodes, and the exact pocket PDF is hash-synced to Nutstore. This does not
complete Hakone; Chapter 11, `One Stop Beyond Hakone`, is the only next
writing gate.

Chapter 9 established the lodging method used by later books: choose a
district from arrival, dinner, the exact entrance, the next morning, and a
poor-weather exit before comparing a named property. Official filters produce
a shortlist only. A generated room scene can illustrate separate booking
questions, but it is never bookable inventory or an accessibility claim.

Chapter 10 established the itinerary method: one anchor, one fixed commitment,
and one usable exit per day. Weather or service disruption swaps a whole day
or removes a branch; it does not trigger a denser replacement list. The
portrait itinerary map is deliberately pannable on mobile and passed B6 plus
left, centre, and right `390 px` inspection.
