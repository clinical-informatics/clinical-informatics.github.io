# Track 2: Working with FHIR servers

> Track 1 had a FHIR bundle on your desk. Where did it come from? In this track you ask the server for it yourself.

You make real calls to `hapi.fhir.org` (the public FHIR test server), read what comes back, build search URLs piece by piece with a LOINC code coming from a dropdown, walk pagination, and pull CRP and ESR for a synthetic cohort of five RA patients across four years into an interactive trend chart. Python is introduced gently: most cells have one or two visible lines that build a URL, send a `GET`, or parse a dict.

The track walks the full request-and-parse loop end to end. The skills here are the same ones you would use against any production FHIR server. The capstone (a CRP/ESR trend chart for the synthetic cohort) is where the pieces come together in one image.


**Prerequisites:** Tracks 0 and 1 of this course. The five-layer interop framework from Track 0 and the resource/reference/bundle/terminology ideas from Track 1 are both load-bearing here.

**How to start:** open `notebook.py` in this folder from the file tree on the left. Marimo loads it in app mode. The notebook caches its `hapi.fhir.org` responses in `cache/` so it runs deterministically and works offline; delete those files to force live re-fetches.

**Companion reading:** [`02.1-fhir-servers.md`](02.1-fhir-servers.md) is a short reference essay covering the same patterns (server, URL, parse, paginate) plus a small section on why real test servers behave the way they do.

**What's next:** Track 3 is where you write FHIR. Track 2 was the read half; Track 3 is the write half.
