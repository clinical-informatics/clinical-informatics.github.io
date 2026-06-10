# Track 08: Implementation and operations of clinical information systems

Go-live day, 07:00. The command center opens. Six months from now, nobody will remember the project; they will know only whether the system works every day. Track 08 specifies what runs between those two points. The organizing distinction is deploy-and-run: a project ends; a system runs. Day-2 operations is where a clinical information system lives for 95% of its lifespan, and four things change hands at the project-to-operations boundary: funding (project budget to operating budget), governance (project steering to change control), staffing (builders to support tiers), and measurement (milestones to KPIs and SLAs). The RA flare-risk alert from the Course 12 capstone, now live at Helios Academic Medical Center, is the worked example throughout.

Three structures carry the track. The go-live command center has a roster, a stand-up cadence, severity levels, and written exit criteria that state, before launch, the conditions under which it closes. The change-control board classifies every modification to a live clinical system as standard, normal, or emergency, by risk and review path rather than by the size of the edit, and the RA-CDS adds a fourth rule: any change that alters model behavior (the firing threshold, the cohort value set, a retrain) requires AI Governance sign-off on top of board review. The support tiers (L1 help desk, L2 application analysts, L3 builders and vendor escalation) route work by the nature of the fix required, with service-level agreements stating the response targets in advance. Around these sit the downtime procedures (forms, read-only shadow access, the recovery sequence, reconciliation, and the RA-CDS's own fail-silent commitment), the two release streams with their regression-test discipline, the post-launch optimization queue from Track 2, and retirement, where data-retention obligations outlive the application.

The notebook's exercise routes eight post-go-live events: some are tickets, some are changes, one is a patient's question, and one is a control-chart signal that no support tier can fix. The artifact is the post-go-live operations plan (command-center exit criteria, tiers and SLAs, change-control rules, downtime procedures, optimization-queue cadence); the capstone collects it as section 9 of the implementation plan.

**Prerequisites:** Track 01 (the committees and roles), Track 02 (the project plan and the Kanban queue), and Track 04 (the control-chart discipline) of this course; Course 12 for the design brief the running scenario continues.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** the course capstone (the implementation plan).
