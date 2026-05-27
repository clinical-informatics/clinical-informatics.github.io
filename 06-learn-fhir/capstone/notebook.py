"""Capstone for course 06: Learn FHIR.

Author, validate, and hand off Ms. Reyes's complete FHIR record. The
capstone integrates every move from the six tracks: Track 0's framing
of why FHIR exists, Track 1's anatomy of resources and bundles,
Track 2's $validate POST pattern, Track 3's profile and must-support
discipline, Track 4's IG awareness, and Track 5's SMART access
boundary. The deliverable is a one-page hand-off the learner can take
to an engineering team and a registry partner.

The validation OperationOutcome shown to the learner is a real
response cached from hapi.fhir.org's `Bundle/$validate` endpoint
against Ms. Reyes's bundle as it ships in `start-here/patients/`. The
22 errors and 40 warnings the validator returns are the actual
findings: pseudo-UUIDs in `urn:uuid:` form, profile references the
default hapi.fhir.org validator can't resolve, a deprecated v2-0004
code, narrative best-practice misses, and missing performer
references on Observations. The Socratic steps ask the learner to
triage real findings on a real artifact, not a toy example.
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

    # Absolute site path where this notebook's WASM export lives. Used only
    # in the Pyodide branch below; `pyodide.http.open_url` resolves a
    # leading-slash path against the page origin, which works identically in
    # the main thread and in the marimo worker. Update this if the notebook
    # is renamed or the site is deployed under a subpath.
    _WASM_DATA_BASE = "/06-learn-fhir/capstone/app"

    def _load_data(*parts):
        """Read a JSON file from this notebook's cache/ dir. Local + WASM.

        Locally: reads from ``Path(__file__).parent / parts``.
        In Pyodide WASM: fetches ``_WASM_DATA_BASE / parts`` via
        ``pyodide.http.open_url``. The build pipeline mirrors ``cache/`` into
        the WASM export (with fhir-bundle.json symlinked from
        start-here/patients/) so the same relative layout resolves in both
        contexts.
        """
        if "pyodide" in sys.modules:
            from pyodide.http import open_url

            url = _WASM_DATA_BASE + "/" + "/".join(parts)
            return json.loads(open_url(url).read())
        return json.loads(Path(__file__).parent.joinpath(*parts).read_text())

    bundle = _load_data("cache", "fhir-bundle.json")
    validation = _load_data("cache", "validate-elena-bundle.json")
    return Counter, bundle, json, mo, validation


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

    def reflection(prompt, placeholder=""):
        widget = mo.ui.text_area(
            label=prompt,
            rows=5,
            full_width=True,
            placeholder=placeholder
            or "Take a few sentences. No reveal here. The reflection is the work.",
        )
        layout = mo.vstack(
            [
                widget,
                mo.callout(
                    mo.md(
                        "_There's no answer key for this one. The point isn't to be right. "
                        "It's to make your reasoning explicit to yourself._"
                    ),
                    kind="neutral",
                ),
            ]
        )
        return widget, layout

    return commit_text, reflection, reveal


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Author and validate a complete FHIR record for Ms. Reyes

        ## The scenario.

        You're the clinical informaticist at Bay Rheumatology Associates. The practice is joining a multi-site rheumatology registry that ingests patient data as FHIR R4 bundles and expects US Core conformance for everything it can profile. Ms. Reyes is your test patient. The registry's engineering team has asked you to produce her bundle, run it through validation, and send a one-page hand-off that says: what's in the bundle, what the validator flagged and your call on each finding, and how the registry's downstream SMART app should be allowed to read it.

        Everything in this capstone is real work. The bundle you'll audit is the same `fhir-bundle.json` that has shown up since Track 1. The OperationOutcome you'll triage was returned by hapi.fhir.org's `Bundle/$validate` endpoint against that bundle. The 22 errors and 40 warnings are not a teaching contrivance; they're the artifact the public validator actually emitted, and the work is deciding which of those findings block a production hand-off and which are validator configuration noise.

        Eight steps cover the six tracks of the course in sequence: a bundle-anatomy view (Track 1), scope (Tracks 0 + 4), profile selection (Tracks 1 + 3 + 4), a real validator verdict (Tracks 2 + 3), triage (Tracks 3 + 4), prioritized fixes (Track 3), SMART access for a downstream registry app (Track 5), and portability versus interoperability with a forward look to course 07 (Tracks 0 + 4). Six of the eight steps are Socratic: they gate a sample answer behind a written commit from you. The other two are display steps that show what the bundle and the validator report contain. At the end the notebook assembles your seven written answers into a one-page hand-off document.
        """
    )
    return


