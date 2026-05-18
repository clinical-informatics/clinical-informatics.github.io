# Track 1: FHIR fundamentals

> A FHIR bundle from another rheumatologist's office lands on your desk an hour before Ms. Reyes's appointment. You need to read it.

This track teaches you to pick up an unfamiliar FHIR bundle, name what's in it, follow the references between resources, and pull a clinically coherent picture out the other side. No FHIR authoring yet (Track 3 covers that). The work here is the navigation skill that makes everything else in the course possible.

Four foundational ideas before the capstone: what a **resource** is and how to recognize one by its fields; how **references** connect resources; what a **bundle** is and what its `type` field means; and which **terminology** system (LOINC, SNOMED CT, RxNorm, UCUM, ICD-10, CVX) belongs in which slot. Plus a concept-level introduction to **search parameters** so Track 2 starts on familiar ground. The capstone walks six clinical questions about Ms. Reyes, each answered by navigating her actual FHIR bundle, then synthesized into a five-to-seven-sentence clinical summary.


**Prerequisites:** Track 0 of this course (Before FHIR, no code). The five-layer interop framework from Track 0 (transport, format, structure, terminology, content) is the spine of this track.

**How to start:** open `notebook.py` in this folder from the file tree on the left. Marimo loads it in app mode. The bundle file is at `patients/elena-reyes/fhir-bundle.json` if you want to inspect it directly while you work.

**Companion reading:** [`01.1-fhir-fundamentals.md`](01.1-fhir-fundamentals.md) is a short reference essay covering the same four foundational ideas plus the three-question framework for reading any unfamiliar resource.

**What's next:** Track 2 introduces talking to a FHIR server with Python. The search-parameter concepts from this track become real queries; the bundle-reading skills become real cohort assembly.
