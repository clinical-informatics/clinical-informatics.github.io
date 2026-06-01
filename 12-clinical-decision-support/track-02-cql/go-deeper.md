# Go deeper: CQL (Clinical Quality Language)

**If you want to understand CQL better before moving on:**

- [The CQL specification at HL7](https://cql.hl7.org/) is the canonical reference. The "Author's Guide" companion document is the most accessible entry point for someone reading or writing CQL for the first time; the formal specification is the deeper reference for syntax and semantics.
- [The CMS Measures Management System](https://mmshub.cms.gov/) hosts the published electronic-clinical-quality-measures (eCQMs) library. Each eCQM is published as a CQL package; reading one or two eCQMs end-to-end is the fastest way to see CQL in its production form.

**If you want to see CQL applied clinically:**

- [The Connectathon archives at Logica Health](https://www.logicahealth.org/) host the CQL artifacts used in HL7 FHIR Connectathon CDS tracks. The artifacts are real CQL rules paired with synthetic FHIR data and represent the closest publicly available analog of production CQL deployment.

**If you want to go significantly further:**

- [The Apelon CQL Engine (CQF Tools)](https://github.com/cqframework/cql-engine) is the open-source reference CQL execution engine. Reading the engine source alongside the CQL specification is the standard path for an informaticist who needs to understand exactly how a CQL rule is evaluated against a FHIR bundle.
- [The Value Set Authority Center (VSAC)](https://vsac.nlm.nih.gov/) maintained by the NLM is the canonical repository of CQL value sets. Browsing the VSAC catalog of published RA-related value sets is the right way to understand the upstream terminology dependency CQL inherits.
