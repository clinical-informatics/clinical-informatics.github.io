# Go deeper: Standards in the EHR

**If you want to understand each standard better before moving on:**

- [LOINC](https://loinc.org/) is the canonical home of LOINC. The browseable search is the fastest way to look up the LOINC for a specific lab.
- [SNOMED CT browser](https://browser.ihtsdotools.org/) lets you navigate the SNOMED hierarchy directly. The is-a relationships are visible in the tree view; useful for understanding why a "clinical finding" code differs from a "disorder" code.
- [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/index.html) at the National Library of Medicine is the canonical source. The RxNav browser linked from that page resolves a brand name or ingredient to its RxNorm code and links it to NDC equivalents.
- [Value Set Authority Center (VSAC)](https://vsac.nlm.nih.gov/) hosts the curated, authored value sets that other teams have published. Search for "rheumatoid arthritis" to see how different authoring teams have enumerated the same concept.

**If you want to see this applied clinically:**

- [Athena](https://athena.ohdsi.org/) is the OHDSI vocabulary browser. It is the most useful single tool for resolving a code in one standard to its equivalent in another. Search for `M05.79` to see the SNOMED, ICD-9, and OMOP-internal concept mappings side by side.
- The [Book of OHDSI chapter on Standardized Vocabularies](https://ohdsi.github.io/TheBookOfOhdsi/StandardizedVocabularies.html) is the most accessible introduction to vocabulary-aware cohort definition. The standard-concept and concept-relationship structure introduced there underpins everything in Track 02.

**If you want to go significantly further:**

- The [UMLS Metathesaurus](https://www.nlm.nih.gov/research/umls/index.html) is the comprehensive crosswalk across all major biomedical vocabularies. Registration is free for non-commercial use. The Metathesaurus is the upstream source for many of the mappings exposed through VSAC and Athena.
- For the deeper structural questions about how biomedical terminologies differ from informal classifications, [Cimino's 1998 paper "Desiderata for Controlled Medical Vocabularies in the Twenty-First Century"](https://pubmed.ncbi.nlm.nih.gov/9865037/) is still the reference. It is the article most cited when describing what a clinical vocabulary should and should not do.
