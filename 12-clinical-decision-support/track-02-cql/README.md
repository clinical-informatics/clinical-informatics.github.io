# Track 02: CQL (Clinical Quality Language)

CQL is the standards-based language for writing the logic of a clinical-quality measure or a clinical-decision rule. It exists for the same reason FHIR and OMOP exist: logic that cannot move between systems has to be re-implemented at every institution, and the rewrite is the source of most of the divergence in how the same rule actually behaves at different sites. The track presents the motivation, walks a published CQL fragment from a CMS quality measure in plain English, has the reader write a small CQL rule against a synthetic patient panel, and addresses the role of VSAC value sets (Course 07 vocabulary territory) as the dependency CQL inherits from the terminology layer.

**Prerequisites:** Track 01 of this course. Course 06 Track 1 (FHIR Patient, Observation, Condition resources) is the data model CQL operates on.

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 03 (CDS Hooks).
