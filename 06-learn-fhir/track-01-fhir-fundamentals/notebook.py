"""Track 1: FHIR fundamentals.

Resources, references, bundles, terminology, and search parameters,
walked on Ms. Elena Reyes's actual FHIR R4 bundle. No FHIR writing
yet (that's Track 3). The capstone is a guided read: six clinical
questions answered by navigating her bundle, then synthesized into a
five-to-seven-sentence clinical summary.

Reads the bundle from `patients/elena-reyes/fhir-bundle.json` via
the course-root `patients/` symlink to `../start-here/patients/`.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import sys
    from collections import Counter
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    # Absolute site path where this notebook's WASM export lives. Used only
    # in the Pyodide branch below; `pyodide.http.open_url` resolves a
    # leading-slash path against the page origin, which works identically in
    # the main thread and in the marimo worker. Update this if the notebook
    # is renamed or the site is deployed under a subpath.
    _WASM_DATA_BASE = "/06-learn-fhir/track-01-fhir-fundamentals/app"

    def load_data_json(*parts):
        """Read a JSON file alongside this notebook. Works locally and in WASM.

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

    bundle = load_data_json("cache", "fhir-bundle.json")

    entries = bundle["entry"]
    resources = [e["resource"] for e in entries]

    def by_type(resource_type):
        return [r for r in resources if r["resourceType"] == resource_type]

    def by_id(resource_id):
        for r in resources:
            if r.get("id") == resource_id:
                return r
        return None

    type_counts = Counter(r["resourceType"] for r in resources)

    type_descriptions = {
        "Patient": "The person. Demographics, contact info, identifiers.",
        "Practitioner": "A clinician or other healthcare professional.",
        "Organization": "A clinic, hospital, lab, or other healthcare entity.",
        "Condition": "A diagnosis, problem, or clinical concern.",
        "MedicationStatement": "A record that a patient is (or was) taking a medication.",
        "AllergyIntolerance": "A patient's allergy or intolerance.",
        "Encounter": "A clinical visit or interaction.",
        "Observation": "Measurements and assertions: labs, vitals, scores, exam findings.",
        "Immunization": "A vaccine administration event.",
    }

    return (
        by_id,
        by_type,
        bundle,
        entries,
        json,
        mo,
        pd,
        resources,
        type_counts,
        type_descriptions,
    )


@app.cell
def _(mo):
    # Socratic helpers inlined from shared/socratic.py so the WASM export is
    # self-contained. Pyodide cannot import sibling modules from the source
    # tree, so the live-site export needs the helpers defined in the notebook
    # itself. Mirrors the API of start-here/shared/socratic.py.

    def commit_text(prompt, *, min_chars=40):
        widget = mo.ui.text_area(
            label=prompt,
            rows=6,
            full_width=True,
            placeholder="Take a few sentences. The reveal won't unlock until you do.",
        )

        def _ready():
            value = widget.value or ""
            return len(value.strip()) >= min_chars

        return widget, _ready

    def reveal(learner_value, ideal_answer, *, learner_label="Your answer"):
        learner_display = learner_value if learner_value else "_(no answer yet)_"
        return mo.hstack(
            [
                mo.callout(
                    mo.vstack(
                        [
                            mo.md(f"**{learner_label}**"),
                            mo.md(str(learner_display)),
                        ]
                    ),
                    kind="neutral",
                ),
                mo.callout(
                    mo.vstack(
                        [
                            mo.md("**How we'd think through this**"),
                            mo.md(ideal_answer),
                        ]
                    ),
                    kind="success",
                ),
            ],
            widths="equal",
        )

    return commit_text, reveal


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 1: FHIR fundamentals

        ## Ms. Reyes is being seen by you for the first time.

        She is coming in this afternoon for a second-opinion appointment after a move from another state. The transferring rheumatologist's office sent her record this morning as a FHIR Bundle. It's the digital version of a sealed envelope with her chart inside: one JSON file, holding every resource that describes her care up to today. You have an hour before she arrives.

        Open it. Read it. Build a picture of who she is, what she has, what she's on, and where she's been. That is the work of this track, and the capstone at the end is exactly that exercise written down.
        """
    )
    return


@app.cell
def _(bundle, mo):
    mo.md(
        rf"""
        ## What's actually in the envelope.

        The top-level Bundle looks like this, before we crack open any of the resources inside it:

        ```json
        {{
          "resourceType": "{bundle["resourceType"]}",
          "id":           "{bundle["id"]}",
          "type":         "{bundle["type"]}",
          "meta": {{
            "lastUpdated": "{bundle["meta"]["lastUpdated"]}",
            "tag": [{{"code": "{bundle["meta"]["tag"][0]["code"]}", "display": "synthetic teaching data"}}]
          }},
          "entry": [ ... {len(bundle["entry"])} entries ... ]
        }}
        ```

        Three things to notice.

        - The Bundle itself is a resource. It has a `resourceType` (`Bundle`), an `id`, and a `meta` block with administrative metadata. The same shape applies to every FHIR resource.
        - The Bundle's own `type` is `collection`. That means it is a snapshot: here are these resources together, no inherent operations to apply. (We'll come back to the other bundle types in a moment.)
        - The actual clinical content lives in `entry[]`, the array at the bottom. Each entry holds one resource. Ms. Reyes's bundle has {len(bundle["entry"])} of them.

        Before we look at any one resource in detail, it's worth seeing what kinds of resources are even in here.
        """
    )
    return


@app.cell
def _(mo, pd, type_counts, type_descriptions):
    type_table = pd.DataFrame(
        [
            {
                "Resource type": rt,
                "Count": n,
                "What it represents": type_descriptions.get(rt, rt),
            }
            for rt, n in sorted(type_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ]
    )
    mo.vstack(
        [
            mo.md("Entries in Ms. Reyes's bundle, grouped by resource type:"),
            mo.ui.table(type_table, selection=None),
            mo.callout(
                mo.md(
                    "Nine distinct resource types across seventeen entries. That's a reasonably-shaped chart for a chronic outpatient: one Patient (her), one Practitioner (her rheumatologist), one Organization (the clinic), two Conditions (her active problem list), three MedicationStatements (her current biologic regimen), one AllergyIntolerance, one Encounter, six Observations (her labs plus DAS28 plus a BP), and one Immunization.\n\n"
                    "For context: FHIR R4 defines around 150 resource types. About twenty cover the workflows most clinicians touch every day. The other 130 are for specialized use cases (workflow, financial, research, public health). You only meet a resource type when you need it."
                ),
                kind="info",
            ),
        ]
    )
    return (type_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 1. A resource is a unit of clinical data.

        Every entry in the bundle is one **resource**: a single piece of clinical information, structured according to a specification published by HL7. A Patient resource follows the Patient specification. An Observation resource follows the Observation specification. The fields inside depend on which resource type it is.

        Three things every resource has:

        - **A `resourceType`.** Names what kind of thing it is.
        - **An `id`.** A stable identifier within the system that produced or stores it.
        - **The fields its type defines.** Patient has `name`, `gender`, `birthDate`. Observation has `code`, `value`, `effectiveDateTime`. MedicationStatement has `medicationCodeableConcept`, `status`, `dosage`.

        The Patient resource for Ms. Reyes is the place to start: every other resource in her bundle points back at it.
        """
    )
    return


