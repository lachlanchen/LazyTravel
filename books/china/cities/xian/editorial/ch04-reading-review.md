# Chapter 4 Reading Review

Status: reviewed on `2026-08-15`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses furigana on kanji-bearing tokens; kana and punctuation remain
  unannotated.
- Concatenating token text reproduces the canonical Chinese or Japanese prose
  exactly.
- The B6 pocket PDF and website consume the same reviewed arrays in
  `data/china/cities/xian/book.json`.

## Editorial Audit

Machine-assisted segmentation was followed by a chapter-specific pass for
proper names, polyphonic characters, Buddhist terms, architectural terms,
stone-inscription vocabulary, and dates. The Chinese audit corrected
`一行行 (yīhángháng)`, `舍利 (shèlì)`, `译场 (yìchǎng)`, `密檐式
(mìyánshì)`, `吕大忠 (lǚ dàzhōng)`, `重排 (chóngpái)`, `重刻
(chóngkè)`, `稍干 (shāogān)`, `拓包 (tàbāo)`, and `官网
(guānwǎng)`. Prose was revised where tokenization exposed an actual ambiguity;
the reading layer was then regenerated instead of patched around stale text.

The Japanese pass checked `訳場（やくじょう）`,
`薦福寺塔（せんぷくじとう）`, `密檐式（みつえんしき）`,
`神合（しんごう）`, `国子監（こくしかん）`,
`呂大忠（りょだいちゅう）`, `114石（ひゃくじゅうよんせき）`, and
`火曜日（かようび）`. Independent line editing also replaced literal or
stiff wording around the tower inscriptions, Beilin's relocation history, and
the generated rubbing illustration.

## Validation

- Chapter 4 Chinese: `1,036` tokens, including `847` ruby-bearing tokens.
- Chapter 4 Japanese: `1,331` tokens, including `571` ruby-bearing tokens.
- Full canonical book after Chapter 4: `3,734` Chinese tokens and `4,807`
  Japanese tokens.
- The reviewed reading payload for Chapters 1–3 retains SHA-256
  `0a3e6666f856a4a14d2af2c8e91f4bfe702e97d8c001e0fedbf5fd81564a1962`.
- `scripts/validate_readings.py` passes reconstruction, coverage, status, and
  tone-mark checks; the destination-book schema also passes.
