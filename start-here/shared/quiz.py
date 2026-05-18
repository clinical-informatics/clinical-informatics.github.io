"""Quiz component for clinical-informatics notebooks.

A quiz is for **genuine decision points**: moments where the learner has
to commit to an answer to engage with the next idea. Two or three per
notebook, maximum. Never at the end of a track. By then the learner has
earned a more substantive capstone.

Usage in a Marimo cell::

    from shared.quiz import question

    q = question(
        prompt="Which of these is most likely to be selection bias?",
        options=[
            "Lab values measured differently in two clinics",
            "Recruiting patients only from the rheumatology clinic for a study about hand pain",
            "Confounding by age",
            "Random measurement error in DAS28",
        ],
        answer=1,
        explanation=(
            "Selection bias happens when the way patients enter the study "
            "shapes who you end up studying. Recruiting only from rheumatology "
            "for a study about hand pain skews the population you observe."
        ),
    )
    q
"""

from __future__ import annotations

from typing import Sequence


def question(
    prompt: str,
    options: Sequence[str],
    answer: int | str,
    explanation: str,
    *,
    multiple: bool = False,
):
    """Return a Marimo component that asks a question and reveals feedback.

    Parameters
    ----------
    prompt:
        The question, in plain English. Don't lead with the vocabulary.
    options:
        The answer choices. Three to five is the sweet spot.
    answer:
        Either the integer index of the correct option, or the option text.
        For ``multiple=True``, a sequence of indices or option strings.
    explanation:
        Why the answer is right (or why the popular wrong answer is wrong).
        This is the actual teaching content. Write it carefully.
    multiple:
        Whether the question allows multiple correct selections.
    """
    import marimo as mo

    correct_text: set[str]
    if multiple:
        if not isinstance(answer, (list, tuple, set)):
            raise TypeError("For multiple-select questions, pass answer as a sequence.")
        correct_text = {
            options[a] if isinstance(a, int) else a for a in answer  # type: ignore[index]
        }
        widget = mo.ui.multiselect(options=list(options), label=prompt)
    else:
        if isinstance(answer, int):
            correct_text = {options[answer]}
        else:
            correct_text = {answer}
        widget = mo.ui.radio(options=list(options), label=prompt)

    def _render():
        chosen = widget.value
        if chosen is None or (multiple and len(chosen) == 0):
            return mo.vstack(
                [
                    widget,
                    mo.callout(
                        mo.md("_Choose an answer to see feedback._"),
                        kind="neutral",
                    ),
                ]
            )

        chosen_set = set(chosen) if multiple else {chosen}
        correct = chosen_set == correct_text

        header = "**Correct.**" if correct else "**Not quite.**"
        body = mo.md(f"{header} {explanation}")
        feedback = mo.callout(body, kind="success" if correct else "warn")
        return mo.vstack([widget, feedback])

    return _render()


def reflection(prompt: str, placeholder: str = ""):
    """A free-text reflection prompt that does not reveal an answer.

    Reflections are not graded. The point is that the learner writes
    something. Use one per notebook, at most, usually inside a capstone.
    """
    import marimo as mo

    box = mo.ui.text_area(
        placeholder=placeholder or "Take a few sentences here.",
        rows=4,
        full_width=True,
        label=prompt,
    )
    return mo.vstack(
        [
            box,
            mo.callout(
                mo.md(
                    "_There is no answer key for this one. The reflection "
                    "is the work."
                ),
                kind="neutral",
            ),
        ]
    )
