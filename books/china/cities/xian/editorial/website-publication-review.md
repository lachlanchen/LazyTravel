# Xi'an Website Publication Review

Status: passed on `2026-08-16`.

Public URL: <https://lachlanchen.github.io/LazyTravel/>

## Deployment Evidence

- GitHub Pages is configured for HTTPS workflow deployment.
- Deployment workflow: `.github/workflows/pages.yml`.
- Published commit: `caac30e32e7d2ad4659f70f5f1d05d6fa8a942e8`.
- Successful Actions run:
  <https://github.com/lachlanchen/LazyTravel/actions/runs/31933869782>.
- Canonical Xi'an JSON SHA-256:
  `b3bba63be1fef2cf39c16b0335550ebe158d5f1b0ed3e4cca60c8f4f36895198`.
- The post-deployment verifier fetched and hashed all `74` manifest files,
  totaling `54,013,731` bytes, and compared the live payload with the complete
  canonical public JSON projection.

## Public Browser QA

- Chromium desktop review at `1440 x 1000` passed for all 11 chapters.
- Chromium mobile review at `390 x 844`, device scale factor `2`, passed for
  all 11 chapters, ten maps, fifteen figures, navigation, and ruby controls.
- The public render contains `125` aligned blocks, `18,640` ruby nodes, and
  `219` chapter-source entries.
- No console error, failed request, page-level horizontal overflow,
  sticky-header overlap, missing map, missing figure, or clipped callout was
  detected.
- Public browser QA JSON SHA-256:
  `98c86947005c780343a4df2fc767bdc403af417c60b966bafcab6a60e29ddc94`.

## Visual Evidence

- `build/qa/site/xian-public-caac30e/desktop-ch01.png`
- `build/qa/site/xian-public-caac30e/desktop-ch11.png`
- `build/qa/site/xian-public-caac30e/mobile-ch11-figure.png`
- `build/qa/site/xian-public-caac30e/mobile-ch11-highlight.png`

Xi'an has passed the complete destination gate: canonical multilingual JSON,
reviewed pinyin and furigana, reproducible B6 pocket PDF, Nutstore hash sync,
public synchronized website, source and asset provenance, page review, public
browser review, and verified GitHub publication.
