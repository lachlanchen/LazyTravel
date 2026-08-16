#!/usr/bin/env python3
"""Render aligned LazyTravel destination JSON into generated LaTeX content."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "data/china/cities/xian/book.json"
DEFAULT_TEMPLATE = ROOT / "books/china/cities/xian/latex/book.tex"
DEFAULT_COVER_UNDERLAY = (ROOT / "assets/images/xian/xian-cover-underlay.png").resolve()


LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

CLOSING_PUNCTUATION = frozenset("，。！？；：、）》」』】〉〕］）〗〙〛…")
OPENING_PUNCTUATION = frozenset("（《「『【〈〔［〖〘〚")


def tex_escape(value: str) -> str:
    return "".join(LATEX_ESCAPES.get(character, character) for character in value)


def url_tex(value: str) -> str:
    return "\\url{" + value.replace("%", r"\%") + "}"


def citation_order(chapter: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for block in chapter["blocks"]:
        for citation_id in block["citation_ids"]:
            if citation_id not in seen:
                seen.add(citation_id)
                ordered.append(citation_id)
    return ordered


def citation_order_for_chapters(chapters: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for chapter in chapters:
        for citation_id in citation_order(chapter):
            if citation_id not in seen:
                seen.add(citation_id)
                ordered.append(citation_id)
    return ordered


def citation_markers(ids: list[str], numbers: dict[str, int]) -> str:
    return " ".join(rf"\hyperlink{{source-{numbers[item]}}}{{[{numbers[item]}]}}" for item in ids)


def reading_tokens_tex(layer: dict[str, Any], command: str) -> str:
    pieces: list[str] = []
    tokens = layer["tokens"]
    for index, token in enumerate(tokens):
        token_text = token["text"]
        previous_text = tokens[index - 1]["text"] if index else ""
        if index and (
            token_text[:1] in CLOSING_PUNCTUATION or previous_text[-1:] in OPENING_PUNCTUATION
        ):
            pieces.append(r"\nobreak{}")
        base = tex_escape(token_text)
        reading = token.get("reading")
        if reading:
            pieces.append(rf"\{command}{{{base}}}{{{tex_escape(reading)}}}")
        else:
            pieces.append(base)
        if index + 1 < len(tokens):
            next_text = tokens[index + 1]["text"]
            if (
                token_text[-1:] not in OPENING_PUNCTUATION
                and next_text[:1] not in CLOSING_PUNCTUATION
            ):
                pieces.append(r"\allowbreak{}")
    return "".join(pieces)


def cover_underlay_path(book: dict[str, Any]) -> Path:
    book_id = book.get("id")
    if not book_id:
        return DEFAULT_COVER_UNDERLAY
    return (ROOT / f"assets/images/{book_id}/{book_id}-cover-underlay.png").resolve()


def series_label(book: dict[str, Any]) -> str:
    explicit = book.get("series_label")
    if explicit:
        return explicit
    path = book.get("series_path", "china/cities/xian")
    replacements = {"xian": "XI'AN"}
    return " · ".join(
        replacements.get(part, part.replace("-", " ").upper()) for part in path.split("/")
    )


def destination_header(book: dict[str, Any]) -> str:
    return book.get("running_title", series_label(book).split(" · ")[-1])


def cover_tex(
    book: dict[str, Any],
    chapters: list[dict[str, Any]],
    cover_path: Path | None = None,
) -> str:
    titles = book["titles"]
    subtitles = book.get("subtitles", {language: "" for language in ("zh", "ja", "en")})
    branding = book["branding"]
    repository_label = branding["repository"].removeprefix("https://")
    preserve_xian_layout = book.get("id") == "xian"
    brand_break = "" if preserve_xian_layout else r"\par"
    brand_gap = 13 if preserve_xian_layout else 10
    gate = (
        rf"{{\displayfont\fontsize{{7}}{{9}}\selectfont\color{{LTMuted}}"
        rf"B6 POCKET REVIEW · CHAPTERS {chapters[0]['order']:02d}--"
        rf"{chapters[-1]['order']:02d}\par}}"
    )
    mid_gate = ""
    bottom_gate = gate
    if book.get("cover_gate_position") == "mid":
        mid_gate = rf"\vspace{{7mm}}{gate}"
        bottom_gate = ""
    return rf"""
