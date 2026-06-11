"""Indicator schema and dataset loading/validation."""
from __future__ import annotations

import csv
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List

PILLAR_ORDER = ["P1", "P2", "P3", "P4", "P5"]

VALID_DIRECTIONS = {"POS", "NEG"}
VALID_UNCERTAINTY = {"observed", "estimated", "proxy", "modelled", "expert_judgement"}

# Default per-class Monte-Carlo perturbation fractions (uniform +/- around 1.0).
UNCERTAINTY_PERTURBATION = {
    "observed": 0.05,
    "estimated": 0.20,
    "proxy": 0.25,
    "modelled": 0.20,
    "expert_judgement": 0.0,   # handled via weight sensitivity, not indicator jitter
}

REQUIRED_COLUMNS = [
    "code", "pillar", "pillar_label", "indicator_name", "direction",
    "raw_value", "min_value", "max_value", "unit", "normalization_basis",
    "normalized_value_reported", "year", "source_group",
    "source_table_or_figure", "source_note", "uncertainty_class",
    "public_redistributable", "limitations_note",
]


@dataclass(frozen=True)
class Indicator:
    """Immutable schema for a single KUTRI indicator (single source of truth)."""
    code: str
    pillar: str
    pillar_label: str
    indicator_name: str
    direction: str
    raw_value: float
    min_value: float
    max_value: float
    unit: str
    normalization_basis: str
    normalized_value_reported: float
    year: str
    source_group: str
    source_table_or_figure: str
    source_note: str
    uncertainty_class: str
    public_redistributable: str
    limitations_note: str

    def __post_init__(self) -> None:
        if self.direction not in VALID_DIRECTIONS:
            raise ValueError(f"{self.code}: direction must be POS/NEG, got {self.direction!r}")
        if self.uncertainty_class not in VALID_UNCERTAINTY:
            raise ValueError(f"{self.code}: invalid uncertainty_class {self.uncertainty_class!r}")
        if self.max_value == self.min_value:
            raise ValueError(f"{self.code}: zero-range bounds (min == max == {self.min_value})")

    @property
    def is_positive(self) -> bool:
        return self.direction == "POS"

    @property
    def uses_raw_corridor_bounds(self) -> bool:
        return self.normalization_basis == "raw_corridor_minmax"


def default_data_path() -> Path:
    """Locate the packaged indicator dataset relative to the repo root."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "data" / "processed" / "kutri_indicators.csv"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("kutri_indicators.csv not found in any parent data/processed/")


def load_indicators(path: str | Path | None = None) -> List[Indicator]:
    """Load the 40-indicator dataset from CSV into Indicator dataclasses."""
    path = Path(path) if path else default_data_path()
    field_names = {f.name for f in fields(Indicator)}
    float_fields = {"raw_value", "min_value", "max_value", "normalized_value_reported"}
    indicators: List[Indicator] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"Dataset missing required columns: {missing}")
        for row in reader:
            kwargs = {k: row[k] for k in field_names}
            for k in float_fields:
                kwargs[k] = float(kwargs[k])
            indicators.append(Indicator(**kwargs))
    return indicators


def validate_dataset(indicators: List[Indicator], expected_count: int = 40) -> None:
    """Raise if the dataset violates structural expectations; warn on lineage gaps."""
    if len(indicators) != expected_count:
        raise ValueError(f"Expected {expected_count} indicators, got {len(indicators)}")
    codes = [i.code for i in indicators]
    if len(set(codes)) != len(codes):
        dupes = {c for c in codes if codes.count(c) > 1}
        raise ValueError(f"Duplicate indicator codes: {sorted(dupes)}")
    for ind in indicators:
        if ind.pillar not in PILLAR_ORDER:
            raise ValueError(f"{ind.code}: unknown pillar {ind.pillar!r}")
        # source lineage completeness
        for fld in ("source_group", "source_table_or_figure"):
            if not getattr(ind, fld).strip():
                raise ValueError(f"{ind.code}: empty lineage field {fld}")
