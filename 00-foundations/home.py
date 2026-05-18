"""Course 00: foundations of clinical informatics.

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
        # 00: Foundations of clinical informatics

        ## The orientation course. What clinical informatics is as a field, how clinical data flows through systems, and where the actors sit in US healthcare. The course every later course assumes.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **What clinical informatics is and how it got here** | Definition, brief history (Weed's POMR, the NLM, HITECH 2009, FHIR, AI), and Ms. Reyes introduced as the running patient. |
        | 02 | **DIKW and the lifecycle of clinical data** | Data, information, knowledge, wisdom with Reyes's CRP walked through each layer. The capture-store-use-share-retire lifecycle. |
        | 03 | **How computers represent and store data** | Bits, data structures, file types (TXT/CSV/JSON/XML), what a database is, relational concept, OLTP vs OLAP, database languages. |
        | 04 | **How computers move data** | Client-server, the hospital LAN/VPN/firewall, the internet, HTTP/REST/APIs at concept level, on-prem vs cloud, security boundaries. |
        | 05 | **The American health system and its parts** | Providers, payers, EHR vendors, regulators, research infrastructure, public health, standards bodies. Where informatics lives within each. |
        | 06 | **Informatics field: roles, ethics, and where the literature lives** | CMIO/CNIO/CRIO/analyst distinctions. The AMIA pathway. Where the field publishes. |

        ### Capstone

        **A community hospital wants to share readmission predictions with its ACO. Walk the problem through DIKW, CS plumbing, network, stakeholders, and governance (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
