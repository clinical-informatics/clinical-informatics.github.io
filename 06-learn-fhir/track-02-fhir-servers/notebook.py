"""Track 2: Working with FHIR servers.

The request/response cycle of a real FHIR server, walked on
hapi.fhir.org with cached fallbacks for offline runs, then applied to
a synthetic five-patient RA cohort fixture for the capstone (CRP and
ESR trends over four years).

Python is introduced gently here. Most cells show one or two visible
lines of code that build a URL, send a GET, or parse a dictionary;
the cell wiring around them stays the same Marimo pattern from
earlier tracks.

Fixtures live in `fixtures/cohort.json` (built by `fixtures/build_cohort.py`).
Cached real responses from hapi.fhir.org live in `cache/`.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import sys
    from datetime import datetime
    from pathlib import Path
    from urllib.parse import urlencode

    import altair as alt
    import marimo as mo
    import pandas as pd

    # fhir_get inlined from shared/fhir_compat.py so the WASM export is
    # self-contained. Uses requests locally and pyodide.http in the browser.
    def fhir_get(url, params=None):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url

            full = url if not params else f"{url}?{urlencode(params)}"
            return json.loads(open_url(full).read())
        import requests

        resp = requests.get(
            url,
            params=params or {},
            headers={
                "Accept": "application/fhir+json",
                "User-Agent": "clinical-informatics/0.1",
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    # Absolute site path where this notebook's WASM export lives. Used only
    # in the Pyodide branch below; `pyodide.http.open_url` resolves a
    # leading-slash path against the page origin, which works identically in
    # the main thread and in the marimo worker. Update this if the notebook
    # is renamed or the site is deployed under a subpath.
    _WASM_DATA_BASE = "/06-learn-fhir/track-02-fhir-servers/app"

    def read_data(*parts):
        """Open a JSON file alongside this notebook. Works locally and in WASM.

        Locally: reads from ``Path(__file__).parent / parts``.
        In Pyodide WASM: fetches ``_WASM_DATA_BASE / parts`` via
        ``pyodide.http.open_url``. The build pipeline mirrors ``cache/`` and
        ``fixtures/`` into the WASM export so the same relative layout
        resolves in both contexts.
        """
        if "pyodide" in sys.modules:
            from pyodide.http import open_url

            url = _WASM_DATA_BASE + "/" + "/".join(parts)
            return json.loads(open_url(url).read())
        return json.loads(Path(__file__).parent.joinpath(*parts).read_text())

    def load_with_cache(cache_filename, live_url=None, live_params=None):
        """Return (data, source). Prefer cached; fetch live only if cache missing.

        The cached responses ship with the curriculum so the notebook is
        deterministic and works offline. Delete the file in `cache/` (locally)
        to force a live re-fetch.
        """
        try:
            return read_data("cache", cache_filename), "cache"
        except Exception:
            pass
        if live_url is None:
            raise FileNotFoundError(
                f"Cache {cache_filename} missing and no live_url provided"
            )
        data = fhir_get(live_url, live_params or {})
        # Local-only: persist for offline re-runs. Best-effort, harmless in WASM.
        try:
            cache_dir = Path(__file__).parent / "cache"
            cache_dir.mkdir(exist_ok=True)
            (cache_dir / cache_filename).write_text(json.dumps(data, indent=2))
        except Exception:
            pass
        return data, "live"

    return (
        read_data,
        alt,
        datetime,
        fhir_get,
        json,
        load_with_cache,
        mo,
        pd,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 2: Working with FHIR servers

        ## The bundle on your desk arrived from somewhere.

        Track 1 had you read a FHIR bundle that another rheumatologist sent over. Track 2 asks a different question: how did the bundle get there in the first place, and what would it take for *you* to ask their server for it?

        A FHIR server is a web service that speaks FHIR over HTTP. You send it requests, it sends back responses. There is no other ceremony. By the end of this track you'll have:

        - Made a real call to a public FHIR test server (`hapi.fhir.org`) and parsed the response.
        - Built a search URL piece by piece, with the LOINC code coming from a dropdown.
        - Worked through how a server reports pagination and how a client walks it.
        - Pulled CRP and ESR for a synthetic cohort of five RA patients across four years and rendered the trend chart.

        Python gets introduced gently. Most cells have one or two visible lines: a URL constructed, a `GET` sent, a dictionary read. The clinical reasoning carries the rest.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The smallest possible FHIR client.

        Four lines of Python make a real FHIR call:

        ```python
        import requests
        url = "https://hapi.fhir.org/baseR4/metadata"
        resp = requests.get(url, headers={"Accept": "application/fhir+json"})
        data = resp.json()
        ```

        Read it line by line.

        - **`import requests`.** Bring in Python's de-facto HTTP library.
        - **`url = ...`.** The full address of the resource on the FHIR server. `/metadata` on any FHIR server returns the server's CapabilityStatement, which describes what it can do.
        - **`resp = requests.get(url, headers=...)`.** Send an HTTP `GET` request. The `Accept` header tells the server we want FHIR JSON back. (Without it, some servers default to XML.)
        - **`data = resp.json()`.** Parse the response body into a Python dictionary. From here, `data["resourceType"]`, `data["software"]["name"]`, and so on.

        That is the entire client. Real production code adds error handling, retries, authentication, and async, but the core remains those four lines.

        This curriculum uses a wrapper at `shared.fhir_compat.fhir_get(url, params)` that does the same thing while also working inside browser-hosted Marimo (where the WASM sandbox can't call `requests` synchronously). Same signature: pass a URL, get back a parsed dictionary.

        Below we'll use the wrapper. Same response shape.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Live demo 1. What can the server do?

        The `/metadata` endpoint on any FHIR server returns its **CapabilityStatement**: a self-description of the server. Which FHIR version it speaks, which resources it supports, what authentication it requires, which search parameters it implements per resource. Any FHIR client starts by reading this, because it tells you whether the server can answer the questions you want to ask.

        The cell below loads a cached copy of `https://hapi.fhir.org/baseR4/metadata`. (The cache file ships with the curriculum so the notebook works offline; delete `cache/capability-statement.json` to force a live re-fetch.)
        """
    )
    return


