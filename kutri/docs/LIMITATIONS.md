# Limitations

KUTRI is a **prototype / case-specific** index. It is an evidence base for Kaş/Bayındır
planning decisions, not a universal or fully validated resilience model. The following
limitations are stated honestly and should be read before any use of the results.

## 1. Single-district scope

The index is calibrated to one district within one comparison corridor (Kaş, Demre, Finike,
Kumluca, Kemer). Bounds and scores are corridor-relative and not transferable to other
regions without recalibration.

## 2. Collapsed ranges / boundary saturation

Several indicators sit exactly at a corridor bound, so their normalized scores are 0 or 1
and carry little discriminating information:

| Indicator | Issue |
|-----------|-------|
| P1.1 Seismic hazard | corridor range is only 1–2; Kaš at ceiling → score 0.00 |
| P2.7 Neighbourhoods | Kaš is the corridor maximum → score 1.00 |
| P3.5 Economic diversification | Kaš is the corridor maximum → score 1.00 |
| P5.2 UNESCO heritage | binary 0/1 → score 1.00 |

## 3. P2.1 normalization-bound anomaly (disclosed, not hidden)

Permanent Population Density normalizes against a **seasonally-adjusted / dasymetric
effective-density** ceiling of 127.5 persons/km², not the raw permanent-density maximum of
106.1 (Kemer). This is a deliberate methodological choice but means P2.1 is not directly
comparable to the raw density table. Raw-bound alternative score: 0.148 (vs 0.12 used).
Flagged programmatically by `normalization.flag_non_raw_bounds()`.

## 4. Estimation-based indicators

GDP per capita, Gini, SEGE sub-proxies, and several P5 counts are regression inferences or
approximate estimates, not direct observations. They carry `uncertainty_class` of
`estimated` or `proxy` and receive wider Monte-Carlo perturbation.

## 5. Rounding propagation

The engine computes from raw bounds (KUTRI = 43.3); the audited report's display-rounded
headline is 43.2. The ~0.1 difference is documented and encoded as a test tolerance, not
silently reconciled.

## 6. Sensitivity / Sobol

Tornado (one-at-a-time) sensitivity is implemented and reproducible, but its ranking differs
from the legacy hand-reported ranking — the code output is canonical. **Sobol
variance-based indices are NOT implemented**; any earlier mention of Sobol is reclassified
as future work (see [`FUTURE_WORK.md`](FUTURE_WORK.md)).

## 7. Data availability

Raw CP202 studio group reports are not redistributed in this repository and may require
permission. The repo includes only **derived indicator metadata** and computation logic.
See [`../data/README.md`](../data/README.md).

## 8. Weighting subjectivity

Both weight schemes embed judgement. The nominal scheme is a policy choice; the AHP scheme
is expert pairwise judgement. Neither is empirically validated against observed resilience
outcomes — no ground-truth resilience labels exist for the corridor.

## 9. Temporal heterogeneity

Source data span 2020–2024, referenced to 2023. Indicators are not all from the same year.
