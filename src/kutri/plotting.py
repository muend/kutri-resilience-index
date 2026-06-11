"""Optional figure generation (matplotlib). Non-fatal if matplotlib is absent."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from .schema import PILLAR_ORDER


def make_all(results: Dict, fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)

    # 1. Pillar scores bar chart
    pillars = results["pillars"]
    fig, ax = plt.subplots(figsize=(7, 4))
    vals = [pillars[p] for p in PILLAR_ORDER]
    ax.bar(PILLAR_ORDER, vals, color="#3b6ea5")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Pillar score (0-1)")
    ax.set_title("KUTRI pillar scores — Kaş")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(fig_dir / "pillar_scores.png", dpi=150)
    plt.close(fig)

    # 2. Tornado sensitivity
    tornado = results["tornado"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    labels = [f"{r.code}" for r in tornado][::-1]
    impacts = [r.impact for r in tornado][::-1]
    ax.barh(labels, impacts, color="#a5483b")
    ax.set_xlabel("Composite swing (+/- index points, ±10%)")
    ax.set_title("Top-10 tornado sensitivity")
    fig.tight_layout()
    fig.savefig(fig_dir / "sensitivity_tornado.png", dpi=150)
    plt.close(fig)