@app.cell
def _(load_with_cache, mo):
    cap_data, cap_source = load_with_cache(
        "capability-statement.json",
        live_url="https://hapi.fhir.org/baseR4/metadata",
    )
    cap_summary = mo.callout(
        mo.md(
            f"""
**Source:** {cap_source}.

- **Server software:** {cap_data['software']['name']}, version {cap_data['software']['version']}
- **FHIR version:** {cap_data['fhirVersion']}
- **Server kind:** {cap_data['kind']} (a `kind` of `instance` means a running server; `capability` would describe a software product abstractly)
- **Implementation:** {cap_data.get('implementation', {}).get('description', 'not provided')}
- **Supported formats:** {', '.join(cap_data.get('format', []))}

The CapabilityStatement also lists every resource type the server can handle. This particular server's first REST endpoint exposes **{cap_data['rest'][0]['resource_count']} different resource types** including the ones we care about: Patient, Observation, Condition, MedicationStatement, AllergyIntolerance, Encounter, and so on.

When you're integrating with a new FHIR server in real life, this is the first call you make. The CapabilityStatement tells you what's possible before you build the rest of your integration around assumptions that won't hold.
"""
        ),
        kind="info",
    )
    cap_summary
    return cap_data, cap_source, cap_summary


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Live demo 2. The simplest possible search.

        Now a search. The query

        ```
        GET https://hapi.fhir.org/baseR4/Patient?_count=2&_format=json
        ```

        says: "Give me up to two Patient resources from this server, formatted as JSON." We're not filtering by name or anything else; just asking for whatever the server has, in batches of two.

        The cell below loads a cached copy of that response.
        """
    )
    return


@app.cell
def _(load_with_cache, mo):
    search_data, search_source = load_with_cache(
        "patient-search.json",
        live_url="https://hapi.fhir.org/baseR4/Patient",
        live_params={"_count": 2, "_format": "json"},
    )

    next_link = next(
        (l["url"] for l in search_data.get("link", []) if l.get("relation") == "next"),
        None,
    )

    patient_rows = []
    for _entry in search_data["entry"]:
        _r = _entry["resource"]
        _names = _r.get("name", [])
        _first_name = _names[0] if _names else {}
        _family = _first_name.get("family") or "(no family name)"
        _given = " ".join(_first_name.get("given", [])) or "(no given name)"
        patient_rows.append(
            f"- **Patient id {_r.get('id')}** -- name: {_family}, {_given}; "
            f"birthDate: {_r.get('birthDate', '(not set)')}; "
            f"gender: {_r.get('gender', '(not set)')}"
        )

    mo.callout(
        mo.md(
            f"""