@app.cell
def _(by_type, json, mo):
    patient = by_type("Patient")[0]
    pretty_patient = json.dumps(patient, indent=2)
    mo.vstack(
        [
            mo.md("**The Patient resource for Ms. Reyes (full):**"),
            mo.md(f"```json\n{pretty_patient}\n```"),
        ]
    )
    return patient, pretty_patient


@app.cell
def _(mo):
    mo.md(
        r"""
        Walk through it once with the field meanings.

        - **`resourceType`: `"Patient"`.** This is a Patient resource. Every Patient anywhere in FHIR R4 has this same outer shape.
        - **`id`: `"elena-reyes"`.** The stable identifier for this resource within the system that produced it. Other resources in this bundle reference this Patient by id.
        - **`meta.profile`** declares that this Patient conforms to the US Core Patient profile, an implementation guide we'll meet in Track 4. Profiles add must-support requirements on top of the base spec.
        - **`identifier[]`.** External identifiers, each tagged with a `type` (here `MR` for Medical Record Number) and a `system` (the URI of the assigning authority). Patients often have several: MRN, SSN, member numbers. Each one lives in this array.
        - **`name[]`.** The patient's name(s). Always an array, even when there's only one (FHIR is unflinching about this; it lets a patient have a maiden name and a current name and a preferred name without changing shape). `family` and `given` are split; `given` is itself an array because middle names are common.
        - **`gender`.** One of `male`, `female`, `other`, `unknown`. Administrative, not biological. Sex-at-birth and gender identity are separate concepts in US Core extensions.
        - **`birthDate`.** ISO date string `YYYY-MM-DD`. No time zone. The patient's birth date.
        - **`address[]`.** Postal addresses. Each has `use` (`home`, `work`, etc.), `line[]` (street lines), `city`, `state`, `postalCode`, `country`.
        - **`telecom[]`.** Phones, emails, fax numbers. Each entry names a `system` (phone / email / fax) and a `value`.
        - **`communication[]`.** Languages, ordered by preference. The `preferred: true` flag marks the patient's primary language. Ms. Reyes prefers English; she also speaks Spanish. This is the field a SMART app uses to decide which language to render UI in.
        - **`extension[]`.** US Core race and ethnicity, attached via FHIR extensions (the formal mechanism for adding data that the base spec doesn't define). The OMB-category codes are inside the extensions, and the same race/ethnicity slot can hold detailed codes alongside the rolled-up category. Extensions are how implementation guides like US Core add jurisdiction-specific data without modifying the base Patient resource.

        That's the Patient resource. Every other Patient in FHIR has the same shape; the *content* differs but the *structure* doesn't. That uniformity is what makes the rest of the course possible.
        """
    )
    return


@app.cell
def _(mo):
    spotter = mo.ui.multiselect(
        options=[
            "Snippet A is a `Patient` (it has `birthDate`, `name`, `gender`)",
            "Snippet A is an `Observation` (it has `valueQuantity` and `code`)",
            "Snippet A is a `Condition` (it has `clinicalStatus` and `code`)",
            "Snippet B is a `MedicationStatement` (it has `medicationCodeableConcept` and `dosage`)",
            "Snippet B is an `Observation` (it has `valueQuantity` and `code`)",
            "Snippet B is a `Patient` (it has `subject` and `effectiveDateTime`)",
            "Snippet C is an `AllergyIntolerance` (it has `reaction[]` and `criticality`)",
            "Snippet C is a `Condition` (it has `verificationStatus` and `code`)",
            "Snippet C is an `Observation` (it has `code` and `valueQuantity`)",
        ],
        label="Which resource types are these three snippets? Pick all the correct identifications.",
    )
    mo.vstack(
        [
            mo.md(
                r"""
**Spot the resource type.** Three snippets, each from a different resource. Don't look at `resourceType` (we've redacted it). Look at the *shape* and the *fields*, the way you'd read an unfamiliar chart structure.

**Snippet A.**
```json
{
  "resourceType": "...",
  "code": {"coding": [{"system": "http://loinc.org", "code": "1988-5"}]},
  "valueQuantity": {"value": 21.4, "unit": "mg/L"},
  "effectiveDateTime": "2026-02-10T08:30:00-05:00",
  "subject": {"reference": "Patient/elena-reyes"},
  "status": "final"
}
```

**Snippet B.**
```json
{
  "resourceType": "...",
  "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "327361"}]},
  "subject": {"reference": "Patient/elena-reyes"},
  "status": "active",
  "dosage": [{"text": "40 mg SC every 14 days"}]
}
```

**Snippet C.**
```json
{
  "resourceType": "...",
  "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
  "verificationStatus": {"coding": [{"code": "confirmed"}]},
  "code": {"coding": [{"system": "http://snomed.info/sct", "code": "239791008"}]},
  "subject": {"reference": "Patient/elena-reyes"}
}
```
"""
            ),
            spotter,
        ]
    )
    return (spotter,)


