# LazyTravel

LazyTravel is a trilingual travel-book and website project from
[lazying.art](https://lazying.art). Each destination is researched and edited
once in aligned Chinese, Japanese, and English JSON, then rendered into a
clean B6 pocket book (`125 x 176 mm`) and a responsive website. Both outputs
must use the same prose, citations, assets, and reviewed pinyin/furigana layer.

Repository: <https://github.com/lachlanchen/LazyTravel>

Public guide: <https://lachlanchen.github.io/LazyTravel/>

Published guide paths:

- Xi'an: <https://lachlanchen.github.io/LazyTravel/china/cities/xian/>
- Hakone: <https://lachlanchen.github.io/LazyTravel/japan/prefectures/kanagawa/hakone/>
- Lanzhou: <https://lachlanchen.github.io/LazyTravel/china/cities/lanzhou/>

## Current Editorial Gate

Xi'an and Hakone are complete and publicly published. Lanzhou at
`china/cities/lanzhou` is the only active book. Chapters 1-4 are accepted public
milestones; Chapter 5 is the sole production gate. Only one destination may be
in production at a time. Broader Gansu and Ningxia sources remain research
context, not destination-book titles.

The series taxonomy is fixed:

```text
china/cities/<city>
japan/prefectures/<prefecture>
japan/prefectures/<prefecture>/<city-or-area>
world/countries/<country>
```

Current verified milestone: all 11 Xi'an chapters, `125` aligned content blocks,
`195` B6 pages, ten reproducible maps, and fifteen realistic editorial figures
with technical provenance. The visual route includes Yongning Gate, Daming
Palace, Terracotta Pit 1, the Big Wild Goose Pagoda, the city wall, Bell Tower,
food practice, the nearby mountain day, Xi'an North, South Gate, the Small Wild
Goose Pagoda, and the four-guide departure check.
Every non-map figure includes at least Aya-chan and Lala Xia; new attraction
plates use all four guides when the location remains dominant and legible. The
Xi'an outline contains exactly `11` chapters. Chapter 7 is the nearby-area
decision chapter; Chapter 8 covers airport/station arrival; Chapter 9 is the
district-first lodging chapter; Chapter 10 supplies nested two-, three-, and
five-day itineraries; and Chapter 11 closes with dated booking, conditions,
conduct, allergy, and emergency checks. The cover uses a text-free four-guide
city-wall scene under live selectable LaTeX text. All chapters have passed the
editorial, reading, page, and public website gate. Xi'an is complete;
Hakone was completed next, and production now advances only to Lanzhou.

The Xi'an pocket PDF SHA-256 is
`ae2872703174ea523b051ccba21e34eeaa2182aba323bc68a23e5cf558af83c5`.
The same verified file is mirrored to the project Nutstore share.
The synchronized 11-chapter website is published through GitHub Pages.

Hakone has a separate locked 11-chapter route. All chapters are accepted:
**Read the Mountain First**, **Odawara to Yumoto**, **Climb to Gora**,
**Cross Owakudani**, **Lake Ashi: Shrine, Wakasagi, and Shore**, and **Old
Tokaido and the Checkpoint**, followed by **One Night in an Onsen Ryokan** and
**Eat Along the Route**, **Where to Stay**, **One, Two, or Three Days**, and
**Beyond Hakone: Choose One Stop**. Together they contain `107` aligned
blocks, 11 code-built maps, 38 four-guide figure placements, `13,914` Chinese
reading tokens, `17,164` Japanese reading tokens, and a verified `218`-page B6
review. The pocket SHA-256 is
`9d9e45fa6150e740d335c10da932bea96283f6c90fa01fb1a33d6b1fa596eaa0`.
The same file is hash-synced to Nutstore. The two-destination website preserves
Xi'an and Hakone at their taxonomy paths and passes desktop/mobile review with
`19,113` Hakone ruby nodes.

Lanzhou has a hash-verified read-only source baseline, an explicit claim and
rejection ledger, and a locked 11-chapter trilingual outline. Chapters 1-4,
through **Cross One Bridge, Read Both Banks**, are accepted: `35` aligned
blocks, `3,449` reviewed Chinese reading tokens, `4,542` reviewed Japanese
reading tokens, 34 chapter-source entries, seven four-guide figures, and four
code-built maps. The same canonical JSON produces a `62`-page B6 pocket and a
responsive site with `4,841` ruby nodes. The pocket SHA-256 is
`0f5b7479d268ff25a5ed3a7470c7a66b74ea2e222144bd49aa388616981ba7f9`, and its
Nutstore copy matches. Chapter 5, **Read One Route Through Gansu Provincial
Museum**, is the only active production gate; the Lanzhou book itself is not
yet complete.

## Source Boundary

The six supplied books in `Sources/` are private research references. They are
ignored by Git and are not redistributed. The open Xi'an and Gansu guides and
the LALACHAN guide-character/tool references are reused read-only from their
external project paths; they are not copied into this repository. Absolute
paths, hashes, dimensions or revision IDs, licenses, and editorial roles are
recorded in
[`data/sources/catalog.json`](data/sources/catalog.json).

Raw OCR, extracted prose, and extracted source images stay under ignored
`build/research/`. Published book and website prose must be original, supported
by the citation ledger, and reviewed independently in all three languages.

## Reproduce The Research Baseline

```bash
python3 scripts/verify_sources.py
python3 scripts/extract_epub.py --source-id xian-family-guide
python3 scripts/extract_epub.py --source-id xian-city-flavor
python3 scripts/extract_pdf_ocr.py \
  --source-id xian-history-1981 --page-end 24 --compile-tex
python3 -m unittest discover -s tests
```

The source verifier writes `build/research/source-verification.json`. EPUB
extraction preserves the spine, block order, source-image references, and
checksums without altering the source archive.

The scanned-PDF command reuses the inspected ZhJpBook Marker/Surya binary and
its cross-project GPU lock, but writes only to LazyTravel's ignored research
cache. It is resumable by source hash and page shard; omitting `--page-end`
continues through the complete source.

## Build The Xi'an Pocket Review

```bash
python3 scripts/build_xian_review.py
python3 scripts/build_website.py
python3 scripts/validate_site_parity.py
```

This regenerates the committed map variants from normalized or declared map
data, validates both JSON contracts and all used visual provenance, renders the
aligned reviewed chapters, runs XeLaTeX twice with a fixed source date, and
rejects malformed PDFs, TeX warnings, unembedded fonts, or a missing text
layer. The B6 pocket review PDF and its hash manifest are written to ignored
`dist/books/xian/`.

Use `--skip-map` only when checking the book layout against the already
committed map variants.

## Build The Hakone Pocket And Series Website

```bash
python3 scripts/build_hakone_review.py
python3 scripts/build_series_website.py
python3 scripts/validate_site_parity.py \
  --book data/japan/prefectures/kanagawa/hakone/book.json \
  --site site/japan/prefectures/kanagawa/hakone
```

The Hakone builder discovers only the consecutive populated chapter prefix,
keeps the book at exactly 11 planned chapters, and rejects pending figure,
map, cover, reading, PDF, or source checks. After browser review, sync only the
verified pocket PDF with:

```bash
python3 scripts/build_hakone_review.py --skip-map --sync-nutstore
```

Serve `site` on an unused temporary project-owned port and run
`scripts/qa_destination_website.py` against that URL. Stop only that temporary
server after QA; do not alter the existing Xi'an preview server or any shared
GUI stack.

The website build writes an ignored static preview to `site/`. It reads the
same aligned destination JSON as the pocket book, removes private local source
paths from the browser payload and public asset-provenance copies, and rejects
text, reading, citation, or asset drift before writing `site/manifest.json`.

## Build The Lanzhou Pocket Milestone

```bash
python3 scripts/build_lanzhou_review.py
python3 scripts/build_series_website.py
python3 scripts/validate_site_parity.py \
  --book data/china/cities/lanzhou/book.json \
  --site site/china/cities/lanzhou
```

The Lanzhou builder accepts only the consecutive reviewed chapter prefix and
keeps the 11-chapter outline intact. It validates readings, source coverage,
asset hashes and provenance, map regeneration, cover geometry, TeX warnings,
trim, fonts, and searchable text. After page and browser review, sync only the
verified pocket with:

```bash
python3 scripts/build_lanzhou_review.py --skip-map --sync-nutstore
```

Serve the generated site in one terminal and run browser QA in another:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
python3 scripts/qa_website.py --url http://127.0.0.1:4173/
```

Every push to `main` rebuilds and publishes the static site through
`.github/workflows/pages.yml`. The deploy job then compares the public payload
with canonical JSON and hashes every file in the deployed manifest. The same
check can be repeated locally:

```bash
python3 scripts/verify_deployed_site.py \
  --url https://lachlanchen.github.io/LazyTravel/japan/prefectures/kanagawa/hakone/ \
  --book data/japan/prefectures/kanagawa/hakone/book.json
```

## Editorial Contract

- Facts are separated into durable history and time-sensitive travel advice.
- Every publishable block carries source IDs and locators.
- Reference books and open guides supply evidence, leads, and contradiction
  checks; LazyTravel supplies the chapter structure, traveler judgment, and
  original prose.
- Chinese, Japanese, and English are aligned by stable block ID, not generated
  as independent documents.
- Chinese and Japanese reading layers use reviewed pinyin and furigana ruby
  from the same JSON consumed by the book and website.
- Each language has its own editorial status and notes.
- Editing rejects filler, generic summaries, awkward literary effects, and
  sentences that sound translated or machine-generated.
- Maps and images require provenance, captions, rights, and visual-QA status.
- Book and website builds consume the same destination JSON.
- Automated parity checks prevent the website and pocket book from drifting.

See [`schemas/destination-book.schema.json`](schemas/destination-book.schema.json)
for the machine-enforced contract.
