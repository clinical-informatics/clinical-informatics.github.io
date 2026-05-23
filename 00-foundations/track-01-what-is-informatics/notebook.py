"""Track 01: What clinical informatics is and how it got here.

Orientation. Plain English. No code visible. The track defines the field,
walks the short history (Weed's POMR, the NLM, HITECH and Meaningful Use,
FHIR, the 2020s AI inflection), and formally introduces Ms. Elena Reyes
as the running patient the rest of the curriculum will follow.
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
        # Track 01: What clinical informatics is and how it got here

        ## A morning in clinic.

        Tuesday morning, rheumatology. The next patient on the schedule is a 52-year-old woman, four years out from a diagnosis of seropositive rheumatoid arthritis, in for a six-month follow-up. You open her chart and within ninety seconds you have done the following.

        You skim the **problem list** to see what is active. You glance at the **medication list** to confirm she is still on methotrexate and adalimumab. You open the **lab trend** for C-reactive protein and erythrocyte sedimentation rate to see whether her inflammatory markers have crept up since November. You hover over a **DAS28 score** that was entered at her last visit. You glance at the **portal note** she sent two weeks ago saying her hands have been stiffer in the mornings. You see a **CDS alert** asking you to confirm she has had her annual TB screening on biologics.

        Six different tools. Six different pieces of plumbing underneath. Each of them is the visible tip of a piece of clinical informatics work that someone, somewhere, designed and built and now maintains. None of it is medicine in the strictest sense. All of it is what makes the medicine possible.

        That is the subject of this field. This track defines it, walks the short history that produced it, and introduces the patient whose chart you have been reading. She will be with you for the rest of the curriculum.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## A working definition.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Clinical informatics** is the field that studies and shapes how clinical information is captured, stored, moved, surfaced, and used in the practice of healthcare. It sits between clinical medicine and the systems that support it: electronic health records, decision support, registries, claims, research data, the patient's own app on her phone.

        Two phrases in that definition do most of the work.

        First, **the practice of healthcare.** The field is anchored to the actual delivery of care to actual patients. A clinical informaticist who has never sat in clinic, never been on call, never written a discharge summary, will produce work that looks correct on paper and fails in the room. The clinical part of clinical informatics is not decorative.

        Second, **captured, stored, moved, surfaced, and used.** Those five verbs are the lifecycle of clinical data. They are the substrate of the entire curriculum. Course 02 of this course (DIKW and the lifecycle) will name them more formally; for now hold them loosely.

        The companion field, **biomedical informatics**, takes the same set of tools and applies them across the broader biomedical enterprise: bench science, public health, consumer health, and the spaces in between. Clinical informatics is the slice of that broader field that touches the bedside.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## What counts.")
    return


@app.cell
def _(mo):
    counts_selector = mo.ui.multiselect(
        options=[
            "Redesigning the order set for inpatient sepsis so the right antibiotic loads at the top.",
            "Performing the actual lumbar puncture on a patient with suspected meningitis.",
            "Building the alert that fires when a clinician orders a contrast study on a patient with a recent creatinine over 2.0.",
            "Choosing whether to admit a patient to the medicine service or to the step-down unit.",
            "Designing how the discharge medication reconciliation page renders for the nurse and the pharmacist.",
            "Mapping a hospital's local lab codes to LOINC so the data can be pooled with three other health systems for a research network.",
            "Reading a chest x-ray and dictating the report.",
            "Auditing why the diabetes registry is dropping 14% of patients who actually do have diabetes.",
        ],
        label="Which of these are clinical informatics work? Pick all that apply.",
    )
    counts_selector
    return (counts_selector,)


@app.cell
def _(counts_selector, mo):
    chosen_counts = set(counts_selector.value or [])
    informatics = {
        "Redesigning the order set for inpatient sepsis so the right antibiotic loads at the top.",
        "Building the alert that fires when a clinician orders a contrast study on a patient with a recent creatinine over 2.0.",
        "Designing how the discharge medication reconciliation page renders for the nurse and the pharmacist.",
        "Mapping a hospital's local lab codes to LOINC so the data can be pooled with three other health systems for a research network.",
        "Auditing why the diabetes registry is dropping 14% of patients who actually do have diabetes.",
    }
    if not chosen_counts:
        counts_response = mo.callout(
            mo.md("_Pick at least one. You can change your mind after seeing the answer._"),
            kind="neutral",
        )
    elif chosen_counts == informatics:
        counts_response = mo.callout(
            mo.md(
                "**Five of the eight.** The order set, the contrast alert, the reconciliation page, "
                "the LOINC mapping, and the registry audit are all clinical informatics work. They "
                "all shape how information moves through the system in service of care. The other "
                "three (LP, admission decision, x-ray read) are clinical work that *uses* the "
                "systems informatics builds. The distinction is the difference between practicing "
                "medicine and shaping the conditions under which medicine is practiced. The field "
                "needs both, but they are not the same job."
            ),
            kind="success",
        )
    else:
        counts_response = mo.callout(
            mo.md(
                "**Close.** The five that count as clinical informatics are the order set, the "
                "contrast alert, the reconciliation page, the LOINC mapping, and the registry audit. "
                "Each one shapes how information moves through the system. The other three "
                "(the lumbar puncture, the admit-or-step-down decision, the chest x-ray read) are "
                "clinical work that uses what informatics builds. Both matter; they are not the "
                "same job. If the distinction feels arbitrary at the edges, that is honest. Some "
                "work sits on the boundary, and a CMIO who reads x-rays half-time has one foot in each."
            ),
            kind="warn",
        )
    counts_response
    return chosen_counts, counts_response, informatics


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How the field got here.

        Five moments do most of the explanatory work. Each of them produced something the others built on. None of them invented the field by themselves; together they account for why the chart you opened this morning looks the way it does.
        """
    )
    return


