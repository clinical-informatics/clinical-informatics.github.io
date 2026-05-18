"""Capstone for course 20: bioinformatics for clinical informaticists (scaffold).

This notebook is a placeholder. The capstone will assemble the moves from
each track in the course into a single design exercise. See the capstone
README in this folder for a one-line summary of what it will require.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: bioinformatics for clinical informaticists

        **Design a precision medicine program (pharmacogenomic testing at the point of high-risk prescribing): infrastructure, standards, returns to patients, research/clinical coexistence, governance, equity (Socratic). Closes the curriculum.**

        This capstone is **scaffolded only**. It will be filled in once the tracks in this course are built.

        Check `tasks.md` in the curriculum root for current status.
        """
    )
    return


if __name__ == "__main__":
    app.run()
