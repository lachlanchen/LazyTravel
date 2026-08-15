# Xi'an Guide-Cast Figure Review

Status: all current non-map figures passed cast continuity, factual-boundary,
B6-page, and mobile-web review on `2026-08-16`.

This review supersedes the figure-specific hashes and anonymous-person visual
evidence in the earlier Chapter 2-5 milestone reviews. Their prose and map
reviews remain valid historical records.

## Enforced Rule

- Every non-map figure contains at least Aya-chan and Lala Xia.
- New attraction plates use Aya, Lala, Sasa, and the Zhuangzi robot together
  when all four remain legible and the destination still leads the frame.
- The robot is a full guide and friend, not equipment.
- Maps remain character-free.
- External LALACHAN references stay read-only and hash-pinned in
  `data/sources/catalog.json`; only new compositions and technical provenance
  are published.
- `validate_figure_cast` in `scripts/build_xian_review.py` rejects a non-map
  asset whose provenance lacks either required guide reference.

## Current Figures

| Asset | PDF page | Guides | Subject boundary | Output SHA-256 | Mobile evidence SHA-256 |
| --- | ---: | --- | --- | --- | --- |
| Yongning Gate arrival | 7 | Aya, Lala, Sasa, Zhuangzi robot | Representative southern approach and city threshold; not an architectural survey or exact pedestrian viewpoint | `7dee351df65662620a39fe824706e586ba33e82f8dcb681276518854f2e7fa42` | `291303fc48ca83181a668158658987ce7a70960633d5d39b8e4a1d5a1820bf6b` |
| Daming Palace site impression | 25 | Aya, Lala, Sasa, Zhuangzi robot | Present-day scale study; no palace reconstruction or exact-view claim | `53c8c54deb4b6af60bbb64bba841d68ba2986576283e11e2b1a37edd0f6ec23a` | `efbc125fcd2fd61abb130be91ef070f06e24c36e36b3b07d1a18b256004a590a` |
| Terracotta Pit 1 first view | 36 | Aya, Lala, Sasa, Zhuangzi robot | Visitor-level hall impression; displayed pits are not presented as the whole mausoleum | `222d8891948875392b10a772b8e1dcce2fda08a02200e385517470aaedec1665` | `a619488f363c6d68aa0e9787e75471c710574ad5b28efd7e92fd1b438bc2d5e4` |
| Terracotta conservation teaching replicas | 41 | Aya, Lala | Modern replica workshop; no Qin artefact or real-laboratory claim | `f79824640189fb925041fd99f7e98165ff377e2f7ef765e283d4ad443b25e7f2` | `7333adcc3b6b0a0d63e5fcd0bd0b149236af5bf45ed75e1377ae179d1a27a571` |
| Big Wild Goose Pagoda courtyard view | 47 | Aya, Lala | Present-day scale and approach study; no claim about a specific crowd level or visit time | `361a6d70e84d4368e5cf3e389a3db6587839ab6e254fcb59c7b9b3ba1620fa96` | `d36737be41690c0383fef271c45b2fbde8579ee7e2b9dd433925630a2c34ce58` |
| Rubbing on a modern replica | 54 | Aya, Lala | Horizontal resin practice slab; no original-contact permission | `059d54d8078dec5895bbb64ded64def17134da9d0b744dd01be96138d5c67b06` | `b4ad0196386771ef502681a97826a45a7388f25b306399fa8fb84e25093b13f2` |
| Xi'an City Wall walk | 60 | Aya, Lala | Representative rampart width and skyline; no exact route-condition or access claim | `28a0a5be08146167a65ffd8bc613b70e09d0d8008c513935f036f42745322e23` | `7e56e048f8b0593faa1a793ee9664e05835592013726a1d64b5cb79cd66acdfe` |
| Bell Tower orientation | 62 | Aya, Lala, Sasa, Zhuangzi robot | Four-avenue orientation scene; no guarantee of traffic, crossing, or access conditions | `aa0414554c58d9132413fbb4975b1ca5e20e770639412408db63bca373c4289f` | `5dae304f6269ac3c090ee675f288a4c5bd34c6df0dfe9044be9b052ae0806753` |
| Lane-to-courtyard threshold | 69 | Aya, Lala | Generic access-etiquette scene; no named-property or open-access claim | `cf82a4a2d93b4344ca1d0b2d851cf4b88df1cfedddbc48fbfd5536b5904090bc` | `54f5a132f08a6fe112aa11009639cf852dae8c2e728f10f5c05e32a92ed3d0b2` |
| Paomo breaking table | 80 | Aya, Lala, Sasa, Zhuangzi robot | Representative dry-bowl sequence; no named restaurant or universal piece-size claim | `7b38c069ad7088192570be07393205eb579055fe0db6de0229a53098a189cd1e` | `4b5bd77431759356844be1baf95f485cbe0c658f812ad9c5dc71be778400401e` |
| Managed mountain day | 103 | Aya, Lala, Sasa, Zhuangzi robot | Representative managed path; no claim to depict a specific Huashan section | `8130f2cda9bcc710c7882d5bece90d0d10ee246337bb58d700c01c6a2041cff4` | `ece7b8cea339aac9d29a133d7d55108e56b9e25b7097af0a9587c56269dcfafe` |
| Xi'an North interchange | 107 | Aya, Lala, Sasa, Zhuangzi robot | Present-day station-forecourt decision scene; no claim of one universal exit, pickup zone, or crowd condition | `cc94fd3acac36e4029e2657c2396460aa4ee8b87cb272b501c3730ff86f74ced` | `3d8084713dda355fd13c69f7ccb54a2d6c4a1552d91424e8762e11160fa8ced4` |

## Visual Findings

- All outputs are `1536 x 1024` sRGB PNG files and remain clear in a `600 x
  400` proof, their actual B6 page, and a `390 px` mobile figure capture.
- Aya and Lala remain recognizable through head shape, clothing, proportions,
  and material treatment rather than labels or reader-facing production notes.
- The full-team Yongning Gate, Daming, Pit 1, Bell Tower, paomo, mountain, and
  Xi'an North scenes give the robot equal guide status without turning the
  place into a cast portrait.
- The teaching-replica scenes preserve the distinction between explaining a
  process and documenting or authorizing work on original heritage.
- Captions describe the travel subject and factual limit. Reference paths,
  generation method, hashes, and rights remain in technical provenance.
- Combined current-PDF figure-page sheet SHA-256:
  `9f105aee0abb7f77486fed5cdabbdeb13848f282203857892d520e432a647da6`.
- Combined mobile figure sheet SHA-256:
  `b311344af2359307e3eccaa99b2b72c119e1a180eb2678f95f97d35351f682cb`.
