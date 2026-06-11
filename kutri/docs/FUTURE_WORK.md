# Future Work — Generalized Resilience Index Engine

> **Status: not implemented.** This document is a controlled roadmap for a *separate, future*
> project. Nothing described here is built in the current repository. The current scope is
> strictly the Kaş/Bayındır KUTRI prototype.

The current KUTRI engine is deliberately structured (machine-readable dataset, schema
validation, pluggable normalization/weighting/aggregation) so it can later support a
generalized, multi-region resilience index. Two future directions are envisioned.

## Direction 1 — Manual multi-parameter calculator

A region-agnostic calculator where a user enters indicator values for any region and
receives a resilience score:

- Reuse `schema.Indicator`, `normalization`, `aggregation`, `ahp`, `uncertainty`,
  `sensitivity` unchanged.
- Add a region-configurable bounds set (each region or corridor supplies its own min/max).
- Provide a simple input form (CLI, then optionally Streamlit/FastAPI).
- Output the composite, pillar breakdown, uncertainty interval, and sensitivity table.

This is a natural, low-risk extension and the recommended **first** future milestone.

## Direction 2 — Optional AI-assisted open-data retrieval (later, gated)

A partially automated system where the user enters a city/region name and the system
assembles pillar-specific data from open reports and databases:

- Open-data connectors (statistical agencies, environmental/hazard datasets).
- Pillar-specific extraction with **source-confidence scoring**.
- Normalization against region-appropriate bounds.
- **Human-in-the-loop verification** before any score is published — no fully autonomous
  scoring.
- A web UI (Streamlit or FastAPI) presenting provenance alongside every value.

### Explicit non-goals for that future project (and absolute non-goals here)

- No web scraping, LLM data extraction, autonomous agents, or web app in the current repo.
- No claim of a "universal" or "scientifically proven" resilience model.
- Any automated value must remain auditable and human-verifiable; confidence and provenance
  must travel with each datum.

## Methodological extensions to consider later

- **Sobol variance-based sensitivity** (first-order S₁ and total-effect S_T) — currently
  only tornado (local, one-at-a-time) sensitivity is implemented.
- Correlation-aware uncertainty (joint perturbation of correlated indicators).
- Alternative aggregators (e.g. partially compensatory penalty functions) as comparators.
- Formal validation against independent resilience outcome data, if such data become
  available.
