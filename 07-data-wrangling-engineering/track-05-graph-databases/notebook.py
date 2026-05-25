"""Track 05: Graph databases, conceptual.

A small set of clinical questions are not naturally tabular. Care-team
networks, medication-transition sequences, and traversal of the SNOMED
is-a hierarchy are shaped as nodes and edges rather than rows and
columns. This track introduces the graph data model at concept level,
specifies the vocabulary (nodes, edges, properties, traversal),
demonstrates one worked example on Reyes's medication graph and one on
SNOMED hierarchy traversal, and identifies when a graph database is and
is not the right tool for a clinical question. No installation is
required; the worked examples are presented as DataFrames plus Cypher
pseudocode.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    import types
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    # Cross-reference helpers inlined from shared/cross_reference.py.
    _COURSE_TITLES = {
        "00": "Foundations of clinical informatics",
        "01": "Computational thinking",
        "02": "Data literacy",
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "05": "EHR systems",
        "06": "Learn FHIR",
        "07": "Data wrangling and engineering",
        "08": "Clinical visualization",
        "09": "AI in medicine",
        "10": "NLP and clinical text",
        "11": "Health economics data",
        "12": "Clinical decision support",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(
                f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"
            ),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(
                f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"
            ),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)
    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Graph databases, conceptual

        ## A different shape of data

        The four tracks before this one assumed a single data shape: the table. Rows are records; columns are attributes; the same shape across the OMOP person table, the measurement table, the drug_exposure table. Most clinical questions fit that shape cleanly. Cohort definitions, per-patient aggregates, group comparisons, and time-to-event analyses all read as SQL or pandas operations over tables.

        A small set of clinical questions do not fit cleanly. The intuitive analogy is the difference between a spreadsheet and a subway map. A spreadsheet is a table: rows are stations, columns describe each station, and the questions you ask of it ("how many stations are downtown," "which stations opened before 1980") are aggregations and filters. A subway map is a network: stations are dots, lines are edges, and the questions you ask of it ("how do I get from Penn Station to Times Square," "which stops are on the path from the Bronx to Brooklyn") are about following edges from one node to another.

        Three recurring clinical questions have the subway-map shape rather than the spreadsheet shape.

        - **Care-team networks.** Given a primary care physician, which specialists do they refer to most often, and what is the path of patient referrals through subspecialty cardiology back to primary care?
        - **Medication-transition sequences.** Given a patient's full medication history, what is the sequence of regimen changes, and at which transition did each change occur?
        - **Ontology traversal.** Given a high-level SNOMED concept (such as "Inflammatory arthropathy"), find every patient whose problem list carries any descendant of that concept, however many levels down in the is-a hierarchy.

        Each of these is expressible in SQL using recursive Common Table Expressions and self-joins, but the SQL becomes long, slow, and difficult to read as the path length grows. The graph data model represents the same data more naturally and supports the corresponding queries directly.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The graph data model

        A graph database stores data as **nodes** connected by **edges**. Each node and each edge carries a **label** that names its type, and a set of key-value **properties** that describe it.

        - A **node** represents an entity. Think of it as a single "thing" the database knows about. In a clinical graph, common node types are a Person, a Drug, a Condition, a Visit, a Provider, a Concept. Each node has a label naming its type (`Person`, `Drug`) and properties giving its attributes (a Person node carries `name` and `date_of_birth`; a Drug node carries `name` and `rxnorm_code`).
        - An **edge** represents a relationship between two nodes. Think of it as an arrow connecting two things. Edges are directed (they go from a start node to an end node) and typed (the edge carries a label naming the relationship). Common edge types in a clinical graph are `:TAKES` (between a Person and a Drug), `:DIAGNOSED_WITH` (between a Person and a Condition), `:REFERRED_TO` (between two Providers), `:IS_A` (between two Concepts).
        - A **property** is a key-value pair attached to either a node or an edge. Node properties describe the entity itself. Edge properties describe the relationship: a `:TAKES` edge between a Person and a Drug carries `start_date` and `end_date` properties to record when the exposure began and ended.

        The same data could also be stored relationally. The relational version would have a `person` table, a `drug` table, and a `drug_exposure` join table linking them, with start and end dates on rows of the join table. The graph model collapses that join: the edge is the join, and the edge carries its own properties directly. A graph database is, in effect, a way of treating the relationships between things as first-class objects rather than as join columns.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: Reyes's medication graph

        Reyes's drug exposures from Track 02 are represented below as a graph. Three node labels are present: `Person`, `Drug`, and `DrugClass`. Two edge labels are present: `:TAKES` (with a start_date property) and `:IS_A` (linking each drug to its therapeutic class).
        """
    )
    return


