# Glossary: 16 Informatics leadership and professional practice

Plain-English definitions for the professional-practice vocabulary course 16 introduces. The curriculum-wide glossary in the [start-here repo](https://github.com/clinical-informatics/start-here/blob/main/GLOSSARY.md) covers terms shared across multiple courses.

---

**5S.** Lean's workplace-organization practice: sort, set in order, shine, standardize, sustain. Applied to digital workplaces it means retiring dead alerts and reports, naming the live ones consistently, assigning owners, and reviewing the inventory on a schedule.

**A3 problem-solving.** Lean's one-page structured problem document (background, current condition, target condition, root-cause analysis, countermeasures, plan, follow-up), named for the paper size. The constraint is the single page: a problem that cannot be stated on one page is not yet understood.

**ABPM clinical informatics certification.** Board certification in the clinical informatics subspecialty, administered by the American Board of Preventive Medicine for most physicians (the American Board of Pathology certifies pathologists). The exam blueprint includes a Leading and Managing Change domain of about 20%. The credential is maintained through ABPM's Continuing Certification Program (CCP), the successor to maintenance of certification.

**ADKAR.** Prosci's individual-level change framework: Awareness of why the change is happening, Desire to participate, Knowledge of how to perform the new behavior, Ability to perform it under real conditions, and Reinforcement to keep it from decaying. It complements organization-level frameworks because a rollout succeeds one clinician at a time. Its practical use is diagnostic: locate which element a specific non-adopter is missing, since each gap has a different fix and only one of them is more training.

**Agile.** A value system for iterative delivery, stated in the 2001 Agile Manifesto: short cycles, working software over comprehensive documentation, requirements allowed to evolve between cycles. It fits novel analytics and model development, where the requirement is discovered by building. It is a value system rather than a single method; Scrum is one formalization of it.

**AMIA 10x10.** Continuing-education courses run by AMIA with university partners, named for the 2005 goal of training 10,000 informaticists by 2010. An on-ramp for clinicians testing the field. It is continuing education, not certification.

**Balanced scorecard.** Kaplan and Norton's guard against one-dimensional measurement: report four perspectives at once (financial, customer or patient, internal process, and learning and growth). A scorecard whose quadrants disagree is not failing; it is reporting honestly.

**BLUF (bottom line up front).** The ordering rule for executive communication: the conclusion and the ask come first, and the supporting detail follows in descending order of importance. The convention comes from military staff writing, where the reader may be interrupted at any line. It inverts the structure clinical training rewards, where the conclusion waits until after methods and results.

**Brooks's law.** The observation that adding people to a late project makes it later, because onboarding consumes the existing team's time before the new people return any. It is the reason cost rarely buys time late in a project. The practical consequence: when the schedule is fixed and pressure arrives mid-build, scope gives, not headcount.

**Build vs buy.** The decision between developing a system internally and licensing a vendor product. Sticker prices converge once integration, local validation, and internal monitoring are added to the vendor path, so the decision turns on control (who owns the firing threshold and the retuning calendar) and exit cost (termination terms, data egress, lock-in) as much as on price.

**Capital cycle.** The fixed annual calendar through which capital money moves: requests submitted in fall, scored and ranked through winter, cut to the executive envelope in early spring, approved by the board, and released when the fiscal year begins July 1. A request that misses the fall window waits a full year, because the budget it would have entered is already closed. The calendar, not project merit, decides timing.

**Capital expenditure (capex).** Money spent once on something that delivers value over multiple years: buildings, imaging equipment, perpetual software licenses, major system builds. Accounting spreads the cost over the asset's useful life (depreciation), and the spend is approved through the capital-planning cycle against a fixed annual pool. Internal FTE time that creates internal-use software can often be capitalized during the development phase.

**Change-control board.** The governance body that reviews modifications to live clinical systems before they are made. It exists because live systems fail most often immediately after someone changes them, and review forces the questions a lone editor does not ask: what consumes this field, what fires off this interface, what is the rollback. The board classifies changes as standard, normal, or emergency by risk and review path, never by the size of the edit.

**Change management.** The discipline of moving an organization, and the individuals inside it, from current behavior to new behavior deliberately. In informatics work it is the half of a deployment plan that addresses people, workflow, and culture rather than the software artifact. A technically sound CDS alert lands in the published 49 to 96 percent override range by default unless the deployment does this work on purpose.

**Change-readiness assessment.** A structured pre-launch scoring of the social half of a deployment. The track's instrument scores five dimensions (clinical champion buy-in, training plan completeness, workflow fit, sustainment plan, equity considerations) from 1 to 5 and maps the 5-to-25 total to a launch recommendation: below 15 do not launch, 15 to 19 soft launch with monitoring, 20 to 25 ready to deploy. The score's value is the conversation it forces about the weakest dimension.

**Clinical informatics fellowship.** An ACGME-accredited training program of a minimum of 24 months, open to physicians who have completed residency in any ABMS specialty. The fellowship pathway is the route to eligibility for the clinical informatics board examination.

**Common-cause variation.** The noise inherent in a stable process: the week-to-week movement a process produces even when nothing about it has changed. Reacting to it as if it were signal is tampering.

**Control chart.** A run chart extended with control limits at roughly 3 sigma above and below the center line, computed from the process's own variation. A stable process stays inside its limits and meets no rule; a point outside the limits or a rule violation signals that something happened. When a planned change occurs, limits are computed from the pre-change period and frozen, then recomputed for the new process.

**Critical path.** The longest dependency-ordered chain of activities through a project plan. Any slip on the critical path slips the end date day for day, because no slack exists along it. Activities off the path have slack; activities on it have none, so the project manager's attention belongs disproportionately to them.

**Day-2 operations.** Everything that happens to a clinical information system after the go-live stabilizes: support, changes, upgrades, outages, and eventually retirement. A system spends about 95% of its lifespan here, and its reputation with clinicians is set here rather than at the build. The term marks the boundary where funding, governance, staffing, and measurement all change hands from the project to the operating organization.

**Decision rights.** The formal answer to who decides, who is consulted, and where a contested decision escalates, settled before the decision arises. In clinical AI and CDS work, decision rights are distributed across committees (model behavior to AI governance, design standards to EMR optimization, portfolio to IT steering) rather than held by the project lead, who routes decisions and supplies evidence.

**Discount rate.** The annual rate used to shrink future cash flows into today's dollars, pricing the fact that a dollar next year is worth less than a dollar now because today's dollar could be earning a return in the meantime. Health-economic analyses conventionally use 3%.

**DMAIC.** Six Sigma's project structure: Define, Measure, Analyze, Improve, Control. The Control phase, holding a gain with monitoring and response rules, is what a control chart implements after a change is adopted, even in projects run on the Model for Improvement.

**Downtime procedure.** The pre-staged plan for working when a clinical system is unavailable, planned or unplanned. Its four components are downtime forms (paper workflows kept current with the live build), read-only shadow access (a business-continuity copy of the chart so clinicians can see the record while writes are down), the recovery sequence (restore in dependency order, verify each layer, declare uptime explicitly), and reconciliation (back-entry of the paper record with late-entry flags and verification of orders placed during the gap).

**Dual reporting.** An org design in which a role answers to two chains at once, one with authority and one with a coordination claim. Informatics roles carry it because their decisions are permanently two-sided: every choice has a clinical face (does this serve patient care) and a platform face (can the systems sustain it). The design forces clinical-vs-platform tradeoffs upward to the executive level instead of letting one side settle them by controlling the resource.

**eCQM.** An electronic clinical quality measure: measure logic computed directly from structured EHR data through certified EHR technology, replacing manual chart abstraction. An eCQM's validity is capped by the structured-data capture underneath it, which is the informaticist's part of the quality enterprise.

**Eight wastes (DOWNTIME).** Lean's catalog of non-value-adding work: Defects, Overproduction, Waiting, Non-utilized talent, Transportation, Inventory, Motion, and Extra-processing. Each has a clinical-informatics form, from alerts firing on the wrong cohort (defects) to reports nobody opens (overproduction) to seven clicks between a card and its order set (motion).

**Escalation path.** The named route a conflict travels when the parties who own it cannot resolve it: from the analyst to the director, from the director to the CMIO, from the CMIO to the executive table where one body holds authority over both sides of the conflict. A working escalation path is what makes dual reporting workable instead of paralytic.

**Fail silent and safe.** The design commitment that when an EHR cannot reach an external CDS service, the chart opens without a card rather than blocking or showing stale content. The timeout is part of the build, and a stale or wrong card is worse than no card. Writing the fail mode into the operations plan turns a service outage into an incident with a severity level instead of a mystery.

**Four pillars of sustainable change.** Workflow, culture, training, and sustainment: the four conditions that must hold on the ground for a change to survive after the project team moves on. The pillars are a conjunction, so the weakest one sets the outcome. Sustainment is the one informatics deployments most often omit: a named post-go-live owner, a recurring override review, and a retuning path.

**Freeze window.** A defined period during which normal changes are not scheduled on a live system: the go-live stabilization period, the EHR vendor's upgrade window, and high-census periods the institution designates. Emergency changes remain available during a freeze; the freeze restricts elective ones.

**Fully loaded FTE cost.** The complete cost of an employee's time: salary plus benefits plus overhead. It is the correct basis for labor lines in a project budget; budgeting bare salary understates labor cost by 30 to 40%.

**Gantt chart.** A schedule chart with time on the horizontal axis and activities on the vertical axis; each bar spans an activity's start and duration, and the ordering encodes dependencies. Milestones are the checkpoints leadership reads; activities are the work the team does. The chart makes visible whether the plan respects the dependency chain and fits inside the committed window.

**Gemba walk.** Lean's instruction to go to where the work happens and watch it directly rather than reading metrics about it. For an informaticist this means sitting in clinic watching the alert appear in real workflow instead of tuning it from a conference room.

**Go-live command center.** The temporary structure that absorbs the first weeks of operation, when issue volume is highest and the support tiers are not yet practiced. It has a roster (a lead, at-the-elbow support, analysts, an engineer on call, a vendor line, a clinical lead), a stand-up cadence with severity-based triage, and written exit criteria so that closing it is a measurement, not a mood. A department-scoped deployment runs the same structure at smaller scale; the structure, not the headcount, is what matters.

**Guiding coalition.** The small group with the authority, credibility, and skill to carry a change, named in Kotter's step 2. For a clinical deployment it pairs clinical authority (a department chief), build authority (an EMR optimization lead), and at least one respected skeptic, because colleagues who distrust the change will watch what the skeptic does. The most common informatics failure is letting the build team substitute for the coalition, so the department experiences the change as something IT did to them.

**HEDIS.** NCQA's Healthcare Effectiveness Data and Information Set, the measure set behind most health-plan quality programs. Plans are measured on their member populations and pass the incentives and data demands down to provider groups, which is how payer quality bonuses reach informatics teams.

**Hospital Inpatient Quality Reporting (IQR).** CMS's hospital-side quality reporting program. It ties the annual Medicare payment update to reporting and feeds the publicly reported comparisons on Care Compare.

**Implementation plan.** The single document that turns an approved design into an executable deployment: who authorized it (charter), who does what (RACI), when (timeline), how people change (change-management plan), how success is measured (KPIs), what it costs and returns (budget and ROI), how it is pitched (executive summary), why it fits the institution (strategic alignment), how it runs afterward (operations plan), and what could go wrong (risk register). It is the deliverable an implementation lead hands the executive sponsor before the build starts.

**IT portfolio management.** Treating the institution's IT investments as a managed, balanced portfolio rather than a backlog served in arrival order. The portfolio question is never whether a project is good; it is what mix of investments serves the strategy, and which good projects the institution therefore declines. Portfolio review recurs at the IT Steering Committee, and its honest outputs include kill and defer decisions recorded in the minutes, not only approvals.

**IT roadmap.** A 3-year sequenced plan of IT commitments, refreshed annually: year 1 firm, year 2 planned, year 3 directional. A roadmap entry has a sequence position, named dependencies, and a funding source; a wish list entry has enthusiasm. Sequencing is the honest form of prioritization because it says when, not only whether.

**Kanban.** A continuous-flow methodology: a visible board of work (to do, in progress, done) with explicit work-in-progress limits and no fixed iterations. It fits operations queues where small independent items arrive unpredictably: support tickets, optimization requests, post-launch alert tuning. It fails when the work is one large interdependent build with a fixed end date.

**Kotter's 8 steps.** The organization-level change framework: establish urgency, build a guiding coalition, form a strategic vision, communicate the vision, empower action by removing barriers, generate short-term wins, sustain acceleration, and anchor the change in culture. The steps are sequential; deployments that fail at step 2 (the coalition) rarely survive long enough for the later steps to apply. Steps 1 to 4 elaborate Lewin's unfreeze, 5 to 7 the change, 8 the refreeze.

**Leading indicator.** A measure that moves early enough to act on, such as the percentage of eligible patients with treat-to-target intensification within 90 days. A lagging indicator confirms after the fact, such as disease-activity prevalence at 12 months. A dashboard with no leading indicators delivers its first honest reading too late to steer.

**Lean.** The Toyota-derived operations philosophy: maximize the value delivered to the customer (in healthcare, the patient) and remove everything that does not contribute to it. Its recurring informatics tools are 5S, value-stream mapping, gemba walks, and A3 problem-solving, plus the eight-wastes vocabulary for naming what to remove.

**Lewin's unfreeze-change-refreeze.** The oldest change model and the shape every deliberate change shares: destabilize the current equilibrium so people accept the status quo is not tenable, transition to the new behavior with support while performance temporarily dips, then stabilize the new behavior so the system does not relax back. Modern clinical systems rarely refreeze before the next change arrives, but the three-phase shape survives inside every later framework.

**Maintenance fee.** The recurring charge a vendor adds to a software license for support, patches, and upgrades, typically 18 to 22% of the license price per year. At 20%, five years of maintenance equals the license, so the effective price of bought software roughly doubles over the first five years before integration and internal staffing are counted.

**Milestone.** A zero-duration checkpoint in a project plan that either happened or did not: sign-off obtained, silent mode started, full launch reached. Milestones are the units of status reporting to sponsors, while activities are the units of work. A good plan pairs every milestone with the dependency that gates it.

**MIPS.** CMS's Merit-based Incentive Payment System for individual clinicians and groups billing Medicare Part B. It scores quality, cost, improvement activities, and promoting interoperability, and adjusts Medicare payment up or down based on performance.

**Mission and vision statements.** A mission statement says what an institution exists to do; a vision statement says what it intends to become. Every durable IT plan derives from them: institutional priorities at the top, IT capabilities in the middle, funded initiatives at the bottom. A funding request that can state its mission link in one sentence gives the committee a reason to rank it; a request that cannot is asking the institution to pay for something it never said it wanted.

**Model for Improvement.** The default quality-improvement method in American healthcare, developed by Associates in Process Improvement and carried into hospitals by IHI. It asks three questions (what are we trying to accomplish; how will we know a change is an improvement; what change can we make that will result in improvement) and tests candidate changes with PDSA cycles. The aim must be stated with a number and a date so that failure is detectable.

**Net present value (NPV).** The sum of a project's yearly net cash flows after each has been discounted back to today's dollars. A positive NPV means the project returns more than the same money earning the discount rate elsewhere; a negative NPV means the dollars are better deployed at the opportunity-cost rate. Raising the discount rate lowers the NPV of any project whose benefits arrive later than its costs, which describes essentially all clinical IT.

**One-page discipline.** The rule that an executive document fits on one page, with an appendix carrying detail for the reader who asks. A document that cannot fit on one page reflects unfinished thinking about what the audience needs. A slide ceiling on a pitch deck is the same discipline applied to presentations.

**Operating expenditure (opex).** Money spent running the organization within the current fiscal year: salaries, subscriptions, maintenance fees, supplies. Operating lines recur, so a $60K annual maintenance commitment is a $300K five-year commitment. The capex-vs-opex classification decides which approval path a request takes, which committee hears it, and when the money becomes available.

**Outcome measure.** A KPI that measures whether the clinical state changed, such as the flare rate or mean DAS28 across a cohort. Outcome measures are the point of the intervention, but they move slowly, and a dashboard of pure outcome measures offers no handle to turn when results disappoint.

**Payback period.** The time it takes a project's cumulative discounted net benefit to cover everything spent so far, the point where the cumulative cash-flow line crosses zero. Stated in months or years from go-live. The RA-CDS breaks even about month 32 after go-live at the canonical assumptions.

**PDSA cycle.** The Model for Improvement's testing loop: Plan a change with an explicit prediction and a data-collection plan, Do the test at small scale, Study the result against the prediction, and Act by adopting the change, adapting it and testing again, or abandoning it. Its discipline is scale: one change, few users, short horizon. A failed PDSA costs a week; a failed big-bang change costs the deployment's credibility.

**PMBOK.** The Project Management Body of Knowledge, the Project Management Institute's reference standard for project work. It organizes projects into five process groups (initiating, planning, executing, monitoring and controlling, closing) and ten knowledge areas. The process groups are the time axis of a project; the knowledge areas are the subject axis.

**Portfolio steward.** The role the portfolio view adds to a clinical informaticist's job beyond project delivery: scoring requests honestly including their own, defending run and transform allocations that no department chief will champion, and arguing for the right things not to do. A deferral with a roadmap slot is a sequencing decision; a deferral without one is a polite kill, and the steward owes the requester clarity about which one was made.

**Position vs interest (interest-based negotiation).** A position is what a party says it wants; an interest is the need underneath it. Positional bargaining trades concessions on stated demands and tends toward win/lose outcomes; interest-based negotiation names the underlying needs and searches for terms that satisfy them. Naming the interest reframes a conflict from whether to under what conditions.

**Process groups (PMBOK).** The five phases of attention PMBOK assigns to a project: initiating (authorize it and name the sponsor), planning (commit to scope, schedule, budget, ownership, risk handling), executing (do the work), monitoring and controlling (measure against the plan and control changes), and closing (hand the deliverable to operations and record what was learned). They are not strictly sequential: monitoring and controlling runs alongside executing from the first week.

**Process measure.** A KPI that measures whether the intended activity happened, such as an alert override rate or the percentage of alerts acted on. Process measures respond quickly and are directly actionable, but a dashboard of pure process measures shows activity without impact.

**Project charter.** The one-page document that establishes what a project is, who authorized it, and how its decisions route: purpose, scope, sponsor, stakeholders, governance path, success criteria. It is signed before detailed planning starts because every later artifact (timeline, budget, KPI dashboard) inherits its scope and governance path from this page.

**Project sponsor.** The executive accountable for a project's existence: secures the budget, holds the decision rights the project lead lacks, and arbitrates when the project's priorities collide with someone else's. The sponsor does not run the project day to day; the implementation lead does. For the RA-CDS the sponsor is the CMIO.

**Quadruple Aim.** The Triple Aim plus a fourth goal: the work life and well-being of the people delivering care, added because workforce burnout was consuming the gains of the first three. For a CDS deployment, the fourth aim is measured in override burden, alert volume per clinician, and clinician satisfaction, and it predicts the deployment's survival.

**RACI matrix.** An ownership table that assigns each role one of four letters per activity: Responsible (does the work, at least one per activity), Accountable (owns the outcome, exactly one per activity), Consulted (gives input before the work, two-way), Informed (told after, one-way). The one-A rule is the load-bearing constraint: two A's defer a negotiation to the worst possible moment, and zero A's orphans the activity. Companion rules: every A needs at least one R, and executives should not appear as R for build work.

**Regression-test suite.** The set of tests an implementation team runs against its own build every time the vendor ships an upgrade, because each upgrade can change the substrate the build sits on. The suite grows by accretion: every defect an upgrade causes becomes a test the next upgrade must pass.

**Repair work.** Elish and Watkins's term, from the Repairing Innovation ethnography of Duke's Sepsis Watch, for the ongoing and mostly invisible labor of integrating an innovation into a social system: trust-building, workflow negotiation, and the scripts people invent to make a new tool usable across professional boundaries. A deployment plan is a hypothesis about workflow, and the people inside the workflow finish the design. If the plan does not name who does this labor, it is extracted invisibly from whoever is nearest.

**Resistance is information.** The operating principle that an override or dismissal is a measurement to investigate, never only a noise level to retune away. A dismiss rate aggregates at least four distinct signals (false positives, redundant timing, workflow mismatch, distrust of the model), and each has a different fix. The rule is investigate before retuning: structured override-reason capture and a handful of interviews classify the signal at almost no cost.

**Return on investment (ROI).** The ratio of net benefit to cost over an explicit horizon: (benefit minus cost) divided by cost. The horizon matters as much as the ratio, since a project that loses money over one year can return 40% over five. For clinical IT the standard horizon is 3 to 5 years.

**Risk register.** A living table of the things that could derail a project, each scored for likelihood and impact and assigned a single owner with a named mitigation. Scoring likelihood times impact ranks the risks so mitigation attention goes to the top rows first. The register is reviewed and re-scored as the project runs, not written once at kickoff.

**Risk score (likelihood times impact).** A simple ranking number for a risk: rate likelihood and impact on a low-medium-high scale (1, 2, 3) and multiply. A high-likelihood, high-impact risk scores 9 and tops the register; a low-likelihood, high-impact risk scores 3 and still stays on the page because impact alone justifies a mitigation. The score orders attention; it does not replace judgment about any single risk.

**Run chart.** A time-series chart with a center line at the median of the plotted points. Three probability-based rules identify special cause: a shift (six or more consecutive points on one side of the median), a trend (five or more consecutive points all ascending or descending), and an astronomical point (a point obviously distinct from the rest).

**Run, grow, transform.** The standard categories for classifying IT investments. Run keeps current operations safe and working (security hardening, system replacements); deferred run work becomes outages. Grow extends current capability to more value (most clinical-informatics requests, including a new CDS deployment). Transform changes what the institution can do at all (warehouse migrations, ambient documentation): high value, high effort, long horizon, and the first category cut when budgets tighten, which is why it needs portfolio protection.

**Scope/time/cost triangle.** The constraint model in which every project reduces to what ships (scope), when it ships (time), and the resources spent shipping it (cost); when one corner is fixed and pressure arrives, another corner gives, and quality gives silently when none is allowed to give openly. In healthcare IT, time is usually fixed because go-live dates anchor to training calendars and EHR freeze windows. That leaves scope as the working margin: the disciplined response to mid-project pressure is deferral to the post-launch queue with a named owner and a committed review date.

**Scrum.** Agile formalized into fixed-length sprints with a prioritized backlog, a sprint goal, and a review and retrospective each cycle. It fits teams doing iterative work that benefits from cadence, such as model validation and tuning cycles. It fails when work arrives continuously as unpredictable single items rather than plannable batches.

**SDLC (software development lifecycle).** The six phases every system passes through: requirements, design, implementation, verification, deployment, maintenance. A project Gantt is the SDLC with dates attached, and maintenance is the longest phase by far. Verification matters most: the cost of discovering a defect rises steeply with every phase it survives.

**Servant leadership.** A leadership style in which the leader removes obstacles and absorbs friction so the team can do its work: securing blocked resources, shielding the team from scope requests, taking escalations personally. It fits a competent team in the middle of a demanding build phase.

**Service-level agreement (SLA).** A commitment, stated in advance, to response and resolution targets per severity level, so "how fast" is not negotiated per ticket. The SLA is also the measurement instrument for the support organization itself: missed-SLA rates form a time series the operations dashboard tracks.

**Severity level.** A predefined classification of how bad an operational issue is, so triage is a rule rather than an argument. Sev1 is system down or active patient-safety exposure; Sev2 is a major function degraded with a workaround; Sev3 is a single-user or low-impact defect; Sev4 is cosmetic or an enhancement request. Each level carries a committed response.

**Situational leadership.** The claim that the right leadership style follows the team's competence and commitment for the specific task and the urgency of the moment, not the leader's personality. It is the rule for selecting among the other styles rather than a fixed style itself. One deployment, run well, uses several styles, sometimes in the same week.

**Six Sigma.** The defect-reduction discipline developed at Motorola: define a defect precisely, measure the process's defect rate, and reduce variation until defects are rare. It suits stable, high-volume processes with countable defects, such as lab turnaround time or barcode-scan compliance.

**Sociotechnical system.** The combined social and technical system in which clinical software operates: the clinicians, workflows, status hierarchies, and department culture together with the artifact itself. The unit that succeeds or fails is the combined system, never the software alone, which is why technical-only deployments fail. Treated at concept level in Course 16 Track 3; Course 17 Track 6 covers it at depth, including the Sittig and Singh eight-dimension model.

**Solid-line vs dotted-line reporting.** A solid line is formal authority: who writes the evaluation, sets the budget, and can reassign the role. A dotted line is structured obligation without authority: a standing duty to coordinate, inform, and align with a second chain. The CMIO's standard placement is solid line to the CMO and dotted line to the CIO.

**Special-cause variation.** Variation unlikely to come from a stable process, identified by run-chart and control-chart rules. It means something happened, and it can be desirable: a card-text revision that shifts the override rate down is special cause in the intended direction.

**Standard, normal, and emergency changes.** The three change classifications in change control. A standard change is pre-approved, low-risk, and routine, with a documented repeatable procedure (adding a user to an existing security class). A normal change carries material risk or novelty and goes to the board with a risk assessment, test evidence, and a rollback plan (revising a CDS card's text). An emergency change is required now to resolve an outage or an active patient-safety exposure: a designated approver authorizes it before it goes in, and the board reviews the full documentation afterward.

**Sunset (system retirement).** The planned end of a system: replaced, consolidated, or retired when the clinical need changes. Retirement is an operations task with a checklist (interfaces disconnected in dependency order, access ended, licenses closed, monitoring removed), and the data outlives the application: record-retention obligations run years past decommissioning, so the plan must choose among migrating the data, extracting it to an archive, or keeping the old application alive read-only, the last being the most common and the most quietly expensive option.

**Support tiers (L1, L2, L3).** The three-level structure that routes operational work by the nature of the fix required. L1 is the help desk, working from scripts and a knowledge base: access requests, how-do-I questions, first-contact triage. L2 is the application analysts: configuration, build investigation, reproducing defects. L3 is the builders, integration engineers, and vendor escalation: code and model defects, where any fix to the build then enters change control.

**SWOT analysis.** A four-cell assessment of an institution's internal strengths and weaknesses and its external opportunities and threats. The internal pair describes what the institution can do today; the external pair describes what the environment will reward or punish. Strategy work starts here because a roadmap built for an institution that does not exist fails on contact with the build queue.

**Tampering.** Deming's term for reacting to common-cause variation as if it were signal. It makes a stable process worse: the manager who demands an explanation for every downtick teaches the team to manufacture explanations and adjust a process that did not change. A dashboard number presented without its time series and limits invites it.

**Total cost of ownership (TCO).** The full cost of a system over a stated period: acquisition or build, integration, training, maintenance, infrastructure, and eventually decommissioning. The build is the visible cost and usually the minority; for the RA-CDS the $240K build is 44% of the $540K five-year total. Underbudgeting the ongoing line is the most common informatics budgeting error.

**Transactional leadership.** A leadership style built on explicit expectations, defined deliverables, monitoring, and correction or reward based on performance. In informatics work it appears as build checklists, deadline tracking, and stand-ups. It fits moments when the task list is explicit and slippage is expensive, such as cutover week or a validation window.

**Transformational leadership.** A leadership style that motivates through a shared vision of a changed future and connects individual effort to purpose. In informatics work it appears as framing an intervention in clinical-mission terms, such as a CDS alert presented as treat-to-target made operational. It fits situations that run on persuasion rather than authority, such as winning over a skeptical clinical department.

**Triple Aim.** IHI's statement of the three simultaneous goals of health-system improvement: better population health, better experience of care, and lower per-capita cost.

**Value-stream mapping.** A Lean diagramming method: chart every step between a triggering event and the delivered value, record the elapsed time of each, and classify each step as value-adding or waiting. In clinical processes most elapsed time is waiting between steps, which is where interventions like a CDS alert aim.

**Waterfall.** A project methodology of sequential phases with sign-off gates: requirements, design, build, test, deploy. It fits work with fixed requirements and high change cost, such as EHR module rollouts and interface builds anchored to freeze windows and training calendars. It fails when requirements are still being discovered, because the first real user feedback arrives after the budget is spent.

**What / so what / now what.** A three-move structure for executive messages: what is true (the finding or status), why it matters to this audience (the so what, in dollars, patients, or risk), and what decision or action is requested (the now what). It is BLUF operationalized into a repeatable template for briefings and one-pagers.
