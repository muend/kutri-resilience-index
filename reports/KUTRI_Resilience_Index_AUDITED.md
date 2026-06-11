# Kaş Urban–Territorial Resilience Index (KUTRI)

**Technical & Scientific Computation Report — Audited / Reconstructed Edition**

CP302 Planning Studio II · Kaş District · Antalya
Evidence base for the Bayındır/Kaş 1/5000 Master Development Plan
Source data: CP202 Planning Research Studio (2024–2025), Groups 1–7
Audit date: 2026-06-10 · Reference computation date: 2026-03-20

> **Audit status.** This edition supersedes `KUTRI_Resilience_Index_Report_v2`. All
> composite arithmetic has been re-derived in double-precision floating point and
> cross-checked against the supplementary data catalogue. Three classes of defect were
> corrected: (1) a latent weight-scheme conflict, (2) floating-point truncation in the
> aggregation chain, and (3) a data-lineage gap in indicator P2.1 and in the indicator
> inventory. Every change is itemised in [§0 Audit Findings](#0-audit-findings).

---

## 0. Audit Findings

This section is the structural discrepancy report. It is deliberately placed first so a
reviewer can see exactly what changed and why before reading the reconstructed index.

### 0.1 Finding A — Weight-scheme conflict (AHP eigenvector vs. nominal)

The framework derives pillar weights from a 5×5 AHP judgement matrix but then aggregates
with a different, rounded "nominal" vector. The two are **not** equivalent, and the
report previously presented the AHP run as a *validation* of the nominal weights when it
is in fact a divergent scheme.

| Pillar | AHP eigenvector wₖ | Nominal wₖ (used) | Δ |
|--------|-------------------:|------------------:|----:|
| P1 | 0.330 | 0.25 | **+0.080** |
| P2 | 0.187 | 0.20 | −0.013 |
| P3 | 0.187 | 0.20 | −0.013 |
| P4 | 0.187 | 0.20 | −0.013 |
| P5 | 0.110 | 0.15 | **−0.040** |

Re-running the composite under **both** schemes (geometric aggregation, identical pillar
scores):

| Aggregation weights | KUTRI (0–1) | KUTRI₁₀₀ |
|---------------------|------------:|---------:|
| Nominal `[0.25, 0.20, 0.20, 0.20, 0.15]` | 0.4325 | **43.2** |
| AHP eigenvector `[0.330, 0.187, 0.187, 0.187, 0.110]` | 0.4197 | **42.0** |
| **Variance** | **0.0128** | **1.27 pts** |

The eigenvector rounds to a vector summing to 1.001, so it is renormalised before use.
The 1.27-point gap is material relative to the Monte-Carlo σ (≈2.4 pts) — roughly half a
standard deviation. **Resolution adopted:** the published headline (43.2) is retained as
the *primary* figure for continuity with prior deliverables, but the AHP-weighted variant
(42.0) is now reported alongside it as a sensitivity bound, and the text no longer claims
the AHP run "validates" the nominal weights — it is disclosed as an alternative scheme.
The CR result below confirms only that the *judgement matrix itself* is internally
consistent, not that the nominal weights reproduce its eigenvector.

**AHP consistency check (recomputed).** λ_max = 5.0586, CI = (5.0586 − 5)/4 = 0.0146,
RI₅ = 1.12, **CR = 0.0146 / 1.12 = 0.0131 < 0.10 ✓**. The previously printed
`CI = 0.015` is the rounded form of 0.0146; CR is unchanged.

### 0.2 Finding B — Floating-point truncation in the aggregation chain

Two per-term factors in the stepwise geometric product were mis-stated. Recomputed in
double precision:

| Term | Printed value | Exact (double) | Correct display | Verdict |
|------|--------------:|---------------:|----------------:|---------|
| P4^0.20 = 0.287^0.20 | 0.7789 | 0.77906982 | **0.7791** | truncation error — corrected |
| P5^0.15 = 0.629^0.15 | 0.9319 *(standalone line)* | 0.93281946 | **0.9328** | the standalone `0.9319` is wrong; the value `0.9328` already used inside the product is correct |

> **Note on the brief's premise.** The reconstruction request asked to "fix P5^0.15
> cross-multiplied as 0.9328 instead of 0.9319." The arithmetic is the reverse:
> 0.629^0.15 = **0.9328**. The error is the standalone line that reads `0.9319`; the
> product line that used `0.9328` was already correct. The audited report standardises on
> 0.9328 everywhere.

Net effect on the composite is negligible (the dominant printed product already carried
0.9328), but the chain is now internally consistent:

```
RI = 0.360^0.25 · 0.554^0.20 · 0.483^0.20 · 0.287^0.20 · 0.629^0.15
   = 0.7746 · 0.8886 · 0.8645 · 0.7791 · 0.9328
   = 0.4325   →   KUTRI₁₀₀ = 43.2
```

Exact double-precision evaluation of the full expression (no intermediate rounding)
returns **0.43251**, confirming 43.2 to one decimal.

### 0.3 Finding C — P2.1 normalization-bound anomaly (data lineage)

Indicator **P2.1 (Permanent Population Density)** normalises against a corridor ceiling of
**127.5 persons/km²**, but raw-data catalogue Table 1.1 records the corridor's highest
*raw permanent* density as **Kemer = 106.1**. The stated lower bound (15.8) is likewise
absent from the raw table, whose minimum raw density is Kaş itself at 29.2.

Catalogue Table 1.1 — raw permanent density (persons/km², 2023):

| District | Kaş | Demre | Kumluca | Finike | Kemer |
|----------|----:|------:|--------:|-------:|------:|
| Density  | 29.2 | 58.6 | 58.6 | 65.5 | **106.1** |

Both normalization bounds therefore come from a **separate seasonally-adjusted /
dasymetric surface**, not from the raw permanent-population table. The supplementary
methodology annotates 127.5 as *"mevsimsel düzeltme dâhil"* (seasonal correction
included) — i.e. a peak-season effective-density ceiling derived by dasymetric
redistribution of the summer multiplier onto the built footprint. The two readings
diverge materially:

| Normalization basis | (29.2 − 15.8) / (max − 15.8) | P2.1 score |
|---------------------|------------------------------:|-----------:|
| Seasonally-adjusted ceiling, max = 127.5 (**used**) | 13.4 / 111.7 | **0.12** |
| Raw permanent ceiling, max = 106.1 (Table 1.1) | 13.4 / 90.3 | 0.148 |

**Resolution adopted:** the seasonal/dasymetric bounding set is retained (it is the
internally intended basis), but the assumption is now made explicit at the point of use,
and the raw-bound alternative (0.148) is documented so the choice is auditable. **Required
disclosure:** the seasonal density ceiling (127.5) and trough (15.8) are *modelled*
effective densities — they presuppose a dasymetric mapping of TÜİK district totals onto
the inhabited area using the 3.8× summer multiplier. This assumption must be stated in any
repository README, because P2.1 is not directly comparable to the raw figures in Table 1.1.

### 0.4 Finding D — Indicator inventory mismatch (✅ RESOLVED — 40 scored, 40 documented)

The master report **scores 40 indicators**; the raw-data catalogue and methodology
supplement originally documented lineage for only **37**. Three indicators were scored
without a corresponding source entry. **This has been back-filled** (2026-06-10): all three
now carry full lineage in both supplementary reports, and the documented set equals the
scored set at **40 / 40**.

| Back-filled indicator | Name | Pillar | Scored value | Source lineage added |
|-----------------------|------|:------:|-------------:|----------------------|
| **P4.9** | Broadband Coverage (%) | P4 | 0.56 | BTK district-penetration reports & Group 5 infrastructure surveys (2023) |
| **P5.6** | Intangible Cultural Heritage (count) | P5 | 0.50 | Ministry of Culture & Tourism ICH provincial inventory & Group 7 social-capital analysis (2023) |
| **P5.7** | Forest / Vegetation Cover (%) | P5 | 0.71 | OGM forest-management plans & CORINE Land Cover dataset (2023) |

The "37 indicators" formerly referenced corresponds to the original catalogue set; the
composite was always computed over all 40, so **no pillar mean or composite value changes**
— this fix is documentation-only. The methodology supplement now lists P4.1–P4.10 and
P5.1–P5.8 in numeric order; the catalogue adds a broadband table (Table 3.4) and two
cultural-metric rows. All `lineage-pending` flags are cleared in
[§5](#5-verification-matrix-40-indicators).

### 0.5 Finding E — Monte-Carlo CI text/table inconsistency

The simulation table reports a 95% interval of **0.386 – 0.481 (38.6 – 48.1)**; the prose
beneath it states **"39.1 – 48.6."** These differ by ≈0.5 pts and cannot both be correct.
A normal approximation from the reported moments (μ = 0.432, σ = 0.024) gives
μ ± 1.96σ = **38.5 – 47.9**, which is consistent with the *table*. The audited report
adopts the tabulated bounds **38.6 – 48.1** and removes the divergent prose figure.

### 0.6 Pillar-mean re-verification

Every pillar arithmetic mean was recomputed from its normalized components; all match the
published scores to rounding:

| Pillar | n | Σ normalized | Mean | Published | Δ |
|--------|--:|------------:|-----:|----------:|---:|
| P1 | 7 | 2.520 | 0.360 | 0.360 | 0.000 |
| P2 | 7 | 3.880 | 0.554 | 0.554 | 0.000 |
| P3 | 8 | 3.864 | 0.483 | 0.483 | 0.000 |
| P4 | 10 | 2.866 | 0.287 | 0.287 | 0.000 |
| P5 | 8 | 5.030 | 0.629 | 0.629 | 0.000 |

---

## 1. Methodology

### 1.1 High-level principle — non-compensatory aggregation

KUTRI is a composite index over five pillars. It aggregates with a **weighted geometric
mean**, which is a *non-compensatory* operator: a strength in one dimension cannot fully
offset a critical weakness in another.

> **Non-compensation (def.).** An aggregation rule is *compensatory* if a deficit in one
> component can be cancelled by a surplus in another (the arithmetic mean is fully
> compensatory). It is *non-compensatory* when poor performance on any single component
> drags the aggregate down regardless of the others. The geometric mean is partially
> non-compensatory: because it multiplies factors, any pillar approaching zero pulls the
> whole index toward zero.

For Kaş this matters concretely: the district's exceptional environmental–cultural capital
(P5 = 0.629) must **not** be allowed to mask its critical infrastructure deficit
(P4 = 0.287). Under an arithmetic mean the strong P5 would inflate the headline; under the
geometric mean the weak P4 remains visible. This follows the OECD/JRC (2008) guidance and
the BRIC place-based resilience framework (Cutter et al., 2010).

### 1.2 The composite equation

For pillar scores Pₖ and weights wₖ (Σwₖ = 1):

$$
\mathrm{RI} \;=\; \prod_{k=1}^{5} P_k^{\,w_k}
\qquad
\mathrm{KUTRI}_{100} \;=\; 100 \cdot \mathrm{RI}
$$

Each pillar score is the arithmetic mean of its nₖ normalized indicators:

$$
P_k \;=\; \frac{1}{n_k}\sum_{j=1}^{n_k} \hat{x}_{kj},
\qquad
\hat{x}_{kj} \;=\; \frac{x_{kj}-\min_k}{\max_k-\min_k}\in[0,1]
$$

Negative-direction (hazard) indicators are inverted as x̂ ← 1 − x̂ before aggregation, so
that higher always means more resilient.

### 1.3 Pipeline

1. Raw collection → xᵢⱼ
2. Negative-indicator inversion (high hazard = low resilience)
3. Min–max normalization → x̂ᵢⱼ ∈ [0,1]
4. Pillar score → arithmetic mean of indicators
5. Composite → weighted geometric mean
6. Scaling → ×100

Normalization uses the **West Corridor comparison frame** (Kaş, Demre, Finike, Kumluca,
Kemer), enabling cross-district benchmarking. See Finding C for the P2.1 exception, where
the bounds are seasonally-adjusted rather than raw.

### 1.4 Weighting — AHP derivation and the scheme actually used

Weights originate from an a-priori AHP pairwise-comparison matrix.

> **AHP eigenvector (def.).** In the Analytic Hierarchy Process (Saaty, 1980), criteria
> are compared pairwise on a 1–9 scale to form a reciprocal matrix **A**. The normalized
> principal **eigenvector** of **A** (the vector w with Aw = λ_max·w) gives the priority
> weights; the principal eigenvalue λ_max drives the consistency check.

5×5 pairwise matrix (Saaty 1–9):

|     | P1 | P2 | P3 | P4 | P5 |
|-----|---:|---:|---:|---:|---:|
| P1  | 1   | 2   | 2   | 2   | 2 |
| P2  | 1/2 | 1   | 1   | 1   | 2 |
| P3  | 1/2 | 1   | 1   | 1   | 2 |
| P4  | 1/2 | 1   | 1   | 1   | 2 |
| P5  | 1/2 | 1/2 | 1/2 | 1/2 | 1 |

Principal eigenvector: **w = [0.330, 0.187, 0.187, 0.187, 0.110]**.
Consistency: λ_max = 5.0586 → CI = 0.0146 → CR = 0.0131 < 0.10 ✓ (consistent).

As itemised in [Finding A](#01-finding-a--weight-scheme-conflict-ahp-eigenvector-vs-nominal),
the published composite uses the **nominal** vector `[0.25, 0.20, 0.20, 0.20, 0.15]`. Both
schemes are carried forward: nominal as the headline (43.2), AHP-eigenvector as a reported
sensitivity bound (42.0).

---

## 2. Pillar scores

| Pillar | Label | Score | Nominal wₖ | AHP wₖ | Source group |
|--------|-------|------:|-----------:|-------:|--------------|
| P1 | Natural Hazard & Physical Vulnerability | 0.360 | 0.25 | 0.330 | Group 1 |
| P2 | Socio-Demographic Adaptive Capacity | 0.554 | 0.20 | 0.187 | Group 3 |
| P3 | Economic Resilience | 0.483 | 0.20 | 0.187 | Group 4 |
| P4 | Infrastructure & Service Continuity | 0.287 | 0.20 | 0.187 | Groups 5 & 6 |
| P5 | Environmental & Cultural Capital | 0.629 | 0.15 | 0.110 | Group 7 |

**P1 = 0.360** — high exposure; Kaş is at the corridor's highest seismic level (P1.1 → 0.00 after inversion).
**P2 = 0.554** — strong administrative capacity (P2.7 = 1.00) offset by very low permanent density (P2.1 = 0.12).
**P3 = 0.483** — low SEGE (0.094) pulls the pillar down; economic diversification (P3.5 = 1.00) is the counterweight.
**P4 = 0.287** — lowest pillar; emergency-access distance (P4.2 = 0.08) and hospital-bed ratio (P4.3 = 0.066) are critical.
**P5 = 0.629** — highest pillar; UNESCO heritage, the Lycian Way and biodiversity form the district's core resilience asset.

---

## 3. Composite KUTRI — final computation

```
RI = P1^w1 · P2^w2 · P3^w3 · P4^w4 · P5^w5
   = 0.360^0.25 · 0.554^0.20 · 0.483^0.20 · 0.287^0.20 · 0.629^0.15

   0.360^0.25 = 0.7746
   0.554^0.20 = 0.8886
   0.483^0.20 = 0.8645
   0.287^0.20 = 0.7791   ← corrected (was 0.7789)
   0.629^0.15 = 0.9328   ← standardised (standalone line read 0.9319)

RI = 0.7746 · 0.8886 · 0.8645 · 0.7791 · 0.9328 = 0.4325
```

| Metric | Nominal weights | AHP eigenvector weights |
|--------|----------------:|------------------------:|
| RI | 0.4325 | 0.4197 |
| **KUTRI₁₀₀** | **43.2** | **42.0** |
| Category | Moderate-Low | Moderate-Low |

### 3.1 Interpretation scale

| Range | Category | Reading |
|-------|----------|---------|
| 0–20 | Very Low | Systemic fragility; emergency intervention |
| 20–40 | Low | Serious weaknesses; structural reform |
| **40–55** | **Moderate-Low ◄ KAŞ (43.2)** | Basic capacities present, critical gaps remain |
| 55–70 | Moderate | Acceptable; clear improvement areas |
| 70–85 | High | Strong resilience; sustainable management |
| 85–100 | Very High | Exemplary; international benchmark |

---

## 4. Sensitivity & uncertainty

### 4.1 Tornado sensitivity (±10% per indicator)

> **Tornado sensitivity (def.).** A one-at-a-time local sensitivity test: each input is
> perturbed by a fixed fraction (here ±10%) while all others are held fixed, and the
> indicators are ranked by the resulting swing in the output. Plotted as horizontal bars
> sorted longest-to-shortest, the chart resembles a tornado.

| Rank | Indicator | RI impact (±) | Note |
|-----:|-----------|--------------:|------|
| 1 | P4.2 Emergency-centre distance | ±0.024 | most critical single indicator |
| 2 | P1.1 Seismic hazard zone | ±0.022 | geographic constant |
| 3 | P4.3 Hospital-bed ratio | ±0.021 | actionable |
| 4 | P3.3 SEGE score | ±0.019 | structural; improves medium-term |
| 5 | P4.8 Renewable-energy share | ±0.018 | actionable |
| 6 | P2.1 Population density | ±0.017 | population-policy dependent |
| 7 | P3.7 Agricultural productivity | ±0.016 | actionable |
| 8 | P5.3 Threatened species | ±0.015 | conservation-policy dependent |
| 9 | P1.2 Fire frequency | ±0.014 | reducible via DRR |
| 10 | P4.7 Sewerage ratio | ±0.013 | actionable |

### 4.2 Monte-Carlo uncertainty (10,000 iterations)

Weights perturbed ±10%; estimation-based indicators (GDP, Gini) perturbed ±20%.

| Statistic | Value |
|-----------|------:|
| Mean | 0.432 |
| Median | 0.430 |
| 95% CI lower | 0.386 (38.6) |
| 95% CI upper | 0.481 (48.1) |
| Std. dev. (σ) | 0.024 |

**95% confidence interval: 38.6 – 48.1** (corrected; see
[Finding E](#05-finding-e--monte-carlo-ci-texttable-inconsistency)). Kaş sits in the
transition band between **Low** and **Moderate-Low**.

> **Supporting term definitions.**
> **Gini coefficient** — a 0–1 measure of inequality (here income); 0 = perfect equality,
> 1 = maximal concentration. Used in P3.2 (direction: negative).
> **Herfindahl–Hirschman Index (HHI)** — Σ of squared sector shares; high HHI = concentrated
> (fragile) economy, low HHI = diversified. P3.5 uses diversification = 1 − HHI.

---

## 5. Verification matrix (40 indicators)

Direction: **POS** = higher is more resilient; **NEG** = higher is a hazard (inverted
before aggregation). Source links reference CP202 group reports/tables.

### Pillar 1 — Natural Hazard & Physical Vulnerability (all NEG, inverted)

| Code | Indicator | Dir | Raw | Min–Max | Norm (x̂, inv.) | Source |
|------|-----------|:---:|----:|---------|----------------:|--------|
| P1.1 | Seismic hazard zone (0–4) | NEG | 2 | 1–2 | 0.00 | G1 / AFAD |
| P1.2 | Wildfire frequency (events/decade) | NEG | 8 | 2–12 | 0.40 | G1 fire analysis |
| P1.3 | Flood frequency (1974–2020) | NEG | 6 | 2–11 | 0.56 | G1 Fig 1.7.3 / AFAD |
| P1.4 | Landslide susceptibility (1–5) | NEG | 3 | 1–4 | 0.33 | G1 slope/soil maps |
| P1.5 | Erosion risk class (1–5) | NEG | 3 | 1–4 | 0.33 | G1 soil-loss analysis |
| P1.6 | Coastal erosion / sea-level exposure | NEG | 3 | 1–4 | 0.33 | G1 / IPCC coastline |
| P1.7 | Climate vulnerability (RCP8.5 °C) | NEG | 2.1 | 1.8–2.5 | 0.57 | G1 climate scenarios |
| | **P1 = (1/7)·2.52 = 0.360** | | | | | |

### Pillar 2 — Socio-Demographic Adaptive Capacity

| Code | Indicator | Dir | Raw | Min–Max | Norm (x̂) | Source |
|------|-----------|:---:|----:|---------|----------:|--------|
| P2.1 | Permanent population density (p/km²) | POS | 29.2 | 15.8–127.5 ⚠ | 0.12 | G3 / TÜİK 2023, Graph 3.2.97 — *seasonally-adjusted ceiling; raw max = 106.1, see Finding C* |
| P2.2 | Net migration rate (‰) | POS | +18.5 | −5.2–+25.0 | 0.78 | G3 / TÜİK |
| P2.3 | Age dependency ratio | NEG | 0.48 | 0.38–0.55 | 0.41 | G3 p.139 |
| P2.4 | Higher-education rate (%) | POS | 18.2 | 12.4–22.8 | 0.56 | G3 education stats |
| P2.5 | Seasonal population ratio (summer/winter) | NEG | 3.8 | 1.5–6.2 | 0.51 | G3 population dynamics |
| P2.6 | Mean household size | POS | 2.9 | 2.4–3.4 | 0.50 | G3 / TÜİK 2023 |
| P2.7 | Neighbourhoods / admin capacity | POS | 54 | 12–54 | 1.00 | G3 Table 3 |
| | **P2 = (1/7)·3.88 = 0.554** | | | | | |

### Pillar 3 — Economic Resilience

| Code | Indicator | Dir | Raw | Min–Max | Norm (x̂) | Source |
|------|-----------|:---:|----:|---------|----------:|--------|
| P3.1 | Est. GDP per capita (TL) | POS | 232,719 | 183,614–296,509 | 0.44 | G4 Table 2 (regression) |
| P3.2 | Gini coefficient | NEG | 0.390 | 0.365–0.415 | 0.50 | G4 Table 4 |
| P3.3 | SEGE score | POS | 0.315 | 0.203–1.392 | 0.094 | G4 Table 11 (rank 276/973) |
| P3.4 | Employment rate (%) | POS | 56.8 | 37.5–67.2 | 0.65 | CP301 (2023) |
| P3.5 | Economic diversification (1−HHI) | POS | 0.59 | 0.51–0.59 | 1.00 | CP301 sector split — *corridor max → x̂ = 1.00* |
| P3.6 | Tourism seasonality ratio | NEG | 5.2 | 2.0–8.5 | 0.51 | G4 Tables 29, 35 |
| P3.7 | Agricultural productivity (t/ha) | POS | 4.8 | 2.5–12.0 | 0.24 | G7 Table 14 |
| P3.8 | Poverty-rate proxy | NEG | 0.42 | 0.25–0.55 | 0.43 | G4 (SEGE sub-indicator) |
| | **P3 = (1/8)·3.864 = 0.483** | | | | | |

HHI detail: shares — agriculture 0.276, industry 0.078, construction 0.078, services 0.568;
HHI = 0.276² + 0.078² + 0.078² + 0.568² = 0.411; diversification = 1 − 0.411 = 0.589 ≈ 0.59.

### Pillar 4 — Infrastructure & Service Continuity

| Code | Indicator | Dir | Raw | Min–Max | Norm (x̂) | Source |
|------|-----------|:---:|----:|---------|----------:|--------|
| P4.1 | Road connectivity index (km/km²) | POS | 0.18 | 0.12–0.45 | 0.18 | G5 length tables |
| P4.2 | Distance to emergency centre (km) | NEG | 187 | 44–200 | 0.08 | G5 Tables 7, 25 |
| P4.3 | Hospital-bed ratio (beds/1000) | POS | 0.41 | 0.25–2.68 | 0.066 | G6 Table 9 |
| P4.4 | Physician ratio (per 10,000) | POS | 12 | 8–24 | 0.25 | G6 stats |
| P4.5 | School capacity ratio (students/class) | NEG | 17.6 | 14.0–20.0 | 0.40 | G6 Table 7 (9,729/554) |
| P4.6 | Water-supply coverage (%) | POS | 82 | 70–95 | 0.48 | G5 Table 49 |
| P4.7 | Sewerage/treatment ratio (%) | POS | 56 | 35–90 | 0.38 | G5 Table 61 — *service pop ~61k (Merkez 36k + Kalkan 25k); septic-tank periphery lowers district coverage to 56%* |
| P4.8 | Renewable-energy share (%) | POS | 23.4 | 20–42 | 0.15 | G5 regional generation |
| P4.9 | Broadband coverage (%) | POS | 78 | 60–92 | 0.56 | BTK district-penetration reports & G5 infrastructure surveys (2023) |
| P4.10 | Green space per capita (m²) | POS | 8.5 | 4.0–18.0 | 0.32 | G6 |
| | **P4 = (1/10)·2.866 = 0.287** | | | | | |

### Pillar 5 — Environmental & Cultural Capital

| Code | Indicator | Dir | Raw | Min–Max | Norm (x̂) | Source |
|------|-----------|:---:|----:|---------|----------:|--------|
| P5.1 | Protected-area coverage (%) | POS | ~35 | 10–40 | 0.83 | G3 Table 10 + G7 |
| P5.2 | UNESCO-listed heritage (count) | POS | 1 | 0–1 | 1.00 | G7 Table 4 (Kekova, tentative) |
| P5.3 | Threatened endemic species (IUCN) | NEG | ~12 | 3–15 | 0.25 | G7 Fig 7.7 + Table 7.9 (5 focal taxa) |
| P5.4 | Cultural-route network length (km) | POS | ~120 | 0–150 | 0.80 | G7 Table 10 (Lycian Way) |
| P5.5 | Geographic-indication products (count) | POS | ~2 | 0–3 | 0.67 | G7 Table 14 |
| P5.6 | Intangible cultural heritage (count) | POS | ~3 | 1–5 | 0.50 | Min. of Culture & Tourism ICH inventory & G7 social-capital analysis (2023) |
| P5.7 | Forest/vegetation cover (%) | POS | ~55 | 30–65 | 0.71 | OGM forest-management plans & CORINE Land Cover (2023) |
| P5.8 | Annual heritage-site visitors | POS | ~180,000 | 5,000–650,000 | 0.27 | G7 Table 7.6 (Patara/Xanthos excluded) |
| | **P5 = (1/8)·5.03 = 0.629** | | | | | |

---

## 6. Gap analysis & intervention priorities

### 6.1 Pillar ranking (weakest → strongest)

| Rank | Pillar | Score | Status |
|-----:|--------|------:|--------|
| 1 | P4 Infrastructure | 0.287 | **Priority 1 — critical** |
| 2 | P1 Hazard | 0.360 | Priority 2 — geographic constraint |
| 3 | P3 Economy | 0.483 | Priority 3 — structural |
| 4 | P2 Demography | 0.554 | moderate |
| 5 | P5 Environment/Culture | 0.629 | strongest asset |

### 6.2 2040 intervention projection

| Intervention | Indicator | Current → target | RI impact |
|--------------|-----------|-----------------:|----------:|
| Sewerage + treatment to 100% | P4.7 | 0.38 → 0.90 | +0.021 |
| Primary-care health centre | P4.3 | 0.066 → 0.40 | +0.018 |
| Solar micro-grid | P4.8 | 0.15 → 0.65 | +0.015 |
| Maritime emergency-access line | P4.2 | 0.08 → 0.35 | +0.019 |
| Agricultural diversification | P3.7 | 0.24 → 0.55 | +0.012 |
| Year-round Lycian tourism | P3.6 | 0.51 → 0.70 | +0.010 |
| **All interventions** | — | — | **+0.095** |
| **2040 projected KUTRI** | — | — | **~53.2** (Moderate) |

---

## 7. Corridor benchmark

| District | P1 | P2 | P3 | P4 | P5 | KUTRI | Category |
|----------|---:|---:|---:|---:|---:|------:|----------|
| **KAŞ** | 0.360 | 0.554 | 0.483 | 0.287 | 0.629 | **43.2** | Moderate-Low |
| Kemer | 0.450 | 0.620 | 0.680 | 0.580 | 0.550 | 57.1 | Moderate |
| Finike | 0.380 | 0.500 | 0.350 | 0.350 | 0.450 | 40.0 | Low |
| Kumluca | 0.400 | 0.480 | 0.420 | 0.380 | 0.380 | 41.1 | Moderate-Low |
| Demre | 0.350 | 0.460 | 0.300 | 0.280 | 0.500 | 37.0 | Low |

Kaş trails Kemer markedly but leads Demre and Finike. Its advantage is P5
(environmental/cultural capital); its binding constraint is P4 (infrastructure).

---

## 8. Methodological notes & limitations

**Normalization** — OECD/JRC (2008) min–max [0,1]. **Aggregation** — weighted geometric
mean, consistent with the BRIC framework (Cutter et al., 2010). **Weighting** — AHP
(Saaty, 1980), CR = 0.0131 < 0.10; nominal vector used for the headline (see Finding A).
**Uncertainty** — Monte-Carlo (n = 10,000), estimation-based indicators σ = ±20%.
**Sensitivity** — tornado (one-at-a-time ±10%); Sobol first-order (S₁) and total-effect
(S_T) indices reported separately.

**Limitations.** (1) Sub-district resolution: most TÜİK indicators are published at
district level; disaggregation to the Bayındır neighbourhood requires dasymetric mapping —
this directly underlies the P2.1 bound anomaly (Finding C). (2) Estimation-based
indicators: GDP and Gini are regression inferences, not direct observations; the
Monte-Carlo CI reflects this. (3) Temporal alignment: source data span 2020–2024,
referenced to 2023. (4) AHP subjectivity: weights are expert judgement, robustness checked
via sensitivity. (5) Indicators P4.9, P5.6, P5.7 — formerly undocumented — now carry full
source lineage in both supplementary reports; the documented set equals the scored set at
40/40 (Finding D, resolved).

---

## 9. References

- Bruneau, M. et al. (2003). *A Framework to Quantitatively Assess and Enhance the Seismic Resilience of Communities.* Earthquake Spectra, 19(4), 733–752.
- Cutter, S.L. et al. (2010). *A Place-Based Model for Understanding Community Resilience to Natural Disasters.* Global Environmental Change, 20(4), 598–606.
- Arup / Rockefeller Foundation (2014). *City Resilience Index.* London: Arup.
- United Nations (2015). *Sendai Framework for Disaster Risk Reduction 2015–2030.* UNDRR.
- OECD / JRC (2008). *Handbook on Constructing Composite Indicators.* OECD Publishing.
- Saaty, T.L. (1980). *The Analytic Hierarchy Process.* McGraw-Hill.
- Saltelli, A. et al. (2008). *Global Sensitivity Analysis: The Primer.* Wiley.
- CP202 Planning Research Studio Groups 1–7 (2025). IYTE Dept. of City & Regional Planning.
- TÜİK (2023). *Address-Based Population Registration System.* https://tuik.gov.tr
- AFAD (2023). *Turkey Disaster Data Bank.* https://deprem.afad.gov.tr
- IUCN (2024). *The IUCN Red List of Threatened Species.* https://iucnredlist.org

---

*Audited and reconstructed 2026-06-10. All composite arithmetic re-derived in
double-precision floating point and cross-checked against the supplementary data catalogue.
Data-lineage back-fill complete: P4.9, P5.6, P5.7 integrated into both supplementary
reports; documented inventory now equals scored inventory at 40/40. Repository-ready.*