@app.cell
def _(mo, spotter):
    chosen = set(spotter.value or [])
    correct = {
        "Snippet A is an `Observation` (it has `valueQuantity` and `code`)",
        "Snippet B is a `MedicationStatement` (it has `medicationCodeableConcept` and `dosage`)",
        "Snippet C is a `Condition` (it has `verificationStatus` and `code`)",
    }
    if not chosen:
        spotter_response = mo.callout(
            mo.md("_Pick the three correct identifications. You can change your mind after seeing feedback._"),
            kind="neutral",
        )
    elif chosen == correct:
        spotter_response = mo.callout(
            mo.md(
                "**All three right.**\n\n"
                "- Snippet A is an **Observation**. The combination of `code` (LOINC 1988-5, which is CRP), `valueQuantity`, `effectiveDateTime`, and `status: final` is unmistakable.\n"
                "- Snippet B is a **MedicationStatement**. `medicationCodeableConcept` and `dosage` are MedicationStatement-shaped fields. The RxNorm code 327361 is adalimumab 40 mg/0.8 mL injection.\n"
                "- Snippet C is a **Condition**. `clinicalStatus` and `verificationStatus` are Condition-defining fields. SNOMED 239791008 is seropositive rheumatoid arthritis.\n\n"
                "Notice what gave each one away: not the data values, but the **field names**. FHIR uses different field names on different resource types deliberately, exactly so that you can tell what you're looking at at a glance. `valueQuantity` is for Observations. `medicationCodeableConcept` is for things-about-medications. `clinicalStatus` and `verificationStatus` are for Conditions."
            ),
            kind="success",
        )
    else:
        spotter_response = mo.callout(
            mo.md(
                "**Close.** The correct identifications:\n\n"
                "- Snippet A is an **Observation**. `valueQuantity` + `code` + `effectiveDateTime` is the Observation shape. LOINC 1988-5 is CRP.\n"
                "- Snippet B is a **MedicationStatement**. `medicationCodeableConcept` + `dosage` is its signature. RxNorm 327361 is adalimumab 40 mg pen.\n"
                "- Snippet C is a **Condition**. `clinicalStatus` + `verificationStatus` + `code` is the Condition shape. SNOMED 239791008 is seropositive RA.\n\n"
                "The trick is to read the **field names**, not the data values. FHIR uses different field names on different resource types so you can tell them apart at a glance."
            ),
            kind="warn",
        )
    spotter_response
    return chosen, correct, spotter_response


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 2. References connect resources.

        Almost every clinical resource is *about* a Patient. The CRP belongs to Ms. Reyes. The adalimumab MedicationStatement belongs to Ms. Reyes. The penicillin AllergyIntolerance belongs to Ms. Reyes. The Encounter from 2022 belongs to Ms. Reyes.

        Each of those resources says so with a **reference**: a small object containing a `reference` field that names the resource being pointed at. The CRP Observation's `subject` field looks like this:

        ```json
        "subject": { "reference": "urn:uuid:patient-elena-reyes" }
        ```

        References come in three flavors, all saying the same thing ("I am about that resource over there"):

        - **Relative reference.** `Patient/elena-reyes`. The thing with id `elena-reyes` of type `Patient` on the same server as the resource you're reading. This is what FHIR servers return.
        - **Absolute URL.** `https://hapi.fhir.org/baseR4/Patient/elena-reyes`. The full address of the resource elsewhere on the web.
        - **`urn:uuid:` reference.** What Ms. Reyes's bundle uses. The reference matches the `fullUrl` of another entry in the same bundle. Used when the bundle is a self-contained snapshot whose resources don't yet have permanent URLs.

        All three flavors are pointers. A receiver reading any of them follows the pointer to find the referenced resource.

        Below is the CRP Observation from 2026 in Ms. Reyes's bundle, alongside the Patient resource its `subject` points at. The reference is the bridge.
        """
    )
    return


@app.cell
def _(by_id, by_type, json, mo):
    crp_obs = by_id("obs-crp-20260210")
    patient_full = by_type("Patient")[0]
    crp_pretty = json.dumps(crp_obs, indent=2)
    patient_minimal = {
        "resourceType": "Patient",
        "id": patient_full["id"],
        "name": patient_full["name"],
        "gender": patient_full["gender"],
        "birthDate": patient_full["birthDate"],
    }
    patient_pretty = json.dumps(patient_minimal, indent=2)
    crp_panel = mo.callout(
        mo.vstack(
            [
                mo.md("**The CRP Observation from 2026:**"),
                mo.md(f"```json\n{crp_pretty}\n```"),
                mo.md("Notice `subject` near the bottom. That's the pointer."),
            ]
        ),
        kind="neutral",
    )
    patient_panel = mo.callout(
        mo.vstack(
            [
                mo.md("**The Patient it points at (trimmed for display):**"),
                mo.md(f"```json\n{patient_pretty}\n```"),
                mo.md("This is who the CRP belongs to. We got here by following the reference."),
            ]
        ),
        kind="info",
    )
    mo.hstack([crp_panel, patient_panel], widths="equal")
    return (
        crp_obs,
        crp_panel,
        crp_pretty,
        patient_full,
        patient_minimal,
        patient_panel,
        patient_pretty,
    )


@app.cell
def _(mo):
    ref_quiz = mo.ui.radio(
        options=[
            "It is about a different patient.",
            "It points at a resource the receiver may not have access to.",
            "It is the same kind of pointer, just written in a different style.",
            "It is invalid; FHIR references must use absolute URLs.",
        ],
        label=(
            "A FHIR server returns Ms. Reyes's CRP Observation, and the `subject` field reads:\n\n"
            "```json\n\"subject\": { \"reference\": \"Patient/elena-reyes\" }\n```\n\n"
            "Compare this to the bundle version above, which used `\"reference\": \"urn:uuid:patient-elena-reyes\"`. What does the difference mean?"
        ),
    )
    ref_quiz
    return (ref_quiz,)


@app.cell
def _(mo, ref_quiz):
    if ref_quiz.value is None:
        ref_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif ref_quiz.value.startswith("It is the same kind"):
        ref_response = mo.callout(
            mo.md(
                "**Right.** Both references say the same thing: this Observation is about Ms. Reyes. The two styles serve different contexts.\n\n"
                "`Patient/elena-reyes` is a **relative reference**. It's the style a FHIR server uses when handing back resources, because the server knows its own base URL and the receiver does too. Resolving the reference means appending `Patient/elena-reyes` to the server's base URL.\n\n"
                "`urn:uuid:patient-elena-reyes` is a **bundle-internal reference** using a UUID. It's the style a self-contained collection bundle uses, because the resources inside the bundle don't yet have permanent server URLs. The UUID matches the `fullUrl` of another entry in the same bundle. Resolving the reference means finding that entry in the bundle's `entry[]` array.\n\n"
                "Same pointer, different addressing scheme. The receiver code handles both with the same logic: 'find the resource this reference points at, by whichever resolution rule applies.'"
            ),
            kind="success",
        )
    elif ref_quiz.value.startswith("It is about a different"):
        ref_response = mo.callout(
            mo.md(
                "**No.** The id portion is `elena-reyes` in both cases. The patient is the same. The two strings are different *addressing schemes* for the same Patient resource, not pointers to different patients."
            ),
            kind="warn",
        )
    elif ref_quiz.value.startswith("It points at a resource"):
        ref_response = mo.callout(
            mo.md(
                "**No.** Both references are resolvable in their respective contexts. The server-returned relative reference is resolved against the server's base URL; the bundle's UUID reference is resolved within the bundle. Access concerns are a separate question (authorization, scoping); the references themselves are well-formed."
            ),
            kind="warn",
        )
    else:
        ref_response = mo.callout(
            mo.md(
                "**No.** FHIR explicitly supports three reference styles: relative (`Patient/elena-reyes`), absolute URL (`https://server/...`), and `urn:uuid:` for bundle-internal use. All three are valid. The spec page on References lists them and the resolution rules for each."
            ),
            kind="warn",
        )
    ref_response
    return (ref_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 3. A bundle is a container of resources.

        Ms. Reyes's bundle has `type: collection`. That's one of several bundle types, each meaning a different thing about how the contained resources should be interpreted.

        | Bundle `type` | What it means | When you'll see it |
        |---|---|---|
        | `collection` | A snapshot. "Here are these resources packaged together." No inherent operations to apply. | Records sent between systems; the synthetic bundle in this track. |
        | `searchset` | The result of a FHIR search query, with pagination info at the top of the bundle. | Every response when you ask a FHIR server to find resources. Track 2 lives here. |
        | `transaction` | A set of operations to apply atomically. Each entry specifies a method (POST/PUT/DELETE) and a target URL. Either all succeed or all fail. | When you write FHIR. Track 3 builds these. |
        | `batch` | Like `transaction`, but each operation is applied independently. Some can succeed while others fail. | Bulk write operations where partial success is acceptable. |
        | `document` | A signed, immutable clinical document, like a discharge summary. The first entry is always a `Composition` resource that names the structure. | The FHIR equivalent of a CDA document. Less common in everyday API work. |
        | `message` | A FHIR-shaped message exchange. The first entry is always a `MessageHeader`. | Workflow / event-driven exchanges. |
        | `history` | The version history of one resource. | When you ask a server for a resource's history. |

        For the rest of this track and Track 2, you'll mostly meet `collection` (this one) and `searchset` (what a server returns). The same outer shape applies to all of them: a top-level Bundle resource with a `type` and an `entry[]` array, each entry holding one resource.
        """
    )
    return


