"""Capstone for course 10: From narrative notes to structured fields.

A pre-built NLP pipeline (inlined per the WASM rule) runs across all 8 of
Ms. Reyes's notes. The output is contrasted against the structured EHR
record for the same period. The capstone is the gap analysis: which
clinical facts that the notes contain never reached a structured row, and
which subset of the gaps would block a research or operational query that
depends on the structured side alone.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import re
    import sys
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    _WASM_DATA_BASE = "/10-nlp-clinical-text/capstone/app"

    def load_cached_text(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return open_url(url).read()
        return (Path(__file__).parent / "cache" / filename).read_text()

    return load_cached_text, mo, pd, re


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: From narrative notes to structured fields, and the gap between

        ## The exercise

        Ms. Reyes's 8 notes (the contents of `start-here/patients/elena-reyes/notes.txt`) carry a complete record of her rheumatoid arthritis diagnosis, her four-year treatment course, and the clinical reasoning behind each decision. Her structured EHR record (the OMOP CSVs in the same patient folder) carries the codes, the medication orders, the lab results, and the visit metadata.

        The two records overlap but are not identical. The capstone runs a pre-built NLP pipeline across the 8 notes, extracts the medication, condition, lab, and procedure mentions, and contrasts the extracted set against the structured EHR side. The gap analysis is the deliverable: which clinically meaningful facts were captured only in the notes, which would block a structured-only query, and which subset is tolerable for retrospective research vs not tolerable for clinical operations.

        The pipeline is the same regex + dictionary architecture used in Track 02, scaled to a slightly larger dictionary. It does not handle negation; spurious "positive" findings on the denied entities are visible in the output and are part of what the gap analysis has to account for.
        """
    )
    return


@app.cell
def _(load_cached_text):
    notes_text = load_cached_text("notes.txt")
    n_chars = len(notes_text)
    n_notes = notes_text.count("Note ") - 1
    return n_chars, n_notes, notes_text


@app.cell
def _(mo, n_chars, n_notes):
    mo.md(
        f"""
        ### The corpus

        - **Number of notes**: {n_notes}
        - **Total characters**: {n_chars:,}
        - **Authors**: Maya Bennett, MD (rheumatology); a primary-care follow-up; a telehealth note
        - **Date range**: 2022-02-14 (new-patient consultation) through 2025-08-19 (most recent visit)
        """
    )
    return


@app.cell
def _(re):
    MEDICATION_DICT = [
        "methotrexate", "MTX", "folic acid", "naproxen", "ibuprofen",
        "adalimumab", "Humira", "prednisone", "hydroxychloroquine",
        "etanercept", "Enbrel", "infliximab", "Remicade",
        "leflunomide", "sulfasalazine", "tocilizumab",
        "acetaminophen", "Tylenol", "calcium", "vitamin D",
    ]
    LAB_DICT = [
        "CRP", "ESR", "anti-CCP", "RF", "rheumatoid factor",
        "ANA", "anti-nuclear antibody", "uric acid", "TSH",
        "hemoglobin", "Hgb", "WBC", "platelet", "plt",
        "ALT", "creatinine", "Cr",
        "QuantiFERON", "Hep B", "Hep C", "hepatitis B", "hepatitis C",
        "vitamin D level", "CBC", "LFT",
    ]
    CONDITION_DICT = [
        "rheumatoid arthritis", "RA", "psoriasis", "IBD",
        "Raynaud", "lupus", "ankylosing spondylitis",
        "osteoarthritis", "gout", "psoriatic arthritis",
        "viral arthropathy", "anemia", "hypertension",
        "fatigue", "morning stiffness", "synovitis",
        "erosive disease", "flare",
    ]
    PROCEDURE_DICT = [
        "hand x-ray", "hand films", "ultrasound", "MRI",
        "joint injection", "intra-articular injection",
        "DXA", "bone density scan",
    ]

    def find_matches(text, dictionary, label):
        matches = []
        for term in dictionary:
            pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
            for m in pattern.finditer(text):
                matches.append({
                    "start": m.start(),
                    "end": m.end(),
                    "surface": m.group(0),
                    "entity_type": label,
                    "canonical": term,
                })
        return matches

    return (
        CONDITION_DICT,
        LAB_DICT,
        MEDICATION_DICT,
        PROCEDURE_DICT,
        find_matches,
    )


