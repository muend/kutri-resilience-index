# Data — availability and licensing

## What is in this repository

- `processed/kutri_indicators.csv` — **derived indicator metadata**: the 40 indicators with
  raw values, normalization bounds, normalized values, source lineage, uncertainty class,
  and limitations notes.
- `processed/pillar_weights_nominal.json` — nominal policy weight scheme.
- `processed/ahp_pairwise_matrix.csv` — AHP pairwise-comparison matrix.

These are derived/aggregated values produced for the KUTRI study.

## What is NOT in this repository

The **raw CP202 Planning Research Studio (2024–2025) group reports** (Groups 1–7) are the
upstream primary sources for most indicators. They are **not redistributed here** and may be
subject to institutional permissions (IYTE Department of City and Regional Planning). Each
indicator's `source_group` and `source_table_or_figure` fields document where the value
originated so the lineage is transparent even though the raw documents are not included.

External national/EU datasets referenced for the back-filled indicators (BTK broadband
penetration, Ministry of Culture & Tourism ICH inventory, OGM forest-management plans,
CORINE Land Cover) are publicly available from their respective providers but are likewise
not bundled here.

## Redistribution

- Indicator metadata and computation logic: reusable for academic purposes with attribution.
- Raw source documents: **request permission** from the originating studio/agency.
- The `public_redistributable` column flags per-indicator redistribution status (currently
  `no` for all, since values derive from CP202 materials).

## Reproducibility without raw sources

All headline results are reproducible from the derived CSV alone — the raw documents are not
required to run the engine, tests, or notebook. They matter only for independently
re-deriving the raw indicator values.
