# LazyTravel

LazyTravel is a trilingual travel-book and website project from
[lazying.art](https://lazying.art). Each destination is researched and edited
once in aligned Chinese, Japanese, and English JSON, then rendered into a
clean B6 pocket book (`125 x 176 mm`) and a responsive website. Both outputs
must use the same prose, citations, assets, and reviewed pinyin/furigana layer.

Repository: <https://github.com/lachlanchen/LazyTravel>

## Current Editorial Gate

Xi'an is the only active destination in the China Cities series. Lanzhou is the
next city book and remains gated until the Xi'an book has passed chapter review,
reproducible PDF builds, page-by-page visual QA, JSON validation, and website
validation. Broader Gansu and Ningxia sources are research context, not
destination-book titles.

The series taxonomy is fixed:

```text
china/cities/<city>
japan/prefectures/<prefecture>
world/countries/<country>
```

Current verified milestone: Xi'an Chapters 1-9, `98` aligned content blocks,
`153` B6 pages, nine reproducible maps, and thirteen realistic editorial figures
with technical provenance. Every reviewed chapter now has a place-led visual:
Yongning Gate, Daming Palace, Terracotta Pit 1, the Big Wild Goose Pagoda, the
city wall, Bell Tower, food practice, the nearby mountain day, or Xi'an North.
Every non-map figure includes at least Aya-chan and Lala Xia; new attraction
plates use all four guides when the location remains dominant and legible. The
Xi'an outline contains exactly `11` chapters. Chapter 7 is the reviewed
nearby-area chapter; Chapter 8 covers airport/station arrival; Chapter 9 is the
reviewed district-first lodging chapter. Chapter 10, practical two-, three-,
and five-day itineraries, is the next production gate.

The current pocket PDF SHA-256 is
`7703a3273523c3fa414947a9fc06fbdb10aab56600ec0099b33b40108415f7bd`.
The same verified file is mirrored to the project Nutstore share.

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

The website build writes an ignored static preview to `site/`. It reads the
same aligned destination JSON as the pocket book, removes private local source
paths from the browser payload and public asset-provenance copies, and rejects
text, reading, citation, or asset drift before writing `site/manifest.json`.

Serve the generated site in one terminal and run browser QA in another:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
python3 scripts/qa_website.py --url http://127.0.0.1:4173/
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
