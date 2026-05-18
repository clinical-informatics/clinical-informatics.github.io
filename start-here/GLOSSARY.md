# Glossary

A curriculum-wide list of terms. Each entry defines the term in plain English, without other jargon inside the definition. Where a term means something subtly different in a particular course, that course will say so.

If a term you encountered is not here, email me at [fmario619@gmail.com](mailto:fmario619@gmail.com) and I will add it.

---

**Anti-CCP.** Short for anti-cyclic citrullinated peptide antibody. It's a blood test. When it's positive, it strongly suggests rheumatoid arthritis. Ms. Reyes is anti-CCP positive. That's a major part of why her diagnosis is "seropositive RA."

**Bias (in epidemiology).** A systematic error in how a study was designed or run that pushes the answer in a wrong direction. The three big families are selection bias (who got into the study), information bias (how data was collected), and confounding (some other variable explaining the link). Bias is not the same as imprecision. Bias is *wrong on average*, not *noisy*.

**Bias (in algorithms).** When a model performs differently for different groups of people in a way that produces harm or unfairness. The two senses share the word but mean slightly different things. The privacy and AI courses use the algorithmic sense.

**Brier score.** A number between 0 and 1 that measures how good a model's *probabilities* are, not only its rankings. Lower is better. If a model predicts a 70% chance of admission and the patient is admitted, the Brier contribution is small; if it predicts 5% and the patient is admitted, the contribution is large. The score averages this across patients. A model can rank patients well (good discrimination) yet still be wrong about the probabilities (bad calibration). Brier captures both.

**Calibration.** How well a model's predicted probabilities match the actual outcome rates. A perfectly calibrated model that says "30% chance" is right exactly 30% of the time. Calibration matters because clinicians often act on the number, not the ranking. See **discrimination** for the contrast.

**Capstone.** The final notebook at the end of each course. A capstone consolidates the work of every track in that course into one applied exercise. Some capstones are building tasks (build a cohort, design a CDS rule). Others are Socratic: you commit to an answer before the ideal analysis is revealed.

**CDS Hooks.** A standard for clinical decision support that defines *moments in the workflow* (called "hooks") at which an EHR can call out to an external service and get back a card with a recommendation. Three hooks matter most: `patient-view` (clinician opened a chart), `order-select` (a medication or test is being ordered), and `order-sign` (the order is about to be signed). The CDS course covers all three.

**Claims data.** Records that an insurer keeps about what was billed for a patient. A claim has a date of service, diagnosis codes (ICD-10), procedure codes (CPT or HCPCS), a place of service, and a dollar amount. Claims are *not* the clinical record. They're what was billed. The health economics course unpacks the gap between the two.

**Clinical Quality Language (CQL).** A language for writing the logic of a quality measure or a clinical decision rule. The point of CQL is that the same rule should run on any system that speaks FHIR, instead of being rewritten for every EHR. The CDS course walks through reading and writing simple CQL.

**Cohort.** A group of patients who share something in common: a diagnosis, an exposure, a date of birth. Cohort definition is most of the work in clinical research. The cohort builder component lets you see how each criterion shrinks the cohort.

**Concept ID.** In OMOP, every clinical fact (a diagnosis, a drug, a lab) gets translated into a stable integer identifier called a concept ID. The concept ID is what makes OMOP portable. Your "metformin" and my "metformin" both become concept ID 1503297, no matter what your EHR called it.

**Confidence interval.** A range of plausible values for whatever you're estimating, calculated in a way that, if you repeated the study many times, the interval would contain the true value 95% of the time (for a 95% CI). What it actually does for you: it tells you how precise your estimate is. A point estimate of 0.6 with a CI of (0.59, 0.61) is very different from 0.6 with a CI of (0.2, 0.95).

**Confounding.** When two things appear to be related, but only because they're both related to a third thing. Coffee drinkers have higher rates of lung cancer, not because coffee causes cancer, but because in the years that data was collected, coffee drinkers smoked more. Smoking confounded the relationship. The epidemiology course is largely about confounders.

**Decision curve analysis (DCA).** A way to evaluate a clinical decision tool that says: "for the range of thresholds a real clinician might use, does using this tool produce more net benefit than treating everyone, or treating no one?" The DCA plot is the unifying tool for the curriculum. It sits at the intersection of test performance, decision making, and clinical value.

**De-identification.** The process of removing the parts of a dataset that could be used to identify a specific person. HIPAA has two methods: Safe Harbor (remove 18 specific things) and Expert Determination (have a qualified statistician certify the risk is small). De-identification is *not* the same as anonymization. Re-identification is sometimes possible from de-identified data.

**Discrimination.** How well a model separates patients who have an outcome from patients who don't. AUC is one common measure. A model with great discrimination ranks the at-risk patients above the not-at-risk ones, *but it might still be wrong about the actual probabilities.* See **calibration** for the contrast. Both matter. The AI course is built around this distinction.

**EHR.** Electronic health record. The software system clinicians use during patient care. Sometimes used to mean the software, sometimes the patient's record inside it. Context usually makes it clear.

**Encounter.** A specific clinical interaction. An office visit, an admission, a phone call. In FHIR it's a resource. In OMOP it's a row in `visit_occurrence`. Encounters are how clinical data gets organized in time.

**FHIR (R4).** Fast Healthcare Interoperability Resources, release 4. A standard for representing clinical data and exchanging it between systems. FHIR uses small, modular resources (Patient, Observation, Condition, MedicationRequest, and so on) along with the web technology you already know: HTTP, REST, JSON. FHIR is the lingua franca of modern health IT.

