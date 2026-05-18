# Ms. Reyes, mapped to OMOP CDM tables

This folder contains Ms. Reyes's data mapped to the OMOP Common Data Model
(version 5.4). Each CSV maps to a standard OMOP table:

| File | OMOP table | What it stores |
|---|---|---|
| `person.csv` | `person` | Demographics. One row per person. |
| `visit_occurrence.csv` | `visit_occurrence` | Each clinical encounter |
| `condition_occurrence.csv` | `condition_occurrence` | Diagnoses recorded during a visit |
| `drug_exposure.csv` | `drug_exposure` | Each known drug exposure period |
| `measurement.csv` | `measurement` | Lab results and vital signs |
| `observation.csv` | `observation` | Other findings (DAS28, allergy, etc.) |

The key thing to look at: every clinical fact gets translated into a
**concept_id** from the OMOP vocabulary. The concept_id is a stable
integer identifier, the same across institutions. Compare this to the
EHR exports in the parent folder, where the same fact might be encoded
as ICD-10, SNOMED, a vendor-internal code, or a free-text string. OMOP
collapses all of those into one shared integer.

In the data-wrangling course (07), you'll build this mapping yourself.
