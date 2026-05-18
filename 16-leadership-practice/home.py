"""Course 16: informatics leadership and professional practice.

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
        # 16: Informatics leadership and professional practice

        ## How to actually do the job. The CMIO just handed you the RA-CDS you designed in the Course 12 capstone. Six tracks teach you the leadership, project management, change management, KPI, financial, and communication moves to deploy it.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **The working clinical informaticist: roles, scope, day-to-day** | Roles, org-chart placement, reporting lines, committees, the 'who decides what' matrix for the RA-CDS deployment. |
        | 02 | **Project management for informatics** | PMBOK, Waterfall/Agile/Scrum/Kanban, the five PMI process groups, RACI, Gantt, the SDLC. Build the RA-CDS plan. |
        | 03 | **Change management** | Kotter, Lewin, ADKAR. Why technical-only deployments fail. The Sepsis Watch case. Change-readiness assessment for the RA-CDS. |
        | 04 | **Quality, KPIs, and operations management** | KPI definition, process vs outcome, leading vs lagging, balanced scorecard, PDSA, Lean/Six Sigma, HEDIS/MIPS/eCQMs. RA-CDS dashboard. |
        | 05 | **Financial management for informaticists** | Capex vs opex, ROI, NPV, TCO, vendor economics. RA-CDS budget and 5-year ROI calculator. |
        | 06 | **Leadership and communication** | Leadership styles, executive communication (BLUF), conflict resolution. RA-CDS 3-slide board pitch builder. Brief board-pathway career orientation. |

        ### Capstone

        **Assemble the six track artifacts plus a risk register into the implementation plan for the RA-CDS the learner designed in Course 12. The 'now actually deploy it' capstone.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
