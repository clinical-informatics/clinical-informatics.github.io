# Go deeper: LLMs and clinical text

**If you want to understand the clinical-LLM landscape better before moving on:**

- [Lee et al., "Benefits, Limits, and Risks of GPT-4 as an AI Chatbot for Medicine" (NEJM 2023)](https://www.nejm.org/doi/full/10.1056/NEJMsr2214184) is the load-bearing clinical-medicine-audience overview of LLM capabilities and failure modes in clinical text settings. It is the same reference cited in Course 09 Track 6 and is the right starting point for the LLM angle on clinical NLP specifically.
- [Singhal et al., "Large language models encode clinical knowledge" (Nature 2023)](https://www.nature.com/articles/s41586-023-06291-2) documents Med-PaLM, the most-cited specifically-clinical large language model from the academic literature, and reports its performance against MedQA, PubMedQA, and the USMLE-style benchmarks the track addresses.

**If you want to see clinical-domain fine-tuning applied:**

- [Lee et al., "BioBERT: a pre-trained biomedical language representation model for biomedical text mining" (Bioinformatics 2020)](https://academic.oup.com/bioinformatics/article/36/4/1234/5566506) is the foundational paper on biomedical-domain BERT fine-tuning. The paper documents the corpus, the fine-tuning procedure, and the performance gains on biomedical NER and relation extraction over general-domain BERT.
- [Alsentzer et al., "Publicly Available Clinical BERT Embeddings" (NAACL 2019)](https://arxiv.org/abs/1904.03323) is the corresponding clinical-text paper. It documents ClinicalBERT, fine-tuned on MIMIC notes, and is the standard starting point for clinical-text BERT applications.

**If you want to go significantly further:**

- [Bommasani et al., "On the Opportunities and Risks of Foundation Models" (Stanford CRFM 2021)](https://arxiv.org/abs/2108.07258) is the comprehensive academic survey of the foundation-model paradigm that produced modern LLMs. Sections 2 (capabilities), 4 (technology), and 5 (applications) cover the architectural and capability landscape; Section 3 addresses the application-domain consequences including the medical setting.
