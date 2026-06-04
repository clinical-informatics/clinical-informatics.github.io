# Track 05: Where the gaps still are

After the Cures Act, after HTI-1 and HTI-2, after TEFCA's QHIN network became operational, and after USCDI reached v6 in 2025 with v7 in draft, what does an interop-curious clinician still find broken? The honest answer is patient matching, the slow USCDI cadence relative to clinical need, and the AI-transparency provisions that HTI-1 created but that enforcement infrastructure has not yet caught up to. Track 05 covers each remaining gap, the policy mechanism each connects to (TEFCA's identity-matching framework, the ONC USCDI rulemaking cadence, the OIG enforcement pathway for HTI-1 DSI disclosures), and the trajectory of each.

Three gaps remain operationally significant. The United States has no national patient identifier; HIPAA in 1996 authorized one under Section 1173(b), and an appropriations rider has prevented its funding every fiscal year since 1999, leaving cross-organizational matching to probabilistic algorithms with match rates between 50% and 90% depending on data quality. USCDI evolves on a roughly one-year cadence that lags clinical need, because the data classes for social determinants, behavioral health, and AI-model outputs each took several versions to appear, and certified-EHR upgrade cycles add another two-to-four-year lag between a USCDI version being finalized and being widely supported in production. The HTI-1 Decision Support Intervention requirements introduce model-transparency obligations on certified EHRs (the source attribute disclosures for any predictive DSI), but the enforcement infrastructure (audits, OIG referrals, civil monetary penalties for algorithmic non-disclosure) is still being built out as of 2026, which means the requirements exist on paper before they have teeth in practice.

**Prerequisites:** Tracks 01 through 04 of this course. Course 09 (AI in medicine) is the substantive anchor for the HTI-1 DSI material.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** the course capstone.
