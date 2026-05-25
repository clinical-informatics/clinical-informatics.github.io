# Go deeper: SQL, the extraction layer

**If you want a fast, hands-on SQL refresher:**

- [SQLBolt](https://sqlbolt.com/) is an interactive in-browser tutorial covering SELECT, WHERE, JOIN, GROUP BY, and the rest of the core SQL language. Each lesson is a few minutes; the in-browser query interface gives immediate feedback.
- [Mode SQL Tutorial](https://mode.com/sql-tutorial) covers the same ground at greater depth and includes an intermediate section on window functions that directly maps onto the patterns demonstrated in this track.

**If you want to see SQL applied to OMOP specifically:**

- The [Book of OHDSI chapter on SQL and R](https://ohdsi.github.io/TheBookOfOhdsi/SqlAndR.html) covers several OMOP-specific patterns: cohort definition, characterization, and population-level effect estimation. The OHDSI `SqlRender` package shown there generates engine-portable SQL from a single OMOP query, which is the way most production OMOP analytics are written.
- [ATLAS](https://atlas-demo.ohdsi.org/) is OHDSI's web-based cohort design tool. It generates the SQL for a cohort definition from a point-and-click interface. The generated SQL is useful both as a reference and as the canonical OMOP-idiomatic style for cohort queries.

**If you want to go significantly further:**

- [Use the Index, Luke](https://use-the-index-luke.com/) is the canonical free reference for SQL performance. It explains how indexes work, why a query plan looks the way it does, and how to read and influence an execution plan. Most analytic queries against a warehouse run on tables large enough that index awareness is required to make the query return within a useful time.
- The [SQLite documentation on window functions](https://www.sqlite.org/windowfunctions.html) is the most precise specification of window-function semantics in any engine. The same semantics apply (with minor syntactic variation) in PostgreSQL, SQL Server, BigQuery, Snowflake, and the other engines used by clinical warehouses.
