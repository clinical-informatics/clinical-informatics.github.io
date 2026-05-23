# Track 03: Clinical data warehouses

Track 01 showed why the operational EHR is fast for one patient and slow for a population. This track is about the system the field built to make the population queries fast: the clinical data warehouse (CDW).

We walk the analytical-versus-transactional split from course 00 forward to its consequences. We walk the ETL and ELT pipelines that move data from the EHR into the warehouse. We compare three storage architectures (data warehouse, data lake, lakehouse) and the trade-offs each makes. We see what Ms. Reyes's CRP looks like as a row in the operational EHR and as a row in a star-schema CDW. We see why the warehouse is what research and quality reporting and population health all live on top of.

**Estimated time:** 75 minutes.

**Prerequisites:** Track 01 of this course. Track 02 helps but is not required.

**How to start:** open `notebook.py` in Marimo. The notebook builds an in-memory star schema and runs side-by-side queries against an operational-shaped copy and the warehouse-shaped copy.

**Companion reading:** `03.1-warehouses.md` in this folder.

**What's next:** Track 04 (imaging informatics).