@app.cell
def _(
    CONDITION_DICT,
    LAB_DICT,
    MEDICATION_DICT,
    PROCEDURE_DICT,
    find_matches,
    notes_text,
    pd,
):
    nlp_matches = []
    nlp_matches.extend(find_matches(notes_text, MEDICATION_DICT, "MEDICATION"))
    nlp_matches.extend(find_matches(notes_text, LAB_DICT, "LAB"))
    nlp_matches.extend(find_matches(notes_text, CONDITION_DICT, "CONDITION"))
    nlp_matches.extend(find_matches(notes_text, PROCEDURE_DICT, "PROCEDURE"))
    nlp_df = pd.DataFrame(nlp_matches).sort_values("start").reset_index(drop=True)
    nlp_summary = (
        nlp_df.groupby(["entity_type", "canonical"])
        .size()
        .reset_index(name="mentions_in_notes")
        .sort_values(["entity_type", "mentions_in_notes"], ascending=[True, False])
        .reset_index(drop=True)
    )
    return nlp_df, nlp_matches, nlp_summary


@app.cell
def _(mo, nlp_df, nlp_summary):
    n_unique = len(nlp_summary)
    n_total = len(nlp_df)
    mo.md(
        f"""
        ### NLP pipeline output

        Across the 8 notes, the pipeline extracted **{n_total} entity mentions** representing **{n_unique} unique canonical entities** across four entity types (medications, labs, conditions, procedures).
        """
    )
    return n_total, n_unique


