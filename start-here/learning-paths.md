# Learning paths

The full curriculum is twenty-one courses, but most learners do not need all of them in order. The path that fits you depends on your role and your goals. Pick a path. You can switch later.

---

## Clinician: understanding the systems you work in

You do not need to write code. You need to follow the conversation in a room with vendors, IT staff, and informaticists. You want to evaluate a CDS alert critically. You want to read a clinical AI paper without trusting it on faith. You want to understand what the EHR is doing when you click on something.

Courses: **00, 01, 03, 04, 06, 12**. Add **17** if patient safety is part of your work.

- **00: Foundations.** Field-level orientation. DIKW, file types and databases at concept level, network architecture, the US health system, the roles within informatics. Every later course assumes it.
- **01: Computational thinking.** Adds pattern-, rule-, and edge-case reasoning to the clinical reasoning you already do. The first course most clinicians benefit from.
- **03: Privacy, ethics, and governance.** Every conversation about clinical data starts here.
- **04: Clinical epidemiology.** Vocabulary you read every day, with intuition built before formulas. The 2x2 table chapter is the most reused content in the curriculum.
- **06: Learn FHIR.** The technical core. Read a FHIR resource and know what it means. Understand why interoperability has been hard and why it is improving.
- **12: Clinical decision support.** Design a complete CDS intervention, end to end, using every previous course.
- **17: Workflow, safety, human factors.** Why most alerts get ignored, and what good CDS design looks like.


---

## Trainee: building a working mental model

You are early in your career. The field is in motion and you do not yet know whether informatics is a side interest or a primary one. You want a broad map and the option to go deeper later.

Courses: **00, 01, 02, 03, 04, 06, 07, 09**.

This covers orientation (00), the conceptual core (01, 04), the technical core (02, 06, 07), the ethical core (03), and the AI core (09). After these eight courses you can read most papers in clinical informatics, ask useful questions in a vendor demo, and know what to read next.

If informatics becomes your primary interest, the natural next steps are 11 (health economics), 12 (CDS), then 16 (leadership and practice).


---

## Clinical researcher: working confidently with the datasets you receive

You need a specific set of skills, quickly. EHR architecture and policy can come later or never. The core needs are data literacy, statistical thinking, dataset wrangling, an honest read on AI, and reproducible practice.

Courses: **00, 01, 02, 03, 04, 07, 09, 11, 13**. Add **18** for population-level work, or **19** for patient-reported and wearable data.

- **00.** Field-level orientation, DIKW, file types, OLTP vs OLAP, the research infrastructure landscape.
- **01, 02.** Conceptual frame.
- **03.** Required reading for anyone touching patient data.
- **04.** The most reused course on this path.
- **07.** SQL, pandas, OMOP. The tools you will actually use.
- **09.** ML evaluation.
- **11.** Decisions, costs, and value.
- **13.** Project organization, version control, provenance, sharing without leaking.
- **18.** Population, registry, and value-based-care work.
- **19.** PROMs, wearables, telemedicine data.


---

## Health IT staff: engineers, analysts, project managers, vendor teams

You build, deploy, or support clinical software, often without a clinical background of your own. The full curriculum fits this role because the field's clinical context and vocabulary are part of the deliverable.

Courses: 00 through 20, in order.

Three notes specific to this path:

1. Spend extra time on **03 and 04**. Privacy/governance and clinical epidemiology often feel furthest from a non-clinical IT role, but they are the courses that change how you read every other course in the sequence.
2. **05 (EHR systems) sits between 04 and 06 for a reason.** You need clinical epidemiology to understand why data quality matters, then EHR internals before FHIR feels like the solution it is.
3. **14 (interoperability policy) lands better after 06 and 07.** The Cures Act changed what FHIR and OMOP could be used for, and the policy is more meaningful once you know the technology.


---

## Clinical informaticist: working in the field

You hold an informatics role already (CMIO, CNIO, CRIO, clinical informaticist, informatics analyst, informatics fellow). You have clinical training and you have done front-line informatics work. What this curriculum offers is the connective tissue: the conceptual frame for the technical work, the professional-practice content the technical curricula skip, and the modern-practice frontiers.

If you are early in this role, take the full sequence 00 through 20.

If you are senior, the gap-fill subset is **12, 16, 17, 18, 19**, optionally with **00** as a refresher.

- **00 (refresher).** Skim or skip depending on your background.
- **12: Clinical decision support.** The curriculum's CDS capstone. The running scenario in **16** picks up from here, so this is the natural starting point for senior practitioners.
- **16: Leadership and practice.** Project management, change management, KPI dashboards, finance, executive communication. The gap-fill the technical courses do not cover.
- **17: Workflow, safety, human factors.** Deeper treatment of the alarm-fatigue and sociotechnical material from Course 12. The CDS sign-off capstone works as a deployment template.
- **18.** Population health and value-based-care infrastructure.
- **19.** Patient-generated data and digital health workflows.


---

## Just curious

You came here because "informatics" keeps coming up and you want to know what is behind the word.

Courses: **00, 01, 03, 04, 09**.

After these five courses you will know:

- what clinical informatics is, where it sits in the US health system, and who does the work
- the difference between a clinician's reasoning and a computer's reasoning
- why patient data is hard to share, and what protects it
- what sensitivity, specificity, and AUC mean
- what an AI model in medicine is and is not doing

If you want more after that, you will know in what direction.

---

## A note about prerequisites

Each course intro page lists prerequisites, but the prerequisites are about *concepts*, not credentials. The privacy course does not require epidemiology. It stands on its own. The AI course does build on the 2x2 table from epidemiology, and the CDS course does build on FHIR. When a course says "do X first," it is because X comes back as a load-bearing idea, not as a gatekeeping requirement.

If a concept appears too fast, the cross-reference callouts always point to where the idea was introduced.
