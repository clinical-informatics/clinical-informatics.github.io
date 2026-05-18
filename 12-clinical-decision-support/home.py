"""Course 12: Clinical decision support.

Marimo course menu. The course is currently scaffolded; track content will
be filled in as the curriculum builds out. The menu below lists the tracks
and a one-sentence description of what each one will cover.
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
        # 12: Clinical decision support

        ## The capstone course. Requires courses 06 and 09. All prior concepts revisited and connected.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **What CDS actually is** | Passive alerts → active recommendations → autonomous actions. Why most CDS fails. The five rights. |
        | 02 | **CQL: Clinical Quality Language** | Why CQL exists. Reading published CQL. Writing simple CQL. Value sets. |
        | 03 | **CDS Hooks** | Architecture in plain English. patient-view, order-select, order-sign. A simulated CDS Hooks request. |
        | 04 | **Evaluating CDS** | DCA from course 11. Before/after study design. Unintended consequences checklist. |
        | 05 | **Governance and the human side** | Who decides what gets built. Equity in CDS. Regulatory landscape. |

        ### Capstone

        **Design a complete CDS intervention for RA end to end, drawing on every prior course; export as PDF.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
