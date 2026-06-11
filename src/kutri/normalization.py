"""Min-max normalization with directional logic and bound validation."""
from __future__ import annotations

import warnings
from typing import List

from .schema import Indicator


def normalize_minmax(value: float, min_value: float, max_value: float) -> float:
    """Raw min-max scaling to [0, 1] (no directional inversion, no clamping)."""
    span = max_value - min_value
    if span == 0:
        raise ValueError("Zero-range bounds: min_value == max_value")
    return (value - min_value) / span


def normalize_indicator(
    value: float,
    min_value: float,
    max_value: float,
    direction: str,
    clamp: bool = True,
) -> float:
    """Directional normalization.

    POS: (value - min) / (max - min)
    NEG: 1 - (value - min) / (max - min)

    If `value` falls outside [min, max] the result leaves [0, 1]; a warning is
    raised and (if `clamp`) the value is clipped to the valid domain.
    """
    x = normalize_minmax(value, min_value, max_value)
    if direction == "NEG":
        x = 1.0 - x
    elif direction != "POS":
        raise ValueError(f"direction must be 'POS' or 'NEG', got {direction!r}")
    if x < 0.0 or x > 1.0:
        warnings.warn(
            f"Normalized value {x:.4f} outside [0,1] (value={value}, "
            f"bounds=[{min_value}, {max_value}]); "
            + ("clamping." if clamp else "not clamping."),
            RuntimeWarning,
        )
        if clamp:
            x = min(max(x, 0.0), 1.0)
    return x


def normalize_dataset(indicators: List[Indicator], clamp: bool = True) -> List[float]:
    """Compute normalized scores for every indicator in dataset order."""
    return [
        normalize_indicator(i.raw_value, i.min_value, i.max_value, i.direction, clamp)
        for i in indicators
    ]


def flag_non_raw_bounds(indicators: List[Indicator]) -> List[str]:
    """Return codes whose normalization bounds are NOT the raw corridor min/max.

    These require explicit disclosure (e.g. P2.1 seasonally-adjusted/dasymetric).
    """
    return [i.code for i in indicators if not i.uses_raw_corridor_bounds]
