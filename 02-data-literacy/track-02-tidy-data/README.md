# Track 02: Tidy data

One fact per cell. Track 01 fixed the **type** of each column. This track fixes the **shape** of each row.

Most clinical data does not arrive in a shape you can analyze. A medication list comes back as one row per patient with twelve columns named `med1` through `med12`, mostly empty, occasionally with a dose suffix glued onto the name. A flowsheet exports as one row per timestamp with eighty columns, one per vital sign, mostly null. A claims pull exports with one row per claim line where the diagnosis and the procedure share a cell. None of these are wrong in content. They are wrong in shape, and the wrong shape costs more downstream time than every other data problem combined.

Three ideas, then a reshape:

1. **The one rule of tidy data:** each row is one observation, each column is one variable, each cell holds one value. The rule sounds obvious until you start looking at clinical extracts and realize most of them violate it.
2. **The four shapes of untidy data you meet in practice.** Each has a name, a definition, and a tidy-rule it violates:
   - **Values-as-columns.** The column headers are values of an underlying variable, not separate variables. Flowsheet exports with `hr`, `bp_sys`, `bp_dia` as columns are six values of one variable (vital sign identity).
   - **Long-when-you-need-wide.** Each row is one (entity, attribute, value) triple, but the analysis treats the *entity* (a visit, a patient) as the observation. Same data, two valid shapes, only one of them fits the question you are asking.
   - **Multi-fact cell.** A single cell holds two or more semantically distinct facts glued into a string. `25 mg SC weekly` is four facts.
   - **Repeating groups.** A one-to-many relationship flattened into numbered columns (`med1`, `med2`, `med3`, ...). The numbered suffix is the giveaway: those columns are the same variable repeated.
3. **What `melt` and `pivot` actually do.** The two reshape moves cover almost all of the work. After this track they should feel like one operation in two directions, not commands to Google.

Then a reshape: a messy medication table for Ms. Reyes, in two of the four untidy shapes at once, gets cleaned into one fact per cell using a small reactive UI.


**Prerequisites:** Track 01 of this course (data types). The reshape moves assume each column already has a sane type. If a date column is still text on arrival, fix that first.

**Companion reading:** `02.1-tidy-data.md` in this folder.

**What's next:** Track 03 on null values and missingness. Once the data is typed and tidy, the next question is: what is missing, and what kind of missingness is it?
