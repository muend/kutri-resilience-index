# Data Dictionary

## `data/processed/kutri_indicators.csv`

40 rows (one per indicator), 18 columns.

| Column | Type | Description |
|--------|------|-------------|
| `code` | str | Indicator code, e.g. `P4.9`. Unique. |
| `pillar` | str | Pillar id: `P1`–`P5`. |
| `pillar_label` | str | Human-readable pillar name. |
| `indicator_name` | str | Indicator name (English). |
| `direction` | str | `POS` (higher = more resilient) or `NEG` (higher = hazard; inverted). |
| `raw_value` | float | Observed/estimated raw value for Kaş. |
| `min_value` | float | Lower normalization bound. |
| `max_value` | float | Upper normalization bound. |
| `unit` | str | Measurement unit. |
| `normalization_basis` | str | `raw_corridor_minmax` or `seasonally_adjusted_dasymetric_effective_density`. |
| `normalized_value_reported` | float | Normalized value as published in the audited report (audit reference only; the engine recomputes from raw). |
| `year` | str | Reference period of the raw value. |
| `source_group` | str | Source CP202 group or external institution. |
| `source_table_or_figure` | str | Specific table/figure/dataset. |
| `source_note` | str | Provenance note. |
| `uncertainty_class` | str | `observed`, `estimated`, `proxy`, `modelled`, or `expert_judgement`. |
| `public_redistributable` | str | `yes`/`no` — whether the underlying raw source may be redistributed. |
| `limitations_note` | str | Indicator-specific caveat. |

## Indicator inventory (40)

| Pillar | Codes | n |
|--------|-------|:-:|
| P1 Natural Hazard | P1.1–P1.7 | 7 |
| P2 Socio-Demographic | P2.1–P2.7 | 7 |
| P3 Economic | P3.1–P3.8 | 8 |
| P4 Infrastructure | P4.1–P4.10 | 10 |
| P5 Environmental & Cultural | P5.1–P5.8 | 8 |

Three indicators (P4.9 Broadband, P5.6 Intangible Cultural Heritage, P5.7 Forest/Vegetation
Cover) were back-filled during the audit (Finding D resolved); their sources are external
national/EU datasets (BTK, Ministry of Culture & Tourism ICH inventory, OGM/CORINE) rather
than CP202 group reports, as noted in `source_note`.

## `data/processed/pillar_weights_nominal.json`

The nominal policy weight scheme. Contains an explicit disclaimer that it is **not**
validated by the AHP consistency ratio.

## `data/processed/ahp_pairwise_matrix.csv`

The 5×5 reciprocal AHP pairwise-comparison matrix (Saaty 1–9 scale), labelled rows/columns
P1–P5. Consumed by `kutri.ahp.load_pairwise_matrix`.

## Uncertainty classes

| Class | Meaning | MC perturbation |
|-------|---------|:---------------:|
| `observed` | Directly measured / official statistic | ±5% |
| `estimated` | Regression or modelled estimate | ±20% |
| `proxy` | Indirect proxy variable | ±25% |
| `modelled` | Scenario / dasymetric model output | ±20% |
| `expert_judgement` | Expert-assigned (weights) | via weight sensitivity |
