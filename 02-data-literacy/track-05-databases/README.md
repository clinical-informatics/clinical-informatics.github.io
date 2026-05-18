# Track 05: What a database actually is

A spreadsheet is a piece of paper that does arithmetic. A database is a system that refuses to store data it can prove is wrong.

That difference is the whole track. By the end you should be able to look at a clinical data system and see, behind the rows-and-columns view, the schema that defines what is and is not a legal value, the constraints that catch bugs before they ship, and the relations that make the joins of Track 04 possible at all.

Five pieces:

1. **The spreadsheet you inherited.** Take a flat clinical extract with all the type, tidy-data, missingness, and join problems Tracks 01 through 04 have covered. The spreadsheet allows all of them. The database would have caught most of them at insert time.
2. **What a schema is.** A schema is the published contract of a table: column names, types, allowed values, relationships to other tables. The `CREATE TABLE` statement is the contract in writing.
3. **The six constraint types.** Types, `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`. Each catches a different class of error before the data lands in the database.
4. **What you get for the trouble.** Data integrity, referential consistency, performance via indexes, query optimization, durable storage, concurrent access. The reasons databases beat spreadsheets when the data matters.
5. **Forward to FHIR and OMOP.** Clinical informatics adds two layers on top of the relational model. FHIR is a clinical *interoperability* schema. OMOP is a clinical *analysis* schema. Both rest on the relational ideas in this track. Course 06 walks FHIR. Course 07 walks OMOP. This track is the rung that gets you to both.

The interactive piece: a "bad insert" demo. A small schema with three tables (patients, encounters, observations). The user submits each of seven malformed rows. The schema rejects some, the constraints catch others, a few sneak through. The diagnostic is which constraint did each job, and which class of error remains the application's responsibility because no constraint catches it.


**Prerequisites:** Tracks 01 through 04 of this course. The schema-and-constraints conversation makes sense once you have felt typed columns (Track 01), tidy shapes (Track 02), structured missingness (Track 03), and joins (Track 04) the hard way. This track explains why the database designer chose those constraints, and why your wrangling was undoing their work.

**Companion reading:** `05.1-databases.md` in this folder.

**What's next:** the course capstone, which takes everything in this course (typed, tidy, missingness-handled, joined, schema-aware) and applies it to three messy synthetic clinical tables. After this course, FHIR (course 06) and OMOP / SQL (course 07) become the clinical instantiations of the relational thinking this course has built.
