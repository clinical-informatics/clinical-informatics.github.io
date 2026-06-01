# Go deeper: CDS Hooks

**If you want to understand the CDS Hooks architecture better before moving on:**

- [The CDS Hooks specification](https://cds-hooks.org/specification/current/) is the canonical reference. The "Overview" and "Hook definitions" sections are short and complete; reading them end-to-end is the fastest way to internalize the hook / request / response / card vocabulary.
- [The CDS Hooks sandbox](https://sandbox.cds-hooks.org/) is the publicly hosted demo environment maintained by the Boston Children's Hospital team. The sandbox lets the reader invoke real CDS services from a simulated EHR and inspect the JSON payloads end-to-end.

**If you want to see this applied clinically:**

- [The Logica Health CDS Hooks catalog](https://www.logicahealth.org/) lists production CDS services with the hooks they implement, the FHIR resources they request, and the cards they return. Reading the catalog gives a feel for the breadth of what CDS services do in real deployments.
- [Kawamoto et al., "Establishing a multidisciplinary initiative for interoperable electronic health record innovations at an academic medical center" (JAMIA Open 2021)](https://academic.oup.com/jamiaopen) documents the Utah CDS service deployment at scale, with discussion of the operational governance and integration choices the institution made.

**If you want to go significantly further:**

- [Kawamoto et al., "Implementing health information exchange-based clinical decision support" (Annual Review of Biomedical Data Science 2024)](https://www.annualreviews.org/journal/biodatasci) is the most current comprehensive review of CDS Hooks in production. The article addresses the standards-and-implementation gap, the governance considerations, and the technical patterns that distinguish successful CDS Hooks deployments from the ones that stalled at pilot.
