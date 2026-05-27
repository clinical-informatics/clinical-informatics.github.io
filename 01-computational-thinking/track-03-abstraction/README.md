# Track 03: Abstraction (what to ignore)

> Your CMO has pulled you into a meeting. The data team is building a 30-day readmission risk score for case management to pilot in six weeks. They have eight hundred candidate features from the data warehouse and they want your clinical input by Friday. Their first cut already includes self-reported race, ADI, the patient's relationship status from the social-work intake, whether the discharge prescription was filled at an in-network pharmacy in the seventy-two hours after discharge, and a dozen flowsheet fields that are missing more than half the time. They are pleased with the AUC. You have a meeting on your calendar to discuss "feedback."

Decomposition (Track 01) takes a rule apart. Patterns and edge cases (Track 02) put it back together while watching the trades. Abstraction is the third move, and the one that lets a rule survive deployment: choosing what to leave out. Every feature you include is a debt (data quality, drift, monitoring, explanation, equity surveillance). Every feature you exclude is a bet that the rule will work without it. The skill is making both decisions deliberately, with reasoning you could defend to a reviewer.

This track works through the readmission-model scenario above. The interactive presents a catalogue of candidate features, lets you select which ones go in, and regenerates a deployment memo live with the equity, leakage, and missingness consequences of your choices. The output is a fifteen-line memo describing a model a real implementation team could take forward.


**Prerequisite:** Tracks 01 and 02. The vocabulary (cohort, signals, thresholds, time window, data source, trigger moment; phenotypic mimics, suppressed signals, off-cohort, off-window, missing data) is reused here without re-introduction.

**How to start:** open `notebook.py` from the file tree on the left. Marimo loads it in app mode.

**Companion reading:** [`03.1-abstraction.md`](03.1-abstraction.md) is the reference essay. Read it first, after, or not at all.

**What's next:** Track 04 takes a worked algorithm (DAS28) and walks line by line through what it is doing with the small set of features it chose to keep. Abstraction is what made DAS28 a usable measure. Track 04 makes the algorithm-in-plain-English move concrete.
