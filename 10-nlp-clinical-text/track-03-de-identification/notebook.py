"""Track 03: De-identification.

Clinical notes carry patient-identifying information embedded in narrative
prose. The track reviews the HIPAA Safe Harbor 18 identifiers, presents
the three common de-identification approaches, shows a before-and-after
on a Reyes note, and addresses the residual-risk problem that quasi-
identifiers can re-identify patients even after Safe Harbor compliance.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import re
    import sys
    import types
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "03": "Privacy, ethics, and governance",
        "13": "Research reproducibility",
        "14": "Interoperability and policy",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    _WASM_DATA_BASE = "/10-nlp-clinical-text/track-03-de-identification/app"

    def load_cached_text(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return open_url(url).read()
        return (Path(__file__).parent / "cache" / filename).read_text()

    return load_cached_text, mo, pd, re, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: De-identification

        ## The problem the track addresses

        Clinical notes can not be shared outside the originating institution without removing the patient-identifying information they carry. The HIPAA Privacy Rule sets the legal floor for sharing: a record is either fully covered by a Business Associate Agreement, fully de-identified under one of two HIPAA-defined methods, or sharing is not permitted. De-identifying a note is therefore the upstream step that has to happen before any NLP pipeline owned outside the institution can process the note, before any research dataset that includes the note can be published, and before any vendor evaluation that requires the note can begin.

        The track addresses the operational mechanics: the 18 identifier categories that the Safe Harbor method requires removed, the three common approaches to removing them, a worked before-and-after on a Reyes note, and the residual-risk problem that no method fully solves.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The HIPAA Safe Harbor 18 identifiers

        HIPAA defines two paths to de-identification. The Expert Determination method requires a qualified statistician to formally certify that the residual re-identification risk is very small. The Safe Harbor method specifies 18 identifier categories that must be removed; once all 18 are removed and the data holder has no actual knowledge that the residual data could re-identify, the record is considered de-identified by rule.

        The 18 categories are operationally precise. They are listed below in the order HHS publishes them, with a note on where each typically appears in a clinical note.
        """
    )
    return