**Source:** {search_source}.

The server returned a Bundle of `type: {search_data['type']}`. The Bundle has:

- **`total`:** {search_data.get('total', '(omitted; some servers skip this for performance)')}
- **{len(search_data['entry'])} entries** in this response
- A **`next` link** pointing at: `{(next_link or 'none')[:90]}{'...' if next_link and len(next_link) > 90 else ''}`

The two patients returned in this page:

{chr(10).join(patient_rows)}

These two were picked from a curated query (`Patient?name=Smith` and `Patient?name=Garcia`, one entry each) because the *uncurated* default query `Patient?_count=10` happens to return ten copies of the same test patient right now. Someone's load-testing script POSTed the same Patient ten times in a row, and FHIR's "every POST creates a new resource with a server-assigned id" semantics means the server now has ten different patient ids pointing at indistinguishable data. **This is what public FHIR test servers actually look like.** Production servers have their own quality issues; the noise on hapi is an underdamped version of what you'll see everywhere, and "find the same patient under multiple ids" is a real production duplicate-MRN problem at every health system.

The two structural takeaways. First, a search response is always a Bundle with `type: searchset`. Second, the `link[]` array carries pagination: the `next` link is what you fetch to get the second page.
"""
        ),
        kind="info",
    )
    return next_link, patient_rows, search_data, search_source


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Build a search URL.

        The general shape of a FHIR search:

        ```
        <base>/<ResourceType>?<param>=<value>&<param>=<value>...
        ```

        Try it. Pick a lab from the dropdown below, plus a patient narrowing and a date floor, and watch the URL update. The URL is exactly what your code would send to a FHIR server.
        """
    )
    return


@app.cell
def _(mo):
    loinc_choices = {
        "CRP (LOINC 1988-5)": "1988-5",
        "ESR (LOINC 4537-7)": "4537-7",
        "DAS28-CRP (LOINC 76374-2)": "76374-2",
        "Anti-CCP (LOINC 32218-7)": "32218-7",
        "Hemoglobin (LOINC 718-7)": "718-7",
    }
    loinc_dropdown = mo.ui.dropdown(
        options=list(loinc_choices.keys()),
        value="CRP (LOINC 1988-5)",
        label="LOINC code to query",
    )
    patient_id = mo.ui.text(
        value="elena-reyes",
        label="Patient id (the part after `Patient/`)",
        full_width=False,
    )
    date_floor = mo.ui.text(
        value="2024-01-01",
        label="Earliest effective date (YYYY-MM-DD)",
        full_width=False,
    )
    sort_desc = mo.ui.checkbox(
        value=True,
        label="Sort newest first",
    )
    count = mo.ui.slider(
        start=1, stop=200, step=1, value=20,
        label="Maximum results per page (`_count`)",
        show_value=True,
    )
    mo.vstack([loinc_dropdown, patient_id, date_floor, sort_desc, count])
    return count, date_floor, loinc_choices, loinc_dropdown, patient_id, sort_desc


