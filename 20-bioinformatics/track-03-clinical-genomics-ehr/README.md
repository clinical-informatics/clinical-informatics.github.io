# Track 03: Clinical genomics in the EHR

The clinical-genomics loop has four parts: the order placed by the clinician, the lab's processing pipeline that produces the variant call, the report returned to the EHR, and the display the clinician reads. The track addresses each part with the standards that govern it (HL7 Genomics Reporting IG for the report shape, GA4GH variant representation for the variant itself), the ACMG 79-gene incidental-findings list that defines what a clinical exome should report back, the canonical pharmacogenomic examples (TPMT before azathioprine, CYP2C19 before clopidogrel, HLA-B*5701 before abacavir), and the operational reality that most US EHRs today store genomic reports as PDFs rather than structured data. Ms. Reyes's HLA-DRB1*04:01 result is the worked example of the PDF-vs-structured-field gap.

**Prerequisites:** Tracks 01 and 02 of this course. Course 06 (Learn FHIR) is the data-model anchor for the structured-genomic-reporting discussion.

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 04 (research bioinformatics infrastructure).
