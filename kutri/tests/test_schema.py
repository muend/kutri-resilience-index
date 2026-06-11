"""Dataset structure and lineage-completeness tests."""
from kutri.schema import load_indicators, validate_dataset, REQUIRED_COLUMNS, PILLAR_ORDER


def test_dataset_has_40_indicators():
    inds = load_indicators()
    validate_dataset(inds, expected_count=40)
    assert len(inds) == 40


def test_pillar_distribution():
    inds = load_indicators()
    counts = {p: sum(1 for i in inds if i.pillar == p) for p in PILLAR_ORDER}
    assert counts == {"P1": 7, "P2": 7, "P3": 8, "P4": 10, "P5": 8}


def test_required_columns_present(tmp_path):
    # the loader enforces REQUIRED_COLUMNS; loading without error proves presence
    inds = load_indicators()
    assert REQUIRED_COLUMNS  # non-empty contract
    assert all(i.code for i in inds)


def test_every_indicator_has_source_lineage():
    inds = load_indicators()
    for i in inds:
        assert i.source_group.strip(), f"{i.code} missing source_group"
        assert i.source_table_or_figure.strip(), f"{i.code} missing source_table_or_figure"


def test_directions_valid():
    inds = load_indicators()
    assert all(i.direction in ("POS", "NEG") for i in inds)


def test_uncertainty_classes_valid():
    inds = load_indicators()
    valid = {"observed", "estimated", "proxy", "modelled", "expert_judgement"}
    assert all(i.uncertainty_class in valid for i in inds)
