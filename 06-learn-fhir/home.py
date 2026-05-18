"""Course 06: Learn FHIR.

Marimo course menu. All six tracks and the course-level capstone are now
built. The menu below lists the tracks with a one-sentence description
of what each one covers.
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
        # 06: Learn FHIR

        ## FHIR from zero. The web architecture healthcare borrowed.

        All six tracks and the course-level capstone are now built. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it covers | Status |
        |---|---|---|---|
        | 0 | **Before FHIR (no code)** | Data vs structure, HTTP/REST/JSON via the restaurant analogy, health data history without condescension; closes with diagnosing four real interop differences between Epic-shaped and Cerner-shaped exports of Ms. Reyes. | Built |
        | 1 | **FHIR fundamentals** | Resources, references, bundles, terminology (LOINC/SNOMED/RxNorm/UCUM/ICD-10/CVX), search parameters at a concept level. Capstone: six clinical questions answered by navigating Ms. Reyes's actual FHIR bundle, then synthesized into a five-to-seven-sentence summary. | Built |
        | 2 | **Working with FHIR servers** | Real hapi.fhir.org calls with cached fallback; gentle Python intro; interactive search URL builder with a LOINC dropdown; pagination patterns. Capstone: pull CRP and ESR for a synthetic 5-patient RA cohort, render a 4-year Altair trend chart. | Built |
        | 3 | **Clinical modeling** | Minimum required fields per resource type; profiles with US Core as the worked example; must-support semantics; extensions; reading OperationOutcomes from `$validate`. Capstone: author Ms. Reyes's next follow-up visit (Encounter + CRP/ESR/DAS28 Observations), live-validate against hapi.fhir.org, assemble a transaction Bundle. | Built |
        | 4 | **Implementation guides** | IG anatomy walked on real US Core Observation Lab and mCODE Primary Cancer Condition StructureDefinitions; the must-support footgun; portability vs interoperability with a cross-reference to Track 0's five-layer framework. Capstone: a one-page gap analysis of US Core for rheumatology, assembled as a markdown report ready to take to a project kickoff. | Built |
        | 5 | **SMART on FHIR** | Two launch flavors; the six-step OAuth dance walked on a real cached well-known/smart-configuration; scope vocabulary with a principle-of-least-privilege quiz; CDS Hooks and Bulk Data at concept level. Capstone: design a SMART app for RA monitoring as a one-page brief, leaning on Track 4's gap analysis as the data model. | Built |

        ### Capstone

        **Author and validate a complete FHIR record for Ms. Reyes on hapi.fhir.org.** Eight steps walking the six tracks in sequence on Ms. Reyes's real bundle: bundle anatomy, scope, profile selection, a real cached `Bundle/$validate` OperationOutcome from hapi.fhir.org (22 errors and 40 warnings), triage, prioritized fixes, SMART access for a downstream registry app, and the portability vs interoperability frame with a forward look to course 07. Six of the eight steps are Socratic commit-and-reveal; the other two are display steps. Output is a one-page hand-off document.

        ---

        Each track folder has a `README.md` and a `notebook.py` you can open. The course capstone lives in `capstone/`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
