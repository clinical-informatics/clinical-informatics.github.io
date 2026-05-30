# Glossary: 10 NLP and clinical text

Most terms used in this course are defined in the [curriculum-wide glossary](../start-here/GLOSSARY.md): annotation, concept unique identifier (CUI), de-identification, F1 score, named entity recognition (NER), negation detection, precision, quasi-identifier, recall, relation extraction, span, tokenization. Two NLP-specific terms appear in this course frequently enough to warrant a definition here.

**Confidence (in NLP).** The probability the model assigns to its prediction. Most clinical NLP pipelines emit a confidence per entity or per relation; downstream consumers can choose to keep only predictions above a confidence threshold.

**Uncertainty marker.** A linguistic cue that the writer is hedging a clinical statement: "possible," "rule out," "concerning for," "appears to be." A clinical NER system that ignores uncertainty extracts "rule out PE" as a positive PE finding; the standard published algorithm for handling uncertainty is the same ConText extension that handles negation.
