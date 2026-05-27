# Track 03: Secondary use of clinical data

A patient consents to a blood draw because her rheumatologist needs to track CRP. That blood draw produces a row in a lab table. The row lives in the EHR, then the CDW, then a research extract, then a training set for an AI model, then a benchmark dataset distributed at a conference. The patient consented to the first step. She was almost certainly not asked about the rest.

This track is about that gap between what patients consent to and what their data ends up doing. The legal framework (Track 02) permits most of what happens in that chain. The ethical question is harder. Legal permission and ethical defensibility are not the same thing, and the literature is full of cases where they came apart.

Five pieces:

1. **The primary/secondary distinction.** Care versus everything else. What "everything else" contains in modern clinical informatics.
2. **The legal/ethical gap.** Why HIPAA can be satisfied while the underlying social contract is violated. Three landmark cases (Henrietta Lacks, Havasupai, Google/Ascension's Project Nightingale).
3. **Consent, broad consent, and waivers.** What patients are asked at the time of care. What research consent at intake does and does not cover. When IRBs grant waivers and what they require.
4. **The five dimensions of ethical risk.** Consent-expectation fit, public versus commercial benefit balance, equity, transparency, reversibility. A framework you can apply to any proposed secondary use.
5. **Commercial versus academic versus translational.** Where the data goes matters. A pharma deal, a vendor partnership, a public benchmark, and a publication are different ethical questions even when they use the same de-identified data.

The interactive piece is a scenario analyzer. The learner picks one of six secondary-use scenarios, scores risk along each of the five dimensions, and then sees a worked ethical analysis. The purpose is not to produce a number. The purpose is to make the dimensions visible so the conversation has a shape.


**Prerequisites:** Tracks 01 and 02 of this course. The threat model from Track 01 and the legal framework from Track 02 are both load-bearing here.

**Companion reading:** `03.1-secondary-use.md` in this folder.

**What's next:** Track 04 on algorithmic fairness. Many of the equity concerns about secondary use surface most sharply in the AI/ML context, which Track 04 covers directly.