@app.cell
def _(nlp_summary):
    nlp_summary
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The structured EHR side

        The structured record for the same period is shown below, reconstructed from `start-here/patients/elena-reyes/omop/`. The structured record captures the medication orders that were placed (the `drug_exposure` rows), the lab results that came back (the `measurement` rows), the conditions that were entered on the problem list (the `condition_occurrence` rows), and the procedures that were billed.
        """
    )
    return


@app.cell
def _(pd):
    structured_df = pd.DataFrame(
        [
            {"entity_type": "MEDICATION", "canonical": "methotrexate", "in_structured_record": True, "notes": "Ordered 2022-03-07, 10 mg PO weekly; titration plan to 20 to 25 mg in note only"},
            {"entity_type": "MEDICATION", "canonical": "folic acid", "in_structured_record": True, "notes": "Ordered 2022-03-07, 1 mg PO daily"},
            {"entity_type": "MEDICATION", "canonical": "naproxen", "in_structured_record": True, "notes": "Ordered 2022-02-14, 500 mg BID PRN"},
            {"entity_type": "MEDICATION", "canonical": "ibuprofen", "in_structured_record": False, "notes": "Patient-reported in HPI only; no structured order (PCP-era prescription, predates EHR encounter)"},
            {"entity_type": "MEDICATION", "canonical": "adalimumab", "in_structured_record": True, "notes": "Ordered 2024-05-15 after MTX inadequate response"},
            {"entity_type": "MEDICATION", "canonical": "Humira", "in_structured_record": False, "notes": "Brand-name mention in notes; structured side uses RxNorm ingredient code for adalimumab only"},
            {"entity_type": "MEDICATION", "canonical": "prednisone", "in_structured_record": True, "notes": "Short taper 2025-01-12 to 2025-04-30"},
            {"entity_type": "MEDICATION", "canonical": "hydroxychloroquine", "in_structured_record": False, "notes": "Discussed in note as future option if flare recurs; never ordered"},
            {"entity_type": "MEDICATION", "canonical": "calcium", "in_structured_record": False, "notes": "OTC, patient-reported; no structured order"},
            {"entity_type": "MEDICATION", "canonical": "vitamin D", "in_structured_record": False, "notes": "OTC, patient-reported; no structured order"},
            {"entity_type": "LAB", "canonical": "CRP", "in_structured_record": True, "notes": "LOINC 1988-5, longitudinal series across all visits"},
            {"entity_type": "LAB", "canonical": "ESR", "in_structured_record": True, "notes": "LOINC 4537-7"},
            {"entity_type": "LAB", "canonical": "anti-CCP", "in_structured_record": True, "notes": "LOINC 32218-7, baseline only"},
            {"entity_type": "LAB", "canonical": "RF", "in_structured_record": True, "notes": "LOINC 11572-5, baseline only"},
            {"entity_type": "LAB", "canonical": "hemoglobin", "in_structured_record": True, "notes": "LOINC 718-7"},
            {"entity_type": "LAB", "canonical": "ALT", "in_structured_record": True, "notes": "LOINC 1742-6"},
            {"entity_type": "LAB", "canonical": "creatinine", "in_structured_record": True, "notes": "LOINC 2160-0"},
            {"entity_type": "LAB", "canonical": "vitamin D level", "in_structured_record": False, "notes": "Mentioned in plan as 'check at next visit', never resulted"},
            {"entity_type": "LAB", "canonical": "CBC", "in_structured_record": False, "notes": "CBC is a panel name in narrative; structured side has the component labs as separate measurement rows"},
            {"entity_type": "LAB", "canonical": "LFT", "in_structured_record": False, "notes": "LFT is a panel name in narrative; structured side has the component labs as separate measurement rows"},
            {"entity_type": "CONDITION", "canonical": "rheumatoid arthritis", "in_structured_record": True, "notes": "ICD-10 M05.79; problem-list entry 2022-03-07"},
            {"entity_type": "CONDITION", "canonical": "anemia", "in_structured_record": False, "notes": "Documented in 2022-02-14 note as 'mild anemia, suspect chronic disease'; never coded"},
            {"entity_type": "CONDITION", "canonical": "morning stiffness", "in_structured_record": False, "notes": "Symptom, not a billable diagnosis; lives in HPI of every note"},
            {"entity_type": "CONDITION", "canonical": "synovitis", "in_structured_record": False, "notes": "Exam finding, not a billable diagnosis; lives in physical exam of multiple notes"},
            {"entity_type": "CONDITION", "canonical": "erosive disease", "in_structured_record": False, "notes": "Radiologic finding; lives in 2022-03-07 note assessment, no structured radiologic-finding code in this EHR"},
            {"entity_type": "CONDITION", "canonical": "flare", "in_structured_record": False, "notes": "Mentioned in 2025-01-12 note as the trigger for the prednisone taper; no structured flare-event field exists in RA care"},
            {"entity_type": "PROCEDURE", "canonical": "hand x-ray", "in_structured_record": True, "notes": "CPT 73120, billed 2022-03-07"},
            {"entity_type": "PROCEDURE", "canonical": "hand films", "in_structured_record": False, "notes": "Narrative synonym for hand x-ray; not a separate structured procedure"},
            {"entity_type": "PROCEDURE", "canonical": "joint injection", "in_structured_record": False, "notes": "Discussed in 2025-01-12 note as future option; never performed during this 4-year record"},
        ]
    )
    structured_df.index = range(1, len(structured_df) + 1)
    return (structured_df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The gap

        The NLP-extracted entities are compared against the structured record. Each row of the table above is one canonical entity the NLP pipeline found in the notes; the `in_structured_record` column says whether the same entity has a row on the structured side. Many entries have `in_structured_record = False`. The gap is what the structured-only query would miss.

        The filter below lets the reader narrow the gap by entity type.
        """
    )
    return


@app.cell
def _(mo):
    gap_filter = mo.ui.dropdown(
        options=["All", "MEDICATION", "LAB", "CONDITION", "PROCEDURE"],
        value="All",
        label="Filter the gap by entity type",
    )
    gap_filter
    return (gap_filter,)


@app.cell
def _(gap_filter, structured_df):
    gap_only = structured_df[~structured_df["in_structured_record"]].copy()
    if gap_filter.value != "All":
        gap_only = gap_only[gap_only["entity_type"] == gap_filter.value]
    gap_only = gap_only.reset_index(drop=True)
    gap_only.index = range(1, len(gap_only) + 1)
    return (gap_only,)


@app.cell
def _(gap_only):
    gap_only[["entity_type", "canonical", "notes"]]
    return


