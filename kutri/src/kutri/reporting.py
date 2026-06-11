"""End-to-end report generation: computes everything and writes outputs/ tables.

Run as a module:  python -m kutri.reporting
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List

from .schema import load_indicators, validate_dataset, PILLAR_ORDER, default_data_path
from .normalization import normalize_indicator, flag_non_raw_bounds
from .ahp import consistency_ratio, load_pairwise_matrix
from .aggregation import pillar_scores, composite_kutri
from .uncertainty import monte_carlo
from .sensitivity import tornado_sensitivity

NOMINAL_WEIGHTS = [0.25, 0.20, 0.20, 0.20, 0.15]


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "data" / "processed").exists():
            return parent
    return Path.cwd()


def _ahp_weights_ordered(root: Path) -> List[float]:
    matrix = load_pairwise_matrix(root / "data" / "processed" / "ahp_pairwise_matrix.csv")
    return list(consistency_ratio(matrix).weights)


def build_results() -> Dict:
    root = repo_root()
    indicators = load_indicators(default_data_path())
    validate_dataset(indicators, expected_count=40)

    pillars = pillar_scores(indicators)
    ahp = consistency_ratio(load_pairwise_matrix(root / "data" / "processed" / "ahp_pairwise_matrix.csv"))
    ahp_weights = list(ahp.weights)

    kutri_nominal = composite_kutri(pillars, NOMINAL_WEIGHTS)
    kutri_ahp = composite_kutri(pillars, ahp_weights)

    mc = monte_carlo(indicators, NOMINAL_WEIGHTS, n_iter=10_000, seed=42)
    tornado = tornado_sensitivity(indicators, NOMINAL_WEIGHTS, delta=0.10, top=10)

    return dict(
        root=root, indicators=indicators, pillars=pillars, ahp=ahp,
        ahp_weights=ahp_weights, kutri_nominal=kutri_nominal, kutri_ahp=kutri_ahp,
        mc=mc, tornado=tornado,
    )


def write_outputs(results: Dict) -> Path:
    root: Path = results["root"]
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    (out / "figures").mkdir(exist_ok=True)
    indicators = results["indicators"]
    pillars = results["pillars"]

    # 1. Full normalized indicator results
    with open(out / "kutri_results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "pillar", "indicator_name", "direction", "raw_value",
                    "min_value", "max_value", "normalized_value", "normalized_value_reported",
                    "normalization_basis", "uncertainty_class"])
        for i in indicators:
            nv = normalize_indicator(i.raw_value, i.min_value, i.max_value, i.direction)
            w.writerow([i.code, i.pillar, i.indicator_name, i.direction, i.raw_value,
                        i.min_value, i.max_value, round(nv, 4), i.normalized_value_reported,
                        i.normalization_basis, i.uncertainty_class])

    # 2. Pillar scores + composites
    with open(out / "pillar_scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pillar", "pillar_score", "nominal_weight", "ahp_weight"])
        for p, nw, aw in zip(PILLAR_ORDER, NOMINAL_WEIGHTS, results["ahp_weights"]):
            w.writerow([p, round(pillars[p], 4), nw, round(aw, 4)])
        w.writerow([])
        w.writerow(["kutri_nominal_100", round(results["kutri_nominal"], 4)])
        w.writerow(["kutri_ahp_100", round(results["kutri_ahp"], 4)])
        w.writerow(["ahp_lambda_max", round(results["ahp"].lambda_max, 4)])
        w.writerow(["ahp_CI", round(results["ahp"].ci, 4)])
        w.writerow(["ahp_CR", round(results["ahp"].cr, 4)])

    # 3. Tornado sensitivity
    with open(out / "sensitivity_tornado.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "code", "indicator_name", "pillar", "impact_pm"])
        for rank, r in enumerate(results["tornado"], 1):
            w.writerow([rank, r.code, r.indicator_name, r.pillar, round(r.impact, 4)])

    # 4. Monte-Carlo summary
    mc = results["mc"]
    with open(out / "monte_carlo_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for k, v in mc.as_dict().items():
            w.writerow([k, round(v, 4) if isinstance(v, float) else v])

    # optional figures (non-fatal if matplotlib absent)
    try:
        from . import plotting
        plotting.make_all(results, out / "figures")
    except Exception as exc:  # pragma: no cover
        print(f"[reporting] figures skipped: {exc}")

    return out


def main() -> None:
    results = build_results()
    out = write_outputs(results)
    ahp = results["ahp"]
    print("=" * 60)
    print("KUTRI computation complete")
    print("=" * 60)
    for p in PILLAR_ORDER:
        print(f"  {p}: {results['pillars'][p]:.4f}")
    print(f"\n  KUTRI (nominal weights) : {results['kutri_nominal']:.4f}  -> {results['kutri_nominal']:.1f}/100")
    print(f"  KUTRI (AHP eigenvector) : {results['kutri_ahp']:.4f}  -> {results['kutri_ahp']:.1f}/100")
    print(f"  AHP lambda_max={ahp.lambda_max:.4f}  CI={ahp.ci:.4f}  CR={ahp.cr:.4f}  (consistent={ahp.is_consistent})")
    mc = results["mc"]
    print(f"  Monte-Carlo (seed={mc.seed}, n={mc.n_iterations}): "
          f"mean={mc.mean:.1f}  95% CI=[{mc.ci_low:.1f}, {mc.ci_high:.1f}]")
    flagged = flag_non_raw_bounds(results["indicators"])
    print(f"  Non-raw-bound indicators (disclosure required): {flagged}")
    print(f"\n  Outputs written to: {out}")


if __name__ == "__main__":
    main()
