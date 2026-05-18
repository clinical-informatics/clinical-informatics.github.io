# Track 04: Joins, the central skill

Most clinical analyses require joining tables: demographics to labs, labs to medications, medications to outcomes. Data lives in separate tables because databases are organized that way, and analyses need it together because clinical questions span more than one table.

The mechanics are short (often four lines of code), but the failure mode is hidden: every join drops the patients who do not match on the key, without warning. Silent patient loss is a leading cause of cohort-size surprises.

Five pieces:

1. **What a join is.** Two tables with a key in common. The join combines the rows. Four basic flavors (inner, left, right, full outer) plus one (anti) that is the most useful data-quality move most analysts have never run.
2. **Join keys.** What makes a key a key. Patient identifiers, MRNs, and the cross-system mapping problem.
3. **The four basic joins, on a real-looking RA dataset.** Each one with concrete tables. Watch which patients appear in the result and which disappear.
4. **The silent patient loss problem.** Inner join and an anti-join, side by side, on the same data. The anti-join is what to run before publishing any cohort number.
5. **Many-to-many joins.** When the join key is not unique on either side, the result table explodes. The most common cause of "why does my cohort have 4,000 patients in a 200-patient table?"

The interactive piece: a reactive UI showing two clinical tables side by side. Toggle the join type and watch the result table update. The patients lost at each step are listed in plain English.


**Prerequisites:** Tracks 01 through 03 of this course. Joins assume tidy, correctly-typed inputs with handled missingness. A join on a column that is still a mix of text and date will fail in ways no error message helpfully describes.

**Companion reading:** `04.1-joins.md` in this folder.

**What's next:** Track 05 on what a database actually is. Once you can join tables, the next question is: what was the table designed for, and which schema decisions are responsible for the joins behaving the way they do?
