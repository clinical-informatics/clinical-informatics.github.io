# Capstone: From narrative notes to structured fields, and the gap between

A pre-built NLP pipeline (provided inline in the notebook) runs across all 8 of Ms. Reyes's notes. The output is a structured representation of every medication change, every lab value mentioned, every condition assessment, and every plan element. The structured EHR record for the same period is shown alongside. The capstone is the gap analysis: which medication changes appear in the notes but never reached a structured medication-order row, which lab values were mentioned in narrative but never coded, which assessments were documented as prose but never carried into the problem list. The reflection asks which gaps are tolerable for retrospective research, which are not, and which the institution would have to close before relying on structured-only queries for clinical operations.

**Prerequisites:** all five tracks in this course.

**How to start:** open `notebook.py`. Marimo loads it in app mode.
