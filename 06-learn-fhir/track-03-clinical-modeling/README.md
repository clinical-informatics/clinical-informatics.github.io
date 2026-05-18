# Track 3: Clinical modeling

> Track 2 read what the server sent back. Track 3 writes the resources the server would receive, and asks a real validator whether what you wrote is any good.

The inverse of Track 2. The track teaches what every FHIR resource type requires at minimum, what a **profile** adds on top (US Core as the worked example), what **must-support** actually means (a contract on the receiver, not the sender), how **extensions** add data the base spec does not have, and how to read the **OperationOutcome** that comes back from a server's `$validate` endpoint. The capstone authors the four resources for Ms. Reyes's next follow-up visit (Encounter + CRP, ESR, DAS28 Observations), validates them live against hapi.fhir.org, and assembles them into a transaction Bundle ready to POST.

This is the write half of FHIR end to end. Combined with Track 2, both the read and write loops are in place.


**Prerequisites:** Tracks 0, 1, and 2 of this course. The vocabulary from Track 1 (resources, references, terminology) and the request/response patterns from Track 2 are both load-bearing here.

**How to start:** open `notebook.py` in this folder from the file tree on the left. Marimo loads it in app mode. The cached OperationOutcomes ship in `cache/` so the validation walks render deterministically; the capstone's `$validate` button fires real network calls (delete the cache and it would still work).

**Companion reading:** [`03.1-clinical-modeling.md`](03.1-clinical-modeling.md) is a short reference essay on the same patterns (minimum fields per resource, profiles, must-support, extensions, `$validate`, transaction bundles).

**What's next:** Track 4 walks profiles and implementation guides systematically, with mCODE as the worked example and a gap-analysis capstone.
