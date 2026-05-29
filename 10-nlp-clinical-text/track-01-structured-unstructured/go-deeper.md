# Go deeper: Structured vs unstructured data

**If you want to understand the structured / unstructured distinction better before moving on:**

- [HL7 FHIR R4 documentation](https://hl7.org/fhir/R4/) is the canonical reference for the structured side. Reading the resource definitions for `Observation`, `Condition`, and `MedicationRequest` is the fastest way to see what the structured EHR is built to capture, and (by exclusion) what falls through to the note.
- [The Book of OHDSI, "Standardized Data: The OMOP Common Data Model"](https://ohdsi.github.io/TheBookOfOhdsi/CommonDataModel.html) presents the same structured-data picture from the secondary-use side. Reading this chapter after the FHIR chapter clarifies which clinical facts have a structured representation in either model and which usually do not.

**If you want to see the information-loss problem applied clinically:**

- [Wang et al., "Clinical Information Extraction Applications: A Literature Review" (Journal of Biomedical Informatics 2018)](https://www.sciencedirect.com/science/article/pii/S1532046417302575) is the most-cited systematic review of clinical NLP applications. The review categorizes the kinds of clinical information that are routinely extracted from notes because no structured equivalent exists in the EHR (functional status, social history, clinical reasoning, symptom severity).

**If you want to go significantly further:**

- [Tayefi et al., "Challenges and opportunities beyond structured data in analysis of electronic health records" (WIREs Computational Statistics 2021)](https://wires.onlinelibrary.wiley.com/doi/10.1002/wics.1549) is a comprehensive overview of the gap between structured and unstructured clinical data and the methods that bridge it. The paper covers the full pipeline from extraction through downstream use, and is the right reference for a researcher designing a study that has to combine the two.
