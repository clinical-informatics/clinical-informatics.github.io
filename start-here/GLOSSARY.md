# Glossary

A curriculum-wide list of terms. Each entry defines the term in plain English, without other jargon inside the definition. Where a term means something subtly different in a particular course, that course will say so.

If a term you encountered is not here, email me at [fmario619@gmail.com](mailto:fmario619@gmail.com) and I will add it.

---

**Annotation.** The act of marking up a clinical document with the labels an NLP system is supposed to produce. The annotation is the gold standard the system is evaluated against. A human annotator reads the note, highlights the medications, the labs, the conditions, and tags each one. Inter-annotator agreement is the practical upper bound on system performance. The NLP course covers the role of annotation in evaluation.

**Anti-CCP.** Short for anti-cyclic citrullinated peptide antibody. It's a blood test. When it's positive, it strongly suggests rheumatoid arthritis. Ms. Reyes is anti-CCP positive. That's a major part of why her diagnosis is "seropositive RA."

**AUC.** Area under the ROC curve. A single number between 0.5 (chance) and 1.0 (perfect ranking) that summarizes a model's discrimination across all thresholds. AUC is the probability that a randomly picked positive case gets a higher score than a randomly picked negative case. AUC says nothing about whether the probabilities themselves are right. See **calibration** for that.

**Bias (in epidemiology).** A systematic error in how a study was designed or run that pushes the answer in a wrong direction. The three big families are selection bias (who got into the study), information bias (how data was collected), and confounding (some other variable explaining the link). Bias is not the same as imprecision. Bias is *wrong on average*, not *noisy*.

**Bias (in algorithms).** When a model performs differently for different groups of people in a way that produces harm or unfairness. The two senses share the word but mean slightly different things. The privacy and AI courses use the algorithmic sense.

**Brier score.** A number between 0 and 1 that measures how good a model's *probabilities* are, not only its rankings. Lower is better. If a model predicts a 70% chance of admission and the patient is admitted, the Brier contribution is small; if it predicts 5% and the patient is admitted, the contribution is large. The score averages this across patients. A model can rank patients well (good discrimination) yet still be wrong about the probabilities (bad calibration). Brier captures both.

**Calibration.** How well a model's predicted probabilities match the actual outcome rates. A perfectly calibrated model that says "30% chance" is right exactly 30% of the time. Calibration matters because clinicians often act on the number, not the ranking. See **discrimination** for the contrast.

**Calibration plot.** A scatter plot of observed event rate against predicted probability. Each point is a bin of patients. The dashed diagonal is perfect calibration: when the model says 30%, 30% of those patients have the outcome. Points above the diagonal mean the model is under-predicting; points below mean it's over-predicting. The AI course uses calibration plots side by side with ROC curves.

**Capstone.** The final notebook at the end of each course. A capstone consolidates the work of every track in that course into one applied exercise. Some capstones are building tasks (build a cohort, design a CDS rule). Others are Socratic: you commit to an answer before the ideal analysis is revealed.

**CDS Hooks.** A standard for clinical decision support that defines *moments in the workflow* (called "hooks") at which an EHR can call out to an external service and get back a card with a recommendation. Three hooks matter most: `patient-view` (clinician opened a chart), `order-select` (a medication or test is being ordered), and `order-sign` (the order is about to be signed). The CDS course covers all three.

**Claims data.** Records that an insurer keeps about what was billed for a patient. A claim has a date of service, diagnosis codes (ICD-10), procedure codes (CPT or HCPCS), a place of service, and a dollar amount. Claims are *not* the clinical record. They're what was billed. The health economics course unpacks the gap between the two.

**Clinical Quality Language (CQL).** A language for writing the logic of a quality measure or a clinical decision rule. The point of CQL is that the same rule should run on any system that speaks FHIR, instead of being rewritten for every EHR. The CDS course walks through reading and writing simple CQL.

**Cohort.** A group of patients who share something in common: a diagnosis, an exposure, a date of birth. Cohort definition is most of the work in clinical research. The cohort builder component lets you see how each criterion shrinks the cohort.

**Concept ID.** In OMOP, every clinical fact (a diagnosis, a drug, a lab) gets translated into a stable integer identifier called a concept ID. The concept ID is what makes OMOP portable. Your "metformin" and my "metformin" both become concept ID 1503297, no matter what your EHR called it.

**Confidence interval.** A range of plausible values for whatever you're estimating, calculated in a way that, if you repeated the study many times, the interval would contain the true value 95% of the time (for a 95% CI). What it actually does for you: it tells you how precise your estimate is. A point estimate of 0.6 with a CI of (0.59, 0.61) is very different from 0.6 with a CI of (0.2, 0.95).