\begin{{titlepage}}
  \thispagestyle{{empty}}
  \begin{{tikzpicture}}[remember picture,overlay]
    \node[anchor=center,inner sep=0] at (current page.center) {{%
      \includegraphics[width=\paperwidth,height=\paperheight]{{%
        \detokenize{{{cover_path or cover_underlay_path(book)}}}}}%
    }};
  \end{{tikzpicture}}
  \LTBrand{brand_break}
  \vspace*{{{brand_gap}mm}}
  {{\displayfont\fontsize{{8}}{{10}}\selectfont\color{{LTWater}}
    \LTSeriesLabel\par}}
  \vspace{{7mm}}
  {{\bfseries\fontsize{{23}}{{29}}\selectfont {tex_escape(titles['zh'])}\par}}
  \vspace{{4mm}}
  {{{{\jpfont\fontsize{{14}}{{20}}\selectfont\color{{LTForest}}
    {tex_escape(titles['ja'])}}}\par}}
  \vspace{{3mm}}
  {{{{\englishfont\fontsize{{13}}{{18}}\selectfont
    \color{{LTWater}}{tex_escape(titles['en'])}}}\par}}
  \vspace{{9mm}}
  {{\color{{LTCoral}}\rule{{24mm}}{{1.2pt}}}}\par
  \vspace{{6mm}}
  {{\fontsize{{8.6}}{{13}}\selectfont {tex_escape(subtitles['zh'])}\par}}
  \vspace{{2mm}}
  {{{{\jpfont\fontsize{{8.2}}{{12.5}}\selectfont\color{{LTForest}}
    {tex_escape(subtitles['ja'])}}}\par}}
  \vspace{{2mm}}
  {{{{\englishfont\fontsize{{8}}{{11.5}}\selectfont\color{{LTMuted}}
    {tex_escape(subtitles['en'])}}}\par}}
  {mid_gate}
  \vfill
  {bottom_gate}
  \vspace{{3mm}}
  {{\displayfont\fontsize{{7}}{{10}}\selectfont
    {tex_escape(branding['studio'])} · {tex_escape(repository_label)}\par}}
\end{{titlepage}}
\cleardoublepage
"""


def publication_note_tex(book: dict[str, Any], frontmatter: dict[str, Any] | None = None) -> str:
    branding = book["branding"]
    how_to_use = (frontmatter or {}).get(
        "how_to_use",
        {
            "zh": (
                "这是一本按旅行决策组织的西安口袋手册。先用地图分清今天的城墙、历代都城与近郊景点，"
                "再走进兵马俑、雁塔、碑林、城内街巷和西安饭桌。历史只在它能解释眼前地点、路线取舍"
                "或饮食习惯时出现；交通、住宿和二日、三日、五日行程放在后半部。每一节只解决一个问题："
                "去哪里，为什么值得去，现场看什么，怎样留出回程余量。"
            ),
            "ja": (
                "この本は、旅の判断順に組み立てた西安のポケットガイドである。まず地図で現在の城壁、"
                "歴代の都城、近郊の見どころを区別し、兵馬俑、雁塔、碑林、城内の路地、西安の食卓へ進む。"
                "歴史は、目の前の場所、経路の選択、食習慣を理解するために必要なところで扱う。交通、宿泊、"
                "二日・三日・五日の旅程は後半にまとめる。各節が答えるのは、どこへ行くか、なぜ行くか、"
                "現地で何を見るか、どう帰路の余裕を残すかである。"
            ),
            "en": (
                "This pocket guide follows the order in which a traveler makes decisions. "
                "It first separates the present wall, successive capital sites, and nearby "
                "excursions on maps, then moves through the Terracotta Army, the pagodas, "
                "Beilin, lanes inside the wall, and the Xi'an table. History appears where "
                "it explains a place, a route choice, or a way of eating; transport, "
                "accommodation, and two-, three-, and five-day plans follow in the second "
                "half. Each section answers one question: where to go, why it matters, "
                "what to notice there, and how to leave enough room to return."
            ),
        },
    )
    return rf"""
