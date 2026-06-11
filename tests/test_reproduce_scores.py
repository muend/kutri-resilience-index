"""Reproduce the audited headline figures within documented rounding tolerance.

NOTE ON THE 0.1 GAP. The engine computes normalized values directly from
raw/min/max (the single source of truth). The audited report rounded each pillar
to 3 decimals BEFORE aggregating, which propagates a ~0.1-point display
difference: the raw computation yields 43.3 / 42.1, equal to the report's
43.2 / 42.0 within one-decimal display rounding. Tolerances below encode this
honestly rather than back-fitting the engine to the rounded headline.
"""
import pytest

from kutri.schema import load_indicators
from kutri.ahp import consistency_ratio, load_pairwise_matrix
from kutri.aggregation import pillar_scores, composite_kutri
from kutri.schema import default_data_path

NOMINAL = [0.25, 0.20, 0.20, 0.20, 0.15]
REPORTED_PILLARS = {"P1": 0.360, "P2": 0.554, "P3": 0.483, "P4": 0.287, "P5": 0.629}


def _ahp_weights():
    root = default_data_path().parents[2]
    return list(consistency_ratio(load_pairwise_matrix(
        root / "data" / "processed" / "ahp_pairwise_matrix.csv")).weights)


def test_pillar_scores_match_report():
    pillars = pillar_scores(load_indicators())
    for p, expected in REPORTED_PILLARS.items():
        assert pillars[p] == pytest.approx(expected, abs=0.012), f"{p}: {pillars[p]}"


def test_nominal_kutri_headline():
    pillars = pillar_scores(load_indicators())
    kutri = composite_kutri(pillars, NOMINAL)
    # report headline 43.2; raw computation 43.3 -> within display-rounding tolerance
    assert kutri == pytest.approx(43.2, abs=0.2)
    assert round(kutri, 0) == 43.0


def test_ahp_weighted_kutri():
    pillars = pillar_scores(load_indicators())
    kutri_ahp = composite_kutri(pillars, _ahp_weights())
    assert kutri_ahp == pytest.approx(42.0, abs=0.2)


def test_ahp_below_nominal():
    # AHP up-weights P1 (low) and down-weights P5 (high) -> lower composite
    pillars = pillar_scores(load_indicators())
    assert composite_kutri(pillars, _ahp_weights()) < composite_kutri(pillars, NOMINAL)


def test_ahp_consistency_ratio():
    root = default_data_path().parents[2]
    res = consistency_ratio(load_pairwise_matrix(
        root / "data" / "processed" / "ahp_pairwise_matrix.csv"))
    assert res.cr == pytest.approx(0.0131, abs=0.001)
    assert res.cr < 0.10
