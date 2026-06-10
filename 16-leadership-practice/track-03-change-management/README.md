# Track 03: Change management

The build is on schedule. The CDS Hooks service passed integration testing, the card renders correctly, and the six-month timeline from Track 02 is holding. Then a colleague at another health system, one year into a similar flare-risk deployment, sends a warning: 47% of their rheumatologists hit dismiss every time the CDS fires. The model was validated and the build was clean; the deployment failed anyway, because the half of the deployment made of people was never engineered. Track 03 covers the discipline that engineers it: change management, the set of frameworks for moving an organization and the individuals inside it from current behavior to new behavior deliberately.

Three frameworks carry the track, at three altitudes. Lewin's unfreeze-change-refreeze names the basic shape of any deliberate change. Kotter's 8 steps are the organization-level playbook, applied here step by step to the RA-CDS rollout: urgency grounded in the treat-to-target gap, a guiding coalition holding the rheumatology chief and one respected skeptic, short-term wins counted during the month 5 soft launch, and the alert anchored as part of the standard visit workflow. ADKAR is the individual-level complement: a rollout succeeds one rheumatologist at a time, and Awareness, Desire, Knowledge, Ability, and Reinforcement name what each of them needs, in order. The track adds sociotechnical systems theory at concept level (Course 17 Track 6 treats it at depth), the four pillars of sustainable change (workflow, culture, training, sustainment), and the operating principle that resistance is information: a 47% dismiss rate is a measurement to investigate, never a verdict to retune away.

The case study is Sepsis Watch at Duke, documented twice: the Sendak et al. implementation paper says what was built, and the Elish and Watkins ethnography says what it took to make it work, including the repair work the architecture diagrams never show. The notebook's interactive is a change-readiness assessment for the RA-CDS: five dimensions scored 1 to 5, a launch recommendation computed from the total, and specific guidance on whichever dimension is weakest. The track's artifact is the change-management plan, which the capstone collects as section 4 of the implementation plan.

**Prerequisites:** Track 01 (the roles and committees) and Track 02 (the project plan and the six-month timeline); Course 12 (the CDS design brief this scenario continues).

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 04 (healthcare quality improvement and operations management).
