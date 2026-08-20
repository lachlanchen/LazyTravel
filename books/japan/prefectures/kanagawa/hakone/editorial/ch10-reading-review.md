# Chapter 10 Language and Reading Review

Status: Chinese, Japanese, English, pinyin, and furigana reviewed on
`2026-08-21`; B6 and responsive-site proof passed.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese span.
- Japanese uses furigana on kanji-bearing spans; kana, Latin text, Arabic
  digits, punctuation, and whitespace remain unannotated.
- Concatenating token text reproduces every canonical Chinese and Japanese
  paragraph exactly.
- The pocket PDF and website consume these same reviewed arrays.

## Chinese Pass

The Chinese pass keeps the itinerary decision ahead of the sightseeing list:
how to enter, which commitment cannot move, and how to leave when the mountain
changes. It distinguishes a coherent one-day crossing, a ryokan-led night, an
art-led trip, a reduced-transfer day, and three movable days. Literal or
inflated phrases were removed, including language about completing Hakone,
restoring missed sights, and treating rain as an automatic museum instruction.

Reviewed readings include `箱根（xiānggēn）`, `早云山（zǎoyúnshān）`,
`大涌谷（dàyǒnggǔ）`, `桃源台（táoyuántái）`,
`仙石原（xiānshíyuán）`, `固定时刻（gùdìng shíkè）`,
`返程（fǎnchéng）`, and `停运（tíngyùn）`.

## Japanese Pass

The Japanese pass was edited as independent guide prose. It uses a daily
`軸`, a fixed arrival or meal, and a usable `下山路` rather than translating
the English planning vocabulary word for word. The reduced-transfer passage
asks about each station, vehicle, entrance, toilet, lodging, and bath
separately; it does not label all of Hakone barrier-free.

Reviewed readings include `早雲山（そううんざん）`,
`大涌谷（おおわくだに）`, `桃源台（とうげんだい）`,
`仙石原（せんごくはら）`, `一館（いっかん）`,
`二館（にかん）`, `高原（こうげん）`, `下山路（げざんろ）`, and
`運行中断（うんこうちゅうだん）`.

## English Pass

The English pass uses route, meal, lodging, weather, and exit decisions rather
than generic travel-book encouragement. Phrases such as "day envelopes" and
"put the trip on one clock" were replaced with concrete actions. Weather
fallbacks remove or exchange complete branches; they do not promise that an
indoor attraction is open or reachable.

## Validation

- Chapter 10 has ten aligned blocks, `27` distinct citations, one map, six
  figure placements, and three trilingual headings.
- Chapter 10 Chinese has `1,435` reviewed tokens.
- Chapter 10 Japanese has `1,740` reviewed tokens.
- Combined Chapters 1-10 have `12,205` Chinese tokens and `15,120` Japanese
  tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese
  block.
- The reading override tests for `一館`, `二館`, and `高原` pass.
- Strict B6 and website builds consume these arrays without reading, source,
  title, or parity drift.
