"""Cohort builder component for clinical-informatics.

Cohort definition is most of the actual work in clinical research. This
component lets a learner add criteria one at a time and watch how many
patients fall out at each step, which makes the "silent patient loss"
problem visible.

Typical usage in a Marimo notebook::

    import pandas as pd
    from shared.cohort_builder import CohortBuilder

    df = pd.read_csv("patients.csv")
    cb = CohortBuilder(df, patient_id_col="patient_id")
    cb.add_criterion("age_years >= 18", "Adults only")
    cb.add_criterion("primary_diagnosis == 'M05.79'", "Seropositive RA without organ involvement")
    cb.add_criterion("methotrexate_active == True", "On methotrexate at index")
    cb.render()
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import pandas as pd


@dataclass
class Criterion:
    expression: str
    plain_english: str
    survivors: int = 0
    lost: int = 0


@dataclass
class CohortBuilder:
    """Build a cohort step by step and visualize attrition.

    Each criterion is a pandas query expression. After each criterion, the
    builder reports how many patients remained and how many were lost,
    with a plain-English label for the criterion.
    """

    df: pd.DataFrame
    patient_id_col: str = "patient_id"
    criteria: list[Criterion] = field(default_factory=list)

    def add_criterion(self, expression: str, plain_english: str) -> "CohortBuilder":
        self.criteria.append(Criterion(expression=expression, plain_english=plain_english))
        return self

    def reset(self) -> "CohortBuilder":
        self.criteria.clear()
        return self

    def evaluate(self) -> pd.DataFrame:
        """Run the criteria in order and return the attrition table."""
        current = self.df.copy()
        starting = len(current)
        rows: list[dict] = [
            {
                "step": 0,
                "criterion": "Starting cohort",
                "patients_remaining": starting,
                "patients_lost_this_step": 0,
            }
        ]
        previous = starting
        for i, crit in enumerate(self.criteria, start=1):
            try:
                current = current.query(crit.expression)
            except Exception as exc:  # noqa: BLE001
                rows.append(
                    {
                        "step": i,
                        "criterion": f"{crit.plain_english} (error: {exc})",
                        "patients_remaining": previous,
                        "patients_lost_this_step": 0,
                    }
                )
                continue
            remaining = len(current)
            lost = previous - remaining
            crit.survivors = remaining
            crit.lost = lost
            rows.append(
                {
                    "step": i,
                    "criterion": crit.plain_english,
                    "patients_remaining": remaining,
                    "patients_lost_this_step": lost,
                }
            )
            previous = remaining
        return pd.DataFrame(rows)

    def surviving_patients(self) -> pd.DataFrame:
        current = self.df.copy()
        for crit in self.criteria:
            try:
                current = current.query(crit.expression)
            except Exception:  # noqa: BLE001
                continue
        return current

    def render(self):
        """Return a Marimo UI showing the attrition table and a plain-English summary."""
        import marimo as mo

        table = self.evaluate()
        starting = int(table.iloc[0]["patients_remaining"])
        ending = int(table.iloc[-1]["patients_remaining"])
        biggest_drop = (
            table.iloc[1:]
            .sort_values("patients_lost_this_step", ascending=False)
            .head(1)
            if len(table) > 1
            else None
        )

        if biggest_drop is not None and len(biggest_drop) > 0:
            drop_label = biggest_drop.iloc[0]["criterion"]
            drop_n = int(biggest_drop.iloc[0]["patients_lost_this_step"])
            summary = (
                f"You started with **{starting}** patients and ended with **{ending}**. "
                f"The single biggest drop happened at the step **{drop_label}**, "
                f"which removed **{drop_n}** patients."
            )
        else:
            summary = f"You started with **{starting}** patients and ended with **{ending}**."

        return mo.vstack(
            [
                mo.md("### Your cohort, step by step"),
                mo.ui.table(table, selection=None),
                mo.callout(mo.md(summary), kind="info"),
            ]
        )


def interactive(
    df: pd.DataFrame,
    candidate_criteria: Iterable[tuple[str, str]],
    patient_id_col: str = "patient_id",
):
    """A fully interactive cohort builder UI for a course notebook.

    Parameters
    ----------
    df:
        The starting dataframe.
    candidate_criteria:
        An iterable of ``(plain_english, expression)`` pairs. The learner
        toggles them on and off with checkboxes.
    """
    import marimo as mo

    pairs = list(candidate_criteria)
    labels = [p[0] for p in pairs]
    expr_by_label = {p[0]: p[1] for p in pairs}

    selector = mo.ui.multiselect(
        options=labels,
        label="Toggle inclusion criteria on and off",
    )

    def _render():
        chosen = selector.value or []
        cb = CohortBuilder(df, patient_id_col=patient_id_col)
        for label in chosen:
            cb.add_criterion(expr_by_label[label], label)
        return mo.vstack([selector, cb.render()])

    return _render
