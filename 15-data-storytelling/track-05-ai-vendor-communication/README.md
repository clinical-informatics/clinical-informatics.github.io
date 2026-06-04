# Track 05: Communicating with AI teams and vendors

A vendor walks into a meeting with a 32-slide deck on their clinical-AI product. Three of those slides will be about model performance; the rest are about market opportunity, customer logos, and integration partners. The clinician in the room is being asked to evaluate whether the product makes sense for the institution. The default failure mode is to defer to the vendor's framing, which by design draws the reader's attention to the strongest claims and away from the weakest. Track 05 covers the practice of the clinician as the domain expert in the room: the questions that surface what the vendor would prefer the buyer not see, the discipline of asking comparative questions rather than absolute ones, and the cross-reference to the AI-evaluation framework Course 09 built.

Three properties of the clinician's questions are load-bearing. The **question is specific**, asking about a precise mechanism rather than the marketing summary (not "is your model accurate" but "what was the AUC in the subgroup with chronic kidney disease at your second validation site"). The **question is comparative**, asking how the feature compares to an explicit alternative (not "does your model detect sepsis" but "how does your model's PPV at the operational threshold compare to the existing rules-based alert at our institution"). The **question is operational**, asking about what happens in failure modes (not "what's your accuracy" but "when the model is wrong, what is the clinical workflow consequence and how is the error surfaced"). The clinician's job is not to evaluate machine learning; the clinician's job is to know what good clinical work looks like and to ask the question that produces the most informative answer about whether the product supports that work.

**Prerequisites:** Tracks 01 through 04 of this course. Course 09 (AI in medicine) is the substantive anchor for the evaluation framework underlying the questions.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** the course capstone.