@app.cell
def _(mo):
    bundle_quiz = mo.ui.radio(
        options=[
            "`collection`. The server is sending you a snapshot of these resources.",
            "`transaction`. The server applied operations and is reporting the result.",
            "`searchset`. The server is responding to a search query with the matching resources.",
            "`document`. The server is sending you a signed clinical document.",
        ],
        label=(
            "You ran `GET /Observation?subject=Patient/elena-reyes&code=1988-5&_sort=-date&_count=5` on a FHIR server. "
            "The server responds with a Bundle containing two Observation entries plus pagination metadata. "
            "What `type` does the Bundle have?"
        ),
    )
    bundle_quiz
    return (bundle_quiz,)


@app.cell
def _(bundle_quiz, mo):
    if bundle_quiz.value is None:
        bundle_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif bundle_quiz.value.startswith("`searchset`"):
        bundle_response = mo.callout(
            mo.md(
                "**Right.** A FHIR server's response to any search is a Bundle of type `searchset`. The `total` field tells you how many matches existed; the `link[]` array contains pagination URLs (`self`, `next`, `previous`). Each entry's resource is one match, with a small `search` object attached that says whether the match is direct or pulled in via `_include`. You'll work with this shape directly in Track 2."
            ),
            kind="success",
        )
    elif bundle_quiz.value.startswith("`collection`"):
        bundle_response = mo.callout(
            mo.md(
                "**Close, but not for a search response.** A `collection` bundle is what you'd send if you were handing someone a packaged snapshot of resources (like Ms. Reyes's bundle in this track). A search response has its own dedicated type, `searchset`, because it carries paging information the server adds. The shape is similar; the semantics differ."
            ),
            kind="warn",
        )
    elif bundle_quiz.value.startswith("`transaction`"):
        bundle_response = mo.callout(
            mo.md(
                "**No.** `transaction` is what *you* would send to the server when you want it to apply multiple writes atomically. The server's response to a transaction is a `transaction-response` bundle, which is again a different type. For a search, the response type is `searchset`."
            ),
            kind="warn",
        )
    else:
        bundle_response = mo.callout(
            mo.md(
                "**No.** `document` is for signed clinical documents (the FHIR equivalent of CDAs), and starts with a Composition resource. A search response is `searchset`."
            ),
            kind="warn",
        )
    bundle_response
    return (bundle_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 4. Terminology lives in the slots, and the slot tells you the vocabulary.

        Almost every clinical fact in FHIR involves a code. The diagnosis on a Condition is a code. The test on an Observation is a code. The drug on a MedicationStatement is a code. The unit on a quantity is a code.

        FHIR doesn't define its own clinical vocabulary. It uses the existing standard vocabularies. The slot tells you which one to use, and the field always looks the same: a `coding` array, each entry an object with a `system` URI naming the vocabulary, a `code` value in that vocabulary, and a `display` string for humans.

        The canonical mapping, with the URIs you'll see on the wire:
        """
    )
    return


@app.cell
def _(pd):
    terminology = pd.DataFrame(
        [
            {"What's coded": "Lab test, vital sign, observation code",
             "Vocabulary": "LOINC", "URI you'll see": "http://loinc.org",
             "Example from Ms. Reyes": "CRP = 1988-5, ESR = 4537-7, DAS28-CRP = 76374-2, anti-CCP = 32218-7."},
            {"What's coded": "Clinical finding, problem, procedure, anatomic site",
             "Vocabulary": "SNOMED CT", "URI you'll see": "http://snomed.info/sct",
             "Example from Ms. Reyes": "Seropositive RA = 239791008. Skin rash = 271807003. Subcutaneous route = 34206005."},
            {"What's coded": "Medication",
             "Vocabulary": "RxNorm", "URI you'll see": "http://www.nlm.nih.gov/research/umls/rxnorm",
             "Example from Ms. Reyes": "Methotrexate 25mg/mL inj = 1156665. Adalimumab 40mg/0.8mL pen = 327361. Folic acid 1mg tab = 315966."},
            {"What's coded": "Unit of measure on a quantity",
             "Vocabulary": "UCUM", "URI you'll see": "http://unitsofmeasure.org",
             "Example from Ms. Reyes": "mg/L for CRP. mm/h for ESR. mmHg coded `mm[Hg]` for BP. mg for medication doses."},
            {"What's coded": "Billing-aligned diagnosis",
             "Vocabulary": "ICD-10-CM", "URI you'll see": "http://hl7.org/fhir/sid/icd-10-cm",
             "Example from Ms. Reyes": "RA = M05.79 (sent alongside the SNOMED code). Anemia of chronic disease = D63.8."},
            {"What's coded": "Vaccine",
             "Vocabulary": "CVX", "URI you'll see": "http://hl7.org/fhir/sid/cvx",
             "Example from Ms. Reyes": "Influenza, inactivated quadrivalent = 150."},
            {"What's coded": "Language",
             "Vocabulary": "BCP-47", "URI you'll see": "urn:ietf:bcp:47",
             "Example from Ms. Reyes": "English (US) = `en-US`. Spanish = `es`."},
            {"What's coded": "Race / ethnicity in US Core extensions",
             "Vocabulary": "CDC race & ethnicity (OMB)", "URI you'll see": "urn:oid:2.16.840.1.113883.6.238",
             "Example from Ms. Reyes": "White = 2106-3. Hispanic or Latino = 2135-2."},
            {"What's coded": "Resource status, clinical status, observation interpretation",
             "Vocabulary": "HL7 / FHIR-defined", "URI you'll see": "http://terminology.hl7.org/...",
             "Example from Ms. Reyes": "Active condition = `active`. High lab interpretation = `H`. Allergy clinical status = `active`."},
            {"What's coded": "Site-specific identifiers (MRNs, internal IDs)",
             "Vocabulary": "Local (site-defined)", "URI you'll see": "URIs the local site defines",
             "Example from Ms. Reyes": "MRN ER-001 uses the curriculum's example MRN system URI."},
        ]
    )
    terminology
    return (terminology,)


@app.cell
def _(mo):
    term_match = mo.ui.multiselect(
        options=[
            "A new lab result for ferritin → LOINC",
            "A new lab result for ferritin → SNOMED CT",
            "A problem-list entry of 'chronic kidney disease, stage 3' → SNOMED CT (with ICD-10 alongside)",
            "A problem-list entry of 'chronic kidney disease, stage 3' → RxNorm",
            "A new prescription for atorvastatin 40 mg → RxNorm",
            "A new prescription for atorvastatin 40 mg → LOINC",
            "The unit on a creatinine result (mg/dL) → UCUM",
            "The unit on a creatinine result (mg/dL) → RxNorm",
            "A flu vaccine administered today → CVX",
            "A flu vaccine administered today → SNOMED CT",
        ],
        label=(
            "For each clinical fact below, pick the appropriate primary vocabulary. (Multiple correct identifications; pick all that apply.)"
        ),
    )
    term_match
    return (term_match,)


@app.cell
def _(mo, term_match):
    term_chosen = set(term_match.value or [])
    term_correct = {
        "A new lab result for ferritin → LOINC",
        "A problem-list entry of 'chronic kidney disease, stage 3' → SNOMED CT (with ICD-10 alongside)",
        "A new prescription for atorvastatin 40 mg → RxNorm",
        "The unit on a creatinine result (mg/dL) → UCUM",
        "A flu vaccine administered today → CVX",
    }
    if not term_chosen:
        term_response = mo.callout(
            mo.md("_Pick the five correct matchups. The ten options pair each clinical fact with two plausible vocabularies; only one is right per fact._"),
            kind="neutral",
        )
    elif term_chosen == term_correct:
        term_response = mo.callout(
            mo.md(
                "**All five right.** The slot-to-vocabulary mapping is what makes coded fields in FHIR predictable:\n\n"
                "- **Labs (and most Observations) → LOINC.** Ferritin lives there.\n"
                "- **Problems, findings, procedures → SNOMED CT**, usually with **ICD-10 alongside** for billing alignment. CKD stage 3 is the standard problem-list example.\n"
                "- **Medications → RxNorm.** Atorvastatin 40 mg tablet has an RxNorm code.\n"
                "- **Units on quantities → UCUM.** mg/dL is `mg/dL` in UCUM.\n"
                "- **Vaccines → CVX.** Flu vaccines are CVX codes (150, 158, 161, etc., depending on formulation)."
            ),
            kind="success",
        )
    else:
        missing = term_correct - term_chosen
        wrong = term_chosen - term_correct
        parts = ["**Close.** Two reminders for the right slot-to-vocab map:"]
        if missing:
            parts.append("\nThese are correct and should be picked:")
            for m in sorted(missing):
                parts.append(f"\n- {m}")
        if wrong:
            parts.append("\nThese pair a fact with the wrong vocabulary:")
            for w in sorted(wrong):
                parts.append(f"\n- {w}")
        parts.append(
            "\n\nThe quick map: labs and observations use **LOINC**; problems and findings use **SNOMED CT** (with **ICD-10** for billing alignment); medications use **RxNorm**; units use **UCUM**; vaccines use **CVX**."
        )
        term_response = mo.callout(mo.md("".join(parts)), kind="warn")
    term_response
    return missing, term_chosen, term_correct, term_response, wrong


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 5. Search parameters, at a concept level.

        Reading a resource you already have (the bundle on your desk) is one thing. Asking a FHIR server for resources you don't yet have is a different operation, and it has a uniform shape across every resource type.

        The shape of a FHIR search:

        ```
        GET https://server.example.org/baseR4/<ResourceType>?<param>=<value>&<param>=<value>
        ```

        For Ms. Reyes's most recent CRP, against a server that has her data, the query would look like:

        ```
        GET /Observation?subject=Patient/elena-reyes&code=http://loinc.org|1988-5&_sort=-date&_count=1
        ```

        Each search parameter is defined by the FHIR spec. The ones you'll meet most:

        - **`subject` / `patient`.** Narrow to one patient. Almost every clinical query starts with this.
        - **`code`.** Narrow to a specific clinical code. Often qualified with the system (`http://loinc.org|1988-5`) so you don't accidentally match a SNOMED code that happens to share the digit string.
        - **`date` / `effective-date` / `onset-date`.** Narrow to a time window. Comparators `gt`, `lt`, `ge`, `le`: `effective-date=ge2024-01-01`.
        - **`status`.** Resources with a particular status. `status=active` for current problems, `status=final` for finished lab results.
        - **`_sort`.** Sort. Prefix with `-` for descending. `_sort=-date` is "newest first."
        - **`_count`.** Maximum results per page.
        - **`_include`.** Pull along referenced resources. `_include=Observation:patient` returns each Observation plus the Patient it points at, in one response.
        - **`_revinclude`.** The reverse: include resources that reference the result. Useful for getting all the labs *for* a patient when starting from the Patient.

        Each resource type defines its own search parameters. Observation defines about thirty. Patient defines about twenty. MedicationRequest about fifteen. You don't need to memorize them; you look them up in the spec page for whichever resource you're querying.

        Track 2 builds real queries against hapi.fhir.org and you'll see exactly what each one returns. For now, the concept worth carrying is that **search is uniform across resource types, parameters are defined by the spec, and the response is always a `searchset` Bundle.**
        """
    )
    return


