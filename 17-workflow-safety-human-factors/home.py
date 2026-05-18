"""Course 17: workflow, patient safety, and human factors.

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
        # 17: Workflow, patient safety, and human factors

        ## Anchored to Ms. Reyes's rheumatology visit. The 7 places to enter joint counts, the 4 alerts dismissed on chart open, the methotrexate near-miss. Workflow mapping, human factors, alarm fatigue, safety frameworks, RCA, FMEA, sociotechnical theory.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Workflow mapping and process re-engineering** | Swimlanes, BPMN, time-motion. Reyes's 20-min visit as the swimlane example. Interactive: drag-and-drop step reorder. |
        | 02 | **Human factors engineering for clinical systems** | Nielsen's 10 heuristics, user-centered design, cognitive load. The 7-places-to-enter-joint-counts problem. |
        | 03 | **Alarm fatigue and alert override** | 90%+ override rates in the literature. The 5 Rights of CDS. Interactive: alert-tuning slider for the 4 chart-open alerts. |
        | 04 | **Patient safety frameworks** | SAFER Guides, Vincent, Reason's Swiss cheese, To Err Is Human, just culture. Reyes's MTX near-miss as the worked example. |
        | 05 | **Root cause analysis and FMEA** | 5 Whys, fishbone, FMEA S/O/D/RPN scoring. Walk the near-miss through both. Interactive: FMEA worksheet with reactive RPN. |
        | 06 | **Sociotechnical systems theory** | Why technical-only deployments fail. Sittig and Singh's 8-dimensional model. Cross-ref Course 16 Track 3 and Course 12. |

        ### Capstone

        **Sign-off review on a sepsis CDS deployment: workflow, human factors, alert tuning, safety risk register, FMEA, sociotechnical readiness (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
