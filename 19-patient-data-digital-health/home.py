"""Course 19: patient-generated data, telemedicine, and digital health.

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
        # 19: Patient-generated data, telemedicine, and digital health

        ## The 2020s reality. Reyes uses MyChart, tracks symptoms in RheumaTrack, wears an Apple Watch monitoring HRV, had a cross-state telemedicine flare visit, fills out PROMIS-29 every 6 months. The gap between what she generates and what her rheumatologist sees is the worked example.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Patient portals and patient-generated health data** | MyChart, FollowMyHealth, Athena. HHS PGHD definition. Integration models (copy-forward, view-only, structured). |
        | 02 | **Wearables and remote patient monitoring** | Apple HealthKit, CGMs, FDA-cleared RPM vs consumer. The data-volume problem. Reyes's HRV time-series. |
        | 03 | **Telemedicine workflows** | Synchronous vs asynchronous, e-consult. Reyes's cross-state flare visit. Licensure, billing, documentation. PHE expansion and after. |
        | 04 | **Digital therapeutics and patient-facing apps** | FDA-cleared SaMD. Pear, Akili, BlueStar. Prescription DTx. Reimbursement realities. |
        | 05 | **Patient-reported outcomes (PROMs/PROs)** | PROMIS, NeuroQOL, EQ-5D. The Reyes PROMIS-29 example. The collect-often, surface-rarely problem. |

        ### Capstone

        **Design a remote-monitoring program for newly-diagnosed RA patients on biologics: data capture, surfacing, telemedicine touchpoints, workflow mesh, governance, equity (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
