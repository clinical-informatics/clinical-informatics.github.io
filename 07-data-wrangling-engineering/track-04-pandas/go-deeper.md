# Go deeper: pandas, the post-extraction analytic layer

**If you want to understand pandas better before moving on:**

- The [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) is the canonical reference. The chapters on group by, merge/join/concatenate, and time series cover the operations demonstrated in this track at the level of detail required for production use.
- The [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) page is the shortest end-to-end introduction. The accompanying [comparison-to-SQL](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html) page maps SQL clauses to their pandas equivalents column by column.

**If you want to compare the alternatives this track named:**

- [DuckDB's "Friendlier SQL"](https://duckdb.org/docs/sql/dialect/friendly_sql.html) and the [Python integration](https://duckdb.org/docs/api/python/overview.html) pages show how to run SQL against CSV and Parquet files without loading them into memory. The DuckDB SQL dialect is closer to PostgreSQL than to SQLite, which makes the queries transfer cleanly between DuckDB and a production warehouse.
- The [polars User Guide](https://docs.pola.rs/user-guide/) covers the lazy execution model and the verb-based expression grammar. The [polars-vs-pandas migration guide](https://docs.pola.rs/user-guide/migration/pandas/) is the fastest path for someone who already knows pandas.

**If you want to go significantly further:**

- [Python for Data Analysis (third edition)](https://wesmckinney.com/book/) by Wes McKinney is the definitive book on pandas, written by its original author. The third edition is openly available online. The chapters on data wrangling and on time series are the most useful for clinical work.
- The [Effective Pandas talk and book](https://leanpub.com/effective-pandas) by Matt Harrison covers the patterns that make pandas code readable and fast in practice. The book itself is paid; the underlying [conference talks](https://www.youtube.com/results?search_query=matt+harrison+effective+pandas) are free.
