"""Track 3: Clinical modeling (authoring valid FHIR).

The inverse of Track 2. Track 2 read what the server sent back; Track
3 writes the resources the server would receive. Concepts: the
minimum required fields per resource type; profiles as constrained
base resources (US Core as the worked example); must-support as a
contract on receivers, not senders; extensions for data the base
spec doesn't have; the `$validate` endpoint that tells you what's
wrong before something else does.

Capstone: build Ms. Reyes's next follow-up visit as a transaction
Bundle (Encounter plus four Observations: CRP, ESR, DAS28-CRP, and
BP), with live validation against hapi.fhir.org's $validate endpoint
on a button click. Cached OperationOutcomes for two reference cases
ship in `cache/`.

All cell-internal variables are underscore-prefixed to satisfy
Marimo's multi-definition check; only values that downstream cells
actually consume escape with normal names.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import math
    import sys
    from pathlib import Path
    from urllib.parse import urlencode

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

    # Absolute site path where this notebook's WASM export lives. See the
    # comment in load_cached below.
    _WASM_DATA_BASE = "/06-learn-fhir/track-03-clinical-modeling/app"

    def load_cached(filename):
        """Read a JSON file from the notebook's cache/ dir. Local + WASM.

        Locally: reads from ``Path(__file__).parent / "cache" / filename``.
        In Pyodide WASM: fetches ``_WASM_DATA_BASE/cache/<filename>`` via
        ``pyodide.http.open_url`` (leading-slash paths resolve against the
        page origin, which works identically in the main thread and in the
        marimo worker). The build pipeline mirrors ``cache/`` into the WASM
        export so the same relative layout resolves in both contexts.
        """
        if "pyodide" in sys.modules:
            from pyodide.http import open_url

            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return json.loads(open_url(url).read())
        return json.loads((Path(__file__).parent / "cache" / filename).read_text())

    def post_validate(resource):
        """POST to hapi.fhir.org/<ResourceType>/$validate. Returns the OperationOutcome.

        Uses urllib locally. In Pyodide WASM, synchronous POST is not
        available; the learner can still run validation locally or read the
        cached results below.
        """
        url = f"https://hapi.fhir.org/baseR4/{resource['resourceType']}/$validate"
        if "pyodide" in sys.modules:
            return {
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "information",
                        "code": "informational",
                        "diagnostics": (
                            "Live $validate is unavailable in the browser-hosted "
                            "version of this notebook. Run this notebook locally, "
                            "or read the cached validation result the next cell "
                            "loads, which is the same response hapi.fhir.org "
                            "produced when the curriculum was built."
                        ),
                    }
                ],
            }
        import urllib.error
        import urllib.request

        body = json.dumps(resource).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/fhir+json",
                "Accept": "application/fhir+json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return json.loads(e.read())

    return (
        Path,
        fhir_get,
        json,
        load_cached,
        math,
        mo,
        pd,
        post_validate,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 3: Clinical modeling

        ## Writing FHIR, not reading it.

        Track 1 had a bundle on your desk; you read it. Track 2 asked the server for resources; you parsed the response. Track 3 is the inverse: you sit down to *write* a FHIR resource from scratch, and a downstream system either accepts what you wrote or sends back a list of complaints.

        The wire format is the same. A FHIR resource is a JSON object with a `resourceType`, an optional `id`, and a set of fields appropriate to that type. The difference is responsibility. As a reader you trusted whatever the sender wrote. As a writer, you *are* the sender, and the receiver will reject your resource if it's malformed.

        The track closes with:

        - You can identify the minimum required fields for Observation, Condition, MedicationRequest, and Encounter.
        - You understand what a profile is (a constrained version of a base resource) and what must-support means (a contract on the receiver, not the sender).
        - You can read an OperationOutcome and act on it.
        - You've authored a small bundle of resources for Ms. Reyes's next follow-up visit and validated it against a real FHIR server.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 1. The minimum required fields.

        Every FHIR resource has a spec page that lists every field plus its **cardinality**. Cardinality is a pair like `0..1` or `1..1` or `0..*` or `1..*`. The first number is the minimum (0 means optional, 1 means required); the second is the maximum (1 means scalar, `*` means array of any size).

        Fields with cardinality `1..1` or `1..*` are required. Everything else is optional.

        For the four resource types you'll author in this track, the minimum requirements are small.
        """
    )
    return


