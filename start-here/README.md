# Clinical Informatics Open Curriculum

A free, open curriculum in clinical informatics. Twenty-one interactive courses for clinicians, trainees, and clinical researchers.

Designed, written, and edited by **Mario David Felix, MD MHS**.

---

## Why this exists

I am a practicing rheumatologist with a Master's in Data Science and Clinical Informatics. I am currently a postdoctoral informatics research fellow at the West Haven VA.

I built this curriculum as a way to study and consolidate the concepts I was working through. The output is this site. It is not meant to teach informatics formally, and it will not prepare you for a board certification exam. The goal is to demystify the field and lay a foundation for anyone who wants to learn more.

I try my best to demystify each concept and then make it interactive. Every track pairs a short written introduction with a [Marimo](https://marimo.io) notebook. Marimo is a Python notebook environment that runs entirely in your browser, with no install required, and is reactive: when you move a slider, change a dropdown, or edit a value, every downstream cell recomputes immediately. Every course closes with a capstone project that consolidates the tracks of that course into a single applied exercise.

The site is open and completely free. It will continue to grow as my knowledge and experience accumulate.

I think about clinical informatics from the perspective of a rheumatologist. That is why the same patient with rheumatoid arthritis, **Ms. Elena Reyes**, appears in every course. She is 52, seropositive, on methotrexate and adalimumab, with moderately active disease. You will meet her data as an EHR export, a FHIR bundle, a claims file, clinical notes, OMOP tables, a decision curve, a population-registry row, PROMIS-29 responses, a hand-radiograph series, and an HLA-DRB1 report. Each format lands on a different course; the patient stays the same.

If you have feedback, suggestions, or comments, write to me at [fmario619@gmail.com](mailto:fmario619@gmail.com).

---

## The full course map

| # | Course | What it teaches |
|---|---|---|
| ... | [start-here](https://github.com/clinical-informatics/start-here) | Orientation, Ms. Reyes's data, the shared components |
| 00 | [foundations](https://github.com/clinical-informatics/00-foundations) | What the field is, DIKW, CS and network fundamentals, the US health system, informatics roles |
| 01 | [computational-thinking](https://github.com/clinical-informatics/01-computational-thinking) | The shift from clinical reasoning to computational thinking |
| 02 | [data-literacy](https://github.com/clinical-informatics/02-data-literacy) | Rows, columns, joins, missingness. Thinking in tables. |
| 03 | [privacy-ethics-governance](https://github.com/clinical-informatics/03-privacy-ethics-governance) | What protects patients and what the rules actually require |
| 04 | [clinical-epidemiology](https://github.com/clinical-informatics/04-clinical-epidemiology) | Frequency and association measures, bias, diagnostic test performance, study designs |
| 05 | [ehr-systems](https://github.com/clinical-informatics/05-ehr-systems) | How the EHR stores and moves data, including imaging (PACS, DICOM) |
| 06 | [learn-fhir](https://github.com/clinical-informatics/06-learn-fhir) | FHIR from zero, the web architecture healthcare borrowed |
| 07 | [data-wrangling-engineering](https://github.com/clinical-informatics/07-data-wrangling-engineering) | SQL, pandas, OMOP, graph databases |
| 08 | [clinical-visualization](https://github.com/clinical-informatics/08-clinical-visualization) | Charts that communicate, charts that mislead |
| 09 | [ai-in-medicine](https://github.com/clinical-informatics/09-ai-in-medicine) | Machine learning for clinicians who evaluate, not build |
| 10 | [nlp-clinical-text](https://github.com/clinical-informatics/10-nlp-clinical-text) | The data that lives in notes, not in fields |
| 11 | [health-economics-data](https://github.com/clinical-informatics/11-health-economics-data) | Claims, costs, decision analysis, decision curves |
| 12 | [clinical-decision-support](https://github.com/clinical-informatics/12-clinical-decision-support) | The CDS capstone. CQL, CDS Hooks, evaluating CDS in practice |
| 13 | [research-reproducibility](https://github.com/clinical-informatics/13-research-reproducibility) | Version control, provenance, sharing without leaking |
| 14 | [interoperability-policy](https://github.com/clinical-informatics/14-interoperability-policy) | The Cures Act and what it changed |
| 15 | [data-storytelling](https://github.com/clinical-informatics/15-data-storytelling) | Communicating findings beyond your own work |
| 16 | [leadership-practice](https://github.com/clinical-informatics/16-leadership-practice) | Project and change management, KPIs, finance, executive communication |
| 17 | [workflow-safety-human-factors](https://github.com/clinical-informatics/17-workflow-safety-human-factors) | Workflow mapping, human factors, alarm fatigue, RCA, FMEA |
| 18 | [population-public-health](https://github.com/clinical-informatics/18-population-public-health) | Registries, risk stratification, value-based care, SDOH, surveillance |
| 19 | [patient-data-digital-health](https://github.com/clinical-informatics/19-patient-data-digital-health) | Patient portals, PGHD, wearables, RPM, telemedicine, digital therapeutics, PROMs |
| 20 | [bioinformatics](https://github.com/clinical-informatics/20-bioinformatics) | Concept-level bioinformatics: clinical genomics and the research infrastructure |

For role-based reading orders, see the [learning paths](learning-paths.md) page.

---

## License

Course content is licensed under Creative Commons BY 4.0. Code is licensed under MIT.
