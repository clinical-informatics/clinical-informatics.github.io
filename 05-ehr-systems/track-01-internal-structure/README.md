# Track 01: How EHRs structure data internally

The medication list on Ms. Reyes's chart looks like one neat list. Pulling it out of the database is six joins across five tables. Same is true for "show me her last CRP" and "show me her active problems." The EHR you use is a fast renderer in front of a relational database, and once you can see the tables behind the rendering, a lot of clinical-informatics work stops feeling mysterious.

This track has two halves.

The first half is the **logical view**. We walk Ms. Reyes's record from the screen back into the tables. We write the SQL that the EHR is writing for you every time you click. We look at the *flowsheet* pattern, which is the place every EHR breaks the relational rules on purpose. We look at indexes, which are why "Reyes, Elena" returns instantly and "everyone in our system on adalimumab" can take minutes.

The second half is the **physical view**. Where those tables actually sit. Block versus object storage. SSD versus spinning disk. On-prem versus cloud. Cold tiers for old encounters. Backups and disaster recovery. The physical layer determines what is cheap, what is expensive, and what is possible at all. Vendors hand out architecture diagrams that paper over a lot of this; the track gives you the vocabulary to read those diagrams with comprehension.

**Estimated time:** 75 minutes.

**Prerequisites:** None within this course. Familiarity with relational concepts (tables, primary keys, joins) at the level of course 02 Track 5 helps but is not required. Track 1 will reintroduce what it needs.

**How to start:** open `notebook.py` in Marimo. The notebook loads cleanly against the synthetic Ms. Reyes Epic-style export shipped with the curriculum and uses an in-memory SQLite database for the SQL examples.

**Companion reading:** `01.1-internal-structure.md` in this folder is the reference essay. The notebook focuses on what you can do interactively; the essay walks the moves and the vocabulary at your own pace.

**What's next:** Track 02 (HL7 v2, CDA, and what we inherited) picks up where this one ends. Track 03 (clinical data warehouses) is where the population-query problem this track surfaces gets a real answer.