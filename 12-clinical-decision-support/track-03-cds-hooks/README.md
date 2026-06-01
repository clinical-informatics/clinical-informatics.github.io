# Track 03: CDS Hooks

CDS Hooks is the standards-based delivery layer for CDS. A hook is a defined workflow moment (the clinician opened a chart, the clinician is selecting a medication, the clinician is signing an order) at which the EHR calls out to one or more external CDS services and receives back a list of recommendation cards to display. The track presents the architecture, walks the three load-bearing hooks (patient-view, order-select, order-sign) with the JSON request and response payload for each, and demonstrates an end-to-end CDS Hooks call on a simulated Reyes order-sign moment with the reader designing the card content.

**Prerequisites:** Tracks 01 and 02 of this course; Course 06 Track 5 (SMART on FHIR and the OAuth launch context that CDS Hooks shares).

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 04 (Evaluating CDS).
