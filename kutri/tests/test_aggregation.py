"""Aggregation primitives tests."""
import numpy as np
import pytest

from kutri.aggregation import weighted_geometric_mean, pillar_scores, composite_kutri
from kutri.schema import load_indicators, PILLAR_ORDER


def test_geometric_mean_equal_weights():
    # geometric mean of [0.25, 1.0] with equal weights = 0.5
    assert weighted_geometric_mean([0.25, 1.0], [0.5, 0.5]) == pytest.approx(0.5)


def test_geometric_mean_is_non_compensatory():
    # a near-zero component drags the aggregate far below the arithmetic mean
    g = weighted_geometric_mean([0.01, 0.99], [0.5, 0.5])
    arith = np.mean([0.01, 0.99])
    assert g < arith
    assert g == pytest.approx(0.0995, abs=0.001)


def test_weights_renormalized():
    # AHP-style weights summing to 1.001 should be renormalized, not error
    v = weighted_geometric_mean([0.5, 0.5, 0.5, 0.5, 0.5],
                                [0.330, 0.187, 0.187, 0.187, 0.110])
    assert v == pytest.approx(0.5)


def test_pillar_keys():
    pillars = pillar_scores(load_indicators())
    assert set(pillars) == set(PILLAR_ORDER)


def test_composite_scaling():
    pillars = pillar_scores(load_indicators())
    c = composite_kutri(pillars, [0.25, 0.20, 0.20, 0.20, 0.15], scale=100.0)
    assert 0 <= c <= 100
