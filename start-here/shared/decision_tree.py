"""Decision tree component for clinical-informatics.

A decision tree is two things at once:

1. **A picture** of a clinical decision: what choice are we making, what
   outcomes can follow, with what probability, and what's the value of
   each.
2. **A math object** that lets you compute expected value and run
   sensitivity analyses.

This component does both. The learner sees the tree update as they move
sliders. Sliders control probabilities and utilities. The component
computes expected values and highlights the preferred branch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class Outcome:
    label: str
    probability: float
    utility: float


@dataclass
class Decision:
    label: str
    outcomes: list[Outcome] = field(default_factory=list)

    def expected_value(self) -> float:
        total_p = sum(o.probability for o in self.outcomes)
        if total_p <= 0:
            return 0.0
        return sum(o.probability * o.utility for o in self.outcomes) / total_p


@dataclass
class Tree:
    """A simple flat decision tree: one choice with several branches."""

    question: str
    decisions: list[Decision] = field(default_factory=list)

    def add(self, decision: Decision) -> "Tree":
        self.decisions.append(decision)
        return self

    def best(self) -> Decision | None:
        if not self.decisions:
            return None
        return max(self.decisions, key=lambda d: d.expected_value())

    def render(self):
        """Render the tree, the EVs, and a plain-English winner statement."""
        import marimo as mo
        import pandas as pd

        rows = []
        for d in self.decisions:
            for o in d.outcomes:
                rows.append(
                    {
                        "decision": d.label,
                        "outcome": o.label,
                        "probability": round(o.probability, 3),
                        "utility": round(o.utility, 3),
                        "contribution": round(o.probability * o.utility, 3),
                    }
                )
        table = pd.DataFrame(rows)
        evs = [
            {"decision": d.label, "expected_value": round(d.expected_value(), 3)}
            for d in self.decisions
        ]
        evs_df = pd.DataFrame(evs)
        winner = self.best()
        if winner is not None:
            ev_text = (
                f"At these probabilities and utilities, **{winner.label}** has the highest "
                f"expected value ({winner.expected_value():.3f}). That doesn't mean it's the "
                f"right choice for every patient. It means it's the choice that, on average, "
                f"produces the most value for a population with these inputs."
            )
        else:
            ev_text = "_Add at least one decision with outcomes._"

        return mo.vstack(
            [
                mo.md(f"### {self.question}"),
                mo.md("**Outcomes (one row per branch)**"),
                mo.ui.table(table, selection=None),
                mo.md("**Expected value by decision**"),
                mo.ui.table(evs_df, selection=None),
                mo.callout(mo.md(ev_text), kind="success"),
            ]
        )


def slider_panel(labels: Sequence[str], minimum: float = 0.0, maximum: float = 1.0, step: float = 0.05):
    """Convenience: build a row of probability sliders.

    Returns a dict mapping each label to its slider widget.
    """
    import marimo as mo

    return {
        label: mo.ui.slider(
            start=minimum,
            stop=maximum,
            step=step,
            value=(minimum + maximum) / 2,
            label=label,
            show_value=True,
        )
        for label in labels
    }