@app.cell
def _(gap_filter, gap_only, mo, structured_df):
    n_gap = len(gap_only)
    n_total_filt = len(structured_df) if gap_filter.value == "All" else int((structured_df["entity_type"] == gap_filter.value).sum())
    pct_gap = n_gap / n_total_filt * 100 if n_total_filt else 0.0
    mo.md(
        f"**Gap size**: {n_gap} of {n_total_filt} canonical entities in the {gap_filter.value} category live only in the notes ({pct_gap:.0f}%)."
    )
    return n_gap, n_total_filt, pct_gap


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The reveal: what was lost

        The structured-only query would miss four operationally important categories of fact, each visible in the gap table above.

        **Patient-reported OTC medications.** Ibuprofen, calcium, vitamin D. None of these have structured medication-order rows because the patient was already taking them when she presented; the rheumatologist documented them in HPI but did not enter orders for them. A structured medication query for "what is this patient taking" returns the prescribed list, not the actual list. The clinical relevance is significant: ibuprofen plus methotrexate is a hepatotoxicity concern, and calcium plus methotrexate plus future bisphosphonates is a bone-health interaction to plan around. None of this is queryable from the structured side.

        **Brand-name vs ingredient-name medication mentions.** "Humira" appears in narrative; the structured side uses the RxNorm ingredient code for adalimumab. A research query that searches for "Humira" specifically would return no rows on the structured side. This is not data loss in the strict sense (the ingredient is there) but is a common source of confusion when researchers write queries.

        **Symptom-level clinical content.** Morning stiffness, fatigue, synovitis. These are present in every note's HPI and exam. None are billable diagnoses; none enter the problem list; none appear in the OMOP `condition_occurrence` table. A cohort study of "RA patients with significant morning stiffness" cannot be defined from the structured side alone; it requires an NLP layer extracting the morning-stiffness duration from each visit's HPI.

        **Plan-and-reasoning content.** Hydroxychloroquine "as a future option if flare recurs." Joint injection "if you would like." Vitamin D level "check at next visit." Each is a clinically meaningful plan element that influenced the rheumatologist's downstream decisions; none has any structured representation in this EHR. A quality measure that tries to assess "shared decision-making was documented" can not run on the structured side.

        The combined gap is the routine reality of structured-vs-unstructured clinical data. The structured side captures the conclusions, the orders, and the results. The narrative side captures the reasoning, the patient-reported information, the plan elements that never became orders, and the symptom-level texture. Both are needed for most clinical questions of interest.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection

        Three reflection questions for the reader. There is no reveal; writing the answers is the work.
        """
    )
    return


@app.cell
def _(mo):
    refl_research = mo.ui.text_area(
        label="1. Which of the gap categories above would be tolerable in a retrospective research study you might design?",
        rows=4,
        full_width=True,
        placeholder="Think about a study design where the structured side alone would be adequate.",
    )
    refl_clinical = mo.ui.text_area(
        label="2. Which of the gap categories would be unacceptable for a clinical-operations use (a CDS rule, a quality measure, a population-management dashboard)?",
        rows=4,
        full_width=True,
        placeholder="Think about a clinical use where the structured side alone would mislead.",
    )
    refl_remedy = mo.ui.text_area(
        label="3. If you had to bridge the gap, would you invest in better structured-data capture at point-of-care, or in better NLP extraction from notes, or both? What considerations drive the answer at your institution?",
        rows=4,
        full_width=True,
        placeholder="Consider the cost, the workflow burden on clinicians, and the maintenance burden on the informatics team.",
    )
    mo.vstack([
        refl_research,
        refl_clinical,
        refl_remedy,
        mo.callout(
            mo.md("_There is no answer key. The reflection is the work._"),
            kind="neutral",
        ),
    ])
    return refl_clinical, refl_remedy, refl_research


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Go deeper

            For the structured-vs-unstructured framing, the Wang et al. 2018 Journal of Biomedical Informatics review (linked from the Track 01 go-deeper) is the canonical reference. For the operational question of how to deploy a production clinical NLP pipeline alongside the structured side, the cTAKES documentation and the Savova et al. 2010 paper (linked from the Track 02 go-deeper) are the foundational references. For the LLM-based alternative to a classical pipeline, the Track 04 go-deeper has the references; Med-PaLM and the BioBERT family are the standard starting points.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A pre-built NLP pipeline applied to Ms. Reyes's 8 notes extracted entities across medications, labs, conditions, and procedures. The structured EHR record for the same period was reconstructed from her OMOP CSVs. The gap analysis showed that the structured side misses four operationally important categories: patient-reported OTC medications, brand-name mentions, symptom-level clinical content, and plan-and-reasoning content. The combined gap is why most clinical questions of interest require both representations of the same encounter.

        Course 10 closes here. Course 11 (Health economics data) takes up the claims-and-cost view of the same clinical record.
        """
    )
    return


if __name__ == "__main__":
    app.run()
