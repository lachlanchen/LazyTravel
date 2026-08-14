# Xi'an Source Audit

Audit date: `2026-08-14`. Current destination gate: `china/cities/xian`.

## Rights Boundary

The three Xi'an books in `Sources/` are private, copyrighted research
references. Their archives, extracted prose, and extracted images are ignored
by Git. No source image is approved for publication. The Chinese and English
Wikivoyage snapshots remain read-only in `/home/lachlan/ProjectsLFS/Books` and
carry CC BY-SA 4.0 attribution and share-alike obligations.

The public book will use original prose. A fact learned from a source is cited;
the source's wording and narrative sequence are not reused.

## Extraction Evidence

| Source | Route | Structural result | Visual result | Editorial use |
| --- | --- | --- | --- | --- |
| `xian-history-1981` | Hash-gated Marker/Surya, 20 resumable shards | 233/233 PDF pages; 100,267 searchable characters; all 29 OCR headings correspond to the printed contents order | 41 extracted references; 39 substantive research candidates; 2 scan fragments rejected; 0 missing | Historical leads, physical geography, city-layer chronology |
| `xian-family-guide` | EPUB package/spine parser with path-traversal rejection | 7 spine documents; 1,759 ordered blocks | 340 referenced figures; 0 missing | Attraction inventory and family-use questions; practical listings are obsolete |
| `xian-city-flavor` | EPUB package/spine parser with path-traversal rejection | 19 spine documents; 18 narrative blocks | 18 referenced illustrations; 0 missing | Food vocabulary, street-life motifs, and cultural prompts |
| `xian-open-guide-zh` | Read exact MediaWiki API snapshot | Revision `209278`; 86 recorded sections | Open-guide media is not automatically adopted | Orientation and leads for current verification |
| `xian-open-guide-en` | Read exact MediaWiki API snapshot | Revision `5297771`; 45 recorded sections | Open-guide media is not automatically adopted | Cross-language orientation and leads for current verification |

Machine evidence is in ignored `build/research/`. Reproduction commands are in
the repository README.

## PDF-to-TeX Pilot Review

The inspected ZhJpBook workflow was reused through its installed Marker/Surya
binary, shared GPU lock, hash/resume contract, figure preservation strategy,
and exact-TeX validation model. LazyTravel writes no files to ZhJpBook.

The first 24-page pilot compiled to a 21-page searchable A4 review PDF and
passed `qpdf --check`. It was correctly rejected as an editorial source edition
because:

- the printed contents on source PDF pages 7-8 became a malformed OCR table;
- Marker produced one repeated-phrase hallucination on source PDF page 23;
- two narrow or tiny scan fragments were initially treated as figures;
- the default CJK font dropped rare characters and circled note numbers;
- one tall image/table combination produced a severe vertical overflow.

The raw OCR remains immutable. The extractor now records exact source pages and
pixel dimensions, rejects the two scan fragments from substantive review, uses
Noto CJK/Devanagari coverage for TeX previews, and treats missing glyphs or an
overflow above 18 pt as a failed acceptance gate.

## Printed Structure

The authoritative section map is
[`data/sources/xian-history-1981-structure.json`](../data/sources/xian-history-1981-structure.json).
It comes from the printed contents on PDF pages 7-8, not from OCR heading
guesswork. Printed page 1 is PDF page 9, giving an offset of eight pages through
the body.

## Image Decision

A contact-sheet review of the EPUB assets found useful subjects but no public
asset candidates. The family guide mixes dated documentary photographs,
low-resolution web graphics, hotel-room photographs, and decorative clip art.
The city-food book contains cohesive commissioned illustrations, but their
copyright prevents reuse. These images may guide shot lists and image-generation
briefs only; they must not be copied, traced, or used as hidden generation
inputs.

The history PDF's maps and diagrams remain useful evidence. Public maps will be
redrawn from verified geographic data with their own provenance; source maps
will not be published unless a later rights review explicitly permits it.

## Chapter 1 Research Gate

The research gate passed on `2026-08-14`:

1. Physical-geography leads were checked against Xi'an municipal material, the
   State Council territorial-plan reply, the Shaanxi provincial gazetteer, and
   UNESCO's Chang'an-Tianshan corridor record.
2. Source-page OCR defects remain isolated in ignored raw research output; no
   damaged OCR sentence is eligible for publication.
3. The accepted, rejected, deferred, durable, and time-sensitive claims are in
   [`ch01-fact-ledger.md`](../books/china/cities/xian/editorial/ch01-fact-ledger.md).
4. The first map's argument, extent, data limits, typography, and acceptance
   gate are in
   [`ch01-map-spec.md`](../books/china/cities/xian/editorial/ch01-map-spec.md).

Chapter 1 may now enter drafting. It cannot enter final review until its map is
rendered, both output formats are built, and every page has been inspected.
