# Xi'an Cover Underlay Prompt

Use case: `stylized-concept`.

Create only a text-free illustrated underlay for the existing B6 portrait
LazyTravel Xi'an cover. Treat the rendered current cover as a geometry mask:
leave the top header strip, the full left and central title field, the
description field, and the lower-left footer field bright and quiet. Reproduce
none of the reference page's text, rules, logos, letters, numbers, or marks.

Build a polished realistic editorial diorama on a clean paper-white field. A
low grey-brick city-wall form enters from the lower-right edge. Aya-chan, Lala
Xia, Sasa-kun, and the Zhuangzi robot appear exactly once, together, in the
lower-right blank zone. Keep their established tactile forms: Aya is the
red-panda girl in a navy sailor uniform, Lala is the rounded panda in beige
overalls, Sasa is the boy in a panda hoodie, and Zhuangzi is the compact
white-and-black articulated robot. A slim Big Wild Goose Pagoda may rise only
along the extreme right margin; a small Bell Tower roofline may sit behind the
guides. These elements are a symbolic cover composition, not a geographic
claim.

Use bright natural studio daylight, crisp masonry and fabric detail, vivid
green foliage, and restrained coral, teal, and cobalt accents. Keep all detail
away from the live title and footer positions. Output no text, pseudo-writing,
watermark, logo, route line, border, decorative blob, additional person,
duplicate guide, night lighting, sepia cast, or dark full-bleed background.

References used for generation:

- `build/research/xian/current-cover-text-reference.png`: layout mask only.
- `assets/images/xian/xian-south-gate-hotel-arrival.png`: four-guide identity
  and material continuity.
- `build/research/xian/visual-references/city-wall-official.png`: wall material
  and silhouette.
- `build/research/xian/visual-references/bell-tower-official.jpg`: Bell Tower
  roof form.
- `build/research/xian/visual-references/big-wild-goose-official.jpg`: Big Wild
  Goose Pagoda proportions.

The final project asset is cropped and resampled to `1476 x 2079` pixels, the
exact B6 page ratio at 300 dpi, before it is placed beneath live LaTeX text.
