# KUTRI — Kaş Urban-Territorial Resilience Index

[![tests](https://github.com/OWNER/kutri/actions/workflows/tests.yml/badge.svg)](https://github.com/OWNER/kutri/actions/workflows/tests.yml)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![license](https://img.shields.io/badge/code-MIT-green)

> **KUTRI is a reproducible urban-territorial resilience index prototype for Kaş/Bayındır,
> Antalya, based on a five-pillar composite indicator framework.** It is a case-specific
> evidence base for planning decisions — *not* a universal or fully validated resilience model.

## Abstract

KUTRI quantifies the territorial resilience of the Kaş district (Antalya, Türkiye) by
combining 40 normalized indicators into five pillars — natural hazard, socio-demographic,
economic, infrastructure, and environmental-cultural — and aggregating them with a
non-compensatory weighted geometric mean. The framework derives candidate weights from an
Analytic Hierarchy Process (AHP) judgement matrix, computes a headline score under a
separate nominal policy-weight scheme, and quantifies robustness through reproducible
Monte-Carlo and tornado-sensitivity analyses. The headline result for Kaş is
**≈ 43.2 / 100 (Moderate-Low)**. The repository packages the dataset, computation engine,
tests, and documentation so a reviewer can clone, install, test, and reproduce the result.

## What KUTRI does

- Loads a machine-readable 40-indicator dataset (the single source of truth).
- Normalizes each indicator to [0, 1] with directional (positive/negative) logic.
- Aggregates indicators into five pillar scores (arithmetic mean) and a composite
  (weighted geometric mean).
- Derives AHP eigenvector weights from a 5×5 pairwise matrix and reports a weight-scheme
  sensitivity variant.
- Propagates uncertainty (indicator-level Monte-Carlo, fixed seed) and ranks drivers
  (tornado sensitivity).
- Exports result tables and figures to `outputs/`.

## Key result

| Quantity | Value |
|----------|-------|
| **Kaş KUTRI (nominal weights)** | **≈ 43.2 / 100 — Moderate-Low** (engine computes 43.3 from raw bounds; see note) |
| Kaş KUTRI (AHP eigenvector weights) | ≈ 42.0 / 100 (sensitivity variant) |
| AHP consistency ratio | CR = 0.0131 < 0.10 (matrix internally consistent) |
| Weakest pillar | P4 Infrastructure (0.288) |
| Strongest pillar | P5 Environmental & Cultural (0.629) |

> **Rounding note.** The engine calculates normalized values directly from raw/min/max, so
> the live composite is **43.3 / 100**. The audited report's display-rounded headline is
> 43.2; the ~0.1 gap is rounding propagation (pillars rounded to 3 dp before aggregating).
> Both figures are reported transparently and the test suite encodes this tolerance.

## Five-pillar framework

| Pillar | Label | Indicators | Score | Nominal weight | AHP weight |
|--------|-------|:---------:|------:|:--------------:|:----------:|
| P1 | Natural Hazard & Physical Vulnerability | 7 | 0.361 | 0.25 | 0.330 |
| P2 | Socio-Demographic Adaptive Capacity | 7 | 0.555 | 0.20 | 0.187 |
| P3 | Economic Resilience | 8 | 0.483 | 0.20 | 0.187 |
| P4 | Infrastructure & Service Continuity | 10 | 0.288 | 0.20 | 0.187 |
| P5 | Environmental & Cultural Capital | 8 | 0.629 | 0.15 | 0.110 |

The **nominal weights are a policy/design scheme and are *not* validated by the AHP
consistency ratio.** The AHP eigenvector is reported as a separate sensitivity scheme. See
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Why geometric aggregation

The weighted geometric mean is *partially non-compensatory*: because factors multiply, a
pillar approaching zero pulls the whole index down. This prevents Kaş's strong
environmental-cultural capital (P5) from masking its critical infrastructure deficit (P4) —
the behaviour an arithmetic mean would hide (OECD/JRC, 2008; Cutter et al., 2010).

## Reproducibility

```bash
git clone https://github.com/OWNER/kutri.git
cd kutri
python -m pip install -e ".[dev]"
pytest                                   # 27 tests
python -m kutri.reporting                # writes outputs/
jupyter nbconvert --execute --to notebook --inplace notebooks/KUTRI_Engine.ipynb
```

## Installation

Requires Python ≥ 3.9.

```bash
python -m pip install -e .          # runtime (numpy, pandas)
python -m pip install -e ".[dev]"   # + pytest, matplotlib, jupyter
```

## Quickstart

```python
from kutri.schema import load_indicators
from kutri.aggregation import pillar_scores, composite_kutri
from kutri.ahp import consistency_ratio, load_pairwise_matrix

inds = load_indicators()
pillars = pillar_scores(inds)
kutri = composite_kutri(pillars, [0.25, 0.20, 0.20, 0.20, 0.15])
print(round(kutri, 1))   # 43.3
```

## Data structure

`data/processed/kutri_indicators.csv` — 40 rows, 18 columns (code, pillar, direction, raw
value, bounds, unit, normalization basis, reported normalized value, year, source lineage,
uncertainty class, redistribution flag, limitations note). Full field definitions in
[`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md). Weight schemes live in
`pillar_weights_nominal.json` and `ahp_pairwise_matrix.csv`.

## Methodological caveats

- **Nominal ≠ AHP.** The headline uses nominal weights; the AHP run is a separate scheme.
  CR confirms only the AHP matrix's internal consistency.
- **P2.1 normalization bound.** Permanent Population Density normalizes against a
  seasonally-adjusted / dasymetric effective-density ceiling (127.5), *not* the raw
  permanent-density maximum (106.1, Kemer). Disclosed in the dataset and
  [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md); using the raw max would give 0.148 vs 0.12.
- **Estimation-based indicators.** GDP, Gini, SEGE proxies are regression inferences, not
  direct observations; reflected in `uncertainty_class` and Monte-Carlo perturbation.
- **Tornado ranking.** The reproducible indicator-level tornado differs from the legacy
  hand-reported ranking; the code output is canonical.

## Known limitations

See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md). Summary: single-district prototype;
corridor-relative bounds collapse some ranges (P1.1, P2.7, P3.5 sit at a bound); Sobol
indices are **not** implemented (future work); raw CP202 source documents may not be
publicly redistributable (see Data availability).

## Repository structure

```
kutri/
  README.md  LICENSE  CITATION.cff  pyproject.toml  requirements.txt  .gitignore
  data/processed/      kutri_indicators.csv, pillar_weights_nominal.json, ahp_pairwise_matrix.csv
  notebooks/           KUTRI_Engine.ipynb
  src/kutri/           schema, normalization, ahp, aggregation, uncertainty, sensitivity, reporting, plotting
  tests/               27 tests across 5 modules
  reports/             KUTRI_Resilience_Index_AUDITED.md (canonical) + supplementary/ + archive/
  docs/                METHODOLOGY, DATA_DICTIONARY, LIMITATIONS, FUTURE_WORK
  outputs/             result CSVs + figures/
  .github/workflows/   tests.yml
```

## Citation

See [`CITATION.cff`](CITATION.cff). Please cite as a case-specific prototype, not a
validated universal model.

## License

Code is released under the **MIT License** ([`LICENSE`](LICENSE)). Derived indicator
metadata and documentation are intended for academic reuse with attribution; raw CP202
studio source documents are **not** redistributed here and may require permission (see
[`data/README.md`](data/README.md)).

## Future work

A future, separate project will generalize this into a multi-region resilience index — first
a manual multi-parameter calculator, later an optional AI-assisted open-data retrieval
system with source-confidence scoring and human-in-the-loop verification. **None of that is
implemented here.** Scope and design notes: [`docs/FUTURE_WORK.md`](docs/FUTURE_WORK.md).
