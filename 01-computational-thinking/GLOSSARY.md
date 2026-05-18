# Glossary: 01 computational thinking

Plain-English definitions of the terms this course introduces, or that it treats in a particular way. The curriculum-wide glossary lives in the [start-here repo](https://github.com/clinical-informatics/start-here/blob/main/GLOSSARY.md). If a term shows up in your reading and isn't here, check there.

If you can't find it in either place, open an issue. The glossary is a living artifact.

---

**Abstraction.** Deciding what to ignore. When you abstract, you keep the parts of a problem that matter for the answer and drop everything else. A radiologist abstracting a chest CT keeps the consolidation and ignores the screw artifact in the patient's shoulder. A model predicting readmission abstracts thousands of medical history details into a handful of features. The whole skill of track 03 is choosing what's safe to drop.

**Algorithm.** A finite list of steps that, if followed, will solve a particular kind of problem. A recipe is an algorithm. The CHADS-VASc score is an algorithm. So is the sepsis screening rule running in the EHR. Calling something an algorithm does not make it correct or trustworthy. It means the procedure is specified clearly enough that another person, or a computer, could follow it.

**Alert fatigue.** What happens when an algorithm fires so often, or so often wrongly, that clinicians stop reading the alerts. Once it sets in, the alert is worse than nothing. Real signals are now missed inside the noise. Most of track 01 is about why this is the default outcome for poorly designed clinical decision rules. Revisited in depth in course 12.

**DAS28.** Disease Activity Score in 28 joints. The standard composite measure of rheumatoid arthritis activity. It folds together a tender-joint count, a swollen-joint count, an inflammation marker (CRP or ESR), and a patient-reported global health score into a single number. Track 04 uses DAS28 as a worked example of an algorithm a clinician can read line by line.

**Decision rule (clinical).** An algorithm meant to help a clinician decide something: admit or not, treat or not, image or not. The Wells score is a decision rule. The Centor criteria are a decision rule. So is "any patient over 65 with new chest pain gets an ECG." The capstone has you write one from scratch.

**Decomposition.** Breaking a problem into smaller, named parts you can think about one at a time. The first move of computational thinking. When you decompose "the sepsis alert is broken," you might end up with "the cohort is too broad," "the threshold is too low," "the data source is unreliable," and "the alert fires after the clinician was already aware." Each of those is now a tractable problem.

**Edge case.** A specific situation where a rule that mostly works produces a wrong or harmful result. Edge cases are the patients your decision rule didn't have in mind. The skill of track 02 is generating edge cases on purpose, before the algorithm encounters them in production.

**Feature (in a model).** One of the inputs a model uses to make a prediction. Age is a feature. Whether a patient has had a previous admission for heart failure in the last 90 days is a feature. Choosing features is mostly an abstraction problem: deciding what to give the model and what to leave out. Used in track 03.

**Generalization.** When a rule developed on one population still works on a different population. The opposite of overfitting. A sepsis rule developed in an academic ICU may not generalize to a community hospital floor. Different patient mix, different baseline rates, different documentation habits. Generalization is one of the four questions track 05 teaches you to ask.

**Pattern (in computational thinking).** A regularity in the problem that lets the same rule cover many cases. "Patients with HR over 100 and temperature over 38.5 are flagged" is a pattern. Patterns are how algorithms get their leverage: one rule, many patients. The risk is that the pattern doesn't actually generalize, which is the edge-case problem.

**Procedure.** A way of doing a thing, written down explicitly enough that another person could follow it without your having to clarify. The DAS28 calculation is a procedure. The order of steps to titrate methotrexate is a procedure. An algorithm is a procedure that runs on a computer.

**Rule (clinical decision).** Synonym for decision rule, used loosely. The thing your EHR is enforcing in the background.

**Sepsis alert.** A clinical decision support tool that monitors patient data in the EHR for signs of sepsis and alerts the team when those signs appear. Track 01 takes apart a fictional sepsis alert that fires 40 times a day. The same alert is the running example in course 12.

**Threshold.** The cut-point in a rule above which something happens. "Flag the patient if their heart rate is above 100." 100 is the threshold. Sliding a threshold up or down changes how many patients get flagged and what fraction of those flags are correct. Track 02 and track 04 both rely on threshold sliders to build intuition. Returns in earnest in course 04 (the 2x2 table) and course 11 (decision curve analysis).

**Trustworthiness (of an algorithm).** Whether you should act on what it tells you. Track 05 frames trustworthiness through four questions: *what was it trained on, what does it optimize for, where does it fail, and who does it fail for?* "Does it have FDA clearance" is not on that list. Clearance is a necessary condition for some uses, not a sufficient condition for any of them.
