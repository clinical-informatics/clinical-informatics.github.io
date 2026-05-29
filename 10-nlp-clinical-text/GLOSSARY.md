# Glossary: 10 NLP and clinical text

The terms below appear across the five tracks. Terms in the curriculum-wide glossary are not repeated here.

**Annotation.** The act of marking up a corpus with labels (entity spans, relations, attributes) that an NLP system is trained or evaluated against. The annotation is the gold standard; the NLP output is judged against it.

**Concept Unique Identifier (CUI).** The UMLS-assigned identifier for a single biomedical concept. CUIs cross-link across the source vocabularies UMLS aggregates (SNOMED, LOINC, RxNorm, ICD, MeSH, and many others); a single CUI may map to multiple codes in different source vocabularies.

**Confidence (in NLP).** The probability the model assigns to its prediction. Most clinical NLP pipelines emit a confidence per entity or per relation; downstream consumers can choose to keep only predictions above a confidence threshold.

**De-identification.** The process of removing or transforming patient-identifying information from a clinical document so the residual document can be shared for research or quality improvement without violating HIPAA. The HIPAA Safe Harbor method enumerates 18 identifier categories that must be removed.

**F1 score.** The harmonic mean of precision and recall. F1 = 2 * (precision * recall) / (precision + recall). F1 is the standard scalar summary of NLP-system performance on entity extraction or classification tasks.

**Named entity recognition (NER).** The NLP task of identifying spans of text that refer to specific categories of entity (person, location, drug, lab test, condition). Clinical NER targets categories like medication, dose, route, frequency, problem, test, anatomical site, and observation.

**Negation detection.** The NLP sub-task of determining whether a clinical concept mentioned in a note is being affirmed, denied, or framed as uncertain. "No fever" mentions fever but should not be extracted as a positive fever finding; the standard published algorithms for this are NegEx and ConText.

**Precision.** Of the entities the NLP system identified, the fraction that the gold-standard annotation also marked. Precision is equivalent to positive predictive value (PPV) from Course 04.

**Quasi-identifier.** A field that is not on its own a HIPAA identifier but that, combined with other quasi-identifiers, can uniquely identify a patient. Examples: ZIP code, date of birth, gender. Removing the 18 Safe Harbor identifiers does not guarantee anonymity in the presence of quasi-identifiers.

**Recall.** Of the entities the gold-standard annotation marked, the fraction the NLP system found. Recall is equivalent to sensitivity from Course 04.

**Relation extraction.** The NLP task of identifying how two entities in a document are related. The dose-medication relation in "methotrexate 25 mg weekly" pairs the drug entity with its dose entity; the change-medication relation in "increased lisinopril from 10 to 20 mg" pairs the drug with both the prior dose and the new dose.

**Span.** A contiguous range of characters (or tokens) in a document. Most NLP systems output entity-extraction results as spans, with a start offset, an end offset, the surface text, and the predicted entity type.

**Tokenization.** Splitting a document into tokens (words, subwords, or characters) that the downstream pipeline operates on. Clinical tokenization is harder than general-domain tokenization because of clinical abbreviations, medication names, and dose expressions that general tokenizers split incorrectly.

**Uncertainty marker.** A linguistic cue that the writer is hedging a clinical statement: "possible," "rule out," "concerning for," "appears to be." A clinical NER system that ignores uncertainty extracts "rule out PE" as a positive PE finding; the standard published algorithm for handling uncertainty is the same ConText extension that handles negation.
