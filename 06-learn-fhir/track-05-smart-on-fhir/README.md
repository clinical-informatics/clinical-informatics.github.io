# Track 5: SMART on FHIR

> Track 4 said SMART is another implementation guide. Track 5 reads it that way: an IG layered on US Core, defining an OAuth flow plus a scope vocabulary plus a launch context that lets a single app plug into every SMART-enabled EHR.

The final track of the FHIR course. You walk the SMART App Launch flow (two launch flavors, six OAuth steps, the well-known/smart-configuration discovery, the scope vocabulary, the token response with launch context), see CDS Hooks and Bulk Data at the concept level (both deepened in Course 12), then write a one-page design brief for a SMART app for rheumatology monitoring that leans on the gap analysis you wrote in Track 4 as its underlying data model.

The capstone is Socratic: six commit-and-reveal steps walking the design questions you would actually face (problem statement, launch flavor, scopes, UI surface, FHIR data needs, optional CDS Hook integration), each gated until you write something. The notebook assembles your committed answers into a one-page design brief ready to take to a project kickoff.


**Prerequisites:** Tracks 0 through 4 of this course. Track 4's gap analysis output is the underlying data model the capstone designs an app around; the SMART spec reads as another IG because Track 4 made you fluent in reading IGs.

**How to start:** open `notebook.py` in this folder from the file tree on the left. Marimo loads it in app mode. The cached `/.well-known/smart-configuration` and a representative token response live in `cache/`.

**Companion reading:** [`05.1-smart-on-fhir.md`](05.1-smart-on-fhir.md) is a short reference essay covering SMART-as-IG, the two launch flavors, the OAuth dance, scopes, CDS Hooks at concept level, Bulk Data at concept level, and what a clinical informaticist should ask when evaluating a vendor's SMART app.

**What's next:** the course-level capstone (`06-learn-fhir/capstone/`), which is to author and validate a complete FHIR record for Ms. Reyes on hapi.fhir.org. Track 3's authoring patterns scale up to her full record; Track 4's profile awareness keeps the resources conformant; this track's vocabulary is what lets a downstream SMART app actually use the record.