@app.cell
def _(pd):
    min_fields = pd.DataFrame(
        [
            {"Resource": "Observation", "Field": "resourceType", "Cardinality": "1..1", "Notes": "Always 'Observation'."},
            {"Resource": "Observation", "Field": "status", "Cardinality": "1..1", "Notes": "Use 'final' for a result you'd hand the patient."},
            {"Resource": "Observation", "Field": "code", "Cardinality": "1..1", "Notes": "What was observed. Usually LOINC."},
            {"Resource": "Observation", "Field": "subject", "Cardinality": "0..1", "Notes": "Optional in base, but practically always sent."},
            {"Resource": "Observation", "Field": "valueQuantity", "Cardinality": "0..1", "Notes": "Or another value[x]. Optional because some Observations record only an interpretation."},
            {"Resource": "Condition", "Field": "resourceType", "Cardinality": "1..1", "Notes": "'Condition'."},
            {"Resource": "Condition", "Field": "subject", "Cardinality": "1..1", "Notes": "Reference to Patient."},
            {"Resource": "Condition", "Field": "code", "Cardinality": "0..1", "Notes": "The condition itself. Almost always sent."},
            {"Resource": "Condition", "Field": "clinicalStatus", "Cardinality": "conditional", "Notes": "Required unless verificationStatus is 'entered-in-error'."},
            {"Resource": "MedicationRequest", "Field": "status", "Cardinality": "1..1", "Notes": "'active', 'on-hold', 'completed', 'stopped', etc."},
            {"Resource": "MedicationRequest", "Field": "intent", "Cardinality": "1..1", "Notes": "'order' for a real prescription."},
            {"Resource": "MedicationRequest", "Field": "medication[x]", "Cardinality": "1..1", "Notes": "Inline RxNorm code or a reference to a Medication resource."},
            {"Resource": "MedicationRequest", "Field": "subject", "Cardinality": "1..1", "Notes": "Reference to Patient."},
            {"Resource": "Encounter", "Field": "status", "Cardinality": "1..1", "Notes": "'planned', 'in-progress', 'finished', etc."},
            {"Resource": "Encounter", "Field": "class", "Cardinality": "1..1", "Notes": "Coding from v3 ActCode: 'AMB' for ambulatory, 'IMP' for inpatient."},
        ]
    )
    min_fields
    return (min_fields,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The smallest *technically valid* Observation is genuinely just:

        ```json
        {
          "resourceType": "Observation",
          "status": "final",
          "code": {"coding": [{"system": "http://loinc.org", "code": "1988-5"}]}
        }
        ```

        Anything beyond that adds content, not structure. To be *clinically useful*, you also want `subject`, `effectiveDateTime`, and `valueQuantity`. To be *profile-conformant* (the next idea), you want a few more.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 2. Profiles are constrained base resources.

        The base spec for Observation has to serve a CRP result, a blood pressure reading, a smoking-status assertion, and a 6-minute walk test. It's intentionally permissive: the union of what every Observation might need.

        A **profile** is a constrained version of a base resource for a specific use case. The US Core Observation Lab profile says, on top of the base Observation spec:

        - `status` must be present (already required by the base; re-confirmed).
        - `category` must include the `laboratory` coding (no longer optional in this profile).
        - `code` must come from a specific value set (LOINC lab codes).
        - `subject` must be present and reference a US Core Patient.
        - `effectiveDateTime` or `effectivePeriod` must be present.
        - `valueQuantity` (or another value variant) must be present. No value-less lab Observations.

        A receiver that "supports US Core Observation Lab" can rely on those guarantees. Without the profile, the receiver would have to check every field defensively. With it, the structure is fixed.

        In a resource, conformance to a profile is declared via `meta.profile`:

        ```json
        {
          "resourceType": "Observation",
          "meta": {
            "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab"]
          },
          ...
        }
        ```

        Most US clinical FHIR traffic conforms to US Core profiles. Other implementation guides (mCODE for oncology, IPS for international patient summary, CARIN BB for payer data) define their own profiles. Track 4 walks profiles and implementation guides systematically.
        """
    )
    return


@app.cell
def _(mo):
    ms_quiz = mo.ui.radio(
        options=[
            "The sender must include this field in every resource conforming to the profile.",
            "If the sender chooses to include this field, the receiver must know what to do with it.",
            "The field is more important than other fields in the resource.",
            "The field's cardinality is forced to 1..1 by the profile.",
        ],
        label=(
            "US Core Patient marks the `race` extension as **must-support**. "
            "Which of these correctly describes what must-support means?"
        ),
    )
    ms_quiz
    return (ms_quiz,)


@app.cell
def _(mo, ms_quiz):
    if ms_quiz.value is None:
        _ms_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif ms_quiz.value.startswith("If the sender chooses"):
        _ms_response = mo.callout(
            mo.md(
                "**Right.** Must-support is a **contract on the receiver**, not on the sender. "
                "A US-Core-conforming sender doesn't have to send race (it's still optional; the extension's cardinality stays `0..1`). "
                "But a US-Core-conforming receiver that gets a Patient with race included must know what to do with it: display it, store it, not silently drop it. "
                "If the receiver silently drops the race field, the receiver is non-conformant.\n\n"
                "The most common misreading is exactly the option you didn't pick (\"the sender must include it\"). Must-support and cardinality are separate axes."
            ),
            kind="success",
        )
    elif ms_quiz.value.startswith("The sender must"):
        _ms_response = mo.callout(
            mo.md(
                "**This is the most common misreading.** Must-support does *not* force the sender to include the field. It applies to the receiver: if the field is present, the receiver must handle it. Cardinality (`0..1`, `1..1`, etc.) is what determines whether the sender must include the field; must-support is a separate axis."
            ),
            kind="warn",
        )
    elif ms_quiz.value.startswith("The field is more important"):
        _ms_response = mo.callout(
            mo.md(
                "**No.** All FHIR fields are meaningful. Must-support is a structural guarantee about receiver handling, not a comment on clinical importance. Many clinically critical fields are not marked must-support; many less-critical fields are."
            ),
            kind="warn",
        )
    else:
        _ms_response = mo.callout(
            mo.md(
                "**No.** Cardinality and must-support are separate. The cardinality of `Patient.extension:race` in US Core remains `0..1`; must-support adds a receiver-side obligation without changing how often the field is required."
            ),
            kind="warn",
        )
    _ms_response
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 3. Extensions: adding what the base resource doesn't have.

        FHIR's base resources stay minimal so they generalize internationally. When a US-specific concept like race or ethnicity needs to be attached to a Patient, the base spec doesn't have a field for it, and FHIR's answer is the **extension**.

        An extension is an object in the `extension[]` array of any resource. It has a `url` naming what the extension is (the canonical identifier of its definition) and a `value[x]` (or a nested `extension[]` for complex extensions). Below is the US Core race extension on a Patient resource:

        ```json
        "extension": [{
          "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
          "extension": [
            {
              "url": "ombCategory",
              "valueCoding": {
                "system": "urn:oid:2.16.840.1.113883.6.238",
                "code": "2106-3",
                "display": "White"
              }
            },
            {
              "url": "text",
              "valueString": "White"
            }
          ]
        }]
        ```

        This is a *complex* extension: the outer extension has no value, but contains an inner `extension[]` array. The inner extensions hold the actual data.

        Two rules.

        - **Don't invent extensions casually.** Reusing existing extensions (from US Core, mCODE, the FHIR core, etc.) is almost always better than minting new ones. Custom extensions are how implementations end up incompatible.
        - **Read the URL as the source of truth.** The `url` tells you exactly which extension definition is in play. If you don't recognize the URL, look it up before acting on the value.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 4. The `$validate` endpoint.

        A FHIR server exposes a special endpoint called `$validate` that takes a resource and reports what's wrong with it.

        ```
        POST <base>/<ResourceType>/$validate
        Content-Type: application/fhir+json

        {resource as JSON body}
        ```

        The response is an **OperationOutcome** resource: a list of `issue[]` entries, each with a `severity` (`fatal`, `error`, `warning`, `information`), a `code` categorizing the issue, and a `diagnostics` string describing what's wrong.

        Below are two real OperationOutcomes cached from `hapi.fhir.org/baseR4/Observation/$validate`. The first one validated a well-formed Observation; the second one validated the same Observation with `status` and `code` removed (the two cardinality-1 fields you can't skip).
        """
    )
    return


