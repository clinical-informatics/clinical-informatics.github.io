"""Course 01: Computational thinking.

This is the Marimo course menu for 01-computational-thinking. It opens
automatically when the Codespace launches. Use it to find your way through
the five tracks and the capstone.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # 01: Computational thinking

        ## The mental shift.

        You already think computationally when you reason through a clinical problem. You just don't call it that. You decompose. You spot patterns. You decide what to ignore. You follow a procedure. And at the end, you ask whether you trust the answer. This course makes those five moves explicit, gives them names, and shows what each one looks like when a machine is the one running them.

        No formulas. No visible code. Every interaction is a slider, a checkbox, or a short reflection prompt. Every screen explains in plain English what just changed and why.

        Take the tracks in order. The capstone pulls them together into a single design exercise you can bring to a real conversation with a data team.
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## The five tracks")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        | # | Track | The scenario |
        |---|---|---|
        | 01 | **Decomposing a clinical problem** | A sepsis alert fires 40 times a day. Clinicians ignore it. Why? |
        | 02 | **Patterns, rules, and edge cases** | Start with "flag HR>100 and temp>38.5." Add a condition. Watch the edge cases appear. |
        | 03 | **Abstraction: what to ignore** | Which features would you leave out of a readmission model, and why? |
        | 04 | **Algorithms in plain English** | DAS28, step by step, with sliders for the joint counts and the labs. |
        | 05 | **When to trust a computer** | Four questions you can ask any algorithm. |

        Each track is one notebook, roughly 20 to 40 minutes. They live in their own folders: `track-01-decomposing/`, `track-02-patterns-rules/`, and so on.
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## The capstone")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Design your own clinical decision rule.**

        A Socratic walkthrough. You'll define an outcome, list the inputs, write the rule in plain English, find three edge cases your rule misses, describe the data you'd need, and identify who it might fail. The output is a written design document. The notebook lives at `capstone/notebook.py`.
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## How to start")
    return


@app.cell
def __(mo):
    start_button = mo.ui.button(
        label="I'm ready. Start with Track 01.",
        kind="success",
    )
    start_button
    return (start_button,)


@app.cell
def __(mo, start_button):
    if start_button.value:
        mo.md(
            r"""
            **Open `track-01-decomposing/notebook.py`** from the file tree on the left. Marimo will load it in app mode. Come back to this menu any time by reopening `home.py`.
            """
        )
    else:
        mo.md("_Click the button above when you're ready to begin._")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        Concepts you build here will return in:

        - **04: Clinical epidemiology**, when we look at what a diagnostic test actually catches.
        - **09: AI in medicine**, when we evaluate a published clinical model.
        - **12: Clinical decision support**, when we design a real CDS rule.

        Each later course will tell you when it's picking up a thread from here. If a term throws you, the [GLOSSARY](GLOSSARY.md) defines every one of them in plain English.
        """
    )
    return


if __name__ == "__main__":
    app.run()