@app.cell
def _(Counter, bundle, mo):
    _entries = bundle.get("entry", [])
    _types = Counter(e["resource"]["resourceType"] for e in _entries)
    _type_lines = "\n".join(f"- **{t}**: {n}" for t, n in _types.most_common())
    _profiled = [
        (e["resource"]["resourceType"], e["resource"].get("meta", {}).get("profile", []))
        for e in _entries
    ]
    _profiled_lines = "\n".join(
        f"- **{t}** -> `{p[0].split('/')[-1]}`"
        for t, p in _profiled
        if p
    )
    mo.callout(
        mo.md(
            "### Ms. Reyes's bundle at a glance.\n\n"
            f"**Total entries:** {len(_entries)}.\n\n"
            "**By resource type:**\n\n"
            f"{_type_lines}\n\n"
            "**Resources that already claim a US Core profile:**\n\n"
            f"{_profiled_lines}\n\n"
            "**Bundle type:** `collection` (not a `transaction`; the registry will receive it as a self-contained snapshot, not as a set of writes to apply)."
        ),
        kind="info",
    )
    return


@app.cell
def _(commit_text):
    scope_widget, scope_ready = commit_text(
        "**Step 1. Scope (Tracks 0 + 4).** Ms. Reyes has four years of data in her EHR. The bundle in front of you holds seventeen entries. What was kept in scope, what was deliberately left out, and what would you tell the registry's product owner about why? Frame your answer as if a non-informatics colleague asked, \"why isn't every lab she ever had in here?\"",
        min_chars=120,
    )
    scope_widget
    return scope_ready, scope_widget


@app.cell
def _(mo, reveal, scope_ready, scope_widget):
    mo.stop(
        not scope_ready(),
        mo.md("_Write a few sentences above. The sample answer unlocks when you commit._"),
    )
    _sample_scope = (
        "The bundle is a clinical snapshot for registry enrollment, not a full longitudinal export. "
        "It carries (a) demographics and the two structured extensions US Core requires for stratification work (race and ethnicity); "
        "(b) the active problem list (seropositive RA, anemia of chronic disease) with the correct ICD-10 plus SNOMED dual coding; "
        "(c) the active medication regimen (methotrexate, adalimumab, folate) as MedicationStatements rather than orders, because the registry needs the *current state* of treatment, not the prescribing event; "
        "(d) the initial diagnostic workup (anti-CCP, the new-patient encounter) for cohort-defining context; "
        "(e) the most recent disease-activity snapshot (CRP, ESR, DAS28-CRP, vital signs from the February 2026 visit); "
        "and (f) one CRP from January 2024 as an anchor before adalimumab started, so the registry has at least one pre-biologic data point.\n\n"
        "**What was deliberately left out:** the four-year longitudinal CRP/ESR trail (the registry will ingest those via a separate Bulk Data pull, not embed them in the enrollment bundle), the historical clinic encounters between February 2022 and February 2026 (the registry only needs the index encounter and the most recent), Ms. Reyes's outpatient notes (the registry doesn't ingest free text), and her claims data (out of scope for clinical registry; lives in a separate health-economics feed).\n\n"
        "**The principle behind the cut:** an enrollment bundle is a *cohort handshake*, not a record dump. The registry needs enough to know she belongs in the cohort and enough to baseline her disease activity. Volume beyond that adds maintenance burden (every update needs to flow through) without adding signal. The longitudinal data has its own pipeline."
    )
    reveal(scope_widget.value, _sample_scope, learner_label="Your scoping rationale")
    return


