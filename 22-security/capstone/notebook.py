"""Capstone for course 22: security in clinical informatics (scaffold).

This notebook is a placeholder. The capstone will assemble the moves from
each track in the course into a single tabletop incident-response exercise.
See the capstone README in this folder for a one-line summary of what it
will require.
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
        # Capstone: security in clinical informatics

        **Tabletop incident-response exercise. A ransomware-style intrusion detected at 03:17 affecting the EHR cluster; within 20 minutes the LIS and pharmacy systems go offline; CDS alerts stop firing; the billing system is locked. The reader works through the first 4 hours, the first 72 hours, and the post-incident review (Socratic).**

        This capstone is **scaffolded only**. It will be filled in once the tracks in this course are built.

        Check `tasks.md` in the curriculum root for current status.
        """
    )
    return


if __name__ == "__main__":
    app.run()