@app.cell
def _(mo):
    search_quiz = mo.ui.radio(
        options=[
            "`GET /Observation?subject=Patient/elena-reyes&code=http://loinc.org|1988-5&effective-date=ge2024-01-01&_sort=-date`",
            "`GET /Patient/elena-reyes/Observation?code=1988-5&date>=2024-01-01`",
            "`GET /Observation?patient=Reyes&test=CRP&since=2024-01-01`",
            "`GET /find?type=Observation&patient=elena-reyes&test=CRP&from=2024`",
        ],
        label=(
            "You want every CRP that Ms. Reyes has had since 2024-01-01, sorted from newest to oldest. Which query is FHIR-compliant?"
        ),
    )
    search_quiz
    return (search_quiz,)


@app.cell
def _(mo, search_quiz):
    if search_quiz.value is None:
        search_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif search_quiz.value.startswith("`GET /Observation?subject="):
        search_response = mo.callout(
            mo.md(
                "**Right.** That's a textbook FHIR R4 query.\n\n"
                "- Resource type at the path: `/Observation`.\n"
                "- Patient narrowed by relative reference: `subject=Patient/elena-reyes`. (`patient=elena-reyes` is also accepted on most resources as a convenience.)\n"
                "- Code with system qualifier so we don't accidentally match a SNOMED 1988-5: `code=http://loinc.org|1988-5`.\n"
                "- Date window with the `ge` comparator: `effective-date=ge2024-01-01`.\n"
                "- Sort by date descending: `_sort=-date`.\n\n"
                "The server responds with a `searchset` Bundle. For Ms. Reyes's data in this curriculum, you'd get two Observations back (2026-02-10 and 2024-01-08 CRPs), in that order."
            ),
            kind="success",
        )
    elif search_quiz.value.startswith("`GET /Patient/elena-reyes/Observation"):
        search_response = mo.callout(
            mo.md(
                "**Not quite.** Two issues. First, the path `/Patient/elena-reyes/Observation` doesn't exist in plain FHIR. Some servers expose a compartment search variant, but the standard FHIR R4 way is `/Observation?subject=Patient/elena-reyes`. Second, FHIR uses `date=ge2024-01-01` for greater-or-equal, not `date>=2024-01-01` (HTTP query strings can't carry `>` without encoding, so FHIR uses two-letter prefixes)."
            ),
            kind="warn",
        )
    elif search_quiz.value.startswith("`GET /Observation?patient=Reyes&test=CRP&since="):
        search_response = mo.callout(
            mo.md(
                "**No.** This invents parameter names that aren't in the FHIR spec. `patient=Reyes` would search by patient *id*, not last name (and the id isn't `Reyes`). There is no `test` parameter; the spec calls it `code`. There is no `since` parameter; the date parameter is `date` (or `effective-date` on Observation) with comparator prefixes like `ge`."
            ),
            kind="warn",
        )
    else:
        search_response = mo.callout(
            mo.md(
                "**No.** There is no `/find` endpoint in FHIR. The search interface is the resource type itself: `GET /<ResourceType>?<param>=<value>`. The parameters are defined per resource type by the FHIR spec."
            ),
            kind="warn",
        )
    search_response
    return (search_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone: read Ms. Reyes's bundle.

        You now have the four foundational ideas (resources, references, bundles, terminology) and a concept-level handle on search. The rest of this track is the work: six clinical questions about Ms. Reyes, each answered by navigating her bundle. You'll write your answer, commit it, and then the sample answer reveals alongside yours.

        At the end, you'll synthesize all six into a five-to-seven-sentence clinical summary, the kind you'd write at the top of a new-patient note.

        **The rules.** Use the field meanings you just learned. Each question names the resource type you'll need to look in. Open the bundle file (`patients/elena-reyes/fhir-bundle.json`, viewable in the file tree) if you want to inspect it directly, or just go from what we've already shown in this notebook.

        Don't worry about format. The sample answers are clinical sentences, not JSON queries.
        """
    )
    return


@app.cell
def _(commit_text):
    q1_widget, q1_ready = commit_text(
        "**Question 1. What is Ms. Reyes's date of birth, and how old is she at the time of her most recent encounter (2026-02-10)?** Find the Patient resource. The relevant field is `birthDate`.",
        min_chars=30,
    )
    q1_widget
    return q1_ready, q1_widget


@app.cell
def _(mo, q1_ready, q1_widget, reveal):
    mo.stop(
        not q1_ready(),
        mo.md("_Write your answer above. The sample unlocks when you commit._"),
    )
    sample_q1 = (
        "Date of birth **1974-02-09**. At the time of the 2026-02-10 encounter, she was **52 years and 1 day old**. "
        "Found at `Patient.birthDate` in the Patient resource (id `elena-reyes`). The birth date in FHIR is a plain "
        "ISO date (`YYYY-MM-DD`) with no timezone; you do the age math yourself."
    )
    reveal(q1_widget.value, sample_q1, learner_label="Your answer")
    return (sample_q1,)


@app.cell
def _(commit_text):
    q2_widget, q2_ready = commit_text(
        "**Question 2. What medications is Ms. Reyes currently on, with doses and routes?** Find the MedicationStatement resources. Only count entries where `status` is `active`. For each, name the drug, the dose, the route, and the frequency.",
        min_chars=80,
    )
    q2_widget
    return q2_ready, q2_widget


@app.cell
def _(mo, q2_ready, q2_widget, reveal):
    mo.stop(
        not q2_ready(),
        mo.md("_Commit your answer above. The sample unlocks when you do._"),
    )
    sample_q2 = (
        "Three active MedicationStatement resources in the bundle:\n\n"
        "1. **Methotrexate 25 mg subcutaneously once weekly.** RxNorm 1156665 (methotrexate sodium 25 mg/mL injectable solution). Effective since 2022-03-07.\n"
        "2. **Adalimumab 40 mg subcutaneously every 14 days.** RxNorm 327361 (adalimumab 40 mg/0.8 mL pen). Effective since 2024-01-08.\n"
        "3. **Folic acid 1 mg by mouth daily.** RxNorm 315966 (folic acid 1 mg oral tablet). Effective since 2022-03-07. Co-administered with the methotrexate, per the methotrexate dosage note.\n\n"
        "Each drug's dose lives in `dosage[].doseAndRate[].doseQuantity` (a UCUM-coded mg quantity). The route is in `dosage[].route` as a SNOMED code (34206005 = subcutaneous). The frequency is in `dosage[].timing.repeat`. The free-text `dosage[].text` carries the human-readable version of the same fact."
    )
    reveal(q2_widget.value, sample_q2, learner_label="Your answer")
    return (sample_q2,)


@app.cell
def _(commit_text):
    q3_widget, q3_ready = commit_text(
        "**Question 3. What was Ms. Reyes's most recent CRP, when was it drawn, and is it within reference range?** Find the Observation resources with the LOINC code 1988-5. If there's more than one, pick the most recent by `effectiveDateTime`. Report the value, the units, the date, and whether it's flagged.",
        min_chars=60,
    )
    q3_widget
    return q3_ready, q3_widget


@app.cell
def _(mo, q3_ready, q3_widget, reveal):
    mo.stop(
        not q3_ready(),
        mo.md("_Commit your answer above. The sample unlocks when you do._"),
    )
    sample_q3 = (
        "Two CRP Observations in the bundle (LOINC 1988-5):\n\n"
        "- 2024-01-08: 36.2 mg/L, flagged High.\n"
        "- **2026-02-10: 21.4 mg/L, flagged High.**\n\n"
        "The most recent is **21.4 mg/L on 2026-02-10**, drawn at 08:30 local time at her rheumatology visit. The reference range is 0 to 5 mg/L (from the 2024 result's `referenceRange`; the 2026 entry omits the range but the interpretation flag `H` carries the same information). "
        "Two readings of clinical interest: the absolute value is still elevated (4x the upper limit of normal), and the trend is downward from the pre-adalimumab 2024 value, consistent with the DAS28 dropping into the low-activity range."
    )
    reveal(q3_widget.value, sample_q3, learner_label="Your answer")
    return (sample_q3,)


@app.cell
def _(commit_text):
    q4_widget, q4_ready = commit_text(
        "**Question 4. What chronic conditions are on Ms. Reyes's problem list, and what's the onset date of each?** Find the Condition resources. For each, name the diagnosis (use the human-readable text or the SNOMED display), the ICD-10 code, the clinical status, and the onset date.",
        min_chars=80,
    )
    q4_widget
    return q4_ready, q4_widget


@app.cell
def _(mo, q4_ready, q4_widget, reveal):
    mo.stop(
        not q4_ready(),
        mo.md("_Commit your answer above. The sample unlocks when you do._"),
    )
    sample_q4 = (
        "Two active Condition resources, both flagged as `problem-list-item`:\n\n"
        "1. **Seropositive erosive rheumatoid arthritis.** ICD-10-CM M05.79, SNOMED CT 239791008, severity SNOMED 6736007 (moderate). Active, confirmed. Onset 2022-03-07. Recorded by Dr. Bennett (referenced via `recorder`).\n"
        "2. **Anemia of chronic disease.** ICD-10-CM D63.8. Active, confirmed. Onset 2022-02-14 (the date of her initial rheumatology consult).\n\n"
        "Worth noticing in passing: the RA Condition carries **both** an ICD-10 coding and a SNOMED CT coding inside its `code.coding[]` array. This is FHIR's standard answer to the multi-vocabulary problem we saw in Track 0: send both, let the receiver pick. The anemia Condition has only ICD-10, which is normal for less specifically-clinical diagnoses."
    )
    reveal(q4_widget.value, sample_q4, learner_label="Your answer")
    return (sample_q4,)


@app.cell
def _(commit_text):
    q5_widget, q5_ready = commit_text(
        "**Question 5. What allergies does Ms. Reyes have, and what reaction does each cause?** Find the AllergyIntolerance resources. Report the substance, the reaction, the severity, and the criticality.",
        min_chars=40,
    )
    q5_widget
    return q5_ready, q5_widget


@app.cell
def _(mo, q5_ready, q5_widget, reveal):
    mo.stop(
        not q5_ready(),
        mo.md("_Commit your answer above. The sample unlocks when you do._"),
    )
    sample_q5 = (
        "**One AllergyIntolerance resource.**\n\n"
        "- **Substance:** Penicillin. RxNorm 7980 (Penicillin G). Type: allergy. Category: medication.\n"
        "- **Reaction:** Skin rash. SNOMED 271807003.\n"
        "- **Severity (of the reaction):** mild.\n"
        "- **Criticality (of the overall allergy):** low.\n"
        "- **Clinical status:** active. Verification status: confirmed.\n\n"
        "Worth noting the distinction between `reaction[].severity` and the top-level `criticality`. `severity` describes how bad the reaction was in the past; `criticality` is the clinician's assessment of how dangerous a re-exposure would be. They're related but not the same: a mild past reaction to a drug with strong cross-reactivity to other essential antibiotics might still warrant high criticality. Here both are low; this is a low-stakes allergy clinically."
    )
    reveal(q5_widget.value, sample_q5, learner_label="Your answer")
    return (sample_q5,)


@app.cell
def _(commit_text):
    q6_widget, q6_ready = commit_text(
        "**Question 6. Who is the rheumatologist who has been treating Ms. Reyes, and where do they practice?** Find the Practitioner resource. Then find the Organization that's referenced by her Encounter's `serviceProvider`. Report the practitioner's name, their NPI, and the practice name and city.",
        min_chars=80,
    )
    q6_widget
    return q6_ready, q6_widget


@app.cell
def _(mo, q6_ready, q6_widget, reveal):
    mo.stop(
        not q6_ready(),
        mo.md("_Commit your answer above. The sample unlocks when you do._"),
    )
    sample_q6 = (
        "- **Practitioner:** Maya Bennett, MD. NPI **1234567890** (in `identifier[]` with system `http://hl7.org/fhir/sid/us-npi`). Qualification: MD.\n"
        "- **Organization (her practice):** Bay Rheumatology Associates, 101 Main Street, Springfield, MA 01103. Phone 555-0100.\n\n"
        "The Encounter from 2022-02-14 references Dr. Bennett as the `participant.individual` and the Organization as the `serviceProvider`. Following those two references is how we connected the practitioner to the practice. "
        "Worth noting: most resources that involve a clinician (Conditions via `recorder`, MedicationStatements via `informationSource`, Encounters via `participant`) reference the same Practitioner resource. The Practitioner is defined once and pointed at many times. That's the database-shaped half of FHIR I mentioned earlier: identity by reference, not duplication."
    )
    reveal(q6_widget.value, sample_q6, learner_label="Your answer")
    return (sample_q6,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Synthesis: write the summary.

        You've gathered the pieces. Write them up as a five-to-seven-sentence clinical summary, the kind you'd put at the top of a new-patient note. A reader who has never met this patient should come out of your summary knowing who she is, what's going on, what she's on, and what's been happening with her disease activity.

        After you commit, the sample summary unlocks alongside yours.
        """
    )
    return


