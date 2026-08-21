# Chapter 3 Reading Review

Status: reviewed on `2026-08-21`.

## Contract

- Chinese uses tone-marked Hanyu Pinyin over the matching Chinese token.
- Japanese uses furigana only on kanji-bearing tokens, including reviewed
  readings for Chinese place names and historical offices.
- Concatenating token text reconstructs every canonical paragraph exactly.
- The B6 pocket and website consume the same reviewed arrays.

## Chinese Pass

The place and history forms were checked as complete units:

- `五泉（wǔquán）`, `金城郡（jīnchéngjùn）`,
  `金城县（jīnchéngxiàn）`, and `城关（chéngguān）`;
- `张掖路（zhāngyè lù）`, `兰州府城隍庙（lánzhōufǔ
  chénghuángmiào）`, and `中山桥（zhōngshānqiáo）`;
- `甘肃巡抚（gānsù xúnfǔ）`, `甘肃布政使司（gānsù
  bùzhèngshǐsī）`, `巩昌（gǒngchāng）`, `临洮府（líntáofǔ）`, and
  `陕甘总督（shǎn-gān zǒngdū）`;
- `天兰铁路（tiānlán tiělù）` and `陇海铁路（lǒnghǎi tiělù）`.

The hyphen in `shǎn-gān` prevents the two province abbreviations from being
misread as one syllable.

## Japanese Pass

The retained Chinese names use stable guide readings:

- `五泉（ごせん）`, `金城郡（きんじょうぐん）`,
  `張掖路（ちょうえきろ）`, and `城隍廟（じょうこうびょう）`;
- `甘粛巡撫（かんしゅくじゅんぶ）`,
  `甘粛布政使司（かんしゅくふせいしし）`, `鞏昌（きょうしょう）`,
  `臨洮府（りんとうふ）`, and `陝甘総督（せんかんそうとく）`;
- `天蘭鉄道（てんらんてつどう）` and
  `隴海鉄道（ろうかいてつどう）`.

The surrounding Japanese was retokenized after the independent line edit and
checked against the final paragraph text.

## Validation

- Chapter 3 Chinese: `865` tokens across nine aligned blocks.
- Chapter 3 Japanese: `1,211` tokens across nine aligned blocks.
- Combined Chapters 1-3: `2,297` Chinese tokens and `2,971` Japanese tokens.
- Exact source-text reconstruction passes for every Chinese and Japanese
  block.
- `scripts/validate_readings.py` reports no candidate layer, missing Han
  reading, invalid pinyin/furigana, or reconstruction mismatch.
