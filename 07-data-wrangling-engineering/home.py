"""Course 07: Data wrangling and engineering.

Marimo course menu. The course presents the analytic stack from the
warehouse outward: code standards, the OMOP schema layered on top, SQL
as the extraction language, pandas as the post-extraction analytic
layer, and graph databases as the model that fits the small set of
clinical questions that are not naturally tabular.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 07: Data wrangling and engineering

        ## From the clinical data warehouse to a clinical answer

        Course 05 introduced the clinical data warehouse as a concept. This course presents the analytic stack that sits on top of it: the code standards that name individual clinical facts, the OMOP schema that organizes those facts into a queryable warehouse, the SQL that extracts cohorts and summaries from the warehouse, the pandas layer that performs the analysis that follows extraction, and the graph data model that fits the small set of clinical questions that are not naturally tabular.

        Every track uses Ms. Reyes plus a small synthetic RA cohort as its worked example. The capstone takes three messy raw input files, maps them to OMOP shape, and runs three clinical queries against the mapped output, one per analytic layer.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **Standards in the EHR** | LOINC, SNOMED CT, ICD-10-CM, CPT, RxNorm, NDC. Which standard names which slice of the record, where in the EHR each is stored, and the failure modes of queries that filter on the wrong vocabulary. |
        | 02 | **OMOP Common Data Model** | The fixed schema layered on top of the code standards. Six core tables presented on Reyes's record. The vocabulary layer and the standard-concept-vs-source-concept distinction. |
        | 03 | **SQL, the extraction layer** | Each clinical question stated first, then the SQL that answers it. Cohort filter, GROUP BY aggregation, window functions, date arithmetic, common table expressions. Demonstrated on a SQLite database in OMOP shape. |
        | 04 | **pandas, the post-extraction analytic layer** | Tidying, per-patient summaries, time-since-event computation, reactive filtering. Tool comparison with DuckDB, polars, and dplyr; the pandas choice explained in terms of cohort size and team language. |
        | 05 | **Graph databases, conceptual** | When a problem is graph-shaped. Nodes, edges, properties, traversal. Cypher pseudocode on Reyes's medication graph and on SNOMED is-a hierarchy traversal. Tools at concept level. |

        ### Capstone

        **From raw EHR files to a clinical answer.** Three messy raw tables (lab export, medications log, encounter file) are mapped to OMOP shape, then queried for three clinical questions, one per analytic layer.

        ---

        Each track folder has a `README.md`, a `notebook.py` (the interactive notebook), and a `go-deeper.md` (a curated reading list).
        """
    )
    return


if __name__ == "__main__":
    app.run()