@app.cell
def _(commit_text):
    summary_widget, summary_ready = commit_text(
        "**Write the clinical summary.** Five to seven sentences. Synthesize the demographic, problem list, medications, recent labs, and the trajectory implied by them.",
        min_chars=300,
    )
    summary_widget
    return summary_ready, summary_widget


@app.cell
def _(mo, reveal, summary_ready, summary_widget):
    mo.stop(
        not summary_ready(),
        mo.md("_Take a few sentences. The sample summary unlocks when you commit._"),
    )
    sample_summary = (
        "**Ms. Elena Reyes** is a 52-year-old woman (DOB 1974-02-09) with **seropositive erosive rheumatoid arthritis** "
        "diagnosed in March 2022 (ICD-10 M05.79, SNOMED 239791008, moderate severity), complicated by **anemia of chronic disease**. "
        "She is followed in rheumatology by **Dr. Maya Bennett** at Bay Rheumatology Associates in Springfield, MA. "
        "Her active regimen is **methotrexate 25 mg SC weekly**, **adalimumab 40 mg SC every 14 days** (added January 2024 for inadequate response to methotrexate monotherapy), and **folic acid 1 mg PO daily**. "
        "She is allergic to **penicillin** (mild cutaneous reaction, low criticality). "
        "Her most recent visit (2026-02-10) shows a **DAS28-CRP of 2.8 (low disease activity)** with CRP 21.4 mg/L and ESR 33 mm/h, both still mildly elevated but markedly improved from her pre-adalimumab baseline (CRP 36.2 in January 2024). "
        "She is up to date on influenza vaccination (October 2024)."
    )
    reveal(summary_widget.value, sample_summary, learner_label="Your summary")
    return (sample_summary,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - You put the four foundational FHIR ideas in place: a **resource** is a unit of clinical data shaped by a published specification; **references** are how resources connect; a **bundle** is a container of resources whose `type` tells you what the container means; and **terminology** lives in `system`+`code` pairs, with the slot determining the vocabulary.
        - You navigated Ms. Reyes's actual FHIR Bundle, answered six clinical questions by reading the right resource type and the right field, and synthesized the six answers into a clinical summary.
        - You picked up the concept-level shape of FHIR search (`GET /<ResourceType>?<param>=<value>...` returns a `searchset` bundle), without writing one yet.

        That is most of what "FHIR fluency" actually means for a clinician: not the ability to author resources from scratch (Track 3 does that), but the ability to read someone else's resources, follow the references, and pull out the clinical story. Every later track builds on this.

        ## What's next.

        **Track 2: Working with FHIR servers.** You'll write actual queries against hapi.fhir.org and parse the responses with a small amount of visible Python (gently introduced). The search-parameter concepts from this track become real queries that return real bundles, and the bundle-reading skills become real cohort assembly.
        """
    )
    return


if __name__ == "__main__":
    app.run()
