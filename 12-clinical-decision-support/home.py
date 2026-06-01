"""Course 12: Clinical decision support.

Marimo course menu. Five tracks plus the curriculum's grand-finale capstone.
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

        ## The curriculum's capstone course.

        Five tracks plus the seven-step CDS-design capstone that integrates every prior course (Courses 01, 03, 04, 06, 09, 10, 11). The course covers what CDS actually is and why most of it fails, the standards-based logic layer (CQL), the delivery layer (CDS Hooks), evaluation methods, and governance and equity.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **What CDS actually is** | The spectrum, the 5 rights, alert fatigue, the diagnostic-test framing. |
        | 02 | **CQL** | Why CQL exists, reading published CQL, writing a small CQL rule, VSAC value sets. |
        | 03 | **CDS Hooks** | Hook-as-workflow-moment, the three load-bearing hooks, simulated request/response. |
        | 04 | **Evaluating CDS** | DCA at the alert threshold, before/after designs, unintended consequences. |
        | 05 | **Governance and the human side** | Who decides, equity, FDA / ONC regulatory landscape, vendor-eval checklist. |

        ### Capstone

        **Seven-step CDS design brief for a Reyes-style RA flare alert.** Integrates the computational decomposition (Course 01), FHIR data specification (Course 06), CQL logic, CDS Hook design, evaluation plan (Course 04), DCA at the alert threshold (Course 11), and equity monitoring (Course 03). Output is a CDS design brief a real implementation team could act on, exportable as Markdown.

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
