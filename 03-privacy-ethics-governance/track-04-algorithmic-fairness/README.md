# Track 04: Algorithmic fairness and equity

Algorithms are not neutral. They are decisions, encoded. Every clinical AI tool, decision-support rule, and risk score embeds choices about who matters, what counts as good care, and whose data shaped the model. When those choices are made carelessly, the resulting tool inherits and amplifies the disparities of the system that produced it.

This track is the working clinician's framework for evaluating any model or CDS tool. It does not require an ML background. It requires careful thinking about where bias enters, what published clinical examples have already documented, and what questions to ask before deploying anything.

Six pieces:

1. **The five places bias enters.** Training data (who is missing). Labels (what the outcome variable actually measures). Features (proxies that smuggle protected characteristics back in). Deployment context (a model is only valid where it was tested). Feedback loops (model decisions shape future training data).
2. **The Obermeyer 2019 case.** A widely deployed commercial algorithm used "cost" as a proxy for "need." Black patients receive less spending on their care. The algorithm therefore underestimated their illness severity. Correcting the proxy would more than double the proportion of Black patients flagged for intervention.
3. **Vyas, Eisenstein, Jones 2020 (Hidden in Plain Sight).** A review of clinical algorithms that explicitly use race as an input: eGFR/MDRD, ASCVD risk, VBAC success calculator, lung function reference equations, and more. Each case raises the same question: what biological mechanism is "race" actually standing in for?
4. **The pulse oximeter case.** Not a learned ML model but the same structural failure. A device validated on a predominantly light-skinned population systematically overstates oxygen saturation in patients with darker skin. Documented at the bedside during COVID.
5. **Fairness metrics and the impossibility result.** Demographic parity, equalized odds, calibration. Kleinberg, Mullainathan, and Raghavan's 2016 result: a non-trivial model cannot satisfy all three simultaneously unless the base rates are equal across groups. The choice of fairness criterion is itself a value judgment.
6. **The seven questions.** A practical checklist for any model, CDS tool, or vendor demo. Each question maps to a class of bias the prior sections named.

The interactive piece is a synthetic deterioration predictor evaluated across subgroups. The learner moves the decision threshold and watches subgroup-specific sensitivity, specificity, and PPV change. When subgroup base rates differ, the curves move in opposite directions, and the impossibility result becomes concrete.


**Prerequisites:** Tracks 01 through 03 of this course. Track 03's equity dimension and Track 01's threat model are both load-bearing here.

**Companion reading:** `04.1-algorithmic-fairness.md` in this folder.

**What's next:** Track 05 on governance. Once you can see where bias enters and which questions to ask, the next question is who is in the room when these decisions are made, and what the clinician's role is.
