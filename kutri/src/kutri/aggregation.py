"""Pillar means and weighted geometric aggregation (non-compensatory)."""
from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

from .schema import Indicator, PILLAR_ORDER
from .normalization import normalize_indicator


def pillar_scores(indicators: List[Indicator], clamp: bool = True) -> Dict[str, float]:
    """Arithmetic mean of normalized indicators within each pillar."""
    buckets: Dict[str, List[float]] = {p: [] for p in PILLAR_ORDER}
    for ind in indicators:
        score = normalize_indicator(
            ind.raw_value, ind.min_value, ind.max_value, ind.direction, clamp
        )
        buckets[ind.pillar].append(score)
    return {p: float(np.mean(v)) for p, v in buckets.items()}


def weighted_geometric_mean(
    scores: Sequence[float], weights: Sequence[float]
) -> float:
    """Double-precision weighted geometric mean. Weights are renormalized to sum 1."""
    s = np.asarray(scores, dtype=np.float64)
    w = np.asarray(weights, dtype=np.float64)
    if w.sum() == 0:
        raise ValueError("weights sum to zero")
    w = w / w.sum()
    s = np.clip(s, 1e-12, 1.0)  # guard log(0); non-compensatory behaviour preserved
    return float(np.exp(np.sum(w * np.log(s))))


def composite_kutri(
    pillars: Dict[str, float], weights: Sequence[float], scale: float = 100.0
) -> float:
    """Composite KUTRI on a 0-`scale` display range from pillar scores + weights."""
    ordered = [pillars[p] for p in PILLAR_ORDER]
    return weighted_geometric_mean(ordered, weights) * scale
