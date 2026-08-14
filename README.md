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

## Source Boundary

The six supplied books in `Sources/` are private research references. They are
ignored by Git and are not redistributed. The open Xi'an and Gansu guides are
reused read-only from `/home/lachlan/ProjectsLFS/Books`; they are not copied
into this repository. Absolute paths, hashes, revision IDs, licenses, and
editorial roles are recorded in
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

## Build The Xi'an Chapter Review

```bash
python3 scripts/build_xian_review.py
python3 scripts/build_website.py
python3 scripts/validate_site_parity.py
```

This regenerates the committed orientation-map variants from normalized map
data, validates both JSON contracts, renders the aligned Chapter 1 content,
runs XeLaTeX twice with a fixed source date, and rejects malformed PDFs, TeX
warnings, unembedded fonts, or a missing text layer. The B6 pocket review PDF
and its hash manifest are written to ignored `dist/books/xian/`.

Use `--skip-map` only when checking the book layout against the already
committed map variants.

The website build writes an ignored static preview to `site/`. It reads the
same aligned destination JSON as the pocket book, removes only private local
source paths from the browser payload, and rejects text, reading, citation, or
asset drift before writing `site/manifest.json`.

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