**HL7 v2.** An older standard for exchanging clinical messages, used since the late 1980s. Messages are pipe-delimited and notoriously hard to read. Still in use everywhere. FHIR is the modern successor for most use cases, but v2 is not going away.

**HIPAA.** The Health Insurance Portability and Accountability Act. The U.S. federal law that, among other things, sets the rules for protecting individually identifiable health information. HIPAA is a *floor*. Your institution will often add more protections on top.

**Incidence.** How many *new* cases of something happen in a period of time. Distinct from prevalence (how many people *have* it right now). For a chronic disease like RA, prevalence is much higher than incidence.

**Information blocking.** Practices that interfere with the access, exchange, or use of electronic health information. The Cures Act made information blocking against the law for most actors in health IT. The policy course goes into what changed and what didn't.

**Interoperability.** When two systems can share information *without either of them having to change*. Your data works in their system. Their data works in yours. Distinct from portability (see below). FHIR is the leading bet on interoperability.

**LOINC.** Logical Observation Identifiers Names and Codes. A coding system for lab tests, vital signs, and other clinical measurements. If you want to say "C-reactive protein in serum, mass per volume" in a way another system will understand, you say LOINC 1988-5.

**Marimo.** The reactive Python notebook environment this curriculum uses. Marimo runs entirely in the browser, with no install required. When you change an input (slider, dropdown, value), every downstream cell recomputes automatically. That reactivity is what carries the interactive parts of each track and each capstone.

**MCAR / MAR / MNAR.** Three kinds of missingness. Missing Completely At Random: data is missing for reasons that have nothing to do with anything. Missing At Random: data is missing for reasons that are explained by other variables you have. Missing Not At Random: data is missing for reasons related to the value that would have been there. Each one calls for a different approach. The data literacy course covers all three.

**NPV.** Negative predictive value. If a test comes back negative, what's the probability the patient really doesn't have the disease? NPV depends on prevalence. In a low-prevalence setting, most negative tests are truly negative, regardless of the test itself.

**Observation (FHIR).** A FHIR resource for any measurement or finding. Vital signs, lab results, imaging measurements, even social history questions. The FHIR course spends a lot of time on Observation because it's the resource you'll touch most often.

**OMOP CDM.** Observational Medical Outcomes Partnership Common Data Model. A standardized table layout and concept vocabulary that lets researchers run the same query against datasets from many different institutions. OMOP is about portability. Making your data look like everyone else's. Distinct from FHIR (see above), which is about interoperability.

**OR / RR / HR.** Odds ratio, risk ratio, hazard ratio. Three ways of expressing how much more (or less) likely an outcome is in one group versus another. They are *not* interchangeable. The epidemiology course explains when each is appropriate, and why mixing them up is one of the most common errors in clinical research.

**Phenotype.** In informatics, a definition of a clinical condition that can be applied to a dataset. "Diabetes" might be defined as "at least one ICD-10 code in the E11.x family AND at least one HbA1c above 6.5%." Phenotyping is most of what cohort building actually is.

**Portability.** When you can move your data from one system to another. Doesn't require both systems to understand the data the same way. Distinct from interoperability (see above). OMOP is about portability. FHIR is about interoperability. You usually want both.

**PPV.** Positive predictive value. If a test comes back positive, what is the probability the patient really has the disease? PPV depends on prevalence: in a low-prevalence setting, a high-specificity test can still produce mostly false positives. The 2x2 table chapter of the epidemiology course is built around this dependency.

**Prevalence.** How many people in a population have a thing right now. Distinct from incidence (how many *new* cases per year). PPV depends on prevalence, which is why a great test can still produce mostly false positives in a low-prevalence setting.

**ROC curve.** Receiver operating characteristic curve. A plot that shows, for every possible threshold of a test or model, the tradeoff between catching real positives (sensitivity) and falsely flagging negatives (1 minus specificity). The curve is the test's discrimination performance. The area under the curve (AUC) summarizes it in a single number.

**RxNorm.** A coding system for medications, maintained by the National Library of Medicine. RxNorm normalizes the many ways a drug might be named in different systems (branded, generic, dose form, route) into a single identifier.

**Sensitivity.** Of the people who really have the disease, what fraction does the test catch? Also called the true positive rate.

**SMART on FHIR.** A standard for launching third-party applications inside an EHR with authorization, identity, and context handled correctly. SMART is *how* an external CDS service gets called from inside an EHR.

**SNOMED CT.** Systematized Nomenclature of Medicine, Clinical Terms. A very large, hierarchical terminology for clinical concepts. Diagnoses, body sites, procedures, findings. SNOMED has codes for all of them. The structure (concepts have parent concepts) lets you ask things like "all forms of inflammatory arthritis" without having to enumerate them.

**Specificity.** Of the people who really don't have the disease, what fraction does the test correctly clear? Also called the true negative rate.

**Standard (in informatics).** An agreement about how data or interactions should be structured, written down formally enough that independent teams can implement it and have their systems interoperate. Standards exist for terminology (LOINC, SNOMED, RxNorm), for data models (OMOP, FHIR), for messages (HL7 v2, CDA), for security (OAuth), and many other layers.

**Value set.** A list of codes that count as "the thing" for a given purpose. The value set "diabetes diagnoses" might include all the E11.x ICD-10 codes plus a few O24.x codes (gestational diabetes). Value sets live in VSAC (Value Set Authority Center) and are the building blocks of quality measures and CDS.

**Visit (OMOP).** A row in the `visit_occurrence` table representing a clinical encounter. OMOP's equivalent of FHIR's Encounter.
