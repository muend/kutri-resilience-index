"""AHP eigenvector and consistency-ratio tests."""
import numpy as np
import pytest

from kutri.ahp import compute_ahp_weights, consistency_ratio, load_pairwise_matrix
from kutri.schema import default_data_path


def _matrix():
    root = default_data_path().parents[2]
    return load_pairwise_matrix(root / "data" / "processed" / "ahp_pairwise_matrix.csv")


def test_eigenvector_matches_published():
    w = compute_ahp_weights(_matrix())
    expected = np.array([0.330, 0.187, 0.187, 0.187, 0.110])
    assert np.allclose(w, expected, atol=0.005)


def test_weights_sum_to_one():
    w = compute_ahp_weights(_matrix())
    assert w.sum() == pytest.approx(1.0)


def test_consistency_ratio():
    res = consistency_ratio(_matrix())
    assert res.cr == pytest.approx(0.0131, abs=0.001)
    assert res.cr < 0.10
    assert res.is_consistent
    assert res.lambda_max == pytest.approx(5.0586, abs=0.01)


def test_non_reciprocal_matrix_raises():
    bad = np.array([[1, 2], [2, 1]], dtype=float)  # 2*2 != 1
    with pytest.raises(ValueError):
        consistency_ratio(bad)
