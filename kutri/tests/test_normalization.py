"""Normalization correctness and domain-handling tests."""
import warnings

import pytest

from kutri.normalization import normalize_minmax, normalize_indicator, flag_non_raw_bounds
from kutri.schema import load_indicators


def test_minmax_basic():
    assert normalize_minmax(5, 0, 10) == 0.5


def test_zero_range_raises():
    with pytest.raises(ValueError):
        normalize_minmax(5, 5, 5)


def test_positive_direction():
    assert normalize_indicator(5, 0, 10, "POS") == 0.5


def test_negative_direction_inverts():
    assert normalize_indicator(5, 0, 10, "NEG") == 0.5
    assert normalize_indicator(2, 0, 10, "NEG") == pytest.approx(0.8)


def test_out_of_range_warns_and_clamps():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        v = normalize_indicator(15, 0, 10, "POS", clamp=True)
    assert v == 1.0
    assert any(issubclass(x.category, RuntimeWarning) for x in w)


def test_all_normalized_within_unit_interval():
    inds = load_indicators()
    for i in inds:
        v = normalize_indicator(i.raw_value, i.min_value, i.max_value, i.direction)
        assert 0.0 <= v <= 1.0, f"{i.code} -> {v}"


def test_p21_flagged_as_non_raw_bound():
    inds = load_indicators()
    flagged = flag_non_raw_bounds(inds)
    assert "P2.1" in flagged
    p21 = next(i for i in inds if i.code == "P2.1")
    assert p21.normalization_basis == "seasonally_adjusted_dasymetric_effective_density"
    assert "106.1" in p21.limitations_note or "106.1" in p21.source_note
