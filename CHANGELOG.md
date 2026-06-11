# Changelog

## v0.1.0 — Publication-ready KUTRI prototype

Initial publication-ready release of the Kaş Urban-Territorial Resilience Index (KUTRI).

### Added
- Reproducible Python package structure under src/kutri/.
- Machine-readable 40-indicator dataset as the single source of truth.
- Five-pillar composite resilience index computation.
- Nominal and AHP-weighted composite score calculation.
- AHP consistency-ratio computation.
- Indicator-level Monte Carlo uncertainty analysis.
- Tornado sensitivity analysis.
- Executed Jupyter notebook workflow.
- Reproducibility tests.
- Methodology, data dictionary, limitations, and future-work documentation.
- Canonical audited report and archived legacy report structure.

### Fixed
- Clarified the difference between nominal policy weights and AHP eigenvector weights.
- Disclosed the P2.1 seasonally adjusted / dasymetric normalization basis.
- Removed misleading claims that AHP validates the nominal weights.
- Separated current reproducible engine outputs from legacy display-rounded report values.
- Cleaned the repository into a publication-ready structure.

### Current reproducible results
- Nominal KUTRI: 43.3 / 100
- AHP-weighted sensitivity result: 42.1 / 100
- Classification: Moderate-Low
