# Hakone Visual Plan

Status: locked foundation, `2026-08-16`.

The visual sequence follows one mountain crossing. Maps explain height,
transfer, and fallback choices. Location plates make the actual station,
landform, lakeshore, road, bath, or meal recognizable. Figures are distributed
through the book rather than collected in a decorative gallery.

## Generation Route

- New raster figures use AgInTi image generation by default.
- Codex supplies a factual brief, destination references, cast references,
  prohibited inventions, required resolution, and reserved crop areas.
- Codex reviews every result at original size, B6 print size, and 390 px mobile
  width before it enters canonical JSON.
- Every non-map figure includes exactly the four recurring guides: Aya-chan,
  Lala Xia, Sasa-kun, and the Zhuangzi robot. Reject duplicates, hybrids,
  background copies, missing guides, and crops that remove one of the four.
- The destination remains the visual subject. The four guides provide scale,
  continuity, and a traveler's point of view; they are not posed as celebrities
  in front of an interchangeable background.
- Maps remain character-free and code-built. Labels must stay readable after
  B6 reduction and on a 390 px screen.

The approved character and tool references remain read-only at:

- `/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png`
- `/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg`
- `/home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg`
- `/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png`
- `/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png`
- `/home/lachlan/ProjectsLFS/LALACHAN/display.png`
- `/home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg`

## Cover Contract

The cover underlay is a high-resolution, text-free Hakone scene with all four
guides. Use the current live-type cover page as a composition reference:

- reserve the same bright, low-detail area for the LaTeX title, language line,
  `LazyTravel`, `lazying.art`, and GitHub text;
- place the guides and destination elements outside that live-type area;
- make Hakone legible through the mountain railway, lake/ridge relationship,
  or a restrained combination of recognizable current places;
- do not embed lettering, logos, pseudo-Japanese signs, or title fragments in
  the bitmap;
- do not guarantee a clear Mount Fuji view; if Fuji appears, it is distant and
  meteorologically plausible;
- test the complete cover with live text, not the bitmap alone.

## Chapter Matrix

| Ch. | Map or diagram | Location/experience figures | Visual job |
| ---: | --- | --- | --- |
| 1 | Regional relief-style orientation map: Odawara, Yumoto, Gora, Owakudani, Lake Ashi, outer ridges, onward edges | Four guides at an elevated real-world viewpoint with the lake/ridges dominant | Explain that short map distances hide large height and weather changes. |
| 2 | Gateway and transfer map with Tokyo/east and Kyoto/west approaches, loop-direction choices, and luggage handoff | Odawara interchange; Hakone-Yumoto arrival with luggage decision | Make the first two transfers and baggage choice visually obvious with two distinct location scenes. |
| 3 | Railway-to-Gora slope schematic with stations and one-museum stop | Ohiradai switchback; Open-Air Museum landscape; short cafe pause with current light-food cues | Show gradient, why one art stop deserves time, and how food changes the visit block. Do not copy protected sculpture compositions or present cafe food as Hakone tradition. |
| 4 | Owakudani access/safety map: Sounzan, Owakudani, Ubako, Togendai, current-check marker | Fumarole-field location plate; black-egg process/meal close-up | Show the live volcanic landscape without removing barriers or inventing access. Separate chemistry from legend. |
| 5 | Lake Ashi shore and crossing map with weather alternatives | Lakeshore and shrine approach; boat/lakeside weather scene | Make the lake route readable even when Fuji is absent. Avoid one impossible composite viewpoint. |
| 6 | Old Tokaido walking-choice map with bus exits, checkpoint, cedar avenue, stone paving, and Amasake Chaya | Wet stone-paving scene; checkpoint reconstruction; tea-house rest | Explain surface, slope, controlled passage, and the value of walking only one coherent section. |
| 7 | Compact onsen/ryokan sequence diagram | Bathing-etiquette scene; room-to-dinner transition | Reduce first-time anxiety without showing nudity or implying one property's rules are universal. |
| 8 | Food-by-place strip rather than a restaurant-pin map | Black egg at Owakudani; amazake and mochi on the old road; ryokan dinner timing | Tie food to route, time, and cultural setting instead of a generic dish list. |
| 9 | Stay-area choice map with slopes, first/last transport logic, and next-morning routes | Arrival at a mountain ryokan; room/meal/accessibility decision scene | Choose a district before star count or brand. Do not depict a fictional named hotel. |
| 10 | One-, two-, and three-day itinerary map with weather and disruption branches | Rainy-day museum/onsen fallback; clear-weather early start | Show that a useful plan contains slack and a real alternative. |
| 11 | Nearby continuation map: one of Odawara, Mishima, or Gotemba | Odawara gateway/castle-scale scene; westbound or Fuji-side departure scene | End with one onward choice rather than an overfilled final day. |

The target cadence is one cover underlay, nine code-built maps or diagrams, and
at least twenty-two approved raster figures: normally two different location or
food scenes per chapter. This is a floor for destination coverage, not
permission to add repeated portraits. Each figure must perform a different
travel job, and text blocks should stay short enough that the visual rhythm is
not buried under explanation.

## Factual Boundaries For AgInTi Briefs

1. Name the exact place and viewpoint class, but do not claim a generated scene
   is a documentary photograph from one exact camera position.
2. Supply current official references for architecture, terrain, transport,
   barriers, road surfaces, and visitor flow. References guide form; they are
   not copied or composited into the deliverable.
3. State forbidden errors in every brief: mixed locations, invented scripts,
   unsafe access, vanished structures presented as current, implausible Fuji
   placement, missing required guides, or generic European alpine scenery.
4. Keep clothing and weather consistent within a scene. Later crops may not
   remove Aya-chan or Lala Xia.
5. Generate at a resolution that supports a full B6 page at 300 dpi after the
   intended crop. Reject upscaled detail that breaks at print size.

## Provenance Record

For each accepted raster asset, store a project-sidecar record containing:

- asset ID, chapter, caption IDs, and intended crop;
- generator route and generation date;
- prompt text and prompt SHA-256;
- character-reference paths and SHA-256 values;
- official place-reference URLs and check dates;
- original output path, dimensions, and SHA-256;
- any color/crop conversion commands and derived hashes;
- factual reviewer, cast-continuity review, B6 proof, and mobile proof;
- rejection notes for variants that could otherwise be selected accidentally.

Reader-facing captions never mention the generator or production method. They
state what the traveler is looking at and why it matters on the route.