@app.cell
def _(mo):
    era_picker = mo.ui.radio(
        options=[
            "1960s: Lawrence Weed and the problem-oriented medical record (POMR).",
            "1970s-1990s: Don Lindberg, the NLM, and the long buildout of medical vocabularies and Medline.",
            "2009: HITECH and Meaningful Use. The federal money that put EHRs in every hospital.",
            "2010s: HL7 FHIR. Health data borrows the architecture of the web.",
            "2020s: AI in clinical care. LLMs, ambient documentation, predictive models in the workflow.",
        ],
        label="Pick a moment to read about. Each one is a paragraph.",
        value="1960s: Lawrence Weed and the problem-oriented medical record (POMR).",
    )
    era_picker
    return (era_picker,)


@app.cell
def _(era_picker, mo):
    if era_picker.value is None:
        era_view = mo.md("")
    elif era_picker.value.startswith("1960s"):
        era_view = mo.callout(
            mo.md(
                "**Lawrence Weed and the POMR.** In the 1960s, Lawrence Weed (an internist, not a "
                "computer scientist) argued that the medical record as practiced was a narrative "
                "diary that nobody could reason against. He proposed a structure: a numbered "
                "**problem list** at the front of the chart, and notes organized as SOAP "
                "(Subjective, Objective, Assessment, Plan) anchored to a problem. The reasoning was "
                "that if information about the patient were structured, clinicians could be held to "
                "account for what they had and had not done. The POMR is why every chart you have "
                "ever opened has a problem list at the front and a SOAP note in the middle. It is "
                "also the first time someone seriously argued that the *structure* of the record "
                "was a clinical intervention in its own right. Everything afterward is downstream "
                "of that idea."
            ),
            kind="info",
        )
    elif era_picker.value.startswith("1970s"):
        era_view = mo.callout(
            mo.md(
                "**Lindberg, the NLM, and the long buildout.** Don Lindberg directed the National "
                "Library of Medicine for thirty years (1984 to 2015) and presided over the work "
                "that made medical knowledge machine-readable and clinical vocabularies "
                "interoperable. Medline (the bibliographic database that became PubMed) and the "
                "Unified Medical Language System (UMLS, the cross-walk between SNOMED, LOINC, "
                "RxNorm, and ICD) both became durable infrastructure on his watch. None of it "
                "was glamorous and most of it took decades. The reason your EHR can map the local "
                "lab code 'CRP-Q' to LOINC 1988-5 and have that mean the same thing in three "
                "other health systems is downstream of this work. The NLM is still the steward."
            ),
            kind="info",
        )
    elif era_picker.value.startswith("2009"):
        era_view = mo.callout(
            mo.md(
                "**HITECH 2009 and Meaningful Use.** The Health Information Technology for Economic "
                "and Clinical Health Act, part of the 2009 stimulus package, put roughly $30 billion "
                "of federal money on the table to subsidize EHR adoption. The condition was that the "
                "EHRs had to be *certified* (meeting an ONC technical standard) and used in a "
                "*meaningful* way (entering structured data, e-prescribing, generating quality "
                "measures). Within five years, hospital EHR adoption went from a minority of "
                "facilities to nearly universal. Many of the workflows clinicians complain about "
                "today (the click counts, the structured data demands, the documentation burden) "
                "are downstream of Meaningful Use criteria that nobody quite wanted to repeal once "
                "the money had been spent. HITECH is also why clinical informatics became a job "
                "title in most health systems instead of a side project."
            ),
            kind="info",
        )
    elif era_picker.value.startswith("2010s"):
        era_view = mo.callout(
            mo.md(
                "**HL7 FHIR.** Before FHIR, moving clinical data between systems meant HL7 v2 "
                "(pipe-delimited messages designed in the 1980s) or CDA documents (XML so verbose "
                "that few engineers enjoyed reading them). FHIR, first drafted around 2012 by Grahame "
                "Grieve and a small HL7 working group, did something simple and unobvious: it borrowed "
                "the architecture of the web. Clinical concepts became **resources** (Patient, "
                "Observation, Condition) with stable URLs. Data moved as **JSON** over **HTTP REST**. "
                "Anything a junior web developer already knew transferred. The 21st Century Cures Act "
                "and the ONC interoperability rules then made FHIR APIs effectively mandatory for "
                "certified EHRs. The 2020s build-out of patient-facing apps and third-party clinical "
                "tools is what FHIR made tractable."
            ),
            kind="info",
        )
    else:
        era_view = mo.callout(
            mo.md(
                "**The 2020s AI inflection.** Two things happened close together. First, large "
                "language models became capable enough that **ambient documentation** (a microphone "
                "in the exam room turning the visit into a draft note) became a real product rather "
                "than a demo. Second, predictive models embedded in the workflow (sepsis scores, "
                "readmission risk, deterioration alerts) graduated from research papers to vendor "
                "modules that ship inside the EHR. The field is now spending most of its energy on "
                "the questions these tools raise: how to evaluate them, how to govern them, how to "
                "monitor them after deployment, how to keep them from amplifying existing inequities. "
                "Course 09 (AI in medicine) and Course 12 (clinical decision support) carry this "
                "thread further."
            ),
            kind="info",
        )
    era_view
    return (era_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The throughline.

        The five moments above are not five separate stories. They are one story about a single problem: clinical work generates information faster than anyone can use it, and that gap has costs.

        Weed's POMR addressed the gap by structuring the record so reasoning could happen against it. The NLM addressed it by making the vocabulary shared so different systems could talk about the same thing. HITECH addressed it by making sure every hospital actually had an electronic system to begin with. FHIR addressed it by making the data movable. AI is addressing it by automating parts of the reasoning that used to require a clinician's time.

        None of those moves are finished. The field exists because the gap is not closed. It is the work itself.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Meet Ms. Elena Reyes.

        For the rest of this curriculum, when a course needs a concrete patient, the patient is Ms. Reyes. She is synthetic. Her data is hand-crafted, with realistic clinical detail, so that every course can pull from the same chart instead of inventing a new fictional patient for every example.

        The short version of her record:

        - **52-year-old woman**, two children, works as a community-college instructor.
        - **Seropositive rheumatoid arthritis**, diagnosed in February 2022 (anti-CCP 178 U/mL, RF 84 IU/mL at diagnosis).
        - On **methotrexate** 25 mg subcutaneous weekly and **adalimumab** 40 mg subcutaneous every two weeks, with **folic acid** 1 mg daily. Started biologic in mid-2022 after csDMARD-only failed to control disease.
        - **Moderate disease activity** by DAS28 around 4.1 at her most recent visit, with morning stiffness lasting forty-five minutes and three swollen MCP joints on exam.
        - **Anemia of chronic disease**, hemoglobin floating between 11.6 and 12.4 g/dL across visits.
        - One **hand radiograph series** spanning 2022 to 2024, scored with the Sharp/van der Heijde method.
        - Lives in a state that borders the one her rheumatology clinic is in; her insurer changed in January 2025.

        Her files live in the `start-here/patients/elena-reyes/` directory at the root of the curriculum repo and are visible from inside every course through the `patients/` symlink in this folder. The same patient appears as:

        - `fhir-bundle.json`. A complete R4 FHIR bundle.
        - `ehr-export-epic.json`. A synthetic Epic-style export.
        - `ehr-export-cerner.json`. The same patient, exported from a different (synthetic) EHR.
        - `claims.csv`. Two years of synthetic claims.
        - `labs.csv`. Four years of longitudinal labs (CRP, ESR, anti-CCP, CBC, LFTs, creatinine).
        - `notes.txt`. Eight synthetic rheumatology notes.
        - `omop/`. Her data mapped to the OMOP common data model.

        Different courses pull different files. The FHIR course works from `fhir-bundle.json`. The data wrangling course works from `omop/`. The NLP course works from `notes.txt`. The pattern is intentional: the same clinical substance, different representations, so that the cross-references between courses are not abstract.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why she matters for the field.

        The throughline above (clinical work outpaces the systems that capture it) has a sharper version when you look at Ms. Reyes.

        Her **CRP value of 42.1 mg/L** at diagnosis (LOINC 1988-5) is captured in the lab system, copied to the EHR, summarized into a DAS28 score, displayed on a flowsheet, possibly graphed in MyChart, sent in a claim to her insurer, pulled into a research dataset her health system contributes to, and quietly retained for a decade or more. Every one of those steps is informatics infrastructure. Any of them can drop the value, mislabel it, or render it in a way that hides the trend.

        Her chart is also where the limits of any one informatics move become visible. A perfectly designed problem list does not help if her rheumatologist's note about hand stiffness is in free text. A perfectly mapped LOINC value does not help if her insurer rejects the LOINC and demands a local code. A perfectly interoperable FHIR API does not help if the data on the other end is wrong.

        The reason this curriculum follows one patient through every course is that the field's questions stack on a single person. The questions of Course 02 (is the data type right) sit on the same person as the questions of Course 09 (is the predictive model calibrated for her) and the questions of Course 12 (does the CDS alert fire on her appropriately). Following one patient is how the stacking becomes visible.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## One more.")
    return


@app.cell
def _(mo):
    placement_quiz = mo.ui.radio(
        options=[
            "Lawrence Weed and the POMR (1960s).",
            "The NLM buildout of medical vocabularies (1970s-1990s).",
            "HITECH and Meaningful Use (2009).",
            "HL7 FHIR (2010s).",
            "The 2020s AI inflection.",
        ],
        label=(
            "A small community hospital in 2024 is buying a third-party prior-authorization tool "
            "from a startup. The tool needs to read the patient's diagnoses, medications, and "
            "recent labs out of the hospital's EHR and write back a recommended prior-auth packet. "
            "The hospital's IT team estimates the integration at two weeks, not two years, because "
            "the EHR ships a standard read API that the startup's product already speaks. "
            "Which single moment in the history above is most responsible for the fact that this "
            "is a two-week job?"
        ),
    )
    placement_quiz
    return (placement_quiz,)


@app.cell
def _(mo, placement_quiz):
    if placement_quiz.value is None:
        placement_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif placement_quiz.value.startswith("HL7 FHIR"):
        placement_response = mo.callout(
            mo.md(
                "**Yes.** A standard read API that a third-party startup can already speak is the "
                "FHIR story specifically. Before FHIR, a startup writing to an EHR meant a custom "
                "HL7 v2 interface engine per hospital, a bespoke contract, a quarter of engineering "
                "time, and a renewal every time the EHR upgraded. After FHIR, the startup writes "
                "to one API spec and a hospital integration becomes credentialing plus configuration. "
                "The other moments are real prerequisites (without HITECH there is no EHR to "
                "integrate with; without the NLM there is no shared vocabulary in the response; "
                "without Weed there is no structured chart to read from), but the *two weeks not "
                "two years* fact is the FHIR fact."
            ),
            kind="success",
        )
    elif placement_quiz.value.startswith("HITECH"):
        placement_response = mo.callout(
            mo.md(
                "**Necessary, not sufficient.** Without HITECH, the community hospital probably "
                "would not have an EHR at all, so there would be nothing to integrate with. But "
                "HITECH-era integrations were custom HL7 v2 work that took months per hospital and "
                "broke on every EHR upgrade. The *two weeks not two years* fact is the FHIR fact."
            ),
            kind="warn",
        )
    elif placement_quiz.value.startswith("Lawrence Weed"):
        placement_response = mo.callout(
            mo.md(
                "**Necessary, not sufficient.** The POMR is the reason there is a structured "
                "problem list and a structured medication list for the prior-auth tool to read. "
                "Without that structure the data would be a free-text note nobody could "
                "automatically reason against. But Weed alone did not make the integration tractable. "
                "What made the integration *fast* was a standard API the startup already speaks, "
                "and that is the FHIR story."
            ),
            kind="warn",
        )
    elif placement_quiz.value.startswith("The NLM"):
        placement_response = mo.callout(
            mo.md(
                "**Necessary, not sufficient.** Without LOINC and RxNorm the lab values and "
                "medications in the prior-auth packet would not have the same meaning across "
                "systems. But shared vocabularies are inside the data; what made the *integration* "
                "fast is the API the data moves over. That is the FHIR story."
            ),
            kind="warn",
        )
    else:
        placement_response = mo.callout(
            mo.md(
                "**Not quite.** AI is where the field's current attention is, and the prior-auth "
                "tool may well use a model under the hood. But the question is about why the "
                "integration takes two weeks instead of two years, not about what the tool does "
                "with the data once it has it. The integration speed is the FHIR story."
            ),
            kind="warn",
        )
    placement_response
    return (placement_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - Named clinical informatics: the field that shapes how clinical information is captured, stored, moved, surfaced, and used.
        - Distinguished the work of the field from the clinical work that uses what the field builds.
        - Read the short history through five moments (POMR, NLM, HITECH, FHIR, AI) and saw how the chart you opened this morning is the cumulative product of all five.
        - Met Ms. Reyes, who will appear in every subsequent course.

        ## What's next.

        **Track 02: DIKW and the lifecycle of clinical data.** The five verbs in the working definition above (captured, stored, moved, surfaced, used) become a formal lifecycle. A CRP value from Ms. Reyes's record gets walked from raw signal to clinical decision, layer by layer, with the philosopher who pushed back on the framework cited along the way.
        """
    )
    return


if __name__ == "__main__":
    app.run()