@app.cell
def _(load_cached, mo, pd):
    _clean = load_cached("validate-clean-observation.json")
    _broken = load_cached("validate-broken-observation.json")

    def _format(outcome):
        return pd.DataFrame(
            [
                {
                    "#": i + 1,
                    "Severity": iss.get("severity"),
                    "Code": iss.get("code"),
                    "Location": (iss.get("expression") or [iss.get("location", "")])[0] if (iss.get("expression") or iss.get("location")) else "",
                    "Diagnostics": (iss.get("diagnostics") or "")[:200],
                }
                for i, iss in enumerate(outcome.get("issue", []))
            ]
        )

    _clean_df = _format(_clean)
    _broken_df = _format(_broken)
    mo.vstack(
        [
            mo.md(
                "**A well-formed Observation, posted to hapi.fhir.org/$validate.**\n\n"
                "Four issues come back. None of them are about the shape of the resource being wrong; they're all about what the server can verify and what it recommends."
            ),
            mo.ui.table(_clean_df, selection=None),
            mo.callout(
                mo.md(
                    "Reading the four issues:\n\n"
                    "- **Warning, code system unknown**: hapi.fhir.org doesn't have LOINC fully loaded, so it can't verify that `1988-5` is a real LOINC code. The resource is still valid; the validator just can't go that deep.\n"
                    "- **Error, unable to resolve reference**: Ms. Reyes doesn't exist on hapi.fhir.org. The reference is syntactically correct, but the referenced Patient is missing. In a production system where she did exist, this would not appear.\n"
                    "- **Warning, dom-6 constraint**: FHIR's base DomainResource spec recommends every resource carry a human-readable narrative (`text.div`). Most production resources skip it; the spec flags it as a best-practice recommendation.\n"
                    "- **Warning, observations should have a performer**: another FHIR best-practice recommendation. The resource is still valid without one.\n\n"
                    "The lesson: a 'clean' resource by spec still gets flags from `$validate`. Read the issues by severity. Errors and fatals are the things you have to fix; warnings tell you what a careful receiver would still complain about."
                ),
                kind="info",
            ),
            mo.md(
                "\n---\n\n**The same Observation with `status` and `code` removed.**\n\n"
                "Now the validator has real complaints."
            ),
            mo.ui.table(_broken_df, selection=None),
            mo.callout(
                mo.md(
                    "Two of these are the cardinality errors we expected: `status` and `code` are required (`1..1`) on Observation, and neither was sent. The other three are the same warnings from before plus the same unresolved-reference issue.\n\n"
                    "When you're reading an OperationOutcome, do it in two passes. Pass 1: find the `error` and `fatal` issues. Those are the things that prevent the resource from being valid. Pass 2: read the warnings to understand what a careful receiver would still complain about."
                ),
                kind="warn",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone: author Ms. Reyes's next follow-up visit.

        Ms. Reyes has a follow-up appointment with Dr. Bennett scheduled. The visit goes well: her DAS28 is stable in the low-activity range, vitals look good. You're going to author the FHIR resources that capture the visit. Specifically:

        - An **Encounter** for the visit itself.
        - An **Observation** for CRP.
        - An **Observation** for ESR.
        - An **Observation** for DAS28-CRP (calculated from her TJC, SJC, CRP, and patient global VAS).

        Enter the clinical inputs below. The notebook constructs the resources from your inputs, shows you the resulting JSON, and lets you `$validate` each one against hapi.fhir.org with a button click.
        """
    )
    return


@app.cell
def _(mo):
    visit_date = mo.ui.date(value="2026-08-15", label="Visit date")
    tjc = mo.ui.slider(start=0, stop=28, step=1, value=2, label="Tender joint count (28)", show_value=True)
    sjc = mo.ui.slider(start=0, stop=28, step=1, value=1, label="Swollen joint count (28)", show_value=True)
    crp = mo.ui.slider(start=0.5, stop=100.0, step=0.5, value=14.2, label="CRP (mg/L)", show_value=True)
    esr = mo.ui.slider(start=1, stop=140, step=1, value=24, label="ESR (mm/h)", show_value=True)
    pga = mo.ui.slider(start=0, stop=100, step=1, value=28, label="Patient global VAS (0-100 mm)", show_value=True)
    mo.vstack([visit_date, tjc, sjc, crp, esr, pga])
    return crp, esr, pga, sjc, tjc, visit_date


@app.cell
def _(crp, math, mo, pga, sjc, tjc):
    _das28 = (
        0.56 * math.sqrt(tjc.value)
        + 0.28 * math.sqrt(sjc.value)
        + 0.36 * math.log(crp.value + 1)
        + 0.014 * pga.value
        + 0.96
    )
    das28_value = round(_das28, 2)
    if das28_value < 2.6:
        das28_interp = "Remission"
    elif das28_value <= 3.2:
        das28_interp = "Low disease activity"
    elif das28_value <= 5.1:
        das28_interp = "Moderate disease activity"
    else:
        das28_interp = "High disease activity"
    mo.callout(
        mo.md(
            f"**DAS28-CRP calculated:** {das28_value}. **EULAR interpretation:** {das28_interp}.\n\n"
            f"_From TJC = {tjc.value}, SJC = {sjc.value}, CRP = {crp.value} mg/L, PGA = {pga.value}._"
        ),
        kind="info",
    )
    return das28_interp, das28_value


@app.cell
def _(crp, das28_interp, das28_value, esr, json, mo, pga, sjc, tjc, visit_date):
    _visit_iso = f"{visit_date.value}T08:30:00-05:00"
    _visit_end_iso = f"{visit_date.value}T09:30:00-05:00"

    encounter = {
        "resourceType": "Encounter",
        "status": "finished",
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "AMB",
            "display": "ambulatory",
        },
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0004",
                        "code": "OUTPATIENT",
                        "display": "Outpatient",
                    }
                ],
                "text": "Rheumatology follow-up",
            }
        ],
        "subject": {"reference": "Patient/elena-reyes"},
        "participant": [{"individual": {"reference": "Practitioner/maya-bennett"}}],
        "period": {"start": _visit_iso, "end": _visit_end_iso},
        "reasonCode": [{"text": "Rheumatoid arthritis follow-up"}],
    }

    def _lab_obs(loinc, display, value, unit, ucum):
        _rng_high = 5 if loinc == "1988-5" else (20 if loinc == "4537-7" else None)
        _flag = "H" if (_rng_high is not None and value > _rng_high) else "N"
        _obs = {
            "resourceType": "Observation",
            "meta": {
                "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab"]
            },
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "laboratory",
                            "display": "Laboratory",
                        }
                    ]
                }
            ],
            "code": {
                "coding": [{"system": "http://loinc.org", "code": loinc, "display": display}],
                "text": display,
            },
            "subject": {"reference": "Patient/elena-reyes"},
            "encounter": {"reference": "Encounter/next-visit"},
            "effectiveDateTime": _visit_iso,
            "valueQuantity": {
                "value": value,
                "unit": unit,
                "system": "http://unitsofmeasure.org",
                "code": ucum,
            },
            "interpretation": [
                {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": _flag}]}
            ],
        }
        if _rng_high is not None:
            _obs["referenceRange"] = [{"low": {"value": 0, "unit": unit}, "high": {"value": _rng_high, "unit": unit}}]
        return _obs

    obs_crp = _lab_obs("1988-5", "C reactive protein [Mass/volume] in Serum or Plasma", crp.value, "mg/L", "mg/L")
    obs_esr = _lab_obs("4537-7", "Erythrocyte sedimentation rate", esr.value, "mm/h", "mm/h")
    obs_das28 = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "exam",
                        "display": "Exam",
                    }
                ]
            }
        ],
        "code": {
            "coding": [{"system": "http://loinc.org", "code": "76374-2", "display": "DAS28-CRP score"}],
            "text": "DAS28-CRP composite disease activity score",
        },
        "subject": {"reference": "Patient/elena-reyes"},
        "encounter": {"reference": "Encounter/next-visit"},
        "effectiveDateTime": _visit_iso,
        "valueQuantity": {
            "value": das28_value,
            "unit": "score",
            "system": "http://unitsofmeasure.org",
            "code": "{score}",
        },
        "note": [
            {"text": f"{das28_interp}. Calculated from TJC {tjc.value}, SJC {sjc.value}, CRP {crp.value} mg/L, patient global VAS {pga.value}."}
        ],
    }

    resources_constructed = {
        "Encounter": encounter,
        "CRP Observation": obs_crp,
        "ESR Observation": obs_esr,
        "DAS28-CRP Observation": obs_das28,
    }

    _previews = []
    for _name, _r in resources_constructed.items():
        _previews.append(mo.md(f"**{_name}.**\n\n```json\n{json.dumps(_r, indent=2)}\n```"))
    mo.vstack(
        [
            mo.md(
                "**The four resources constructed from your inputs.** Each one is shaped to be a valid FHIR R4 resource; the lab Observations declare conformance to US Core Observation Lab via `meta.profile`. References point at Ms. Reyes and Dr. Bennett by relative reference."
            ),
            mo.accordion({k: v for k, v in zip(resources_constructed.keys(), _previews)}),
        ]
    )
    return encounter, obs_crp, obs_das28, obs_esr, resources_constructed


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Validate against hapi.fhir.org.

        Each constructed resource gets sent to `https://hapi.fhir.org/baseR4/<ResourceType>/$validate` via `POST`. Click the button to fire the calls. Expect the same flavor of OperationOutcome we saw earlier: a couple of warnings about external code systems and missing narrative, plus one error about not being able to resolve `Patient/elena-reyes` (because she doesn't exist on hapi.fhir.org). The shape of the resources themselves should validate clean.

        First click is a live network call. The button re-fires on each click so you can revalidate after changing inputs above.
        """
    )
    return


@app.cell
def _(mo):
    validate_button = mo.ui.run_button(label="Send the four resources to $validate")
    validate_button
    return (validate_button,)


@app.cell
def _(mo, pd, post_validate, resources_constructed, validate_button):
    mo.stop(
        not validate_button.value,
        mo.md("_Click the button above to send the resources to hapi.fhir.org for validation. (Live network call.)_"),
    )

    _all_issues = []
    for _name, _resource in resources_constructed.items():
        _outcome = post_validate(_resource)
        for _issue in _outcome.get("issue", []):
            _all_issues.append(
                {
                    "Resource": _name,
                    "Severity": _issue.get("severity"),
                    "Code": _issue.get("code"),
                    "Location": (_issue.get("expression") or [_issue.get("location", "")])[0]
                    if (_issue.get("expression") or _issue.get("location")) else "",
                    "Diagnostics": (_issue.get("diagnostics") or "")[:200],
                }
            )
    _validation_df = pd.DataFrame(_all_issues) if _all_issues else pd.DataFrame(
        [{"Resource": "(no issues)", "Severity": "", "Code": "", "Location": "", "Diagnostics": ""}]
    )

    _errors = sum(1 for i in _all_issues if i["Severity"] in ("error", "fatal"))
    _warnings = sum(1 for i in _all_issues if i["Severity"] == "warning")
    _summary = f"**{len(_all_issues)} issues across the four resources.** {_errors} errors/fatal, {_warnings} warnings."

    mo.vstack(
        [
            mo.md(_summary),
            mo.ui.table(_validation_df, selection=None, pagination=True, page_size=20),
            mo.callout(
                mo.md(
                    "If most of your errors are 'Unable to resolve resource with reference Patient/elena-reyes' or 'Practitioner/maya-bennett', "
                    "that's the validator complaining that those resources don't exist on hapi.fhir.org. The shape of your resources is fine; the references just point at things hapi doesn't have. "
                    "In a system where Ms. Reyes's Patient and Dr. Bennett's Practitioner resources had already been POSTed (the prerequisite for a real production deployment), those errors would not appear."
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
        ## Assemble the transaction Bundle.

        Real systems usually POST a visit's worth of resources together, as a **transaction bundle**. The Bundle has `type: "transaction"`, and each entry carries a `request` object describing the operation to apply. The server applies all of them atomically: either every entry succeeds or none of them do.

        Below is the transaction Bundle that would POST the four resources you just authored.
        """
    )
    return


@app.cell
def _(encounter, json, mo, obs_crp, obs_das28, obs_esr):
    _entries = [
        {"resource": encounter, "request": {"method": "POST", "url": "Encounter"}},
        {"resource": obs_crp, "request": {"method": "POST", "url": "Observation"}},
        {"resource": obs_esr, "request": {"method": "POST", "url": "Observation"}},
        {"resource": obs_das28, "request": {"method": "POST", "url": "Observation"}},
    ]
    transaction_bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": _entries,
    }
    mo.vstack(
        [
            mo.md(
                f"**Transaction Bundle with {len(_entries)} entries.** To actually apply it, your code would `POST` this Bundle to `https://hapi.fhir.org/baseR4/` (root URL, no resource type). The server returns a `transaction-response` Bundle with one entry per request, including the new server-assigned IDs and the `Location` headers for each created resource."
            ),
            mo.accordion(
                {
                    "Show the full transaction Bundle JSON": mo.md(
                        f"```json\n{json.dumps(transaction_bundle, indent=2)[:6000]}\n... (truncated if longer)\n```"
                    )
                }
            ),
        ]
    )
    return (transaction_bundle,)


@app.cell
def _(mo):
    _reflection = mo.ui.text_area(
        placeholder="A few sentences. Think about who maintains the profiles, how a multi-system rollout deals with vocabulary mismatches, what changes when you write at production scale.",
        rows=5,
        full_width=True,
        label=(
            "Imagine you're a clinical informatics lead at a 600-bed hospital starting a new FHIR integration with an outside specialty group. "
            "Both organizations claim to support US Core. What would you actually do to make sure their resources validate against your endpoint and vice versa? "
            "(No reveal. The writing is the work.)"
        ),
    )
    mo.vstack(
        [
            _reflection,
            mo.callout(
                mo.md(
                    "_No answer key. Some moves worth at least having on your list: "
                    "(1) ask for sample resources from their system and run them through your validator before exchanging real data; "
                    "(2) confirm which US Core *version* each side uses (US Core has minor-version differences that bite); "
                    "(3) map your respective local code sets to the US Core required value sets and document the deltas; "
                    "(4) agree on what extensions are in use and whether both sides support them; "
                    "(5) write down which fields are must-support on each side and what 'support' means concretely (display, store, ignore-with-no-loss); "
                    "(6) build a small bidirectional test bundle and validate it end to end before going to production._"
                ),
                kind="neutral",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - You put four ideas in place for authoring FHIR: the **minimum required fields** per resource type (small, set by cardinality on the spec page); **profiles** as constrained base resources (US Core Observation Lab as the worked example); **must-support** as a contract on the receiver (not the sender); and **extensions** as the formal mechanism for adding data the base spec doesn't have.
        - You read two real OperationOutcomes from hapi.fhir.org's `$validate` and learned the two-pass reading (errors first, warnings second).
        - You authored four resources for Ms. Reyes's next follow-up visit (Encounter, CRP, ESR, DAS28), validated them against hapi.fhir.org live, and assembled them into a transaction Bundle ready to POST.

        That is the write half of FHIR end to end. Reading (Tracks 1 and 2) plus writing (this track) plus validation (this track again) is most of what FHIR-fluent informatics work actually looks like.

        ## What's next.

        **Track 4: Implementation guides.** Profiles in detail. The StructureDefinition resource that backs every profile. mCODE as a worked example. Portability vs interoperability returned-to. Reading a gap analysis. The track-level capstone is a one-page gap analysis of US Core for rheumatology: which fields your work actually needs that US Core doesn't require, and how an IG author would close those gaps.
        """
    )
    return


if __name__ == "__main__":
    app.run()