@app.cell
def _(pd):
    nodes = pd.DataFrame(
        [
            {"node_id": "n1", "label": "Person", "name": "Elena Reyes", "key": "person_id=1001"},
            {"node_id": "n2", "label": "Drug", "name": "methotrexate", "key": "rxnorm=6851"},
            {"node_id": "n3", "label": "Drug", "name": "folic acid", "key": "rxnorm=4511"},
            {"node_id": "n4", "label": "Drug", "name": "adalimumab", "key": "rxnorm=327361"},
            {"node_id": "n5", "label": "Drug", "name": "prednisone", "key": "rxnorm=8640"},
            {"node_id": "n6", "label": "DrugClass", "name": "csDMARD", "key": ""},
            {"node_id": "n7", "label": "DrugClass", "name": "TNFi", "key": ""},
            {"node_id": "n8", "label": "DrugClass", "name": "Glucocorticoid", "key": ""},
            {"node_id": "n9", "label": "DrugClass", "name": "Vitamin supplement", "key": ""},
        ]
    )
    nodes.index = range(1, len(nodes) + 1)
    nodes.index.name = "row"
    nodes
    return (nodes,)


@app.cell
def _(pd):
    edges = pd.DataFrame(
        [
            {"start": "n1 (Reyes)", "edge": ":TAKES", "end": "n2 (methotrexate)", "properties": "start_date=2022-03-07, ongoing"},
            {"start": "n1 (Reyes)", "edge": ":TAKES", "end": "n3 (folic acid)",   "properties": "start_date=2022-03-07, ongoing"},
            {"start": "n1 (Reyes)", "edge": ":TAKES", "end": "n4 (adalimumab)",   "properties": "start_date=2024-01-08, ongoing"},
            {"start": "n1 (Reyes)", "edge": ":TAKES", "end": "n5 (prednisone)",   "properties": "start_date=2025-11-21, end_date=2025-12-06"},
            {"start": "n2 (methotrexate)", "edge": ":IS_A", "end": "n6 (csDMARD)",          "properties": ""},
            {"start": "n3 (folic acid)",   "edge": ":IS_A", "end": "n9 (Vitamin supplement)", "properties": ""},
            {"start": "n4 (adalimumab)",   "edge": ":IS_A", "end": "n7 (TNFi)",              "properties": ""},
            {"start": "n5 (prednisone)",   "edge": ":IS_A", "end": "n8 (Glucocorticoid)",     "properties": ""},
        ]
    )
    edges.index = range(1, len(edges) + 1)
    edges.index.name = "row"
    edges
    return (edges,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Nine nodes, eight edges. Reyes is connected to four `Drug` nodes through `:TAKES` edges, each carrying the date the exposure began and (where applicable) the date it ended. Each `Drug` node is connected to its `DrugClass` node through an `:IS_A` edge.

        The same data in relational form would require a `person` row, four `drug_exposure` rows, four `drug` rows, four `drug_class` rows, and a `drug_to_class` join table. The graph form is denser: the relationships that the relational form represents through join columns are first-class objects in the graph, with their own labels and properties.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cypher: the query language for graphs

        Cypher is the query language most widely used for graph databases. Its central construct is a **pattern-matching syntax** that mirrors the visual shape of a graph. The convention is:

        - **Parentheses** `()` for nodes.
        - **Square brackets** `[]` for edges.
        - **Arrows** `->` for the direction of an edge.

        A node pattern inside the parentheses can name a variable (`p` below), give a label (`Person` below), and constrain properties (`{name: 'Elena Reyes'}` below). An edge pattern inside the square brackets gives the edge type prefixed with a colon (`:TAKES` below).

        The query below asks "what drugs is Elena Reyes on."

        ```
        MATCH (p:Person {name: 'Elena Reyes'})-[:TAKES]->(d:Drug)
        RETURN d.name, d.key
        ```

        The query reads as a sentence: start from a `Person` node whose `name` property is `'Elena Reyes'`, follow a `:TAKES` edge in the direction of the arrow to a `Drug` node, and return the drug's `name` and `key` properties. Cypher tries to match the pattern against the actual graph; every successful match produces one row of output. The result is four rows, one per drug Reyes is on.

        A second example asks the class-level question: which drug classes does Reyes have at least one drug in?

        ```
        MATCH (p:Person {name: 'Elena Reyes'})-[:TAKES]->(d:Drug)-[:IS_A]->(c:DrugClass)
        RETURN DISTINCT c.name
        ```

        The pattern now traverses two edges in a single match: from `Person` to `Drug` along `:TAKES`, then from `Drug` to `DrugClass` along `:IS_A`. Each successful match produces one row; `DISTINCT` collapses duplicates because a single class node may be reached through multiple drugs. The result is four class names: csDMARD, TNFi, Glucocorticoid, Vitamin supplement.

        The same questions in relational SQL would require joining `person` to `drug_exposure` to `drug` to `drug_class` on the appropriate key columns. The Cypher version is shorter because the joins are implicit in the edge pattern. The Cypher query reads almost like the corresponding clinical sentence, where the SQL would require holding several JOIN clauses in mind at once.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Traversal: the operation graph databases are built for

        **Traversal** is the technical term for moving from one node to another along the graph's edges. The subway-map analogy is exact: traveling from one station to another means following the line that connects them, one stop at a time. A query that asks "what drugs is Reyes on" performs a single-edge traversal from her Person node along the `:TAKES` edges to the connected Drug nodes. A query that asks "what drug classes does Reyes have at least one drug in" performs a two-edge traversal: Person -> Drug -> DrugClass.

        What makes graph databases distinctive is **variable-length traversal**: a single query that follows an edge type some unspecified number of times, stopping when a condition is met or when no further edges of that type exist. The subway analogy: "follow the green line until you reach Park Street," regardless of how many stops are between here and there.

        The textbook clinical use case is the **SNOMED is-a hierarchy**. SNOMED CT organizes clinical findings into a hierarchy of increasing specificity. "Rheumatoid arthritis with multiple-site involvement" `IS_A` "Rheumatoid arthritis" `IS_A` "Inflammatory arthropathy" `IS_A` "Arthropathy" `IS_A` "Disorder of musculoskeletal system" `IS_A` "Clinical finding". A patient who carries the specific code at the bottom of the chain is, by the meaning of the hierarchy, also a patient with every ancestor in the chain.

        The relevant clinical question is "find every patient whose problem list carries any descendant of 'Inflammatory arthropathy', anywhere down the chain." In Cypher, that query is one line.

        ```
        MATCH (specific:Concept)-[:IS_A*]->(ancestor:Concept {name: 'Inflammatory arthropathy'})
        RETURN specific.name
        ```

        The new piece of syntax is the `*` in `[:IS_A*]`. The asterisk is the **variable-length operator**. It says "follow this edge type any number of times, including zero, until the pattern on the right side matches." The pattern as a whole reads as: starting from any `Concept` node (call it `specific`), follow a path of `:IS_A` edges of any length, and arrive at the `Concept` node named "Inflammatory arthropathy". Every starting node from which such a path exists is a match. The result is every descendant of "Inflammatory arthropathy" in the hierarchy.

        Expressing the same query in relational SQL requires a recursive Common Table Expression that iterates a self-join on the is-a table until no more parents exist. The SQL is longer, slower, and harder to read. For ontology traversal at the scale of SNOMED (roughly 350,000 concepts and several million IS_A relationships), the graph form is the only one that runs in interactive time on typical hardware.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Tools

        Four graph databases account for most production clinical use.

        - **Neo4j** is the most widely deployed graph database in clinical informatics. It uses Cypher as its query language (Cypher originated in Neo4j and is now standardized as GQL, an ISO standard analogous to SQL for relational databases). Neo4j has a free community edition and a paid enterprise edition with clustering support.
        - **Memgraph** is a Cypher-compatible graph database designed for in-memory workloads. The query language and data model are essentially Neo4j-compatible. Memgraph is often chosen for use cases where the entire graph fits in RAM and very low query latency is required.
        - **Amazon Neptune** is AWS's managed graph database. It supports both the property-graph model (with Gremlin or openCypher) and the RDF triple-store model (with SPARQL). It is the typical choice when the rest of the data infrastructure already lives on AWS.
        - **ArangoDB** is a multi-model database that supports graph, document, and key-value workloads in a single engine. It is the typical choice when the graph is one of several data shapes the team works with and consolidation simplifies operations.

        For SNOMED specifically, OHDSI provides the SNOMED is-a relationships in the OMOP `concept_ancestor` table, which is a pre-computed transitive closure. Queries that need ancestor information against OMOP-shaped data can use `concept_ancestor` directly in SQL without a graph database, at the cost of storing the closure rather than the edges. The graph form is the better fit when the data model itself is graph-shaped (referral networks, drug-drug interactions, knowledge graphs assembled from multiple sources) rather than purely hierarchical.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## When a graph database is not the right choice

        The graph model adds value when the shape of the question is "follow a path." It adds overhead when the shape of the question is "count rows" or "compute an aggregate per group." Three common cases where the relational model is the correct choice:

        - **Cohort definition.** Filtering a population to patients with a condition is a row-level filter against `condition_occurrence`. SQL handles it directly.
        - **Per-patient aggregates.** Computing the mean of a lab value per patient is a `GROUP BY` aggregation. SQL or a DataFrame library handles it more concisely than Cypher.
        - **Cross-tabulations.** Counting patients by treatment group and outcome is a relational pivot. The relational model is the natural fit.

        A practical rule: when the answer to "what is the central operation in this query?" is "join several tables and aggregate," use SQL or pandas. When the answer is "follow a chain of relationships of unknown length," use a graph database.
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "A SQL `JOIN` with a `GROUP BY` clause.",
            "A SQL recursive Common Table Expression that traverses the is-a hierarchy.",
            "A Cypher query using the variable-length traversal operator `[:IS_A*]`.",
            "Either the recursive CTE or the Cypher query, depending on whether the data is in a relational warehouse or a graph database.",
        ],
        label=(
            "A clinical research question requires identifying every patient "
            "whose problem list carries any descendant of SNOMED concept "
            "'Inflammatory arthropathy', traversing the SNOMED is-a "
            "hierarchy to arbitrary depth. Which query construct is best "
            "suited to the question?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("Either")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                Both forms express the query correctly; the choice depends on where the data lives. If the SNOMED hierarchy is in a relational warehouse (which is the typical OMOP setup, where the `concept_ancestor` table holds the pre-computed transitive closure), a SQL query against that table avoids the recursive CTE entirely. If the SNOMED hierarchy is in a graph database (which is the typical setup when the ontology is one piece of a larger knowledge graph), the Cypher variable-length traversal expresses the query in one line. The first option (`JOIN` with `GROUP BY`) does not handle the unknown-depth traversal at all; the second option works but is the longest and slowest form. The fourth option is the realistic answer for production work: the choice follows the data model, not a global preference for one engine.
                """
            ),
            kind="success" if correct1 else "warn",
        )
    out1
    return


@app.cell
def _(mo):
    q2 = mo.ui.radio(
        options=[
            "Graph database. The question is shaped as nodes (drugs) and edges (transitions).",
            "Relational warehouse. The question is a per-patient aggregate over the drug_exposure table.",
            "Either model handles the question; the choice depends on team familiarity.",
            "Graph database, because medication histories naturally form a sequence.",
        ],
        label=(
            "A clinical analytics team is asked: 'For each patient in our "
            "RA cohort, what is the total number of distinct medications "
            "they have ever been exposed to?' Which data model is the "
            "natural fit?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Relational warehouse")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                The question is a per-patient aggregate: `SELECT person_id, COUNT(DISTINCT drug_concept_id) FROM drug_exposure GROUP BY person_id`. The data has a graph-shaped representation, but the question does not exercise the graph structure. No traversal, no path-finding, no variable-length operation is required. Using a graph database to compute this aggregate would add overhead without adding capability. The general rule is to match the data model to the question's central operation: aggregations and filters belong in the relational model; path-following and traversal belong in the graph model. The fourth option is wrong for the same reason as the first: the shape of the data is not the determining factor; the shape of the question is.
                """
            ),
            kind="success" if correct2 else "warn",
        )
    out2
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to the course capstone.

        1. **A clinical question from your work** has the shape of "follow a path of relationships of unknown length." Specify the question. Identify the nodes, the edges, and the property values that would describe the relevant entities. State the query in Cypher pseudocode using the patterns shown in this track.

        2. **A team proposes** moving the entire clinical warehouse from PostgreSQL into Neo4j on the argument that "everything is a graph eventually." Identify the operational risks of the move. State which categories of query would suffer and which would benefit, and recommend the boundary at which a hybrid (relational warehouse plus a separate graph database for specific subgraphs) would be the better architecture.
        """
    )
    return


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        placeholder="Write 4-6 sentences here. Your text stays in your browser; copy it out if you want to keep it.",
        rows=8,
        full_width=True,
    )
    reflection
    return


@app.cell
def _(mo, xref):
    xref.forward(
        "07-data-wrangling-engineering",
        "07-data-wrangling-engineering",
        "The course capstone integrates every layer.",
        (
            "The course has now covered the four layers required to take a "
            "clinical question from raw EHR data to an analytic answer: "
            "code standards (Track 01), the OMOP schema layered on top "
            "(Track 02), SQL as the extraction language (Track 03), and "
            "pandas as the post-extraction analytic layer (Track 04), plus "
            "the graph model for the questions that do not fit the tabular "
            "shape (this track). The capstone presents three messy raw "
            "tables and asks for one OMOP-shaped output and three clinical "
            "queries against it, one per layer. Continue to the course "
            "capstone."
        ),
    )
    return


if __name__ == "__main__":
    app.run()
