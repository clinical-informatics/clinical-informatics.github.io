# Go deeper: Evaluating NLP tools

**If you want to understand precision, recall, and F1 better before moving on:**

- [Jurafsky and Martin, "Speech and Language Processing"](https://web.stanford.edu/~jurafsky/slp3/), Chapter 4 ("Naive Bayes, Text Classification, and Sentiment") section 4.7 covers precision, recall, F1, and the related evaluation metrics in their general NLP form. The free online edition is the standard graduate reference.
- The [scikit-learn user guide on classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) is the most-used practical reference. The precision, recall, and F1 sections include the exact formulas and the macro- vs micro-averaging distinction that matters for multi-class clinical NLP tasks.

**If you want to see this applied clinically:**

- [Uzuner et al., "2010 i2b2/VA challenge on concepts, assertions, and relations in clinical text" (JAMIA 2011)](https://academic.oup.com/jamia/article/18/5/552/830538) is the foundational clinical-NLP shared-task paper. The paper documents the annotation guidelines, the inter-annotator agreement, the strict-vs-lenient matching definitions, and the system-comparison results. It is the historical benchmark every clinical NER paper compares against.
- The [n2c2 shared tasks site](https://n2c2.dbmi.hms.harvard.edu/) maintains the modern clinical-NLP benchmark tasks. The annotation guidelines for each task are linked from the task pages and are the right reference for understanding what counts as a correct extraction in each clinical sub-domain.

**If you want to go significantly further:**

- [Aronson and Lang, "An overview of MetaMap: historical perspective and recent advances" (JAMIA 2010)](https://academic.oup.com/jamia/article/17/3/229/2909118) covers the canonical clinical-NER tool (MetaMap, mapping text to UMLS Concept Unique Identifiers) and the evaluation methodology that has been applied to it across the literature. The paper is the right deep reference for the clinical-NLP-specific evaluation considerations (concept-level vs span-level matching, the UMLS-CUI normalization step that other domains do not face).
