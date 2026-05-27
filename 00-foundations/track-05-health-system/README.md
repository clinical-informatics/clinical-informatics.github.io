# Track 05: The American health system and its parts

The boundaries Track 04 covered (LAN to firewall, firewall to internet, internet to vendor cloud, vendor cloud to research collaborator) are between systems run by different actors. *We need ONC to certify this*, *the BAA with the vendor is the blocker*, *CMS will pay for it under the new rule*, *the IRB owns the research authorization*, *LOINC won't have a code for that for two cycles*: each of those sentences references a specific actor doing a specific job. This track is the org chart. Knowing the actors is most of what makes the sentences legible.

Seven sets of actors do most of the work.

1. **Providers.** Hospitals (AMC, community, critical-access, safety-net), clinics, physician practices, FQHCs, allied health.
2. **Payers.** Commercial insurers, Medicare, Medicaid, TRICARE, VA, IHS.
3. **EHR vendors.** Epic, Oracle Health (formerly Cerner), MEDITECH, Athenahealth, and the specialty-specific vendors that sit alongside them.
4. **Regulators.** CMS, ONC, FDA, HHS, OCR. What each one regulates and how the rules connect.
5. **Research infrastructure.** NIH, AHRQ, CTSAs, disease registries, PCORnet, the FDA's Sentinel System.
6. **Public health.** CDC, state Departments of Public Health, local health departments. Where the COVID-era visibility came from.
7. **Standards bodies.** HL7, IHE, LOINC, SNOMED CT, RxNorm, ICD-10, NCPDP, X12. The vocabularies and protocols that hold the rest together.

Every clinical informatics decision touches more than one of these groups. The closing exercise of the track maps a single referral scenario (Ms. Reyes seeing an out-of-state hand surgeon) to the five actor groups whose agreement is load-bearing and notices why the visit's timing is set by the slowest of the shared agreements.

**Prerequisites:** Track 04 (the boundaries the actors govern).

**How to start:** open `notebook.py` from the file tree on the left.

**What's next:** Track 06 (roles, ethics, and where the literature lives).
