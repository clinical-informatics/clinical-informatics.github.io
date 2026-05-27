"""Course 00: Foundations of clinical informatics.

Marimo course menu. The six tracks and the capstone are the orientation
to the field that every later course assumes.
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
        # 00: Foundations of clinical informatics

        ## The orientation course.

        What clinical informatics is as a field, how clinical data flows through systems, and where the actors sit in U.S. healthcare. Six tracks and a Socratic capstone. No coding. Plain English throughout.

        This is the course every later course assumes. Most learning paths in the curriculum route through here before `01-computational-thinking`. Roughly two to three hours end to end.

        You will meet **Ms. Elena Reyes** in Track 01. She is the synthetic patient who appears in every subsequent course. Her data lives in `start-here/patients/elena-reyes/` and is accessible from inside every course through the `patients/` symlink.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## The six tracks")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        | # | Track | What it covers |
        |---|---|---|
        | 01 | **What clinical informatics is and how it got here** | Definition, brief history (Weed's POMR, the NLM, HITECH 2009, FHIR, AI), and Ms. Reyes introduced as the running patient. |
        | 02 | **DIKW and the lifecycle of clinical data** | Data, information, knowledge, wisdom with Reyes's CRP at each layer. The capture-store-use-share-retire lifecycle. |
        | 03 | **How computers represent and store data** | Bits, data structures, file types (TXT/CSV/JSON/XML), what a database is, relational concept, OLTP vs OLAP, database languages. |
        | 04 | **How computers move data** | Client-server, the hospital LAN/VPN/firewall, the internet, HTTP/REST/APIs at concept level, on-prem vs cloud, security boundaries. |
        | 05 | **The American health system and its parts** | Providers, payers, EHR vendors, regulators, research infrastructure, public health, standards bodies. Where informatics lives within each. |
        | 06 | **Informatics field: roles, ethics, and where the literature lives** | CMIO/CNIO/CRIO/analyst distinctions. The AMIA pathway. Where the field publishes. |

        Each track is one notebook with a paired short intro page. Open them from the file tree on the left in order: `track-01-what-is-informatics/notebook.py`, then `track-02-dikw-lifecycle/`, and so on.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## The capstone")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Walden Community Hospital wants to share its readmission predictions with its ACO.**

        A Socratic walkthrough of one scenario in which every track in this course is in play. Four committed answers across DIKW, plumbing, stakeholders, and governance, each with a reveal. The notebook lives at `capstone/notebook.py`. Orientation capstone, not technical depth; the goal is to verify you can see the whole system at once.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## How to start")
    return


@app.cell
def _(mo):
    start_button = mo.ui.button(
        label="I'm ready. Start with Track 01.",
        kind="success",
    )
    start_button
    return (start_button,)


@app.cell
def _(mo, start_button):
    if start_button.value:
        next_md = mo.md(
            r"""
            **Open `track-01-what-is-informatics/notebook.py`** from the file tree on the left. Marimo will load it in app mode. Come back to this menu any time by reopening `home.py`.
            """
        )
    else:
        next_md = mo.md("_Click the button above when you're ready to begin._")
    next_md
    return (next_md,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        Concepts you build here return in:

        - **01: Computational thinking**, immediately, where every move (decomposition, abstraction, algorithms) sits on top of the DIKW and lifecycle vocabulary from here.
        - **02: Data literacy**, where the file-types and data-types ideas from Track 03 become hands-on work.
        - **03: Privacy, ethics, and governance**, where Track 04's security boundaries and Track 06's ethical premise get treated seriously.
        - **05: EHR systems**, where Track 03's OLTP vs OLAP becomes a deep look at clinical data warehouses.
        - **06: Learn FHIR**, where Track 04's HTTP/REST/APIs sketch becomes a working knowledge of the field's main interoperability standard.

        Each later course flags when it continues a thread from here. If a term is unfamiliar, the [GLOSSARY](GLOSSARY.md) defines every one of them in plain English.
        """
    )
    return


if __name__ == "__main__":
    app.run()
