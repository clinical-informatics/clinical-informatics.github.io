"""Capstone for course 15: Data storytelling (scaffold).

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
        # Capstone: Data storytelling

        **Take the CDS design brief from course 12 and produce a 2-minute pitch + one-page visual summary.**

        This capstone is **scaffolded only**. It will be filled in once the tracks in this course are built.

        Check `tasks.md` in the curriculum root for current status.
        """
    )
    return


if __name__ == "__main__":
    app.run()
