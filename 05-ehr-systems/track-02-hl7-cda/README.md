# Track 02: HL7 v2, CDA, and what we inherited

Most of the messages flowing between systems in your hospital right now are HL7 v2 pipe-and-caret messages. Your lab system sends an ORU^R01 to the EHR every time a result lands. Your ADT system sends an ADT^A04 every time someone registers for a visit. Your radiology system sends an ORM^O01 every time an imaging order goes out. The format is from 1987.

This track is the historical arc. Why HL7 v2 looks the way it does. Why CDA happened in 2005 and what it solved (and didn't). Why FHIR happened in 2014 and where it picks up. You read real messages, you parse them, and by the end you can look at a pipe-delimited dump from a lab system and know what it is saying.

**Estimated time:** 60 minutes.

**Prerequisites:** Track 01 of this course. Familiarity with the idea of clinical messaging is helpful but not required.

**How to start:** open `notebook.py` in Marimo. The notebook ships with three real-shaped synthetic messages (one HL7 v2 ADT, one HL7 v2 ORU, one CDA fragment) all about Ms. Reyes.

**Companion reading:** `02.1-hl7-cda.md` in this folder walks the history at your own pace.

**What's next:** Track 03 (clinical data warehouses).
