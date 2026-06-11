# Methodology

## 1. Framework

KUTRI is a composite indicator over five pillars (P1–P5). Each pillar aggregates several
normalized indicators by arithmetic mean; the five pillar scores are combined by a weighted
geometric mean and scaled to 0–100.

```
x̂_kj = (x_kj − min_k) / (max_k − min_k)        # min-max normalization
x̂ ← 1 − x̂   if direction == NEG               # invert hazard / "lower is better"
P_k = mean_j x̂_kj                               # pillar score (arithmetic mean)
RI  = Π_k P_k^{w_k}                              # weighted geometric mean (Σ w_k = 1)
KUTRI_100 = 100 · RI
```

## 2. Non-compensatory aggregation

A weighted **geometric** mean is used instead of an arithmetic mean because it is partially
non-compensatory: since the pillars multiply, a pillar approaching zero drives the composite
toward zero. This prevents a strong pillar (here P5, environmental-cultural capital) from
masking a critical weakness (P4, infrastructure). Reference: OECD/JRC (2008), *Handbook on
Constructing Composite Indicators*; Cutter et al. (2010), BRIC framework.

## 3. Weighting — two distinct schemes

### 3.1 Nominal policy weights (headline)

`[P1, P2, P3, P4, P5] = [0.25, 0.20, 0.20, 0.20, 0.15]` — a design/policy choice. This
produces the headline KUTRI.

### 3.2 AHP eigenvector weights (sensitivity)

Derived from the 5×5 reciprocal pairwise-comparison matrix
(`data/processed/ahp_pairwise_matrix.csv`) by taking the normalized principal eigenvector:

`[0.330, 0.187, 0.187, 0.187, 0.110]`, with λ_max = 5.0586, CI = 0.0147, **CR = 0.0131**.

> **The AHP consistency ratio confirms ONLY the internal logical consistency of the
> judgement matrix. It does NOT validate the nominal weights.** The two schemes differ
> materially (AHP up-weights P1 by +0.08 and down-weights P5 by −0.04), producing different
> composites: nominal ≈ 43.2 vs AHP ≈ 42.0. We report both and never claim that AHP
> validates the nominal scheme.

## 4. Floating-point discipline

All computation is double precision. Normalized values are computed from raw/min/max at
run time; rounded values appear only for display. The audited report's display-rounded
headline is 43.2 / 42.0; computing from raw bounds yields 43.3 / 42.1. The ~0.1 difference
is rounding propagation (the report rounded pillars to 3 dp before aggregating) and is
encoded as a tolerance in `tests/test_reproduce_scores.py`. Corrected display factors:
`0.287^0.20 = 0.7791`, `0.629^0.15 = 0.9328`, exact RI ≈ 0.43251.

## 5. Normalization-bound provenance

Most indicators normalize against raw West-Corridor min/max (Kaş, Demre, Finike, Kumluca,
Kemer). The exception is **P2.1 Permanent Population Density**, which uses a
seasonally-adjusted / dasymetric *effective-density* ceiling of 127.5 persons/km² rather
than the raw permanent-density maximum of 106.1 (Kemer). This is disclosed via the
`normalization_basis` field and flagged by `normalization.flag_non_raw_bounds()`. Using the
raw max would change the P2.1 score from 0.12 to 0.148.

## 6. Uncertainty — Monte-Carlo

Indicator-level Monte-Carlo (`uncertainty.monte_carlo`, seed 42, 10,000 iterations). Each
indicator is perturbed by a uniform ± fraction set by its `uncertainty_class`:

| class | perturbation |
|-------|:------------:|
| observed | ±5% |
| estimated | ±20% |
| proxy | ±25% |
| modelled | ±20% |
| expert_judgement | 0% (handled via weight sensitivity) |

Perturbed values are re-normalized within their own bounds (clamped to the valid domain),
re-aggregated, and the composite distribution is summarized (mean, median, std, 2.5/97.5
percentiles). This **indicator-level** scheme is methodologically preferred over the legacy
**pillar-level** ±20% perturbation that produced the report's [38.6, 48.1]; the new scheme's
interval is exported to `outputs/monte_carlo_summary.csv`.

## 7. Sensitivity — tornado

One-at-a-time ±10% perturbation per indicator (`sensitivity.tornado_sensitivity`), ranked by
the half-range swing in the composite. Top-10 exported to `outputs/sensitivity_tornado.csv`.
The reproducible ranking differs from the legacy hand-reported ranking; the code output is
canonical. **Sobol variance-based indices are not implemented** — see
[`FUTURE_WORK.md`](FUTURE_WORK.md).

## References

- OECD / JRC (2008). *Handbook on Constructing Composite Indicators.*
- Cutter, S.L. et al. (2010). *A Place-Based Model for Understanding Community Resilience.*
- Saaty, T.L. (1980). *The Analytic Hierarchy Process.*
- Saltelli, A. et al. (2008). *Global Sensitivity Analysis: The Primer.*
