# Go deeper: Bias, fairness, and clinical risk

**If you want to understand the central published case:**

- [Obermeyer et al., "Dissecting racial bias in an algorithm used to manage the health of populations" (Science 2019)](https://www.science.org/doi/10.1126/science.aax2342) is the load-bearing reference for clinical algorithmic bias. The paper documents how a widely deployed risk-prediction tool used healthcare cost as a proxy for healthcare need and as a result systematically under-flagged Black patients. The paper is the most-cited single example of a label-choice bias entering at the proxy step.

**If you want the methodological foundations:**

- [Fairness and Machine Learning: Limitations and Opportunities](https://fairmlbook.org/) by Barocas, Hardt, and Narayanan is free online and is the standard graduate-level treatment of the fairness-metric trade-off. Chapter 2 ("Classification") and Chapter 3 ("Relationships between criteria") cover the demographic-parity vs equalized-odds vs calibration-parity impossibility the track summarizes.
- The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) is the published US federal framework for AI risk management, including bias and fairness. It is the document a clinical informaticist negotiating with a vendor or a procurement team would cite.

**If you want to see this applied clinically:**

- [Rajkomar et al., "Ensuring Fairness in Machine Learning to Advance Health Equity" (Annals of Internal Medicine 2018)](https://www.acpjournals.org/doi/10.7326/M18-1990) is the clinical-medicine-audience treatment of the same material as the Barocas / Hardt / Narayanan book. It defines the fairness metrics in clinical terms and addresses the trade-offs in clinical examples.
- [Wiens et al., "Do no harm: a roadmap for responsible machine learning for health care" (Nature Medicine 2019)](https://www.nature.com/articles/s41591-019-0548-6) is the most-cited clinical-AI ethics framework paper. It addresses the same vendor-evaluation questions the track closes with.

**If you want to go significantly further:**

- The [Algorithmic Justice League](https://www.ajl.org/) extends the clinical material into the broader societal context of algorithmic bias. The site hosts publications, advocacy material, and pointers to the original facial-recognition audit work (Buolamwini and Gebru 2018) that brought algorithmic bias to broad public attention.
