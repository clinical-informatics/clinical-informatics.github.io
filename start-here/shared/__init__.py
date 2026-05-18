"""Shared components for the clinical-informatics curriculum.

These components are designed to be imported into Marimo notebooks across
all courses. Each one builds intuition through interactivity first. The
math and vocabulary come after the learner has seen the behavior.

Each module documents its own usage in a docstring at the top. The
curriculum-wide conventions that apply to all of them live in CLAUDE.md
at the curriculum root.
"""

from __future__ import annotations

__all__ = [
    "quiz",
    "socratic",
    "cross_reference",
    "cohort_builder",
    "decision_tree",
    "roc_explorer",
    "calibration_plot",
    "dca_plot",
    "structured_form",
    "fhir_compat",
]
