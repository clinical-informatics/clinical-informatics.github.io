# Go deeper: What NLP actually does

**If you want to understand the classical pipeline better before moving on:**

- [The cTAKES documentation](https://ctakes.apache.org/) covers the canonical open-source clinical NLP pipeline (Apache cTAKES). The pipeline is the standard reference implementation of the tokenization plus NER plus relation-extraction plus negation-detection architecture and is widely used in clinical NLP research.
- [The scispaCy documentation](https://allenai.github.io/scispacy/) covers a more modern, Python-native clinical NLP toolkit from the Allen AI institute. The site includes a quick-start guide that runs end-to-end on a sample biomedical document; reading the demo is the fastest way to see the pipeline outputs side by side.

**If you want to see this applied clinically:**

- [Savova et al., "Mayo clinical Text Analysis and Knowledge Extraction System (cTAKES)" (JAMIA 2010)](https://academic.oup.com/jamia/article/17/5/507/830823) is the foundational clinical NLP paper. The paper documents the pipeline architecture and reports performance on the i2b2 shared-task data; it is the most-cited single reference for the architecture pattern.
- [Demner-Fushman et al., "What can natural language processing do for clinical decision support?" (Journal of Biomedical Informatics 2009)](https://www.sciencedirect.com/science/article/pii/S1532046409001087) is the clinical-CDS perspective on the same toolkit. The paper addresses which NER targets matter for which CDS tasks and is the right complement to the cTAKES technical paper.

**If you want to go significantly further:**

- [Stanford NLP, "Speech and Language Processing"](https://web.stanford.edu/~jurafsky/slp3/) by Jurafsky and Martin is free online and is the standard graduate textbook. Chapters 4 (text classification), 8 (sequence labeling), and 19 (information extraction) cover the pipeline at the level of someone who has to implement or extend it.