@app.cell
def _(pd):
    safe_harbor_table = pd.DataFrame(
        [
            {"#": 1, "Identifier category": "Names", "Where it usually appears in a note": "Patient name in the header; provider names in body and signature; family-member names in HPI."},
            {"#": 2, "Identifier category": "Geographic subdivisions smaller than a state (street address, city, ZIP)", "Where it usually appears in a note": "Patient address in header; institutional addresses in signature; locations mentioned in the social history."},
            {"#": 3, "Identifier category": "All elements of dates (except year) for dates directly related to a patient: birth date, admission date, discharge date, date of death", "Where it usually appears in a note": "Date of service field; birth-date references in HPI; admission and discharge dates in summaries."},
            {"#": 4, "Identifier category": "Telephone numbers", "Where it usually appears in a note": "Header; signature blocks; sometimes patient-stated numbers in social history."},
            {"#": 5, "Identifier category": "Vehicle identifiers and serial numbers, including license plate numbers", "Where it usually appears in a note": "Trauma notes; transplant notes (donor vehicle in some cases)."},
            {"#": 6, "Identifier category": "Fax numbers", "Where it usually appears in a note": "Header; signature blocks; referral notes."},
            {"#": 7, "Identifier category": "Device identifiers and serial numbers", "Where it usually appears in a note": "Implant notes (pacemaker model, hip prosthesis catalog number)."},
            {"#": 8, "Identifier category": "Email addresses", "Where it usually appears in a note": "Header; portal-message documentation; patient-provided contact details."},
            {"#": 9, "Identifier category": "Web Universal Resource Locators (URLs)", "Where it usually appears in a note": "References to patient-facing resources; embedded EHR template URLs."},
            {"#": 10, "Identifier category": "Social Security numbers", "Where it usually appears in a note": "Disability paperwork; insurance documentation; rarely free-text but the failure case is severe when present."},
            {"#": 11, "Identifier category": "Internet Protocol (IP) address numbers", "Where it usually appears in a note": "Audit logs and metadata more often than narrative; can appear in messaging system documentation."},
            {"#": 12, "Identifier category": "Medical record numbers", "Where it usually appears in a note": "Header; cross-references between visits; clinical correspondence."},
            {"#": 13, "Identifier category": "Biometric identifiers, including finger and voice prints", "Where it usually appears in a note": "Specialized clinics; consent documentation; rare in routine narrative."},
            {"#": 14, "Identifier category": "Health plan beneficiary numbers", "Where it usually appears in a note": "Insurance verification documentation; rare in clinical narrative."},
            {"#": 15, "Identifier category": "Full-face photographic images and any comparable images", "Where it usually appears in a note": "Attached imaging; dermatology and ophthalmology notes; the image itself, not the text."},
            {"#": 16, "Identifier category": "Account numbers", "Where it usually appears in a note": "Billing documentation; financial-counseling notes."},
            {"#": 17, "Identifier category": "Certificate or license numbers", "Where it usually appears in a note": "Occupational-medicine notes; documentation for clinicians who are also patients."},
            {"#": 18, "Identifier category": "Any other unique identifying number, characteristic, or code", "Where it usually appears in a note": "The catch-all. Includes rare-disease-cohort identifiers, clinical-trial patient codes, research-registry IDs."},
        ]
    )
    safe_harbor_table.index = range(1, len(safe_harbor_table) + 1)
    safe_harbor_table.index.name = "row"
    safe_harbor_table
    return (safe_harbor_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The age cap and the date rule

        Two additional Safe Harbor requirements deserve calling out.

        **Ages over 89.** Ages over 89 (or any element of date including year that indicates such an age) must be aggregated into a single "90 or older" category. The reason: very elderly patients in a small geographic area are easy to re-identify even with all the 18 categories removed.

        **Year is kept; all other date components are removed.** "2022-03-07" is replaced with "2022" or with a shifted date. Date shifting (subtracting a per-patient random offset of 0 to 365 days from every date in that patient's record) preserves intervals while obscuring absolute dates and is the standard technique for longitudinal studies that need to preserve time-between-events.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three common de-identification approaches

        Three families of de-identification systems are used in production. Each handles the 18 categories in a different way and has different residual-risk profiles.
        """
    )
    return


@app.cell
def _(pd):
    approaches_table = pd.DataFrame(
        [
            {
                "Approach": "Rule-based",
                "How it works": "Hand-authored regular expressions and dictionaries. A name detector uses a list of common first and last names plus contextual cues ('Dr.', 'Mr.'). A date detector uses a pattern library covering common date formats.",
                "Strengths": "Transparent; easy to audit; deterministic; no training data needed; high recall on common patterns.",
                "Weaknesses": "Brittle on unusual formats; misses uncommon names; high false-positive rate on common-word surnames ('Hall', 'White').",
                "Example systems": "DEID (MGH); regex-only filters built into many EHR vendors.",
            },
            {
                "Approach": "ML-based",
                "How it works": "A sequence-labeling model trained on an annotated clinical-text corpus. Each token gets a label (PHI-NAME, PHI-DATE, PHI-LOCATION, NOT-PHI). The model generalizes beyond the training-set dictionary.",
                "Strengths": "Handles unusual names; generalizes across institutions; lower false-positive rate on common-word ambiguities.",
                "Weaknesses": "Requires training data (the i2b2 2014 corpus and equivalents are the standard); behavior on out-of-distribution text is unpredictable; harder to audit.",
                "Example systems": "BERT-based de-id models; CRF-based de-id models from i2b2 challenge era.",
            },
            {
                "Approach": "Hybrid",
                "How it works": "A rule-based layer for high-recall identifier categories (MRN, SSN, phone numbers, formatted dates) plus an ML layer for names and free-form geographic mentions. Outputs are unioned.",
                "Strengths": "Best operational performance in published evaluations; rule layer ensures the high-stakes identifiers are caught; ML layer handles the ambiguous ones.",
                "Weaknesses": "More moving parts; the two layers can disagree; tuning requires both engineering and ML expertise.",
                "Example systems": "Philter (UCSF/Penn); commercial enterprise de-id systems.",
            },
        ]
    )
    approaches_table.index = range(1, len(approaches_table) + 1)
    approaches_table.index.name = "row"
    approaches_table
    return (approaches_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two operational rules guide the choice between approaches.

        First, rule-based systems are appropriate when the source documents have a predictable structure (a single institution's EHR with consistent note templates). The rules can be tuned against the actual document distribution and audited.

        Second, ML-based or hybrid systems are required when the source documents have variable structure (multi-institutional research datasets, vendor evaluations across health systems, federated learning corpora). The ML layer is what allows performance to hold when the document structure changes.

        Every production system, regardless of approach, ships with a documented residual-risk analysis. A vendor that cannot provide one is selling a system that has not been honestly evaluated.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: before and after on a Reyes note fragment

        The fragment below is the header and first paragraph of Note 1 of 8 from Ms. Reyes's record. The "before" panel is the raw text; the "after" panel is the same text after a Safe Harbor de-identification.
        """
    )
    return


@app.cell
def _(mo):
    before = mo.md(
        """
        ```
        Note 1 of 8
        Date of service: 2022-02-14
        Author: Maya Bennett, MD - Rheumatology
        Encounter type: New patient consultation

        CHIEF COMPLAINT
        Bilateral hand and wrist pain with morning stiffness, 4 months.

        HISTORY OF PRESENT ILLNESS
        Ms. Reyes is a 48-year-old accountant referred by her PCP for evaluation
        of polyarticular joint pain. She reports symmetric pain and swelling of
        the MCP and PIP joints bilaterally, starting in October 2021, gradually
        worsening. Morning stiffness lasts approximately 90 minutes most days. She
        denies psoriasis, IBD, recent rash, sicca symptoms, or Raynaud phenomenon.
        ```
        """
    )

    after = mo.md(
        """
        ```
        Note 1 of 8
        Date of service: 2022
        Author: [PROVIDER_NAME] - Rheumatology
        Encounter type: New patient consultation

        CHIEF COMPLAINT
        Bilateral hand and wrist pain with morning stiffness, 4 months.

        HISTORY OF PRESENT ILLNESS
        [PATIENT_NAME] is a 48-year-old accountant referred by her PCP for evaluation
        of polyarticular joint pain. She reports symmetric pain and swelling of
        the MCP and PIP joints bilaterally, starting in [YEAR], gradually
        worsening. Morning stiffness lasts approximately 90 minutes most days. She
        denies psoriasis, IBD, recent rash, sicca symptoms, or Raynaud phenomenon.
        ```
        """
    )

    mo.hstack(
        [
            mo.vstack([mo.md("**Before**"), before]),
            mo.vstack([mo.md("**After Safe Harbor de-id**"), after]),
        ],
        widths="equal",
    )
    return after, before


@app.cell
def _(mo):
    mo.md(
        r"""
        Two observations about the transformation.

        First, the clinically meaningful content is preserved. The chief complaint, the symptom description, the duration of morning stiffness, the family-history mention (in the full note), the physical-exam findings, the assessment, and the plan all survive the de-identification. A clinical NLP pipeline that consumes the de-identified text can still extract the same medical entities and the same clinical reasoning.

        Second, the identifier replacement uses category-typed placeholders rather than nulls. `[PATIENT_NAME]` and `[PROVIDER_NAME]` carry the category information forward; a downstream system that needs to know "the subject of this note is the patient, not a clinician" can read the placeholder type. The alternative (replacing all identifiers with a single `[REDACTED]` token) loses category information and tends to break downstream NLP that expects entity boundaries to be visible.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Residual risk: the quasi-identifier problem

        Safe Harbor compliance does not guarantee anonymity. The 18 categories cover direct identifiers (name, MRN, SSN, address). They do not cover quasi-identifiers: fields that are not individually identifying but that, in combination, can re-identify a patient.

        The canonical academic example: Sweeney (2000) showed that 87% of the US population can be uniquely identified by the combination of ZIP code, date of birth, and gender. Safe Harbor removes the ZIP-code element below the state level and removes most of the date-of-birth element but keeps the year. The year-of-birth plus state plus gender combination remains; in a small subgroup (a 75-year-old female in Wyoming with a rare comorbidity, say), the combination still functions as a quasi-identifier.

        Three operational consequences follow.

        - **k-anonymity** is the published framework for measuring residual risk. A dataset is k-anonymous on a set of quasi-identifier fields if every combination of those fields appears in at least k records. Common targets are k >= 5 or k >= 11 depending on the data-sharing context.
        - **The "no actual knowledge" clause** in HIPAA conditions Safe Harbor compliance on the data holder having no actual knowledge that the residual data could be used to re-identify the patient. A data holder who sees that the quasi-identifier combination is unique in the data set has actual knowledge and Safe Harbor compliance is no longer sufficient.
        - **Rare-disease cohorts** are typically not de-identifiable under Safe Harbor alone. A rare diagnosis is itself a quasi-identifier when the cohort is small; the Expert Determination pathway with formal disclosure-risk modeling is the only honest route.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What clinical NLP pipelines do with de-identified text

        Once a note has been de-identified, the downstream NLP pipeline operates on it the same way it would on the original. The identifier placeholders are skipped by the entity-extraction step (they do not match any clinical NER target). The clinical text around them is unaffected.

        One operational note: NLP systems that perform coreference resolution (linking pronouns to their antecedents) lose the ability to attach pronouns to specific persons after de-identification. "She denies psoriasis" still works because "she" remains as a pronoun; but if the note mentioned "Dr. Smith advised Ms. Reyes that..." and both names were de-identified to `[PROVIDER_NAME]` and `[PATIENT_NAME]`, the coreference step has to operate on the placeholders rather than on the names. Most pipelines handle this gracefully; the failure mode is corner cases where the placeholder type matters for the clinical reasoning.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "10",
        "03",
        "The HIPAA framework that motivates Safe Harbor",
        "Course 03 Track 2 introduced HIPAA as a floor rather than a ceiling and introduced the Safe Harbor and Expert Determination methods. This track operationalizes the Safe Harbor 18 categories at the document level and addresses the operational mechanics of identifier removal. The residual-risk discussion here is the operational consequence of the 'no actual knowledge' clause Course 03 introduced.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "10",
        "13",
        "De-identification as a reproducibility issue",
        "Course 13 takes up the broader reproducibility framework. A de-identification step in a research pipeline has to be documented (which method, which version, which residual-risk analysis) for the downstream analysis to be reproducible. The Expert Determination certificate is a research-artifact dependency in the same way a data-use agreement is.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Clinical notes carry patient-identifying information embedded in narrative prose. The HIPAA Safe Harbor method specifies 18 identifier categories that must be removed before a note can be shared. Three approaches (rule-based, ML-based, hybrid) implement the removal; hybrid systems are the production standard. Safe Harbor compliance does not guarantee anonymity because quasi-identifiers (year-of-birth plus state plus gender, rare diagnoses) can re-identify patients even after the 18 categories are removed; k-anonymity and the Expert Determination pathway address the residual risk.

        Track 04 takes up large language models in clinical text, the second strand of clinical NLP that has joined the classical pipeline since 2023.
        """
    )
    return


if __name__ == "__main__":
    app.run()
