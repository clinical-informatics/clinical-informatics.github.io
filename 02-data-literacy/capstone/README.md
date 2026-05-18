# Capstone: Course 02 Data Literacy

Clean, join, and summarize three messy synthetic clinical tables.

You inherit three CSVs from a research coordinator: demographics, labs, and medications for an RA cohort. The data arrives in the shape most real clinical exports ship in: mixed date formats, sentinel values, a repeating-groups med list, one orphan lab row, and a different way of writing sex in every other row.

Your task is to produce one coherent patient summary the rheumatology team can act on. The path uses every move this course has taught:

- **Track 01.** Fix the types: dates, the CRP `<2.0` sentinel, the sex value set.
- **Track 02.** Reshape: melt the `med1...med4` columns; split the dose-route cell.
- **Track 03.** Decide what to do with the missing CRPs and the missing demographics.
- **Track 04.** Join demographics + labs + medications, with anti-joins to measure the silent patient loss.
- **Track 05.** Verify the assembled table would have passed a sane schema's constraints.

The interactive app drives the flow with checkboxes and dropdowns. As you toggle each step, a decision log accumulates in plain English, in the order you made the decisions. At the end you pick a patient, see the assembled summary, and copy the decision log out as the methods-section paragraph of your analysis.

**Prerequisite:** all five tracks of course 02.


**How to start:** `marimo run capstone/notebook.py`, or click the run button from the course home page.

## What the capstone is checking

- Can you spot the data problems without being told what they are?
- Can you decide what to do about each one on purpose, not by default?
- Can you defend each decision in writing, in the order you made it?
- Can you measure the silent patient loss before publishing a cohort number?

If yes to all four, you are done with this course. The next stops are course 06 (FHIR) and course 07 (SQL, OMOP, data wrangling at scale).