@app.cell
def _(commit_text):
    profile_widget, profile_ready = commit_text(
        "**Step 2. Profile selection (Tracks 1 + 3 + 4).** Of the seventeen entries in the bundle, only three currently claim a US Core profile: Patient, the RA Condition, and the two CRP Observations. List the other entries and say, for each, whether a US Core profile applies, which one, and what changes for the bundle if you stamp it.",
        min_chars=200,
    )
    profile_widget
    return profile_ready, profile_widget


@app.cell
def _(mo, profile_ready, profile_widget, reveal):
    mo.stop(
        not profile_ready(),
        mo.md("_Commit your profile call above. The sample unlocks when you do._"),
    )
    _sample_profile = (
        "- **Practitioner (Dr. Bennett)** -> `us-core-practitioner`. NPI is already present; stamping the profile commits us to also surfacing `name` and `identifier` as must-support, which we have.\n"
        "- **Organization (Bay Rheumatology)** -> `us-core-organization`. Name and address are present; must-support `active` and `identifier` (we'd add an NPI for the org).\n"
        "- **Condition (anemia of chronic disease)** -> `us-core-condition-problems-health-concerns`. Same profile as the RA condition; the bundle currently profiles RA but not anemia, which is an inconsistency to fix.\n"
        "- **MedicationStatement (MTX, adalimumab, folate)** -> US Core does *not* have a MedicationStatement profile in the R4 IG; it standardizes on MedicationRequest. Two options: (1) re-author these as MedicationRequest with `status=active` and stamp `us-core-medicationrequest`, or (2) leave as MedicationStatement and accept that the registry will fall back to base FHIR validation for these. Option 1 is cleaner if the registry will ever care about prescriber, refill cadence, or dispense history; option 2 is fine if the registry only wants the current regimen as a list.\n"
        "- **AllergyIntolerance** -> `us-core-allergyintolerance`. Must-support includes `clinicalStatus`, `verificationStatus`, `patient`, `code`; all present. Stamping is free.\n"
        "- **Encounter** -> `us-core-encounter`. Must-support `class`, `type`, `subject`, `period`, `participant`; all present. The `type` text we use (\"New patient consultation\") is fine; the code we use under it (v2-0004#OUTPATIENT) is not, and validation will catch it (see Step 4).\n"
        "- **Observation (ESR, anti-CCP, DAS28)** -> the two LOINC lab observations (ESR, anti-CCP) should stamp `us-core-observation-lab` like the CRPs already do. DAS28 is a clinical assessment, not a lab; the right US Core profile is `us-core-observation-clinical-result` (the broader profile US Core 6.x added for non-lab observations).\n"
        "- **Observation (blood pressure)** -> `us-core-blood-pressure` (the vital-signs profile lineage from FHIR vital-signs plus the US Core constraints on it). Stamping requires the component LOINCs we already have (8480-6 systolic, 8462-4 diastolic).\n"
        "- **Immunization (flu vaccine)** -> `us-core-immunization`. Must-support `status`, `vaccineCode`, `patient`, `occurrenceDateTime`; all present. Stamping is free.\n\n"
        "**What changes when you stamp:** each `meta.profile` URL is a *promise* the resource conforms. The validator now checks the must-support list for that profile, and any consumer can rely on those fields being present. The cost is that every must-support gap that was a soft warning becomes a hard expectation, and your data team has to backfill anywhere the field is empty."
    )
    reveal(profile_widget.value, _sample_profile, learner_label="Your per-resource profile plan")
    return


