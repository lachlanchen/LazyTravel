# Chapter 11 Website Review

Status: synchronized series build, responsive browser review, GitHub Pages
deployment, and public manifest verification passed on `2026-08-21`.

## Parity

- Stable path: `japan/prefectures/kanagawa/hakone/`.
- Complete Hakone book: `107` aligned blocks.
- Chinese reading layer: `13,914` tokens.
- Japanese reading layer: `17,164` tokens.
- Browser rendering: `19,113` ruby nodes, including `2,343` in Chapter 11.
- Chapter 11: `10` blocks, `21` source entries, three figures, one map, and
  three trilingual headings.

The website and B6 pocket consume the same final JSON, readings, citations,
captions, and asset choices. The series build also preserves Xi'an at
`china/cities/xian/`; the compact destination menu switches between the two
books without changing their canonical content.

## Browser Gate

The destination-neutral QA ran in Google Chrome at `1440 x 1000` and at
`390 x 844` with device scale factor `2`.

- Desktop retains aligned Chinese, Japanese, and English columns, complete
  pinyin and furigana, the chapter rail, and the new destination menu.
- Mobile retains the destination, language, ruby, chapter, and section
  controls without overlap or page-level horizontal overflow.
- The Chapter 11 map uses a `760 px` pannable vector stage inside the `390 px`
  viewport. Left, centre, and right positions at `0`, `185`, and `370 px`,
  plus zoom and reset, pass inspection.
- Odawara Castle, Mishima Taisha, and Niihashi Sengen remain recognizable in
  all three mobile figures, each with exactly the four recurring guides.
- The dated final callout fits at mobile size with all three languages and
  readings intact.
- The menu successfully navigates from Hakone to Xi'an and loads Xi'an's 11
  chapters from its stable series path.
- No console error, failed request, content mismatch, missing ruby, clipped
  callout, or incoherent overlap was observed in either destination.

## Evidence

- Hakone browser report: `build/qa/hakone-website-release/qa.json`, SHA-256
  `1a261889fb15b3c1650cbaacead26700881c6ecea4f49034d4692486078e44bf`.
- Chapter 11 desktop viewport:
  `build/qa/hakone-website-release/desktop-11-viewport.png`, SHA-256
  `0c541fc32a4f0439335f5151bdba475364c6df7c3a43c7d769d5606a0932a2dd`.
- Chapter 11 mobile viewport:
  `build/qa/hakone-website-release/mobile-11-viewport.png`, SHA-256
  `7e443e658f36c3ba9bfa9058e72083df945f341900ebee0a6672aebc1afcee56`.
- Three-position mobile map contact:
  `build/qa/hakone-website-release/mobile-11-map-contact.jpg`, SHA-256
  `12e7caf588be4ad0a9f07808d814aec711b76bdf61d12fdce37442530b0753f6`.
- Mobile figure captures, in Odawara/Mishima/Gotemba order: SHA-256
  `6f7245ea884b4f3e9d39e81a84bea161e21d5a3c10353eb747e694c45523d2ec`,
  `7279432d87e37021648e5a06dfba75d0dd8ca87f0c451ff83297cec1197fa7f3`,
  and `93b26a4e4ce25a5311b7891abd60417d67b1d135d96c97bab6f06136689e32a8`.
- Xi'an regression report: `build/qa/xian-website-release/qa.json`, SHA-256
  `c188c0404f54d33e271bb75b16ff0da9f401c6147b129afa7348724ae5adf795`.
- Public workflow: GitHub Pages run `32418706768`, commit `d6818e1`.
- Public Xi'an verification: `75` files and `54,020,545` bytes matched source
  SHA-256 `c24e2d81f22973a32e51aa42c824c517a07d36d3b010f93850c5dc63162692e3`.
- Public Hakone verification: `158` files and `131,111,623` bytes matched
  source SHA-256
  `da8ccd33116884bd6f48d91de0b6e715ad2d6867de0622759c0b10faf33d624d`.