**Confounding.** When two things appear to be related, but only because they're both related to a third thing. Coffee drinkers have higher rates of lung cancer, not because coffee causes cancer, but because in the years that data was collected, coffee drinkers smoked more. Smoking confounded the relationship. The epidemiology course is largely about confounders.

**CUI.** Concept Unique Identifier. The identifier UMLS assigns to a single clinical concept across the source vocabularies UMLS aggregates (SNOMED, LOINC, RxNorm, ICD, MeSH, and many others). A single CUI cross-links the codes used in different vocabularies for the same concept. The NLP course covers UMLS-CUI normalization as the standard endpoint of clinical NER.

**Decision curve analysis (DCA).** A way to evaluate a clinical decision tool that says: "for the range of thresholds a real clinician might use, does using this tool produce more net benefit than treating everyone, or treating no one?" The DCA plot is the unifying tool for the curriculum. It sits at the intersection of test performance, decision making, and clinical value.

**De-identification.** The process of removing the parts of a dataset that could be used to identify a specific person. HIPAA has two methods: Safe Harbor (remove 18 specific things) and Expert Determination (have a qualified statistician certify the risk is small). De-identification is *not* the same as anonymization. Re-identification is sometimes possible from de-identified data.

**Discrimination.** How well a model separates patients who have an outcome from patients who don't. AUC is one common measure. A model with great discrimination ranks the at-risk patients above the not-at-risk ones, *but it might still be wrong about the actual probabilities.* See **calibration** for the contrast. Both matter. The AI course is built around this distinction.

**Dual axis.** A chart with two y-axes sharing one x-axis, used to plot two unrelated variables together. Dual-axis charts are easy to construct and easy to misread; the visual impression of correlation is set by where the chart author placed each scale, not by the data. The visualization course argues against them as a default.

**EHR.** Electronic health record. The software system clinicians use during patient care. Sometimes used to mean the software, sometimes the patient's record inside it. Context usually makes it clear.

**Encoding (visual encoding).** The mapping from a data field to a visual property of a mark on a chart. Position, color, length, area, and shape are the common encodings. The accuracy with which a reader can decode each one differs; position is the most accurate, area and color are the least. Several of the chart-type decisions in the visualization course come down to which encoding to use for which variable.

**Encounter.** A specific clinical interaction. An office visit, an admission, a phone call. In FHIR it's a resource. In OMOP it's a row in `visit_occurrence`. Encounters are how clinical data gets organized in time.

**F1 score.** The harmonic mean of precision and recall. The standard scalar summary of NLP-system performance, between 0 and 1, higher is better. F1 punishes the case where one of the two is much lower than the other (a model with precision 1.0 and recall 0.1 has F1 of only 0.18). The NLP course uses F1 as the default headline number.

**FHIR (R4).** Fast Healthcare Interoperability Resources, release 4. A standard for representing clinical data and exchanging it between systems. FHIR uses small, modular resources (Patient, Observation, Condition, MedicationRequest, and so on) along with the web technology you already know: HTTP, REST, JSON. FHIR is the lingua franca of modern health IT.

**Generalization.** A model's performance on patients it has not seen during training, drawn from the same population as the training set. Generalization is the goal of training. **Overfitting** is the failure of generalization (good training performance, bad test performance). The AI course is built around the distinction.

**Hallucination.** A confidently produced output from a large language model that is not supported by any source the model had access to. Hallucinations are a property of next-token prediction, not a fixable bug. Common clinical forms include fabricated citations and made-up drug doses. The AI course covers what to do about them (retrieval-augmented generation, verification before action).

**HL7 v2.** An older standard for exchanging clinical messages, used since the late 1980s. Messages are pipe-delimited and notoriously hard to read. Still in use everywhere. FHIR is the modern successor for most use cases, but v2 is not going away.

**HIPAA.** The Health Insurance Portability and Accountability Act. The U.S. federal law that, among other things, sets the rules for protecting individually identifiable health information. HIPAA is a *floor*. Your institution will often add more protections on top.

**Incidence.** How many *new* cases of something happen in a period of time. Distinct from prevalence (how many people *have* it right now). For a chronic disease like RA, prevalence is much higher than incidence.

**Information blocking.** Practices that interfere with the access, exchange, or use of electronic health information. The Cures Act made information blocking against the law for most actors in health IT. The policy course goes into what changed and what didn't.

**Interoperability.** When two systems can share information *without either of them having to change*. Your data works in their system. Their data works in yours. Distinct from portability (see below). FHIR is the leading bet on interoperability.

**LOESS.** Locally estimated scatterplot smoothing. A way to fit a smooth curve to a noisy series without committing to a global shape (a straight line, a parabola). LOESS is useful on noisy longitudinal lab data when the underlying trend is the question. The visualization course covers LOESS alongside rolling means as the two common smoothers.

