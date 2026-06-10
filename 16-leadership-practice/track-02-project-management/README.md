# Track 02: Project management for informatics

You have six months. The CMIO wants a project plan in two weeks. A project plan is three commitments in one document: what will ship (scope), when each piece happens and in what order (the schedule), and who does and who answers for each piece (ownership). Track 02 presents the toolkit that produces those commitments: PMBOK's five process groups as the shared vocabulary, methodology selection (waterfall, Agile, Scrum, Kanban) as a fit decision rather than an allegiance, the Gantt chart with its milestones, dependencies, and critical path, the RACI matrix with the one-A rule, the scope/time/cost triangle that governs what gives under pressure, and the SDLC that names where the build sits inside the plan.

The RA-CDS deployment is the worked example throughout, and it is a hybrid, which is the usual case in clinical informatics: the EHR integration build runs as waterfall against freeze windows and sign-off gates, model validation and card-text tuning run as Scrum sprints, and the post-launch optimization queue runs as Kanban. Two interactives carry the track. A Gantt builder renders the six-month plan reactively and flags dependency violations (training before the build completes, validation after launch) and unrealistic compression. A RACI builder assigns the five deployment activities across five roles and validates the structure: exactly one Accountable per activity, no Accountable without a Responsible, no executive doing build work. The track's artifacts, the milestone timeline and the RACI matrix, become sections 2 and 3 of the capstone implementation plan.

**Prerequisites:** Track 01 (the roles and committees the plan assigns work to); Course 12 (the CDS design brief this project implements).

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 03 (change management).
