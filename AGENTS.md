# LazyTravel Working Agreement

These instructions apply only inside this repository. Read `PROJECT_GOAL.md`,
`PROJECT_MEMORY.md`, and `INIT.md` before continuing production.

## Scope And Destination Gate

- Work only in `/home/lachlan/ProjectsLFS/LazyTravel`.
- Xi'an at `china/cities/xian` is complete and publicly published.
- Hakone at `japan/prefectures/kanagawa/hakone` is complete and publicly
  published with all 11 chapters, a reproducible B6 pocket book, and a
  synchronized two-destination website.
- Lanzhou at `china/cities/lanzhou` is the only next production destination.
  Establish its factual spine and lock a reasonable chapter count before
  drafting; do not reopen Hakone or start another destination in parallel.
- The Xi'an book has exactly 11 chapters. Do not add or remove chapters to solve
  a local editorial problem.
- The Hakone book also has exactly 11 chapters, locked in
  `books/japan/prefectures/kanagawa/hakone/editorial/outline.md`. Populate and
  accept them in order; a later chapter never bypasses an unfinished earlier
  chapter.
- All 11 Hakone chapters have passed editorial, reading, PDF-page, public
  website, provenance, Nutstore, and GitHub publication review. Do not reopen
  a settled Xi'an or Hakone chapter unless a factual, language, layout, or
  build failure is demonstrated.
- All 11 Xi'an chapters have passed editorial, reading, PDF-page, public
  website, Nutstore, and GitHub publication review. Do not reopen a settled
  Xi'an chapter unless a factual, language, layout, or build failure is
  demonstrated.
- Ignore unrelated world-literature work and retain only useful multilingual
  book-production experience.

## Editorial And Data Rules

- The aligned Chinese, Japanese, and English JSON is canonical. The B6 book and
  responsive website must consume the same text, readings, citations, and
  assets.
- Keep pinyin ruby for Chinese and furigana ruby for Japanese. Review each
  language independently; alignment is not permission to translate literally.
- Write original, concrete guide prose. Reject filler, generic summaries,
  invented detail, awkward sentiment, repetition, and wording that sounds
  machine-generated or copied from a source.
- Separate durable history from volatile prices, hours, bookings, routes, and
  hotel operations. Date and recheck volatile advice.
- Every factual block needs traceable citations or a fact-ledger entry. Source
  books provide evidence and leads, not the book's prose or structure.
- Work chapter by chapter, then review the finished chapter page by page in the
  pocket PDF and at desktop/mobile website sizes.
- Keep the travel decision in front: place and route first, then the history or
  food context that changes how the reader sees or uses that place. Do not mix
  disconnected eras into a synthetic story.
- Stop a review pass once facts, natural language, route usefulness, layout,
  readings, and reproducibility pass. Do not repeatedly adjust details with no
  reader-visible or technical consequence.

## Source Boundary

- Treat the six files under `Sources/`, the external open guides, the reference
  ledger, `../ZhJpBook/pdf2tex` tooling, and LALACHAN visual references as
  read-only inputs.
- Do not copy source archives, open-guide PDFs, or raw visual references into
  this repository. Keep raw extraction under ignored `build/research/`.
- Record external paths and hashes in `data/sources/catalog.json`. Commit only
  original writing and derived, reproducible project artifacts with rights and
  provenance review.
- Do not create session backups, rewrite Codex history, or commit private logs,
  browser profiles, credentials, caches, or runtime state.

## Guide Cast And Visual Continuity

- The four recurring guides are Aya-chan, Lala Xia, Sasa-kun, and the Zhuangzi
  robot. The robot is a full person and friend in the group, never equipment or
  background decoration.
- Every new non-map figure must contain exactly the same four guides: Aya-chan,
  Lala Xia, Sasa-kun, and the Zhuangzi robot. This includes instructional
  close-ups or scenes that might otherwise show anonymous hands, backs, or
  distant visitors. Maps remain character-free.
- Stage the full group clearly without making them the attraction. Do not add a
  fifth traveler, duplicate a guide, insert them into documentary evidence, or
  imply they witnessed a historical event.
- For new location-led attraction plates, use all four guides when they remain
  distinct at B6 size. Distribute these plates through the actual trip rather
  than clustering decorative images, and stop when another view would not help
  recognition, comparison, or movement.
- Preserve continuity with the LALACHAN travel-video series by using the
  hash-pinned external character references. Do not replace the guides with
  anonymous generated people.
- The patchwork notebook, LightMind glasses, and word-card device are recurring
  travel tools. Include them only when natural and secondary; never crowd a map,
  food procedure, or attraction view to display every prop.
- Generate a new composition from the references. Keep technical generation
  and source-reference details in provenance, not in reader-facing captions.
- Use the AgInTi image-generation route by default for Hakone and later raster
  figures. Keep Codex on research, briefing, selection, provenance, layout, and
  visual QA so generation does not consume the main writing context.
- Maps and figures must remain readable at B6 print size and a 390 px viewport.
  Use larger labels, simple hierarchy, clean captions, and explicit visual QA.
- In attraction-led chapters, include a view in which the actual destination is
  dominant and recognizable. Aya-chan and Lala Xia remain present, but small
  cast staging or an instructional close-up cannot replace the attraction view.

## Product And Release Discipline

- The only distributed book artifact is the verified B6 pocket PDF. Keep the
  website synchronized from the same JSON.
- Use the vivid LazyTravel palette: white with vermilion, jade, cobalt, and
  coral accents. Keep ruby legible inside highlight bubbles and callouts.
- Build LaTeX and JSON continuously. Validate readings, assets, citations,
  website parity, mobile/desktop layout, PDF trim, fonts, text layer, and every
  touched page before a milestone is accepted.
- Sync only the verified pocket PDF to
  `/home/lachlan/Nutstore Files/Share/LazyTravel/`, then compare hashes.
- Commit and push only coherent verified milestones to the LazyTravel GitHub
  repository. Do not batch unfinished chapters into a release commit.
- Do not stop, restart, or modify existing noVNC, Xvfb, x11vnc, websockify, or
  unrelated project processes and ports. Follow the shared workstation resource
  policy before starting heavy work.
