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
            token_text[:1] in CLOSING_PUNCTUATION
            or previous_text[-1:] in OPENING_PUNCTUATION
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


def cover_tex(book: dict[str, Any], chapters: list[dict[str, Any]]) -> str:
    titles = book["titles"]
    subtitles = book.get("subtitles", {language: "" for language in ("zh", "ja", "en")})
    branding = book["branding"]
    return rf"""
\begin{{titlepage}}
  \thispagestyle{{empty}}
  \LTBrand
  \vspace*{{13mm}}
  {{\displayfont\fontsize{{8}}{{10}}\selectfont\color{{LTWater}}
    CHINA · CITIES · XI'AN\par}}
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
  \vfill
  {{\displayfont\fontsize{{7}}{{9}}\selectfont\color{{LTMuted}}
    B6 POCKET REVIEW · CHAPTERS {chapters[0]['order']:02d}--{chapters[-1]['order']:02d}\par}}
  \vspace{{3mm}}
  {{\displayfont\fontsize{{7}}{{10}}\selectfont
    {tex_escape(branding['studio'])} · {tex_escape(branding['repository'])}\par}}
\end{{titlepage}}
\cleardoublepage
"""


def publication_note_tex(book: dict[str, Any]) -> str:
    branding = book["branding"]
    return rf"""
\thispagestyle{{empty}}
\vspace*{{10mm}}
{{\displayfont\bfseries\fontsize{{13}}{{17}}\selectfont About this review edition\par}}
\vspace{{6mm}}
{{\englishfont\fontsize{{8}}{{12}}\selectfont
This pocket review is generated from the same aligned Chinese, Japanese, and English JSON
used by the LazyTravel website. Historical claims are separated from dated travel
information; source text and source images are not republished. Map generalisation is
disclosed on the map and in its provenance ledger. Chinese pinyin and Japanese furigana
come from the reviewed token layer in that JSON.\par}}
\vspace{{5mm}}
{{\fontsize{{8}}{{12}}\selectfont
本章审阅版由同一份中、日、英对齐 JSON 生成。历史事实与有时效的旅行信息分开处理，
不转载参考书原文或图片；地图中的概化河段均在图面与溯源记录中说明。\par}}
\vspace{{5mm}}
{{\jpfont\fontsize{{8}}{{12}}\selectfont
本章レビュー版は、ウェブサイトと共通の中国語・日本語・英語対訳 JSON から生成している。
歴史的記述と更新を要する旅行情報を分け、参照資料の本文や画像は転載しない。
地図の概略化区間は図面と来歴記録に明記した。\par}}
\vfill
{{\displayfont\fontsize{{7}}{{10}}\selectfont\color{{LTMuted}}
LazyTravel · {tex_escape(branding['studio'])}\par
Repository: {url_tex(branding['repository'])}\par
Edition: {tex_escape(book['edition'])}\par}}
\clearpage
"""


def block_tex(
    block: dict[str, Any],
    citation_numbers: dict[str, int],
    assets: dict[str, dict[str, Any]],
) -> str:
    text = block["text"]
    readings = block["readings"]
    pieces = [r"\clearpage", rf"\LTBlockStart{{{tex_escape(block['id'])}}}"]
    if block["kind"] == "callout":
        pieces.append(
            rf"\LTCalloutBlock"
            rf"{{{reading_tokens_tex(readings['zh'], 'LTRubyZH')}}}"
            rf"{{{reading_tokens_tex(readings['ja'], 'LTRubyJA')}}}"
            rf"{{{tex_escape(text['en'])}}}"
            rf"{{{citation_markers(block['citation_ids'], citation_numbers)}}}"
        )
        return "\n".join(pieces) + "\n"
    if block["kind"] == "practical":
        pieces.append(r"\LTPracticalHeading")
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
        publication_note_tex(book),
        r"\frontmatter",
        r"\begingroup",
        r"\hyphenpenalty=10000",
        r"\exhyphenpenalty=10000",
        r"\tableofcontents",
        r"\endgroup",
        r"\mainmatter",
    ]
    for chapter in chapters:
        titles = chapter["titles"]
        deck = " · ".join(item.upper().replace("-", " ") for item in chapter["coverage"])
        pieces.append(
            rf"\LTChapterTitle{{{chapter['order']:02d}}}"
            rf"{{{tex_escape(titles['zh'])}}}"
            rf"{{{tex_escape(titles['ja'])}}}"
            rf"{{{tex_escape(titles['en'])}}}"
            rf"{{{tex_escape(deck)}}}"
        )
        pieces.extend(
            block_tex(block, citation_numbers, assets) for block in chapter["blocks"]
        )
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
    chapter_ids = args.chapters or ["ch01-ground-before-time"]
    content_path.write_text(render_document(document, chapter_ids), encoding="utf-8")
    wrapper_path.write_text(
        f"\\def\\GeneratedContent{{{content_path}}}\n" f"\\input{{{DEFAULT_TEMPLATE}}}\n",
        encoding="utf-8",
    )
    print(f"rendered: {content_path}")
    print(f"wrapper: {wrapper_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
