# Track 05: When to trust a computer

The first four tracks covered the moves of computational thinking: decomposition, pattern recognition with edge cases, abstraction, and algorithmic reading. The closing question is when, given a working algorithm, to act on what it tells you. The short answer is: when you can answer four questions about it. The long answer is the work of this track.

The four questions:

1. **What was it trained on?**
2. **What does it optimize for?**
3. **Where does it fail?**
4. **Who does it fail for?**

Answer all four for any clinical algorithm in front of you, and you can decide whether to deploy it on your patients. If you cannot, you are deciding by trust, and trust is a separate decision that should be made consciously.

This track applies the framework to a fictional but realistic case. A vendor is offering your 320-bed community hospital a deterioration-prediction score advertised at AUC 0.84, trained on 2.4 million encounter-snapshots across twelve academic medical centers. The pitch deck is glossy. The contract is in front of you. The CMO wants your input by next week's CDS committee. The notebook applies the four questions against what the pitch deck says (and does not say) and produces a defensible recommendation.


**Prerequisite:** Tracks 01 to 04. The vocabulary of cohorts, signals, thresholds, time windows, data sources, trigger moments, phenotypic mimics, suppressed signals, leakage, equity flags, and algorithmic reading is reused without re-introduction.

**How to start:** open `notebook.py` from the file tree on the left. Marimo loads it in app mode.

**Companion reading:** [`05.1-when-to-trust.md`](05.1-when-to-trust.md) is the reference essay. Read it first, after, or not at all.

**What's next:** the course capstone. A Socratic walkthrough that designs a clinical decision rule using every move from the five tracks. The output is a written design document an implementation team could act on.
