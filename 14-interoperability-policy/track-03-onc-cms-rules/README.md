# Track 03: ONC and CMS interoperability rules

Why did FHIR adoption accelerate so rapidly between 2020 and 2024? The technical case for FHIR R4 over HL7 v2 had been clear for several years. The proximate cause of acceleration was regulatory. The 2020 ONC Cures Act Final Rule and the 2020 CMS Interoperability and Patient Access Final Rule together made FHIR R4 the required wire format for certified EHRs and for CMS-regulated payers, and the 2024 HTI-1 Final Rule extended both the data scope (USCDI v3, now v6 in 2025) and the algorithmic-transparency requirements (the Decision Support Intervention criteria). Track 03 covers what each rule requires, how the rules interlock, and how the requirements connect to the FHIR material from Course 06.

Two regulatory tracks converge to mandate FHIR R4. ONC mandates it of certified EHRs through the Conditions and Maintenance of Certification, which require a standardized API for patient and population services (FHIR R4 plus the SMART App Launch IG) and conformance to the current USCDI version for the certified data set. CMS mandates it of regulated payers through the 2020 Patient Access Final Rule (CMS-9115-F: the Patient Access API, the Provider Directory API, and Payer-to-Payer exchange) and the 2024 Advancing Interoperability and Improving Prior Authorization Final Rule (CMS-0057-F: a Prior Authorization API, a Provider Access API, and an expanded Payer-to-Payer API). The cross-reference back to Course 06 is direct: every API the rules mandate is built on the FHIR resources that course covered, and the SMART on FHIR launch flow Track 5 of Course 06 walked is the same OAuth flow CMS now requires payers to support for patient-app authorization.

**Prerequisites:** Track 02 of this course. Course 06 is the technical anchor for the FHIR references throughout this track.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 04 (the international landscape).