**LOINC.** Logical Observation Identifiers Names and Codes. A coding system for lab tests, vital signs, and other clinical measurements. If you want to say "C-reactive protein in serum, mass per volume" in a way another system will understand, you say LOINC 1988-5.

**Marimo.** The reactive Python notebook environment this curriculum uses. Marimo runs entirely in the browser, with no install required. When you change an input (slider, dropdown, value), every downstream cell recomputes automatically. That reactivity is what carries the interactive parts of each track and each capstone.

**MCAR / MAR / MNAR.** Three kinds of missingness. Missing Completely At Random: data is missing for reasons that have nothing to do with anything. Missing At Random: data is missing for reasons that are explained by other variables you have. Missing Not At Random: data is missing for reasons related to the value that would have been there. Each one calls for a different approach. The data literacy course covers all three.

**Named entity recognition (NER).** The NLP task of identifying spans of text that refer to specific kinds of clinical entity (medication, lab, condition, anatomical site). NER is the second stage of the classical clinical NLP pipeline after tokenization. The NLP course walks NER on Ms. Reyes's notes.

**Negation detection.** The NLP sub-task of deciding whether a clinical concept mentioned in a note is affirmed, denied, or hedged. "No fever" mentions fever but should not be extracted as a positive fever finding. The standard published algorithms are NegEx and ConText. The NLP course covers both.

**NPV.** Negative predictive value. If a test comes back negative, what's the probability the patient really doesn't have the disease? NPV depends on prevalence. In a low-prevalence setting, most negative tests are truly negative, regardless of the test itself.

**Observation (FHIR).** A FHIR resource for any measurement or finding. Vital signs, lab results, imaging measurements, even social history questions. The FHIR course spends a lot of time on Observation because it's the resource you'll touch most often.

**OMOP CDM.** Observational Medical Outcomes Partnership Common Data Model. A standardized table layout and concept vocabulary that lets researchers run the same query against datasets from many different institutions. OMOP is about portability. Making your data look like everyone else's. Distinct from FHIR (see above), which is about interoperability.

**OR / RR / HR.** Odds ratio, risk ratio, hazard ratio. Three ways of expressing how much more (or less) likely an outcome is in one group versus another. They are *not* interchangeable. The epidemiology course explains when each is appropriate, and why mixing them up is one of the most common errors in clinical research.

**Overfitting.** A model that has memorized the training set has training error near zero and test error well above zero. The model has learned features of the specific training examples rather than features of the population they're drawn from. Overfitting is what the train / validation / test split exists to detect. The AI course demonstrates it on polynomial fits of increasing complexity.

**Phenotype.** In informatics, a definition of a clinical condition that can be applied to a dataset. "Diabetes" might be defined as "at least one ICD-10 code in the E11.x family AND at least one HbA1c above 6.5%." Phenotyping is most of what cohort building actually is.

**Portability.** When you can move your data from one system to another. Doesn't require both systems to understand the data the same way. Distinct from interoperability (see above). OMOP is about portability. FHIR is about interoperability. You usually want both.

**PPV.** Positive predictive value. If a test comes back positive, what is the probability the patient really has the disease? PPV depends on prevalence: in a low-prevalence setting, a high-specificity test can still produce mostly false positives. The 2x2 table chapter of the epidemiology course is built around this dependency.

**Precision.** Two related senses. In NLP and machine learning, precision is: of the predictions a tool makes, the fraction that were correct. That is the same idea as **PPV** from epidemiology, with different vocabulary. In statistical writing, "precise" sometimes means the opposite of "noisy" (a narrow confidence interval is a more precise estimate). Context usually makes it clear.

**Prediction.** Applying a trained model to a new patient and obtaining its output. For a classifier the output is a probability or a class label; for a regressor it's a numerical score. Prediction is what the model does after training is finished.

**Prediction interval (PI).** A range constructed to contain a single future observation on a stated proportion of repeats. A 95% prediction interval is wider than a 95% confidence interval on the same data, because the PI accounts for the variability of an individual observation, not just the uncertainty in the mean. The visualization course contrasts PI with CI explicitly.

**Prevalence.** How many people in a population have a thing right now. Distinct from incidence (how many *new* cases per year). PPV depends on prevalence, which is why a great test can still produce mostly false positives in a low-prevalence setting.

**Quasi-identifier.** A field that is not on its own a HIPAA identifier but that, combined with other quasi-identifiers, can uniquely identify a patient. Examples are ZIP code, year of birth, and gender. Removing the 18 Safe Harbor identifiers does not guarantee anonymity in the presence of quasi-identifiers. The NLP course covers this in the de-identification track.

**Recall.** Of the true positives in the gold standard, the fraction a tool found. In NLP this is the same idea as **sensitivity** from epidemiology, with different vocabulary. Clinical NLP usually prioritizes recall over precision because missed entities (a missed drug allergy in a chart) tend to cost more than spurious ones.