@app.cell
def _(Counter, mo, validation):
    _issues = validation.get("issue", [])
    _by_sev = Counter(i.get("severity") for i in _issues)

    def _category(i):
        diag = i.get("diagnostics", "")
        if "UUIDs must be valid and lowercase" in diag:
            return "Pseudo-UUIDs in urn:uuid (real, fixable)"
        if "Profile reference" in diag and "could not be found" in diag:
            return "Profile reference unresolvable (validator config artifact)"
        if "dom-6" in diag:
            return "Narrative not present (best practice)"
        if "CodeSystem is unknown" in diag:
            return "CodeSystem not loaded by validator (terminology artifact)"
        if "should have a performer" in diag:
            return "Observation missing performer (best practice)"
        if "Unknown code" in diag and "OUTPATIENT" in diag:
            return "Deprecated v2-0004 code OUTPATIENT (real)"
        if "Unknown extension" in diag:
            return "Extension not recognized by base validator (US Core extension)"
        if "UCUM Codes" in diag and "annotations" in diag:
            return "UCUM annotation style {score} flagged (real, low priority)"
        return "Other"

    _by_cat = Counter((_category(i), i.get("severity")) for i in _issues)
    _table = "\n".join(
        f"| {cat} | {sev} | {n} |"
        for (cat, sev), n in sorted(_by_cat.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    mo.callout(
        mo.md(
            "### Step 3. The validator's verdict.\n\n"
            "We POSTed the bundle to `https://hapi.fhir.org/baseR4/Bundle/$validate` "
            "and cached the OperationOutcome. The response below is verbatim, grouped by category.\n\n"
            f"**Issue totals.** Errors: **{_by_sev.get('error', 0)}**, "
            f"warnings: **{_by_sev.get('warning', 0)}**, "
            f"information: **{_by_sev.get('information', 0)}**, "
            f"total: **{sum(_by_sev.values())}**.\n\n"
            "| Category | Severity | Count |\n"
            "|---|---|---|\n"
            f"{_table}\n\n"
            "**How to read this.** Severity is the validator's call; *category* is the clinically meaningful grouping. "
            "Three categories are validator-configuration artifacts on the public hapi.fhir.org endpoint: "
            "profile references it doesn't fetch by default, code systems it doesn't load by default, "
            "and US Core extensions it doesn't recognize because the IG package isn't installed. "
            "A validator run against your registry's own IG-aware validator (the HL7 `validator_cli.jar` "
            "preloaded with `hl7.fhir.us.core`) would silence those categories and leave the real findings."
        ),
        kind="warn",
    )
    return


@app.cell
def _(commit_text):
    triage_widget, triage_ready = commit_text(
        "**Step 4. Triage (Tracks 3 + 4).** The validator returned 22 errors and 40 warnings. Go through the categories above and say which of them are real findings against the bundle, which are artifacts of the public validator's configuration, and what action each category implies before the hand-off.",
        min_chars=200,
    )
    triage_widget
    return triage_ready, triage_widget


@app.cell
def _(mo, reveal, triage_ready, triage_widget):
    mo.stop(
        not triage_ready(),
        mo.md("_Commit your triage above. The sample unlocks when you do._"),
    )
    _sample_triage = (
        "**Real findings (must address before hand-off):**\n\n"
        "- *17 errors: pseudo-UUIDs in `urn:uuid:` form.* The `fullUrl`s read `urn:uuid:patient-elena-reyes` and the like. `urn:uuid:` requires a syntactically valid lowercase UUID; the strings we used are human-readable tokens, which violates the bundle-entry rules. Action: replace each `fullUrl` with a real UUID (Python's `uuid.uuid4()`), update every `reference` that points to it, and keep the readable id inside the resource itself (`resource.id`) for chart-traceability.\n"
        "- *1 error: v2-0004#OUTPATIENT on the Encounter.* That code system used to carry OUTPATIENT but the modern v2-0004 doesn't include it; the modern coding lives in v3-ActCode (which the bundle already uses correctly for `class` -> AMB). Action: remove the v2-0004 `type` coding and leave the text, or replace with an appropriate code from a current value set (e.g., `http://snomed.info/sct` 308335008 \"Patient encounter procedure\").\n"
        "- *1 warning: UCUM annotation `{score}` on the DAS28 Observation.* UCUM allows annotations in curly braces but flags them as non-portable. Action: drop the `{score}` UCUM code on DAS28 and use a `valueString` or a non-quantitative coded value; alternatively, leave it with a note that the registry accepts it.\n"
        "- *6 warnings: Observation missing performer.* Best-practice warning, not a US Core must-support failure, but the registry will almost certainly want to know who measured the CRP, ESR, anti-CCP, etc. Action: add a `performer` reference to either the Practitioner (Dr. Bennett) or the lab Organization on each Observation.\n\n"
        "**Artifacts (no action; document in the hand-off):**\n\n"
        "- *4 errors: us-core-patient / us-core-condition-problems-health-concerns / us-core-observation-lab profile references unresolvable.* The public hapi.fhir.org validator is configured not to fetch unknown profiles from the network. The bundle is profile-stamped correctly; the validator simply doesn't have the US Core package installed. Fix: run the IG-aware validator (`validator_cli.jar -ig hl7.fhir.us.core`) locally; these errors disappear.\n"
        "- *16 warnings: CodeSystem unknown (loinc.org, snomed.info/sct, terminology.hl7.org/CodeSystem/condition-clinical, etc.).* Same root cause. The validator isn't loading the terminology servers. Code-system validation against tx.fhir.org or a local Snowstorm instance would clear these.\n"
        "- *2 information: us-core-race / us-core-ethnicity extension unknown.* Same root cause; the extensions are correctly authored.\n\n"
        "**Best-practice warnings (judgment call):**\n\n"
        "- *17 warnings: dom-6 narrative missing.* Every DomainResource is *recommended* (not required) to carry a generated `text.div`. For an enrollment bundle going to a structured-data ingestion pipeline, narratives add storage with no consumer. For a bundle that might be human-rendered (a patient summary export, an IPS), narratives matter. Call: skip for this registry; revisit if the bundle ever flows somewhere a human reads it raw.\n\n"
        "**Net.** Roughly 25 of the 64 issues are real; the rest are validator config. The hand-off needs to say this explicitly so the registry's engineering team doesn't open a thread about \"22 errors.\""
    )
    reveal(triage_widget.value, _sample_triage, learner_label="Your triage call")
    return


@app.cell
def _(commit_text):
    fix_widget, fix_ready = commit_text(
        "**Step 5. The three fixes you ship first (Track 3).** From your triage, name the three changes you'd commit before sending the bundle to the registry, in order of priority. For each: what changes in the JSON, why this one before the others, and whether the registry could ingest the bundle as-is if you ran out of time before this fix landed.",
        min_chars=180,
    )
    fix_widget
    return fix_ready, fix_widget


@app.cell
def _(fix_ready, fix_widget, mo, reveal):
    mo.stop(
        not fix_ready(),
        mo.md("_Commit your top-three fixes above. The sample unlocks when you do._"),
    )
    _sample_fix = (
        "1. **Real UUIDs in `fullUrl` and `reference` (blocks ingestion).** "
        "Replace each `urn:uuid:patient-elena-reyes` with a real `urn:uuid:f47ac10b-58cc-4372-a567-0e02b2c3d479`-style identifier from `uuid.uuid4()`, then propagate to every internal reference in the bundle. Keep the readable `resource.id` (`elena-reyes`, `ra-condition`, etc.) inside each resource for human traceability. **Why first:** the registry's validator will reject the bundle with the same 17 errors and the engineering team will not be able to load it. This is the only finding that genuinely blocks the hand-off.\n\n"
        "2. **Drop the v2-0004#OUTPATIENT code on the Encounter (blocks profile conformance).** "
        "Either remove the `type` coding and keep the `text`, or replace with a current code (SNOMED 308335008). The Encounter's `class` is already correct (v3-ActCode AMB). **Why second:** the registry's US Core validator will reject this specific Encounter once the IG-aware run replaces the public hapi.fhir.org artifact-errors with real US Core checks. Painless one-line fix; ship now to avoid a re-roundtrip.\n\n"
        "3. **Stamp the remaining seven US Core profiles and backfill performer on Observations (improves conformance, not blocking).** "
        "Add `meta.profile` to the second Condition, the MedicationStatements (re-authored as MedicationRequest if we go that route), the AllergyIntolerance, the Encounter, the ESR, anti-CCP, DAS28, BP, and Immunization. Add `performer` references on the six Observations that lack them. **Why third:** the registry will accept the bundle without these (US Core allows base-FHIR resources where no US Core profile applies, and missing-performer is a warning). But every stamped profile is a future-proofing move: it tightens the contract and makes downstream consumers more reliable. Worth doing inside the same change set if time permits; if not, the registry can ingest the bundle today and we can ship this as a follow-up.\n\n"
        "**If we ran out of time:** fixes 1 and 2 are blocking. Fix 3 is a quality improvement. The first two are an hour of work; the third is a half-day if we also re-author the medications."
    )
    reveal(fix_widget.value, _sample_fix, learner_label="Your prioritized fixes")
    return


@app.cell
def _(commit_text):
    smart_widget, smart_ready = commit_text(
        "**Step 6. SMART access for the registry's app (Track 5).** The registry's investigator-facing dashboard is a SMART-on-FHIR app. It will read this bundle from the clinic's FHIR server using OAuth. Write the scope string you would grant the app and the scope string you would refuse, and say what trust trade-off each line represents.",
        min_chars=120,
    )
    smart_widget
    return smart_ready, smart_widget


@app.cell
def _(mo, reveal, smart_ready, smart_widget):
    mo.stop(
        not smart_ready(),
        mo.md("_Commit your SMART scope call above. The sample unlocks when you do._"),
    )
    _sample_smart = (
        "**Grant** (least-privilege read for the registry's dashboard):\n\n"
        "```\n"
        "patient/Patient.read patient/Condition.read patient/MedicationStatement.read patient/AllergyIntolerance.read patient/Encounter.read patient/Observation.read patient/Immunization.read launch openid fhirUser offline_access\n"
        "```\n\n"
        "Patient-context scopes (the `patient/` prefix), read-only, restricted to the resource types the bundle actually contains. `launch` tells the EHR this is an EHR-launched app; `openid fhirUser` lets us identify the launching clinician (for the registry's audit log); `offline_access` lets the app refresh its token in the background without re-prompting.\n\n"
        "**Refuse:**\n\n"
        "- `user/*.read` or `system/*.read`. These grant the app access to *every* patient at the clinic, not just Ms. Reyes's record under the current launch context. The registry's dashboard is a per-patient view; cohort-level reads belong to Bulk Data, not to the live SMART app.\n"
        "- Any `.write` scope. The app is read-only; if it ever needs to write, that's a separate consent moment with a separate scope.\n"
        "- `patient/DocumentReference.read` or `patient/Binary.read`. The bundle has no notes or attachments; granting these creates surface area we don't intend to use, which is exactly the kind of scope creep the principle of least privilege exists to prevent.\n\n"
        "**The trust trade-off.** Every additional scope is a contract the EHR exposes to a third-party server. The registry could, in principle, log everything it reads (and a careful one will). The clinic's privacy posture is a function of the scopes the EHR will issue and the registry's audit and retention practices on the other end. The grant above is the smallest scope that does the job; the refusals are the surface area we're explicitly choosing not to open."
    )
    reveal(smart_widget.value, _sample_smart, learner_label="Your SMART scope call")
    return


@app.cell
def _(commit_text):
    layer_widget, layer_ready = commit_text(
        "**Step 7. Portability vs interoperability (Tracks 0 + 4, with a forward look to course 07).** This bundle is interoperable: any US Core-conformant FHIR server can ingest it without negotiation. Where does it sit on the portability spectrum? When would you want the data in OMOP form instead, and what would the registry lose if it asked for OMOP instead of FHIR?",
        min_chars=150,
    )
    layer_widget
    return layer_ready, layer_widget


@app.cell
def _(layer_ready, layer_widget, mo, reveal):
    mo.stop(
        not layer_ready(),
        mo.md("_Commit your portability-vs-interoperability call above. The sample unlocks when you do._"),
    )
    _sample_layer = (
        "**Interoperability is high.** The bundle uses globally standardized vocabularies (LOINC, SNOMED, RxNorm, ICD-10, CVX, UCUM), reference resolution that any FHIR server understands, and the same profiles (US Core) the rest of the US healthcare ecosystem aims at. Plug it into a different US Core-conformant server and it loads.\n\n"
        "**Portability is moderate, not high.** Portability is whether *I* can move my data into a system that wasn't expecting it. FHIR's portability is gated by the receiving system's profile expectations: a server that requires mCODE for cancer data won't accept a bundle that only meets US Core. Inside the world of US Core registries, this bundle is portable; outside it, not without re-profiling.\n\n"
        "**When you'd want OMOP instead.** Population-scale research that asks the same SQL question across dozens of institutions: drug exposure cohorts, comparative effectiveness, real-world evidence trial emulation. The OMOP CDM normalizes vocabularies to a single concept set (the OHDSI standard vocabularies, with cross-walks from RxNorm, SNOMED, ICD-10, LOINC) and lays the data into the same six core tables regardless of the source EHR. A query you write at one OMOP site runs at every other OMOP site unchanged. That's the portability payoff OMOP was built for.\n\n"
        "**What the registry would lose by asking for OMOP instead of FHIR.** Three things: (1) reference granularity. OMOP collapses Observation, Condition, Procedure, and Measurement into separate tables joined by `person_id`; reference resolution between resources (which clinician ordered which lab in which encounter) requires extra joins and sometimes isn't preserved at the same fidelity. (2) Profile semantics. OMOP doesn't carry must-support; if a field is missing from the source, it's missing from the OMOP record without a profile-level expectation flagging it. (3) Real-time clinical context. OMOP is built for analytics; the latency assumption is days, not seconds. A clinical app that wants to react to a new lab posting today wants FHIR.\n\n"
        "**The clean framing.** This bundle is the *clinical handshake*; OMOP is the *analytic substrate*. Most multi-site programs end up with both, populated by different pipelines, and that's not redundancy. It's two different jobs."
    )
    reveal(layer_widget.value, _sample_layer, learner_label="Your portability/interoperability call")
    return


@app.cell
def _(reflection):
    final_reflection, final_reflection_layout = reflection(
        "**Final reflection.** You'll send this hand-off to the registry's engineering team and to your clinic's privacy officer. What's the *first* objection or question you expect from each, and how would you answer it on the spot? (No reveal. The writing is the work.)",
        placeholder="A paragraph each. The engineer's question is usually \"what about field X?\"; the privacy officer's question is usually \"what controls what leaves and where it goes?\"",
    )
    final_reflection_layout
    return (final_reflection,)


@app.cell
def _(
    final_reflection,
    fix_widget,
    layer_widget,
    mo,
    profile_widget,
    scope_widget,
    smart_widget,
    triage_widget,
    validation,
):
    _sections = [
        ("1. Scope of the bundle", scope_widget.value or "_(not yet written)_"),
        ("2. Per-resource profile plan", profile_widget.value or "_(not yet written)_"),
        ("3. Validator triage", triage_widget.value or "_(not yet written)_"),
        ("4. Prioritized fixes before hand-off", fix_widget.value or "_(not yet written)_"),
        ("5. SMART access for the registry app", smart_widget.value or "_(not yet written)_"),
        ("6. Portability vs interoperability", layer_widget.value or "_(not yet written)_"),
        ("7. Anticipated reviewer questions and answers", final_reflection.value or "_(not yet written)_"),
    ]
    _issues = validation.get("issue", [])
    _e = sum(1 for i in _issues if i.get("severity") == "error")
    _w = sum(1 for i in _issues if i.get("severity") == "warning")
    _header = (
        "# FHIR bundle hand-off: Ms. Elena Reyes\n\n"
        "**Prepared by:** _(your name)_  **Date:** _(today)_  **Bundle source:** `patients/elena-reyes/fhir-bundle.json`.  "
        "**Target environment:** US Core-conformant FHIR R4 server at the registry.\n\n"
        f"**Validator summary:** hapi.fhir.org/baseR4/Bundle/$validate returned {_e} errors and {_w} warnings on the bundle as-is; "
        "see Section 3 for the triage. Roughly two-thirds of the findings are public-validator configuration artifacts; "
        "the remaining one-third are real findings, prioritized in Section 4.\n\n"
        "---\n"
    )
    _body = "\n\n".join(f"## {title}\n\n{content}" for title, content in _sections)
    mo.vstack(
        [
            mo.md("### Your one-page hand-off document."),
            mo.callout(mo.md(_header + _body), kind="info"),
            mo.md(
                "Copy the hand-off above out of the browser (Cmd/Ctrl + P -> Save as PDF, "
                "or select-and-copy). This is the artifact you'd send the registry's engineering "
                "team alongside the corrected bundle, and the artifact you'd take to your clinic's "
                "privacy review."
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this capstone.

        You covered the six tracks of the course in sequence and applied each one to a single real artifact:

        - **Track 0 (Before FHIR)** when you decided what *belongs* in a clinical snapshot versus what belongs in a longitudinal feed or a claims pipeline. The framing of "different jobs, different layers" is Track 0's mental model applied to a packaging decision.
        - **Track 1 (FHIR fundamentals)** when you read the bundle's seventeen entries by resource type, recognized the internal-reference pattern (`urn:uuid:` plus `fullUrl`), and noticed which resources already carried a `meta.profile` declaration.
        - **Track 2 (FHIR servers)** when you understood that the validator response was a real POST to a real public endpoint, and that the OperationOutcome is a structured resource you can parse, group, and report on the same way you'd parse any other FHIR response.
        - **Track 3 (Clinical modeling)** when you triaged validator errors as either real conformance problems or validator-configuration artifacts, and when you decided which fixes block ingestion versus which are quality improvements.
        - **Track 4 (Implementation guides)** when you proposed profile stamps for every resource and reasoned about what changes when a profile commits the resource to a must-support list. The recognition that US Core does not profile MedicationStatement, and the decision about whether to re-author as MedicationRequest, is the IG-fluency move Track 4 was building toward.
        - **Track 5 (SMART on FHIR)** when you wrote the scope string the registry's app should get and the scope string it shouldn't, and named the trust trade-off each line represents.

        Read together, the eight Socratic answers and the validator-triage table are the artifact a real clinical informaticist produces when a registry asks for a patient bundle. The hand-off document is what makes the work auditable: the choices are written down, the validator's verdict is acknowledged, and the boundary with downstream consumers is explicit.

        ## What's next.

        The fluency you built in this course continues into two adjacent courses immediately:

        - **Course 07 (Data wrangling and engineering)** continues the portability vs interoperability split and covers OMOP end-to-end. The Step 7 sample answer is a preview of the framing course 07 takes seriously across all five tracks.
        - **Course 12 (Clinical decision support)** comes back to FHIR through CDS Hooks and CQL. The bundle you just hand-handed off is exactly the data shape a CDS Hooks service would receive as the patient context for a `patient-view` hook; the scope discussion in Step 6 is the negotiation that determines whether the service can read it. CDS Hooks is introduced at the concept level in Track 5; course 12 builds the rest.

        Other entries you'll meet again with this fluency in hand: course 09 (AI in medicine) when a clinical prediction service is delivered as a SMART app over FHIR; course 11 (health economics) when claims and clinical data are joined to evaluate value-based care; and course 14 (interoperability policy) when the 21st Century Cures Act and ONC information-blocking rules name the FHIR endpoints whose existence the rest of this course assumed.

        Pick whichever one is closest to the next problem in front of you and start there.
        """
    )
    return


if __name__ == "__main__":
    app.run()
