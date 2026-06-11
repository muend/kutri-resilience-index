"""KUTRI: Kaş Urban-Territorial Resilience Index.

A reproducible, case-specific five-pillar composite indicator framework for the
Kaş/Bayındır district, Antalya. This package provides the computation engine:
schema validation, min-max normalization, AHP weight derivation, weighted
geometric aggregation, Monte-Carlo uncertainty, and tornado sensitivity.

This is a prototype / case-specific index, not a universal or fully validated
resilience model. See docs/LIMITATIONS.md.
"""

from .schema import Indicator, load_indicators, validate_dataset, PILLAR_ORDER
from .normalization import normalize_minmax, normalize_indicator
from .ahp import compute_ahp_weights, consistency_ratio
from .aggregation import pillar_scores, weighted_geometric_mean, composite_kutri
from .uncertainty import monte_carlo
from .sensitivity import tornado_sensitivity

__version__ = "1.0.0"

__all__ = [
    "Indicator", "load_indicators", "validate_dataset", "PILLAR_ORDER",
    "normalize_minmax", "normalize_indicator",
    "compute_ahp_weights", "consistency_ratio",
    "pillar_scores", "weighted_geometric_mean", "composite_kutri",
    "monte_carlo", "tornado_sensitivity",
    "__version__",
]
