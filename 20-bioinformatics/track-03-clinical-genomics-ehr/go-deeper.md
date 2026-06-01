# Go deeper: Clinical genomics in the EHR

**If you want to understand the standards better before moving on:**

- [The HL7 FHIR Genomics Reporting Implementation Guide](https://hl7.org/fhir/uv/genomics-reporting/) is the canonical specification for representing genomic test results as structured FHIR resources. The guide defines the Observation profiles for variants and the DiagnosticReport profiles for the lab report; it is the operational answer to the PDF-genomic-report problem.
- [The Global Alliance for Genomics and Health (GA4GH) Variation Representation Specification](https://www.ga4gh.org/product/variation-representation/) is the cross-standard reference for how a genomic variant is represented unambiguously. The VRS spec sits underneath the FHIR Genomics IG and is the right reference for the variant-representation layer specifically.

**If you want to see this applied clinically:**

- [The CPIC (Clinical Pharmacogenetics Implementation Consortium) guidelines](https://cpicpgx.org/guidelines/) are the published consensus on pharmacogenomic-guided dosing for individual drug-gene pairs. The TPMT-azathioprine, CYP2C19-clopidogrel, and HLA-B*5701-abacavir guidelines are short, well-written, and are the operational reference for the canonical pharmacogenomic CDS interventions.
- [The ACMG / AMP Standards and Guidelines for the Interpretation of Sequence Variants (Richards et al., Genetics in Medicine 2015)](https://www.gimjournal.org/article/S1098-3600\(21\)00876-4/fulltext) is the canonical reference for the five-tier (pathogenic, likely pathogenic, uncertain significance, likely benign, benign) variant-classification framework that clinical-genomics reports use.

**If you want to go significantly further:**

- [The ACMG Recommendations for Reporting of Secondary Findings (current version)](https://www.acmg.net/ACMG/Medical-Genetics-Practice-Resources/Practice-Guidelines.aspx) maintains the list of genes (originally 56, currently 79) for which a pathogenic variant identified incidentally should be reported. The ACMG page hosts the current revision and the historical rationale; the list is updated periodically as new actionable conditions are added.
