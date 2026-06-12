# KUTRI — Kaş Urban-Territorial Resilience Index

[![tests](https://github.com/muend/kutri-resilience-index/actions/workflows/tests.yml/badge.svg)](https://github.com/muend/kutri-resilience-index/actions/workflows/tests.yml)
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
**≈ 43.3 / 100 (Moderate-Low)**. The repository packages the dataset, computation engine,
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
| **Kaş KUTRI (nominal weights)** | **≈ 43.3 / 100 — Moderate-Low** |
| Kaş KUTRI (AHP eigenvector weights) | ≈ 42.1 / 100 (sensitivity variant) |
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
git clone [https://github.com/muend/kutri-resilience-index.git](https://github.com/muend/kutri-resilience-index.git)
cd kutri-resilience-index
python -m pip install -e ".[dev]"
pytest                                   # 27 tests
python -m kutri.reporting                # writes outputs/
jupyter nbconvert --execute --to notebook --inplace notebooks/KUTRI_Engine.ipynb