@app.cell
def _(count, date_floor, loinc_choices, loinc_dropdown, mo, patient_id, sort_desc):
    _loinc_code = loinc_choices[loinc_dropdown.value]
    _base = "https://hapi.fhir.org/baseR4"
    _params = [
        f"subject=Patient/{patient_id.value}",
        f"code=http://loinc.org|{_loinc_code}",
        f"effective-date=ge{date_floor.value}",
        f"_sort={'-date' if sort_desc.value else 'date'}",
        f"_count={count.value}",
    ]
    _formatted = f"GET {_base}/Observation\n    ?" + "\n    &".join(_params)

    mo.callout(
        mo.md(
            f"""
**Constructed FHIR query** (formatted across lines for readability; the real URL is one continuous string with no whitespace):

```http
{_formatted}
```

Read it like a sentence. *Give me Observations* (`/Observation`), *for this patient* (`subject=Patient/...`), *with this LOINC code* (`code=http://loinc.org|...`), *dated on or after this floor* (`effective-date=ge...`), *sorted by date* (`_sort=...`), *no more than this many per page* (`_count=...`). The `ge` in front of the date is the FHIR comparator for greater-or-equal; the alternatives are `gt`, `lt`, `le`, `eq`, `ne`.

The `code` parameter is qualified with the system (`http://loinc.org|...`) so we don't accidentally match a SNOMED code that happens to share the digit string. For LOINC this rarely matters; for SNOMED and ICD-10 it matters a lot, because the same digit string is often a valid code in multiple vocabularies.
"""
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Parse the response.

        Every search response is a Bundle of `type: "searchset"`. The shape is uniform across every FHIR server. In Python, the parsing pattern is one loop:

        ```python
        bundle = resp.json()
        assert bundle["resourceType"] == "Bundle"
        for entry in bundle.get("entry", []):
            resource = entry["resource"]
            rtype = resource["resourceType"]
            # do something with the resource
        ```

        Two small details that catch people off guard.

        - **Not every server reports `total`.** Some servers omit it for performance; counting all matches against a 50-million-row table is expensive. Don't rely on `total` being present; rely on the actual entry count.
        - **`search.mode` distinguishes matches from includes.** When your query uses `_include`, the response contains both the resources matching your search and the resources they reference. `mode: "match"` means it matched your search; `mode: "include"` means it was pulled along because something else referenced it.
        """
    )
    return


@app.cell
def _(mo):
    parse_quiz = mo.ui.radio(
        options=[
            "`bundle['entry'][0]['family']`",
            "`bundle['entry'][0]['resource']['name']['family']`",
            "`bundle['entry'][0]['resource']['name'][0]['family']`",
            "`bundle.entry[0].resource.name[0].family`",
        ],
        label=(
            "Given a `searchset` Bundle returned from `GET /Patient?_count=5` and stored as the Python dict `bundle`, "
            "which expression gives you the family name of the first patient in the response?"
        ),
    )
    parse_quiz
    return (parse_quiz,)


@app.cell
def _(mo, parse_quiz):
    _v = parse_quiz.value
    _correct = "`bundle['entry'][0]['resource']['name'][0]['family']`"
    _missing_resource = "`bundle['entry'][0]['family']`"
    _missing_name_index = "`bundle['entry'][0]['resource']['name']['family']`"
    _dot_access = "`bundle.entry[0].resource.name[0].family`"

    if _v is None:
        parse_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif _v == _correct:
        parse_response = mo.callout(
            mo.md(
                "**Right.** Step by step: `bundle['entry']` is the array of entries. `[0]` is the first entry. `['resource']` reaches into the resource (entries also carry `fullUrl` and `search` metadata; the clinical content is under `resource`). `['name']` is the array of names (always an array, even for one name). `[0]` is the first name. `['family']` is the family-name string on that name object.\n\nThe pattern of `entry[].resource.<field>` is the workhorse access path for every FHIR client. You'll write it constantly."
            ),
            kind="success",
        )
    elif _v == _missing_resource:
        parse_response = mo.callout(
            mo.md(
                "**Almost.** `bundle['entry'][0]` gives you the entry, which is a dict with `fullUrl`, `resource`, and (in a search response) `search`. The Patient resource itself is one level deeper, at `entry[0]['resource']`. Inside the Patient, `name` is an array, so you index with `[0]` again. Family is on each name object. Correct path: `bundle['entry'][0]['resource']['name'][0]['family']`."
            ),
            kind="warn",
        )
    elif _v == _missing_name_index:
        parse_response = mo.callout(
            mo.md(
                "**Almost.** `name` in a FHIR resource is **always an array**, even when there's only one. You need an index step: `name[0]`. Otherwise this throws a TypeError when Python tries to use a string key on a list. Correct path: `bundle['entry'][0]['resource']['name'][0]['family']`."
            ),
            kind="warn",
        )
    elif _v == _dot_access:
        parse_response = mo.callout(
            mo.md(
                "**Not quite.** Dot-access (`bundle.entry`) doesn't work on plain Python dictionaries; you need bracket-access (`bundle['entry']`). Some FHIR client libraries wrap dicts in objects that *do* support dot-access, but the parsed-JSON dict returned by `resp.json()` and `fhir_get()` uses brackets. Correct path: `bundle['entry'][0]['resource']['name'][0]['family']`."
            ),
            kind="warn",
        )
    else:
        parse_response = mo.callout(mo.md(f"_Unrecognized option: {_v}_"), kind="neutral")
    parse_response
    return (parse_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pagination.

        Servers cap how many results they return in one response. If there are more matches than fit in one page, the Bundle carries a `next` link in its `link[]` array, and your client fetches that URL to get the second page. Keep walking the `next` links until there isn't one.

        The pattern:

        ```python
        def collect_all(start_url):
            results = []
            url = start_url
            while url:
                bundle = fhir_get(url)
                for entry in bundle.get("entry", []):
                    results.append(entry["resource"])
                url = _next_link(bundle)
            return results

        def _next_link(bundle):
            for link in bundle.get("link", []):
                if link.get("relation") == "next":
                    return link["url"]
            return None
        ```

        Two practical notes.

        - **`_count` is a hint, not a requirement.** The server may give you fewer results than you asked for. It may also cap your request at its own maximum. Don't assume page size.
        - **The `next` URL is opaque.** Don't parse it; just fetch it. Some servers embed encrypted continuation tokens; some put offsets in the URL. Your client treats it as a black-box pointer to the next page.
        """
    )
    return


@app.cell
def _(mo):
    paging_quiz = mo.ui.radio(
        options=[
            "1 request returning 87 results.",
            "5 requests of 20 results each.",
            "5 requests: four of 20 results and one of 7.",
            "It depends on the server; the spec doesn't define this."
        ],
        label=(
            "You ask a FHIR server for all Observations matching a query, with `_count=20`. "
            "The server's `total` field on the first page reads 87. "
            "Assuming the server honors your `_count` and reports `next` links until there are no more matches, "
            "how many HTTP requests does your code make to collect all 87 results?"
        ),
    )
    paging_quiz
    return (paging_quiz,)


@app.cell
def _(mo, paging_quiz):
    if paging_quiz.value is None:
        paging_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif paging_quiz.value.startswith("5 requests: four of 20"):
        paging_response = mo.callout(
            mo.md(
                "**Right.** 87 results with `_count=20` means 4 full pages of 20 (covering results 1 to 80) plus a final page of 7 (results 81 to 87). The final page has no `next` link, which is how your loop knows to stop. Five HTTP requests total."
            ),
            kind="success",
        )
    elif paging_quiz.value.startswith("1 request"):
        paging_response = mo.callout(
            mo.md(
                "**No.** `_count=20` caps each page at 20 results. The server honors that and uses `next` links to give you the rest. To collect 87 results you need ceil(87/20) = 5 requests."
            ),
            kind="warn",
        )
    elif paging_quiz.value.startswith("5 requests of 20"):
        paging_response = mo.callout(
            mo.md(
                "**Close.** 5 requests is right, but the last one only returns 7 results (87 minus the 80 you already have). The server doesn't pad the last page to fill it."
            ),
            kind="warn",
        )
    else:
        paging_response = mo.callout(
            mo.md(
                "**Not quite.** Pagination behavior is defined by the FHIR spec: `_count` caps page size, `link[].relation = 'next'` carries the continuation URL, the loop stops when there's no `next`. Some details are server-specific (whether `total` is included, how the `next` URL is constructed), but the page-counting math is uniform: ceil(total/_count) requests."
            ),
            kind="warn",
        )
    paging_response
    return (paging_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone: the synthetic RA cohort.

        From here, we leave hapi.fhir.org behind. The data there is too noisy for the kind of cohort work the rest of this track does. Instead, we load a hand-crafted fixture: a `searchset` Bundle representing what a well-behaved server *would* return for a query like

        ```
        GET /Observation?code=http://loinc.org|1988-5,http://loinc.org|4537-7
            &_include=Observation:patient
            &_count=200
        ```

        Five patients, their Condition records for RA, and every CRP and ESR observation across the cohort over the 2022 to 2026 window. About 150 entries total.

        Loading the fixture is one line:

        ```python
        bundle = read_data("fixtures/cohort.json")
        ```
        """
    )
    return


@app.cell
def _(read_data, mo, pd):
    cohort_bundle = read_data("fixtures", "cohort.json")

    _type_counts = {}
    for _entry in cohort_bundle["entry"]:
        _rt = _entry["resource"]["resourceType"]
        _type_counts[_rt] = _type_counts.get(_rt, 0) + 1
    summary_table = pd.DataFrame(
        [{"Resource type": _rt, "Count in bundle": _n} for _rt, _n in sorted(_type_counts.items(), key=lambda kv: -kv[1])]
    )
    mo.vstack(
        [
            mo.md(
                f"""
**Cohort bundle loaded.** Bundle type: `{cohort_bundle['type']}`, `total`: {cohort_bundle.get('total')}, entries: {len(cohort_bundle['entry'])}.

The `link[].self` URL on the bundle:

```
{cohort_bundle['link'][0]['url']}
```
"""
            ),
            mo.ui.table(summary_table, selection=None),
        ]
    )
    return cohort_bundle, summary_table


@app.cell
def _(cohort_bundle, mo, pd):
    patients_in_cohort = [
        _e["resource"] for _e in cohort_bundle["entry"]
        if _e["resource"]["resourceType"] == "Patient"
    ]
    _rows = []
    for _p in patients_in_cohort:
        _n = _p["name"][0]
        _rows.append(
            {
                "Patient id": _p["id"],
                "Name": f"{', '.join(_n['given'])} {_n['family']}",
                "Gender": _p["gender"],
                "Birth date": _p["birthDate"],
            }
        )
    patients_df = pd.DataFrame(_rows)
    mo.vstack(
        [
            mo.md("**The five patients in the cohort:**"),
            mo.ui.table(patients_df, selection=None),
            mo.callout(
                mo.md(
                    "Each patient also has one Condition (RA) and a series of CRP and ESR observations roughly every three months. Different patients have different trajectories on purpose: a moderate responder, a slow worsener on MTX monotherapy, a dramatic responder with a hold-and-flare event, an aggressive case that failed three agents, and a freshly-diagnosed patient still titrating. Reading the chart should let you tell them apart."
                ),
                kind="info",
            ),
        ]
    )
    return patients_df, patients_in_cohort


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone, part A. Pull CRP and ESR into a table.

        The work is one loop. Walk the entries, keep the Observations, read three fields off each one, build a row. This is what `entry[].resource.<field>` access looks like in practice:

        ```python
        rows = []
        for entry in cohort_bundle["entry"]:
            r = entry["resource"]
            if r["resourceType"] != "Observation":
                continue
            loinc_code = r["code"]["coding"][0]["code"]
            patient_ref = r["subject"]["reference"]            # 'Patient/<id>'
            patient_id = patient_ref.split("/")[1]
            rows.append({
                "patient_id": patient_id,
                "test": "CRP" if loinc_code == "1988-5" else "ESR",
                "date": r["effectiveDateTime"][:10],
                "value": r["valueQuantity"]["value"],
                "unit": r["valueQuantity"]["unit"],
            })
        df = pd.DataFrame(rows)
        ```

        Run mentally and then look at the result below.
        """
    )
    return


@app.cell
def _(cohort_bundle, mo, pd):
    _lab_rows = []
    for _entry in cohort_bundle["entry"]:
        _r = _entry["resource"]
        if _r["resourceType"] != "Observation":
            continue
        _loinc_code = _r["code"]["coding"][0]["code"]
        if _loinc_code not in ("1988-5", "4537-7"):
            continue
        _patient_ref = _r["subject"]["reference"]
        _pid = _patient_ref.split("/")[1]
        _lab_rows.append(
            {
                "patient_id": _pid,
                "test": "CRP" if _loinc_code == "1988-5" else "ESR",
                "date": _r["effectiveDateTime"][:10],
                "value": _r["valueQuantity"]["value"],
                "unit": _r["valueQuantity"]["unit"],
                "flag": (_r.get("interpretation") or [{}])[0].get("coding", [{}])[0].get("code", ""),
            }
        )
    labs_df = pd.DataFrame(_lab_rows)
    labs_df = labs_df.sort_values(["patient_id", "test", "date"]).reset_index(drop=True)
    mo.vstack(
        [
            mo.md(f"**Lab dataframe.** {len(labs_df)} rows across {labs_df['patient_id'].nunique()} patients."),
            mo.ui.table(labs_df, selection=None, pagination=True, page_size=20),
        ]
    )
    return (labs_df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone, part B. The trend chart.

        With CRP and ESR per patient as a long-format DataFrame, the chart writes itself. Each patient is a line; the upper-limit-of-normal sits as a horizontal reference. Switch between CRP and ESR with the dropdown.
        """
    )
    return


@app.cell
def _(mo):
    lab_pick = mo.ui.dropdown(
        options=["CRP", "ESR"],
        value="CRP",
        label="Which lab to plot",
    )
    lab_pick
    return (lab_pick,)


@app.cell
def _(alt, lab_pick, labs_df, mo, patients_in_cohort):
    _chosen = lab_pick.value
    _df = labs_df[labs_df["test"] == _chosen].copy()
    _df["date"] = _df["date"].astype("datetime64[ns]")

    _name_lookup = {
        _p["id"]: f"{_p['name'][0]['given'][0]} {_p['name'][0]['family']}"
        for _p in patients_in_cohort
    }
    _df["patient_name"] = _df["patient_id"].map(_name_lookup)

    _uln = 5 if _chosen == "CRP" else 20
    _units = "mg/L" if _chosen == "CRP" else "mm/h"

    _line = alt.Chart(_df).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title=f"{_chosen} ({_units})", scale=alt.Scale(zero=True)),
        color=alt.Color("patient_name:N", title="Patient"),
        tooltip=["patient_name", "date", "value", "flag"],
    )
    _reference = alt.Chart(alt.InlineData(values=[{"uln": _uln}])).mark_rule(
        strokeDash=[4, 4], color="gray"
    ).encode(y="uln:Q")

    _chart = (_line + _reference).properties(width="container", height=380).interactive()
    mo.vstack(
        [
            mo.ui.altair_chart(_chart),
            mo.callout(
                mo.md(
                    f"**Reading the chart.** "
                    f"{_chosen} upper limit of normal is **{_uln} {_units}** (dashed gray line). Every line above it is an elevated value; every line below is in range. "
                    "Five trajectories are visible: Reyes shows a high-then-tamed pattern with the adalimumab addition in early 2024; Chen shows a slow re-worsening on MTX monotherapy through 2025 with the recent biologic add starting to bend the line back down; Williams is the dramatic responder whose 2024 hold-and-flare shows up as a single spike; Patel started highest of anyone, took most of two years to control, and now sits stably above the line on rituximab; Russo only appears in the last year because she was just diagnosed.\n\n"
                    "Hover any point for the underlying value and the high/low/normal flag."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection.

        Take a moment with this one. The chart above was assembled from a synthetic bundle. If this were a real, live FHIR server in front of you, what would change?
        """
    )
    return


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        placeholder="A few sentences. Think about authentication, data quality, pagination, missing observations, terminology drift across sites.",
        rows=5,
        full_width=True,
        label=(
            "Imagine this same chart, but pulled from your hospital's production FHIR endpoint covering 200 RA patients. "
            "Name three things that would be harder than the version we just did. (No reveal; the writing is the work.)"
        ),
    )
    mo.vstack(
        [
            reflection,
            mo.callout(
                mo.md(
                    "_There's no answer key for this one. A few things worth at least having on your list when you write it: "
                    "(1) authentication (real servers don't let anonymous clients pull patient data); "
                    "(2) data quality (real cohorts have missing observations, duplicate observations from different lab systems, codes from local code sets that don't match LOINC, dates in the wrong time zone); "
                    "(3) pagination at scale (200 patients with quarterly labs over five years is 4,000+ observations, which will paginate); "
                    "(4) cohort definition (your real cohort isn't 'five patients with RA Conditions' but 'patients whose most recent active problem-list entry includes an RA code, who saw a rheumatologist within the last two years, who weren't enrolled in a clinical trial during the period'); "
                    "(5) terminology drift (a hospital that recently migrated from ICD-10 to SNOMED on the problem list will have both, sometimes for the same patient)._"
                ),
                kind="neutral",
            ),
        ]
    )
    return (reflection,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - You made real calls to a real FHIR server. The CapabilityStatement endpoint told you what the server can do. A Patient search showed you what a searchset Bundle looks like, including the unicode mojibake that comes with public test-server data.
        - You built FHIR search URLs piece by piece, with the LOINC code coming from a dropdown, and read the resulting URL like a sentence.
        - You learned the access path that every FHIR client repeats: `bundle["entry"][i]["resource"][<field>]`, with `name[0].family` and the other "always an array" quirks called out.
        - You walked the pagination pattern: `link.relation = 'next'`, fetch until exhausted, treat the URL as opaque.
        - You pulled CRP and ESR for five synthetic RA patients out of a 146-entry searchset bundle, into a pandas DataFrame, and rendered the four-year disease-activity trajectory for each one as an Altair line chart with the upper-limit-of-normal as a reference.

        That is what a FHIR client looks like end to end. The data quality questions you wrote in the reflection above are the work of Tracks 3 through 5.

        ## What's next.

        **Track 3: Clinical modeling.** Now you write FHIR. Observation, Condition, MedicationRequest. Profiles and extensions. The US Core implementation guide. Must-support fields. The track-level capstone is to author Ms. Reyes's record from scratch, validate it on hapi.fhir.org's `$validate` endpoint, and get a clean validation report back. Track 2 was the read half. Track 3 is the write half.
        """
    )
    return


if __name__ == "__main__":
    app.run()
