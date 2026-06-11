"""One-at-a-time tornado sensitivity at the indicator level."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

import numpy as np

from .schema import Indicator, PILLAR_ORDER
from .normalization import normalize_indicator
from .aggregation import weighted_geometric_mean


@dataclass(frozen=True)
class SensitivityRow:
    code: str
    indicator_name: str
    pillar: str
    impact: float  # half-range swing in composite (display units) from +/-delta


def _composite(indicators: List[Indicator], weights: Sequence[float],
               override_idx: int, override_value: float, scale: float) -> float:
    pillar_vals = {p: [] for p in PILLAR_ORDER}
    for k, ind in enumerate(indicators):
        v = override_value if k == override_idx else ind.raw_value
        pillar_vals[ind.pillar].append(
            normalize_indicator(v, ind.min_value, ind.max_value, ind.direction, clamp=True)
        )
    pillars = [float(np.mean(pillar_vals[p])) for p in PILLAR_ORDER]
    return weighted_geometric_mean(pillars, weights) * scale


def tornado_sensitivity(
    indicators: List[Indicator],
    weights: Sequence[float],
    delta: float = 0.10,
    scale: float = 100.0,
    top: int | None = 10,
) -> List[SensitivityRow]:
    """Perturb each indicator by +/-`delta` (fraction); rank by composite swing.

    Impact = (composite_high - composite_low) / 2, i.e. the +/- half-range.
    """
    rows: List[SensitivityRow] = []
    for k, ind in enumerate(indicators):
        hi = _composite(indicators, weights, k, ind.raw_value * (1 + delta), scale)
        lo = _composite(indicators, weights, k, ind.raw_value * (1 - delta), scale)
        rows.append(SensitivityRow(
            code=ind.code, indicator_name=ind.indicator_name,
            pillar=ind.pillar, impact=abs(hi - lo) / 2.0,
        ))
    rows.sort(key=lambda r: r.impact, reverse=True)
    return rows[:top] if top else rows