\thispagestyle{{empty}}
\vspace*{{7mm}}
{{\displayfont\bfseries\fontsize{{12}}{{16}}\selectfont
这本手册怎么用 · この手引きの使い方\par}}
\vspace{{1.5mm}}
{{\englishfont\bfseries\fontsize{{9}}{{12}}\selectfont\color{{LTWater}}
HOW TO USE THIS GUIDE\par}}
\vspace{{5mm}}
{{\fontsize{{8}}{{12}}\selectfont
{tex_escape(how_to_use['zh'])}\par}}
\vspace{{4mm}}
{{\jpfont\fontsize{{8}}{{12}}\selectfont
{tex_escape(how_to_use['ja'])}\par}}
\vspace{{4mm}}
{{\englishfont\fontsize{{7.8}}{{11.3}}\selectfont
{tex_escape(how_to_use['en'])}\par}}
\vfill
{{\displayfont\fontsize{{7}}{{10}}\selectfont\color{{LTMuted}}
One aligned ZH · JA · EN JSON · reviewed pinyin and furigana · dated sources\par
LazyTravel · {tex_escape(branding['studio'])}\par
Repository: {url_tex(branding['repository'])}\par
Edition: {tex_escape(book['edition'])}\par}}
\clearpage
"""


def contents_tex(chapters: list[dict[str, Any]]) -> str:
    pieces = [
        r"\frontmatter",
        r"\thispagestyle{empty}",
        r"\vspace*{5mm}",
        r"{\displayfont\bfseries\fontsize{15}{19}\selectfont 目录 · 目次\par}",
        r"\vspace{1mm}",
        r"{\englishfont\bfseries\fontsize{9}{12}\selectfont\color{LTWater}CONTENTS\par}",
        r"\vspace{6mm}",
    ]
    for index, chapter in enumerate(chapters):
        if index == 4:
            pieces.extend(
                [
                    r"\clearpage",
                    r"\thispagestyle{empty}",
                    r"\vspace*{5mm}",
                    (
                        r"{\displayfont\bfseries\fontsize{13}{17}\selectfont "
                        r"目录（续） · 目次（続き）\par}"
                    ),
                    r"\vspace{1mm}",
                    (
                        r"{\englishfont\bfseries\fontsize{8.5}{11}\selectfont"
                        r"\color{LTWater}CONTENTS CONTINUED\par}"
                    ),
                    r"\vspace{6mm}",
                ]
            )
        titles = chapter["titles"]
        label = f"lt-chapter-{chapter['order']:02d}"
        pieces.append(
            rf"\LTContentsEntry{{{chapter['order']:02d}}}"
            rf"{{{tex_escape(titles['zh'])}}}"
            rf"{{{tex_escape(titles['ja'])}}}"
            rf"{{{tex_escape(titles['en'])}}}"
            rf"{{\pageref{{{label}}}}}"
        )
    pieces.extend([r"\clearpage", r"\mainmatter"])
    return "\n".join(pieces) + "\n"


def block_tex(
    block: dict[str, Any],
    citation_numbers: dict[str, int],
    assets: dict[str, dict[str, Any]],
) -> str:
    text = block["text"]
    readings = block["readings"]
    heading = block.get("heading")
    if block["kind"] in {"callout", "practical"} and heading is None:
        raise ValueError(f"{block['kind']} block {block['id']} requires a heading")
    heading_tex = (
        " · ".join(tex_escape(heading[language]) for language in ("zh", "ja", "en"))
        if heading
        else ""
    )
    pieces = [r"\clearpage"]
    if block["kind"] == "callout":
        pieces.append(
            rf"\LTCalloutBlock"
            rf"{{{heading_tex}}}"
            rf"{{{reading_tokens_tex(readings['zh'], 'LTRubyZH')}}}"
            rf"{{{reading_tokens_tex(readings['ja'], 'LTRubyJA')}}}"
            rf"{{{tex_escape(text['en'])}}}"
            rf"{{{citation_markers(block['citation_ids'], citation_numbers)}}}"
        )
        return "\n".join(pieces) + "\n"
    pieces.append(rf"\LTBlockStart{{{tex_escape(block['id'])}}}")
    if block["kind"] == "practical":
        pieces.append(rf"\LTPracticalHeading{{{heading_tex}}}")
    pieces.extend(
        [
            rf"\LTChinese{{{reading_tokens_tex(readings['zh'], 'LTRubyZH')}}}",
            rf"\LTJapanese{{{reading_tokens_tex(readings['ja'], 'LTRubyJA')}}}",
            rf"\LTEnglish{{{tex_escape(text['en'])}}}",
            rf"\LTSources{{{citation_markers(block['citation_ids'], citation_numbers)}}}",
        ]
    )
    if block["kind"] in {"map", "figure"}:
        if len(block["asset_ids"]) != 1:
            raise ValueError(
                f"{block['kind']} block {block['id']} must reference exactly one asset"
            )
        asset = assets[block["asset_ids"][0]]
        visual_path = (ROOT / asset.get("variants", {}).get("print", asset["path"])).resolve()
        if block["kind"] == "map":
            pieces.append(rf"\LTMapPage{{\detokenize{{{visual_path}}}}}")
        else:
            captions = asset["captions"]
            pieces.append(
                rf"\LTFigurePage{{\detokenize{{{visual_path}}}}}"
                rf"{{{tex_escape(captions['zh'])}}}"
                rf"{{{tex_escape(captions['ja'])}}}"
                rf"{{{tex_escape(captions['en'])}}}"
            )
    return "\n".join(pieces) + "\n"


def bibliography_tex(
    ordered_ids: list[str],
    citation_numbers: dict[str, int],
    citations: dict[str, dict[str, Any]],
) -> str:
    pieces = [
        r"\cleardoublepage",
        r"\chapter*{资料来源 · 出典 · Sources}",
        r"\addcontentsline{toc}{chapter}{资料来源 · 出典 · Sources}",
        (
            r"{\fontsize{8.5}{12.5}\selectfont\color{LTMuted}"
            r"Only sources cited in these chapters are listed. Each entry carries its "
            r"own access date.\par}"
        ),
    ]
    for citation_id in ordered_ids:
        citation = citations[citation_id]
        details = [
            tex_escape(citation["locator"]),
            f"Checked {tex_escape(citation['accessed_at'])}",
        ]
        if citation.get("license"):
            details.append(f"License: {tex_escape(citation['license'])}")
        link = ""
        if citation.get("url"):
            link = rf"{{\fontsize{{7}}{{10}}\selectfont {url_tex(citation['url'])}\par}}"
        number = citation_numbers[citation_id]
        pieces.append(rf"\hypertarget{{source-{number}}}{{}}")
        pieces.append(
            rf"\LTSourceEntry{{{number}}}{{{tex_escape(citation['title'])}}}"
            rf"{{{' · '.join(details)}}}{{{link}}}"
        )
    return "\n".join(pieces) + "\n"


def render_document(document: dict[str, Any], chapter_ids: str | list[str]) -> str:
    book = document["book"]
    chapters_by_id = {chapter["id"]: chapter for chapter in document["chapters"]}
    requested_ids = [chapter_ids] if isinstance(chapter_ids, str) else chapter_ids
    chapters: list[dict[str, Any]] = []
    for chapter_id in requested_ids:
        if chapter_id not in chapters_by_id:
            raise ValueError(f"chapter not found: {chapter_id}")
        chapter = chapters_by_id[chapter_id]
        if not chapter["blocks"]:
            raise ValueError(f"chapter has no blocks: {chapter_id}")
        chapters.append(chapter)

    citations = {citation["id"]: citation for citation in document["citations"]}
    assets = {asset["id"]: asset for asset in document["assets"]}
    ordered_ids = citation_order_for_chapters(chapters)
    missing = [citation_id for citation_id in ordered_ids if citation_id not in citations]
    if missing:
        raise ValueError(f"missing citations: {', '.join(missing)}")
    citation_numbers = {citation_id: index for index, citation_id in enumerate(ordered_ids, 1)}

    pieces = [
        cover_tex(book, chapters),
        publication_note_tex(book, document.get("frontmatter")),
        contents_tex(chapters),
    ]
    for chapter in chapters:
        titles = chapter["titles"]
        deck_rows: list[str] = []
        deck_row: list[str] = []
        deck_row_length = 0
        for item in chapter["coverage"]:
            label = item.upper().replace("-", " ")
            added_length = len(label) + (3 if deck_row else 0)
            if deck_row and deck_row_length + added_length > 36:
                deck_rows.append(" · ".join(deck_row))
                deck_row = []
                deck_row_length = 0
                added_length = len(label)
            deck_row.append(rf"\mbox{{{tex_escape(label)}}}")
            deck_row_length += added_length
        if deck_row:
            deck_rows.append(" · ".join(deck_row))
        deck = r"\par ".join(deck_rows)
        pieces.append(
            rf"\LTChapterTitle{{{chapter['order']:02d}}}"
            rf"{{{tex_escape(titles['zh'])}}}"
            rf"{{{tex_escape(titles['ja'])}}}"
            rf"{{{tex_escape(titles['en'])}}}"
            rf"{{{deck}}}"
        )
        pieces.extend(block_tex(block, citation_numbers, assets) for block in chapter["blocks"])
    pieces.append(bibliography_tex(ordered_ids, citation_numbers, citations))
    pieces.extend(
        [
            r"\cleardoublepage",
            r"\thispagestyle{empty}",
            r"\vspace*{\fill}",
            r"{\centering\displayfont\bfseries\fontsize{15}{19}\selectfont LazyTravel\par}",
            r"\vspace{3mm}",
            (
                r"{\centering\fontsize{8}{11}\selectfont "
                r"lazying.art · github.com/lachlanchen/LazyTravel\par}"
            ),
            r"\vspace*{\fill}",
        ]
    )
    return "\n".join(pieces) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument(
        "--chapter",
        action="append",
        dest="chapters",
        help="chapter id to include; repeat for a continuous review",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    document = json.loads(args.book.read_text(encoding="utf-8"))
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    content_path = output_dir / "generated-content.tex"
    wrapper_path = output_dir / "main.tex"
    chapter_ids = args.chapters or [
        next(chapter["id"] for chapter in document["chapters"] if chapter["blocks"])
    ]
    content_path.write_text(render_document(document, chapter_ids), encoding="utf-8")
    book = document["book"]
    landscape_profile = "" if book.get("id") == "xian" else "\\def\\LTUseWideLandscape{1}\n"
    wrapper_path.write_text(
        f"\\def\\GeneratedContent{{{content_path}}}\n"
        f"\\def\\LTSeriesLabel{{{tex_escape(series_label(book))}}}\n"
        f"\\def\\LTDestinationHeader{{{tex_escape(destination_header(book))}}}\n"
        f"{landscape_profile}"
        f"\\input{{{DEFAULT_TEMPLATE}}}\n",
        encoding="utf-8",
    )
    print(f"rendered: {content_path}")
    print(f"wrapper: {wrapper_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
