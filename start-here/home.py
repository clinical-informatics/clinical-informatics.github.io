"""Welcome to clinical-informatics.

This is the Marimo course menu for the start-here repo. It opens automatically
when you launch the Codespace. From here you can read the orientation notebook,
meet Ms. Reyes, or jump straight to any of the courses.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # Clinical Informatics Open Curriculum

        ## Welcome

        Twenty-one interactive courses in clinical informatics, written for clinicians, trainees, and clinical researchers. Every course runs in your browser. Each concept is defined in plain English before it is used technically.

        Below you'll find three things:

        1. **The orientation notebook.** About ten minutes. It walks you through how the curriculum works and how to read Ms. Reyes's data.
        2. **The course map.** Pick a course and we'll link you to its repo.
        3. **The shared components.** The reusable parts every course imports.

        If you don't know where to start, the orientation notebook is the right place.
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## 1. Orientation")
    return


@app.cell
def __(mo):
    orientation_button = mo.ui.button(
        label="Open orientation notebook",
        kind="success",
    )
    orientation_button
    return (orientation_button,)


@app.cell
def __(mo, orientation_button):
    if orientation_button.value:
        mo.md(
            r"""
            **Orientation notebook.**

            Open `orientation.py` in this repo to begin. In Codespaces, you'll find it in the file tree on the left. Click it, and Marimo will open it in app mode.
            """
        )
    else:
        mo.md("_Click the button above when you're ready to begin._")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 2. The course map

        Pick the course that matches your interest. Each course is its own repo. Open it in Codespaces from there.

        ### Start here

        | # | Course | Best for |
        |---|---|---|
        | 00 | **Foundations of clinical informatics** | Everyone, before anything else. The field, the DIKW framework, file types and databases at concept level, network architecture, the org chart of US healthcare, informatics roles. |

        ### The foundational courses

        | # | Course | Best for |
        |---|---|---|
        | 01 | **Computational thinking** | Everyone. The mental shift before any tooling. |
        | 02 | **Data literacy** | If you keep getting handed datasets. |
        | 03 | **Privacy, ethics, governance** | If you'll touch patient data, ever. |
        | 04 | **Clinical epidemiology** | If you've nodded along to "sensitivity and specificity" without it quite clicking. |

        ### The technical core

        | # | Course | Best for |
        |---|---|---|
        | 05 | **EHR systems** | If you want to understand the system you click through every day. Now includes imaging, PACS, DICOM. |
        | 06 | **Learn FHIR** | If you want to understand the modern interoperability standard, from zero. |
        | 07 | **Data wrangling and engineering** | If you'll write SQL, Python, or OMOP queries. |
        | 08 | **Clinical visualization** | If you'll ever present data to anyone. |

        ### The applied courses

        | # | Course | Best for |
        |---|---|---|
        | 09 | **AI in medicine** | If you want to evaluate AI claims, not build models. |
        | 10 | **NLP and clinical text** | If you care about what's hidden in notes. |
        | 11 | **Health economics data** | If you want decisions, costs, value. |
        | 12 | **Clinical decision support** | The curriculum's CDS capstone. Don't take this first. |

        ### The wider field

        | # | Course | Best for |
        |---|---|---|
        | 13 | **Research reproducibility** | If you'll do research and want it to last. |
        | 14 | **Interoperability policy** | If you want to know why the field changed. |
        | 15 | **Data storytelling** | If you want anyone outside informatics to understand your work. |

        ### The working informaticist's toolkit

        | # | Course | Best for |
        |---|---|---|
        | 16 | **Leadership and professional practice** | If you'll lead a project. PM, change management, KPIs, finance, executive communication. Chains directly from course 12. |
        | 17 | **Workflow, safety, human factors** | If you'll design or evaluate a clinical workflow. Alarm fatigue, SAFER Guides, RCA, FMEA, sociotechnical theory. |

        ### Modern practice frontiers

        | # | Course | Best for |
        |---|---|---|
        | 18 | **Population and public health informatics** | If your work is at the population, registry, ACO, or public-health-surveillance level. |
        | 19 | **Patient-generated data, telemedicine, digital health** | The 2020s reality. Patient portals, wearables, RPM, telemedicine, digital therapeutics, PROMs. |
        | 20 | **Bioinformatics for clinical informaticists** | The final course. Concept-level genomic file types, clinical genomics in the EHR, the research bioinformatics infrastructure. |
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## 3. Meet Ms. Elena Reyes")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        Every course in this curriculum follows the same patient.

        **Ms. Elena Reyes** is 52 years old. She was diagnosed with seropositive rheumatoid arthritis four years ago. She takes methotrexate weekly and adalimumab every two weeks. Her most recent DAS28 was 4.1, which is moderate disease activity. She is anti-CCP positive and has had an elevated CRP for most of the time we've followed her. She works as an accountant, lives with her partner, and has one daughter in college.

        Her data lives in `patients/elena-reyes/`. In every course, you'll see her in a different format.

        - `fhir-bundle.json`: her complete record as a FHIR R4 bundle (used in course 06)
        - `ehr-export-epic.json` and `ehr-export-cerner.json`: the same patient as exported from two different EHR vendors (course 05)
        - `claims.csv`: two years of synthetic insurance claims (course 11)
        - `labs.csv`: longitudinal CRP, ESR, anti-CCP, and CBC values (every course)
        - `notes.txt`: synthetic rheumatology and primary care notes (course 10)
        - `omop/`: her data mapped to OMOP common data model tables (course 07)

        She is **not a real person**. Her data is synthetic. But she's consistent. Every course pulls from the same source files, so what you learn about her in one course carries into the next.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 4. The shared components

        Every course imports from `start-here/shared/`. These are the reusable parts of the curriculum, the building blocks every notebook reaches for first.

        | Component | What it does |
        |---|---|
        | `quiz.py` | The standard quiz component used at decision points |
        | `socratic.py` | The capstone pattern for question-based assessments |
        | `cross_reference.py` | The callouts that link concepts across courses |
        | `cohort_builder.py` | Interactive cohort definition with patient-loss visualization |
        | `decision_tree.py` | Decision tree with probability sliders |
        | `roc_explorer.py` | ROC curve, threshold slider, 2x2 table. The workhorse. |
        | `calibration_plot.py` | Calibration plot with Brier score |
        | `dca_plot.py` | Decision curve analysis plot with net benefit |
        | `structured_form.py` | Guided form with live preview and PDF export |
        | `fhir_compat.py` | HTTP shim that works in WASM and locally |

        If you're a learner, you'll see these in action throughout the curriculum. There's no need to read the source.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        That's the whole tour. Pick a course and dive in.

        If you ever feel lost: the cross-reference callouts in every notebook tell you where a concept was first introduced. You can always click back.

        And if something is unclear or wrong, open an issue.
        """
    )
    return


if __name__ == "__main__":
    app.run()
