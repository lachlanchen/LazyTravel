# Chapter 7 Reading Review

Status: reviewed on `2026-08-15`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over every Han-bearing token.
- Japanese uses hiragana furigana on kanji-bearing tokens; kana, Latin text,
  numerals, and punctuation remain unannotated.
- Concatenating token text reproduces the final Chinese or Japanese prose
  exactly.
- The B6 pocket PDF, practical bands, callouts, and website consume the same
  arrays in `data/china/cities/xian/book.json`.

## Editorial Audit

The Chinese pass reviewed the chapter's place and route vocabulary, including
`临潼 (líntóng)`, `华山 (huàshān)`, `华清宫 (huáqīnggōng)`,
`汉阳陵 (hàn yánglíng)`, `翠华山 (cuìhuáshān)`, `乾陵
(qiánlíng)`, `乾县 (qiánxiàn)`, `堰塞湖 (yànsèhú)`, `述圣纪碑
(shùshèngjìbēi)`, and `无字碑 (wúzìbēi)`. The safety sentence now
segments `身体 / 不适 / 时` as `shēntǐ / bùshì / shí`, rather than the
incorrect automatic grouping `不 / 适时`.

The Japanese pass reviewed names and archaeological terms independently,
including `臨潼（りんどう）`, `華山（かざん）`, `華山北駅
（かざんきたえき）`, `漢陽陵（かんようりょう）`, `翠華山
（すいかざん）`, `乾陵（けんりょう）`, `乾県（けんけん）`,
`唐御湯（とうぎょとう）`, `遺跡博物館（いせきはくぶつかん）`,
`崩積洞（ほうせきどう）`, `述聖紀碑（じゅつせいきひ）`, and
`無字碑（むじひ）`. `唐御湯` and `遺跡博物館` remain separate ruby
tokens so the long museum name can break cleanly at B6 size.

## Validation

- Chapter 7 Chinese: `1,260` tokens, including `1,056` ruby-bearing tokens.
- Chapter 7 Japanese: `1,630` tokens, including `724` ruby-bearing tokens.
- Full canonical book after Chapter 7: `7,463` Chinese tokens and `9,476`
  Japanese tokens.
- All `12` Chapter 7 reading arrays in each language are marked `reviewed`.
- `scripts/validate_readings.py` passes reconstruction, Han coverage, review
  status, and tone-mark checks.
