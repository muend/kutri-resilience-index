"""Analytic Hierarchy Process: eigenvector weights and consistency ratio.

The AHP consistency ratio (CR) confirms ONLY the internal logical consistency of
the pairwise judgement matrix. It does NOT validate any separate (e.g. nominal
policy) weight scheme. See docs/METHODOLOGY.md.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

# Saaty random-index values for consistency-ratio denominator, by matrix order n.
RANDOM_INDEX = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41}


@dataclass(frozen=True)
class AHPResult:
    weights: np.ndarray
    lambda_max: float
    ci: float
    cr: float
    n: int

    @property
    def is_consistent(self) -> bool:
        return self.cr < 0.10


def _validate_reciprocal(matrix: np.ndarray) -> None:
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("AHP matrix must be square")
    n = matrix.shape[0]
    if not np.allclose(np.diag(matrix), 1.0):
        raise ValueError("AHP matrix diagonal must be all 1s")
    for i in range(n):
        for j in range(n):
            if not np.isclose(matrix[i, j] * matrix[j, i], 1.0, rtol=1e-6):
                raise ValueError(f"AHP matrix not reciprocal at ({i},{j})")


def compute_ahp_weights(matrix: np.ndarray) -> np.ndarray:
    """Normalized principal eigenvector (priority weights) of a reciprocal matrix."""
    matrix = np.asarray(matrix, dtype=np.float64)
    _validate_reciprocal(matrix)
    eigvals, eigvecs = np.linalg.eig(matrix)
    idx = int(np.argmax(eigvals.real))
    w = eigvecs[:, idx].real
    w = w / w.sum()
    return w


def consistency_ratio(matrix: np.ndarray) -> AHPResult:
    """Full AHP consistency diagnostics: weights, lambda_max, CI, CR."""
    matrix = np.asarray(matrix, dtype=np.float64)
    _validate_reciprocal(matrix)
    n = matrix.shape[0]
    eigvals, eigvecs = np.linalg.eig(matrix)
    idx = int(np.argmax(eigvals.real))
    lambda_max = float(eigvals[idx].real)
    w = eigvecs[:, idx].real
    w = w / w.sum()
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RANDOM_INDEX.get(n)
    if ri is None or ri == 0.0:
        cr = 0.0
    else:
        cr = ci / ri
    return AHPResult(weights=w, lambda_max=lambda_max, ci=ci, cr=cr, n=n)


def load_pairwise_matrix(path: str | Path) -> np.ndarray:
    """Load an AHP pairwise-comparison matrix from a labelled CSV."""
    rows: List[List[float]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # header row of pillar labels
        for line in reader:
            rows.append([float(x) for x in line[1:]])  # drop row label
    return np.array(rows, dtype=np.float64)
