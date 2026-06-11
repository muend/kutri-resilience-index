"""Reproducible Monte-Carlo uncertainty propagation at the indicator level."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Sequence

import numpy as np

from .schema import Indicator, PILLAR_ORDER, UNCERTAINTY_PERTURBATION
from .normalization import normalize_indicator
from .aggregation import weighted_geometric_mean


@dataclass(frozen=True)
class MonteCarloSummary:
    n_iterations: int
    seed: int
    mean: float
    median: float
    std: float
    ci_low: float
    ci_high: float
    scale: float

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)


def monte_carlo(
    indicators: List[Indicator],
    weights: Sequence[float],
    n_iter: int = 10_000,
    seed: int = 42,
    scale: float = 100.0,
    perturbation_by_class: Dict[str, float] | None = None,
) -> MonteCarloSummary:
    """Indicator-level Monte-Carlo.

    Each indicator's raw value is perturbed by a uniform +/- fraction set by its
    uncertainty_class (see schema.UNCERTAINTY_PERTURBATION), re-normalized within
    its own bounds (clamped to the valid domain), re-aggregated to pillar means,
    then to the weighted geometric composite. Reproducible via fixed `seed`.
    """
    pert = dict(UNCERTAINTY_PERTURBATION)
    if perturbation_by_class:
        pert.update(perturbation_by_class)

    rng = np.random.default_rng(seed)
    raw = np.array([i.raw_value for i in indicators], dtype=np.float64)
    fracs = np.array([pert.get(i.uncertainty_class, 0.0) for i in indicators])
    pillar_idx = {p: [k for k, i in enumerate(indicators) if i.pillar == p] for p in PILLAR_ORDER}
    w = np.asarray(weights, dtype=np.float64)

    results = np.empty(n_iter, dtype=np.float64)
    for it in range(n_iter):
        factors = rng.uniform(1.0 - fracs, 1.0 + fracs)
        perturbed = raw * factors
        norm = np.array([
            normalize_indicator(perturbed[k], ind.min_value, ind.max_value, ind.direction, clamp=True)
            for k, ind in enumerate(indicators)
        ])
        pillars = [float(np.mean(norm[pillar_idx[p]])) for p in PILLAR_ORDER]
        results[it] = weighted_geometric_mean(pillars, w) * scale

    lo, hi = np.percentile(results, [2.5, 97.5])
    return MonteCarloSummary(
        n_iterations=n_iter, seed=seed,
        mean=float(results.mean()), median=float(np.median(results)),
        std=float(results.std()), ci_low=float(lo), ci_high=float(hi), scale=scale,
    )
