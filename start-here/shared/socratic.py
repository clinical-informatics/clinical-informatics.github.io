"""Socratic capstone component for clinical-informatics.

Use this for question-based capstones. The pattern:

1. Present a scenario, usually featuring Ms. Reyes.
2. Ask the learner to commit to an answer first.
3. ``mo.stop()`` gates the reveal. The ideal answer cannot be seen
   without engaging.
4. The ideal answer is shown alongside the learner's answer.
5. The ideal answer explains *reasoning*, not just *conclusion*.
6. End with a reflection prompt that is never revealed.
7. Add a go-deeper callout tied to what the question surfaced.

This module is the scaffolding. Each capstone notebook composes its own
sequence of these functions.
"""

from __future__ import annotations

from typing import Iterable


def scenario(title: str, body: str):
    """Render the scenario at the top of a Socratic capstone."""
    import marimo as mo

    return mo.vstack(
        [
            mo.md(f"## {title}"),
            mo.callout(mo.md(body), kind="info"),
        ]
    )


def commit_text(prompt: str, *, min_chars: int = 40):
    """Ask the learner for a written answer. Returns the widget and a stop guard.

    The guard is a function that returns ``True`` when the learner has
    written at least ``min_chars`` characters. Use it with ``mo.stop()``
    in a downstream cell::

        widget, ready = commit_text("How would you define the cohort?")
        widget  # in one cell

        # in the next cell:
        mo.stop(not ready(), mo.md("_Write at least a paragraph above to see the ideal answer._"))
    """
    import marimo as mo

    widget = mo.ui.text_area(
        label=prompt,
        rows=6,
        full_width=True,
        placeholder="Take a few sentences. The reveal won't unlock until you do.",
    )

    def _ready() -> bool:
        value = widget.value or ""
        return len(value.strip()) >= min_chars

    return widget, _ready


def commit_choice(prompt: str, options: Iterable[str]):
    """Ask the learner to commit to a discrete choice before the reveal."""
    import marimo as mo

    widget = mo.ui.radio(options=list(options), label=prompt)

    def _ready() -> bool:
        return widget.value is not None

    return widget, _ready


def commit_multiselect(prompt: str, options: Iterable[str], min_selected: int = 1):
    """Ask the learner to select one or more options before the reveal."""
    import marimo as mo

    widget = mo.ui.multiselect(options=list(options), label=prompt)

    def _ready() -> bool:
        chosen = widget.value or []
        return len(chosen) >= min_selected

    return widget, _ready


def reveal(learner_value, ideal_answer: str, *, learner_label: str = "Your answer"):
    """Show the learner's answer alongside the ideal answer, side by side."""
    import marimo as mo

    learner_display = learner_value if learner_value else "_(no answer yet)_"
    return mo.hstack(
        [
            mo.callout(
                mo.vstack(
                    [
                        mo.md(f"**{learner_label}**"),
                        mo.md(str(learner_display)),
                    ]
                ),
                kind="neutral",
            ),
            mo.callout(
                mo.vstack(
                    [
                        mo.md("**How we'd think through this**"),
                        mo.md(ideal_answer),
                    ]
                ),
                kind="success",
            ),
        ],
        widths="equal",
    )


def reflection(prompt: str, placeholder: str = ""):
    """Open-ended reflection prompt. Never revealed. Writing it is the point.

    Returns ``(widget, layout)``. Display ``layout``; read ``widget.value``
    when the reflection text needs to flow into a downstream cell (for
    example, a hand-off document that assembles the learner's answers).
    """
    import marimo as mo

    widget = mo.ui.text_area(
        label=prompt,
        rows=5,
        full_width=True,
        placeholder=placeholder or "Take a few sentences. No reveal here. The reflection is the work.",
    )
    layout = mo.vstack(
        [
            widget,
            mo.callout(
                mo.md(
                    "_There's no answer key for this one. The point isn't to be right. "
                    "It's to make your reasoning explicit to yourself._"
                ),
                kind="neutral",
            ),
        ]
    )
    return widget, layout


def go_deeper(body: str):
    """Render the go-deeper callout that closes a Socratic capstone."""
    import marimo as mo

    return mo.callout(
        mo.vstack(
            [
                mo.md("### Go deeper"),
                mo.md(body),
            ]
        ),
        kind="info",
    )