**Reference range.** The interval that contains the central 95% of values from a healthy reference population, typically reported on the laboratory report. CRP 0 to 5 mg/L for an adult. A value outside the reference range is flagged abnormal. Reference ranges are population-level, not individual-level; an in-range value can still represent a real deviation from the patient's own baseline.

**Relation extraction.** The NLP task of identifying how two entities in a document relate. The dose-medication relation in "methotrexate 25 mg weekly" pairs the drug entity with its dose entity. Relation extraction is the third stage of the classical clinical NLP pipeline after NER.

**Retrieval-augmented generation (RAG).** A pattern that retrieves documents relevant to a query and supplies them to a large language model as context, so the model answers from the supplied sources rather than from its training distribution alone. RAG is the standard mitigation for hallucination on enterprise clinical content. The AI course covers the three stages (retrieval, augmentation, generation).

**ROC curve.** Receiver operating characteristic curve. A plot that shows, for every possible threshold of a test or model, the tradeoff between catching real positives (sensitivity) and falsely flagging negatives (1 minus specificity). The curve is the test's discrimination performance. The area under the curve (AUC) summarizes it in a single number.

**RxNorm.** A coding system for medications, maintained by the National Library of Medicine. RxNorm normalizes the many ways a drug might be named in different systems (branded, generic, dose form, route) into a single identifier.

**Sensitivity.** Of the people who really have the disease, what fraction does the test catch? Also called the true positive rate.

**SMART on FHIR.** A standard for launching third-party applications inside an EHR with authorization, identity, and context handled correctly. SMART is *how* an external CDS service gets called from inside an EHR.

**SNOMED CT.** Systematized Nomenclature of Medicine, Clinical Terms. A very large, hierarchical terminology for clinical concepts. Diagnoses, body sites, procedures, findings. SNOMED has codes for all of them. The structure (concepts have parent concepts) lets you ask things like "all forms of inflammatory arthritis" without having to enumerate them.

**Span.** A contiguous range of characters (or tokens) in a document. Most NLP systems output entity-extraction results as spans, with a start offset, an end offset, the surface text, and the predicted entity type. Strict vs lenient matching on spans is the standard distinction in NLP evaluation.

**Sparkline.** A small, label-free line chart designed for inline use, typically inside a table cell. Sparklines are useful when the shape of a trend is more important than the exact values. The visualization course covers them as a compact alternative to a full-size time series.

**Specificity.** Of the people who really don't have the disease, what fraction does the test correctly clear? Also called the true negative rate.

**Standard (in informatics).** An agreement about how data or interactions should be structured, written down formally enough that independent teams can implement it and have their systems interoperate. Standards exist for terminology (LOINC, SNOMED, RxNorm), for data models (OMOP, FHIR), for messages (HL7 v2, CDA), for security (OAuth), and many other layers.

**Standard error (SE).** The standard deviation of a sample statistic. The SE of the mean shrinks as the sample size grows, since adding observations refines the estimate of the population mean. SE is the basic uncertainty unit from which confidence intervals are constructed.

**Subgroup performance.** A model's discrimination and calibration computed separately within strata defined by patient demographics or clinical features. Equal overall performance does not imply equal subgroup performance; a model with overall AUC 0.85 can have AUC 0.65 in the smallest subgroup. Subgroup performance is the central concern of clinical fairness.

**Tokenization.** Splitting a document into tokens (words, subwords, or characters) that the downstream pipeline operates on. Clinical tokenization has to handle abbreviations, medication names, and dose expressions that general-domain tokenizers split incorrectly. The first stage of the classical clinical NLP pipeline.

**Training.** The procedure that picks the parameter values of a model by minimizing a loss function against a labeled dataset. Training does not produce a model that is correct on every patient; it produces a model that is on average close to the known outcomes for the patients in the training set. The AI course walks the picture of training without math.

**Truncated axis.** An axis whose origin is set above zero (for the y-axis) or after the natural start of the time period (for the x-axis). A truncated y-axis exaggerates small absolute changes; a truncated x-axis can omit the part of the trajectory that gives context. The visualization course covers truncated axes as one of the common misleading patterns.

**Validation set.** A subset of the data held out from training and used to tune model hyperparameters or compare candidate models. A separate test set, held out from both training and validation, is used for the final performance estimate. The AI course covers the three-way train / validation / test split and the test-set-hygiene discipline.

**Value set.** A list of codes that count as "the thing" for a given purpose. The value set "diabetes diagnoses" might include all the E11.x ICD-10 codes plus a few O24.x codes (gestational diabetes). Value sets live in VSAC (Value Set Authority Center) and are the building blocks of quality measures and CDS.

**Visit (OMOP).** A row in the `visit_occurrence` table representing a clinical encounter. OMOP's equivalent of FHIR's Encounter.
