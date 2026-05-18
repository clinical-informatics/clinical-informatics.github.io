"""Track 4: Implementation guides.

Profiles in detail. The anatomy of a published IG. US Core
Observation Lab and mCODE Primary Cancer Condition walked as the
worked examples (cached from hl7.org/fhir/us/core and
hl7.org/fhir/us/mcode). Must-support footguns. Portability vs
interoperability defined and distinguished, with a cross-reference
callout to Track 0's five-layer framework and a forward reference to
Course 07's OMOP coverage.

Capstone: a one-page gap analysis of US Core for rheumatology. The
learner rates US Core Observation Lab's coverage of RA monitoring
needs row by row, names RA-specific gaps US Core doesn't cover, and
the notebook assembles the answers into a markdown report ready to
copy out.

Cross-cell widgets have plain names; cell-internal vars are
underscore-prefixed. Marimo treats `_name` as cell-private, so any
widget shared across cells must use a plain name.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import sys
    from pathlib import Path

    _track_dir = Path(__file__).parent
    _course_dir = _track_dir.parent
    if str(_course_dir) not in sys.path:
        sys.path.insert(0, str(_course_dir))

    import marimo as mo
    import pandas as pd

    from shared.cross_reference import callback, forward

    cache_dir = _track_dir / "cache"

    def load(filename):
        with open(cache_dir / filename) as fh:
            return json.load(fh)

    us_core_obs_lab = load("us-core-observation-lab.json")
    mcode_primary_cancer = load("mcode-primary-cancer-condition.json")

    return (
        callback,
        forward,
        json,
        load,
        mcode_primary_cancer,
        mo,
        pd,
        us_core_obs_lab,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 4: Implementation guides

        ## What "supports US Core" actually means.

        Two vendors both say they support US Core Observation Lab. One of them displays the `interpretation` flag prominently in the chart. The other stores it but never shows it. Both can defensibly claim conformance.

        The work of this track is making that disagreement explicit. By the end you can:

        - Read the anatomy of a published implementation guide (US Core, mCODE) without getting lost.
        - Trace the profile inheritance chain a single resource has to satisfy.
        - Spot the "ambiguous must-support" footguns that produce claimed-conformance disputes.
        - Distinguish **portability** (data moves intact) from **interoperability** (data works intact in another system).
        - Write a one-page gap analysis of US Core for rheumatology, naming what US Core covers, what it doesn't, and what an RA-specific IG layered on top would have to define.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 1. An IG is a versioned package.

        A FHIR **implementation guide** is a published package that says, for a specific use case, exactly what FHIR resources should look like. It bundles together:

        - **Profiles** (StructureDefinitions) that constrain base FHIR resources.
        - **Extensions** (also StructureDefinitions) for data the base spec doesn't have.
        - **Value sets and code systems** that constrain which codes can go in which slots.
        - **CapabilityStatements** describing what conforming servers must support.
        - **Examples** of conforming resources.
        - **Narrative documentation** explaining the why behind each constraint.

        Most importantly: an IG is **versioned**. "US Core 6.1" is a snapshot. Conforming systems claim conformance to a specific version, not to "US Core" in general.

        The IGs you'll meet most:
        """
    )
    return


@app.cell
def _(pd):
    igs = pd.DataFrame(
        [
            {"IG": "US Core", "Scope": "US clinical FHIR exchange (the base IG most US production systems claim).",
             "Anchor URL": "hl7.org/fhir/us/core"},
            {"IG": "mCODE", "Scope": "Minimal Common Oncology Data Elements. Cancer condition, staging, treatments, genetic findings.",
             "Anchor URL": "hl7.org/fhir/us/mcode"},
            {"IG": "IPS", "Scope": "International Patient Summary. Cross-border patient summary exchange.",
             "Anchor URL": "hl7.org/fhir/uv/ips"},
            {"IG": "CARIN BB", "Scope": "Patient access to claims (the IG behind CMS Blue Button 2.0).",
             "Anchor URL": "hl7.org/fhir/us/carin-bb"},
            {"IG": "DaVinci", "Scope": "Payer-provider data exchange: prior authorization, formulary, member match.",
             "Anchor URL": "hl7.org/fhir/us/davinci-pdex (and family)"},
            {"IG": "SDOH-CC", "Scope": "Social determinants of health in clinical care.",
             "Anchor URL": "hl7.org/fhir/us/sdoh-clinicalcare"},
            {"IG": "SMART App Launch", "Scope": "OAuth flow, launch context, scope vocabulary for SMART apps (Track 5 lives here).",
             "Anchor URL": "hl7.org/fhir/smart-app-launch"},
        ]
    )
    igs
    return (igs,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Most production deployments conform to a handful of IGs at once, layered. US Core for the base patient summary. mCODE for the cancer data. DaVinci for payer interactions. SMART for app authentication. Each one constrains a different slice; resources have to satisfy the union.

        ## Idea 2. Anatomy of an IG.

        Open any published IG website and the structure is similar. The IG's home page has tabs for:

        - **Profiles.** The list of StructureDefinitions in the IG.
        - **Extensions.** New data fields the IG defines.
        - **Value sets / Code systems.** The terminology bindings.
        - **Examples.** Conforming resources you can read.
        - **Conformance.** The CapabilityStatement plus the list of profiles a conforming server must support.
        - **Downloads.** The IG packaged as a `.tgz` you can feed to validators.

        Each profile has its own page with four sections that matter most:

        - **Differential.** What the profile changed relative to its parent. Short. Human-readable. This is what the IG author actually wrote.
        - **Snapshot.** The full element list expanded against the base spec. Long. Computed.
        - **Constraints.** Invariants beyond cardinality. ("If `effectivePeriod` is present, both `start` and `end` must be present.")
        - **Must-Support.** The list of must-support elements plus narrative on what "support" means for each.

        For everyday reading, start with the **differential**. Read the snapshot only when you need the full element shape (often when generating code).
        """
    )
    return


@app.cell
def _(mo, pd, us_core_obs_lab):
    _diff_paths = [
        e.get("path", e.get("id", "")) for e in us_core_obs_lab.get("differential", {}).get("element", [])
    ]
    _ms_elements = [e["id"] for e in us_core_obs_lab.get("snapshot", {}).get("element", []) if e.get("mustSupport")]
    _snapshot_count = len(us_core_obs_lab.get("snapshot", {}).get("element", []))

    mo.vstack(
        [
            mo.md("### Worked example 1: US Core Observation Lab"),
            mo.md(
                f"""
This is the canonical "lab result" profile in US Core. The cached StructureDefinition is the real one, downloaded from `{us_core_obs_lab['url']}`.

- **id:** `{us_core_obs_lab['id']}`
- **version:** `{us_core_obs_lab.get('version', '(not set)')}`
- **status:** `{us_core_obs_lab.get('status')}`
- **baseDefinition:** `{us_core_obs_lab['baseDefinition']}` (this profile extends another US Core profile, not the base FHIR Observation directly)
- **differential elements:** {len(_diff_paths)} (the profile's own constraints; what the IG author wrote)
- **snapshot elements:** {_snapshot_count} (the full element list expanded against the base spec)
- **must-support elements:** {len(_ms_elements)}

The differential, in its compact form, names which elements this profile constrains:
"""
            ),
            mo.ui.table(
                pd.DataFrame([{"#": i + 1, "path": p} for i, p in enumerate(_diff_paths)]),
                selection=None,
            ),
            mo.callout(
                mo.md(
                    "Each row in that differential is a place the IG author added a constraint. The most consequential is the slicing on `Observation.category` to require a `laboratory` coding (the `category:us-core` slice). Without this profile, an Observation could omit `category` entirely; with this profile, lab-category coding is mandatory.\n\n"
                    "Notice how short the differential is. **The substantial work of a profile is small.** What the IG author wrote fits in a screen; the rest is inherited."
                ),
                kind="info",
            ),
            mo.md("\nThe full must-support list for US Core Observation Lab:"),
            mo.ui.table(
                pd.DataFrame([{"#": i + 1, "must-support element": m} for i, m in enumerate(_ms_elements)]),
                selection=None,
            ),
            mo.callout(
                mo.md(
                    "Every one of these elements is a contract on the receiver: if the sender sends `interpretation`, the receiver has to handle it; if the sender sends `referenceRange`, the receiver has to handle it. Cardinality (whether the field is required) stays a separate question, set by the spec page for the resource and the profile's own constraints."
                ),
                kind="neutral",
            ),
        ]
    )
    return


@app.cell
def _(mcode_primary_cancer, mo, pd):
    _diff_paths_m = [
        e.get("path", e.get("id", "")) for e in mcode_primary_cancer.get("differential", {}).get("element", [])
    ]
    _ms_elements_m = [e["id"] for e in mcode_primary_cancer.get("snapshot", {}).get("element", []) if e.get("mustSupport")]
    mo.vstack(
        [
            mo.md(
                f"""
### Worked example 2: mCODE Primary Cancer Condition

mCODE (Minimal Common Oncology Data Elements) layers on top of US Core for cancer-specific data. The Primary Cancer Condition profile is its iconic example.

- **id:** `{mcode_primary_cancer['id']}`
- **baseDefinition:** `{mcode_primary_cancer['baseDefinition']}` (extends US Core's Condition Problems and Health Concerns profile, which in turn extends FHIR base Condition)
- **differential elements:** {len(_diff_paths_m)}
- **must-support elements:** {len(_ms_elements_m)}

Inheritance chain:

```
mCODE Primary Cancer Condition
    extends US Core Condition Problems and Health Concerns
        extends FHIR R4 Condition
```

A Condition that claims conformance to mCODE Primary Cancer Condition is implicitly conforming to US Core Condition (because mCODE extends it) and to base Condition. **Constraints accumulate down the chain.** Each level's differential describes only what it adds.

The mCODE differential adds the following:
"""
            ),
            mo.ui.table(
                pd.DataFrame([{"#": i + 1, "path": p} for i, p in enumerate(_diff_paths_m)]),
                selection=None,
            ),
            mo.callout(
                mo.md(
                    "Two extensions, `assertedDate` and `histologyMorphologyBehavior`, are mCODE-specific (cancer registries care about asserted date as distinct from onset date, and ICD-O-3 morphology is a defining oncology concept). The `bodySite` slicing for `locationQualifier` and `lateralityQualifier` lets mCODE record \"left\" vs \"right\" cleanly, which the base Condition resource cannot do. The `stage` extensions support cancer-specific staging.\n\n"
                    "The principle: an IG **constrains** the base and **extends** it where the base doesn't have what's needed. mCODE does both."
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
        ## Idea 3. The must-support footgun.

        Track 3 introduced must-support as a contract on the receiver. Track 4 adds the realistic complication: **what "support" means depends on the IG author's interpretation, and IGs disagree.**

        US Core publishes detailed narrative for each must-support element. mCODE largely does too. Other IGs flag must-support without elaboration and leave the reader guessing. That gap is the source of most claimed-conformance disputes.

        Concrete scenario: two EHR vendors both say they support US Core Observation Lab. One vendor displays the `interpretation` (high/low/normal) flag prominently on the lab result card. The other vendor stores the flag in the database but never surfaces it on any screen. **Both can defensibly claim conformance** if "support" is read loosely as "we can receive and store the field without dropping it." The clinical difference is enormous: one shows you that your patient's CRP came back flagged H; the other shows you only the number.
        """
    )
    return


@app.cell
def _(mo):
    ms_footgun_quiz = mo.ui.radio(
        options=[
            "Both vendors are non-conformant; must-support requires display.",
            "Both vendors are conformant; must-support requires storage, not display.",
            "Vendor A is conformant; Vendor B is non-conformant.",
            "It depends on how that specific IG defines 'support' for the `interpretation` element. Without the IG's narrative being explicit, conformance is ambiguous.",
        ],
        label=(
            "You're evaluating two EHRs that both claim US Core conformance. "
            "Vendor A displays the lab result's `interpretation` flag (e.g., 'H' for high) on the chart card. "
            "Vendor B stores it in the database but never displays it. "
            "Which statement best describes the conformance situation?"
        ),
    )
    ms_footgun_quiz
    return (ms_footgun_quiz,)


@app.cell
def _(mo, ms_footgun_quiz):
    if ms_footgun_quiz.value is None:
        _r = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif ms_footgun_quiz.value.startswith("It depends on how that specific IG"):
        _r = mo.callout(
            mo.md(
                "**Right.** US Core 6.1 is reasonably explicit (its narrative for `interpretation` says the receiver must be able to display the flag), so under US Core 6.1 specifically, Vendor B is the weaker claim. But the general lesson is what matters: **'must-support' without IG-defined narrative is ambiguous**, and 'we support the field' can mean very different things. The right move when evaluating a vendor is to ask for each must-support element: do you display it? Do you let it be searched? Do you round-trip it? What happens if it's absent? Without those specifics, claimed conformance is decorative."
            ),
            kind="success",
        )
    elif ms_footgun_quiz.value.startswith("Both vendors are non-conformant"):
        _r = mo.callout(
            mo.md(
                "**Too strict.** The spec text for must-support doesn't say \"must display.\" It says the receiver has to do something meaningful with the field. What's meaningful is set by the IG's narrative on that element. Some IGs are explicit (US Core says display is expected for `interpretation`); some aren't. Conformance assessment depends on the IG's elaboration, not on the bare must-support flag."
            ),
            kind="warn",
        )
    elif ms_footgun_quiz.value.startswith("Both vendors are conformant"):
        _r = mo.callout(
            mo.md(
                "**Too lenient.** \"Support\" doesn't mean \"merely store.\" That reading would make must-support meaningless: every database stores what you put in it. The intent of must-support is that the receiver does something useful with the field. The argument is over what 'useful' means in a specific IG. Without the IG's narrative being explicit, the answer is ambiguous, not 'both fine.'"
            ),
            kind="warn",
        )
    else:
        _r = mo.callout(
            mo.md(
                "**Almost, but not by general principle.** Under US Core's specific narrative for `interpretation`, Vendor A is the stronger claim and Vendor B's behavior is non-conformant. But the *general* situation, without the IG's narrative, is ambiguous; what makes the answer concrete here is US Core's explicit elaboration of what supporting `interpretation` involves. The fully-correct answer names the dependency on IG narrative."
            ),
            kind="warn",
        )
    _r
    return


@app.cell
def _(callback, forward, mo):
    mo.md(
        r"""
        ## Idea 4. Portability is not interoperability.

        These two get used interchangeably. They aren't the same.

        - **Portability.** I can move my data to another system. The data travels intact. The receiving system doesn't necessarily have to know how to *interpret* it, just how to store it.
        - **Interoperability.** My data works in your system without either of us changing anything. The receiver reads, displays, computes on, and reasons about the data with full fidelity.

        OMOP gives portability. The standard is the table schema; the receiver loads your OMOP data into their own OMOP instance and can run OHDSI tools against it. They didn't need to understand your source EHR's schema.

        FHIR aims at interoperability. The standard is not just the wire format but also the semantics: this is a CRP, this LOINC code, this UCUM unit, this reference range. The receiver doesn't just store the value; they know what it *means* and can do clinical work with it.

        Most real systems need both. Portability tells you how your data exits a system; interoperability tells you whether the next system can read it. An IG sits squarely on the interoperability side: it specifies not just the resource shape but also the value sets, the must-support semantics, and the conformance expectations.

        Shorthand: **portability is one-way (out of your system); interoperability is two-way (between any two systems that speak the same IG).**
        """
    )
    return


@app.cell
def _(callback, mo):
    callback(
        from_course="06",
        to_course="06-learn-fhir Track 0",
        topic="the five-layer interop framework",
        body=(
            "Track 0 named five layers an interop failure can live at: transport, format, structure, terminology, content. "
            "Implementation guides operate primarily on **structure** (the profile says where each fact lives), **terminology** (the value sets bind which codes are acceptable), and partially on **content** (must-support sets receiver-side expectations that imply content capture on the sender). "
            "Transport and format are below the IG layer; they're network and serialization. **Portability** is what happens when you've solved structure and terminology well enough to move data; **interoperability** is when both sides also agree on content semantics."
        ),
    )
    return


@app.cell
def _(forward, mo):
    forward(
        from_course="06",
        to_course="07-data-wrangling-engineering",
        topic="OMOP",
        body=(
            "Course 07 walks OMOP (the OHDSI Common Data Model) in detail. The connection to this track: OMOP solves portability by standardizing on a table schema and a controlled vocabulary; FHIR aims for interoperability by standardizing on resource semantics, profiles, and must-support contracts. "
            "Most research workflows use both: clinical data exits an EHR via FHIR, gets ETL'd into OMOP for analysis, and OMOP-shaped results are sometimes re-emitted as FHIR for clinical feedback. The two standards solve different problems at different layers; treating them as competitors is the wrong frame."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone: a one-page gap analysis of US Core for rheumatology.

        You're the clinical informaticist on a project to build an RA monitoring dashboard. The data layer is FHIR; the conformance claim will be US Core. Before writing a line of code, you need to know what US Core covers for an RA workflow and what it doesn't.

        The exercise has two parts.

        - **Part A.** Rate US Core Observation Lab's coverage of RA monitoring needs, one row per US Core must-support element. For each, decide whether US Core's coverage is sufficient for what an RA workflow needs.
        - **Part B.** Name the RA-specific data the workflow needs that US Core doesn't capture cleanly. For each gap, propose what an "RA Monitoring IG" layered on top of US Core would have to add.

        The final cell assembles your answers into a one-page markdown report you can copy out as your draft.
        """
    )
    return


@app.cell
def _(mo):
    coverage_options = [
        "Covers cleanly",
        "Partial; usable but with caveats",
        "Doesn't cover this need",
    ]

    part_a = mo.ui.dictionary(
        {
            "status": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.status** -- the lab result's status (final, amended, etc.). Covers your need to know whether a CRP is preliminary or final?",
            ),
            "category": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.category** (US Core lab slice) -- categorizes the result as a laboratory observation. Covers your need to filter RA labs out of the broader Observation pool?",
            ),
            "code": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.code** -- the LOINC code. Covers your need to identify CRP, ESR, anti-CCP, RF, hemoglobin, ALT, creatinine?",
            ),
            "subject": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.subject** -- reference to the Patient. Covers your need to attach the lab to the patient?",
            ),
            "encounter": mo.ui.radio(
                coverage_options,
                value="Partial; usable but with caveats",
                label="**Observation.encounter** -- reference to the visit. Covers your need to tie labs to a particular rheumatology follow-up visit?",
            ),
            "effective_x": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.effective[x]** -- when the observation applies. Covers your need to plot CRP over time?",
            ),
            "performer": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.performer** -- who performed the observation. Covers your need to know which lab ran the assay?",
            ),
            "value_x": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.value[x]** -- the actual value with units. Covers your need to capture CRP in mg/L, ESR in mm/h, anti-CCP in U/mL?",
            ),
            "interpretation": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.interpretation** -- the H/L/N flag. Covers your need to know whether a CRP is flagged elevated?",
            ),
            "reference_range": mo.ui.radio(
                coverage_options,
                value="Covers cleanly",
                label="**Observation.referenceRange** -- the assay's reference range. Covers your need to know what 'normal' is for a given CRP assay (which varies by lab)?",
            ),
        }
    )
    mo.vstack(
        [
            mo.md("### Part A. Rate US Core Observation Lab's coverage of RA monitoring needs."),
            part_a,
        ]
    )
    return coverage_options, part_a


@app.cell
def _(mo):
    coverage_for_gaps = [
        "US Core covers this without help",
        "Need a new profile or extension",
        "Need a fresh profile in a custom RA IG",
    ]

    part_b = mo.ui.dictionary(
        {
            "das28_composite": mo.ui.radio(
                coverage_for_gaps,
                value="Need a new profile or extension",
                label="**DAS28-CRP composite score** with its sub-components (TJC, SJC, CRP, PGA). Does US Core's plain Observation give you what you need to represent this cleanly, with the components linked to the parent score?",
            ),
            "joint_counts": mo.ui.radio(
                coverage_for_gaps,
                value="Need a new profile or extension",
                label="**Joint-count assessments (TJC28, SJC28)** as standalone Observations with anatomic detail. Does US Core's Observation capture which joints were examined and which were tender/swollen?",
            ),
            "biologic_line": mo.ui.radio(
                coverage_for_gaps,
                value="Need a new profile or extension",
                label="**Treatment line / sequence on biologics** (which biologic is current, how many prior agents failed, the time on current agent). Does US Core MedicationStatement track this concept?",
            ),
            "treat_to_target": mo.ui.radio(
                coverage_for_gaps,
                value="Need a fresh profile in a custom RA IG",
                label="**Treat-to-target target** (the disease activity goal, e.g., DAS28 < 2.6) and adherence to the plan. Does US Core have a concept for this?",
            ),
            "anti_ccp_baseline": mo.ui.radio(
                coverage_for_gaps,
                value="US Core covers this without help",
                label="**Anti-CCP positivity at diagnosis** as a 'baseline' value, distinct from current value. Does US Core's plain Observation capture the distinction between baseline and current assertions cleanly?",
            ),
        }
    )

    extras = mo.ui.text_area(
        placeholder="Free-text: list any other RA-specific data you'd want captured that US Core doesn't cover.",
        rows=4,
        full_width=True,
        label="**Any other gaps you'd add to the analysis?** (Free text.)",
    )
    mo.vstack(
        [
            mo.md("### Part B. Name the RA-specific gaps."),
            part_b,
            extras,
        ]
    )
    return coverage_for_gaps, extras, part_b


@app.cell
def _(mo):
    summary_notes = mo.ui.text_area(
        placeholder="A few sentences. What's the headline finding from your gap analysis?",
        rows=4,
        full_width=True,
        label=(
            "**Summary.** In one paragraph, what would you tell the project lead about US Core's fit for an RA monitoring dashboard? "
            "Cite specific must-support elements and gaps you identified above."
        ),
    )
    summary_notes
    return (summary_notes,)


@app.cell
def _(extras, mo, part_a, part_b, summary_notes):
    _readable = {
        "status": "Observation.status (result status)",
        "category": "Observation.category (laboratory slice)",
        "code": "Observation.code (LOINC)",
        "subject": "Observation.subject (patient reference)",
        "encounter": "Observation.encounter (visit reference)",
        "effective_x": "Observation.effective[x] (when)",
        "performer": "Observation.performer (who performed)",
        "value_x": "Observation.value[x] (the value with units)",
        "interpretation": "Observation.interpretation (H/L/N flag)",
        "reference_range": "Observation.referenceRange (reference interval)",
    }
    _readable_b = {
        "das28_composite": "DAS28-CRP composite score with linked sub-components",
        "joint_counts": "Joint-count assessments (TJC28, SJC28) with anatomic detail",
        "biologic_line": "Treatment line/sequence tracking on biologics",
        "treat_to_target": "Treat-to-target target and adherence",
        "anti_ccp_baseline": "Anti-CCP baseline vs current distinction",
    }

    _part_a_lines = []
    for k, label in _readable.items():
        v = (part_a.value or {}).get(k, "")
        _part_a_lines.append(f"| {label} | {v} |")

    _part_b_lines = []
    for k, label in _readable_b.items():
        v = (part_b.value or {}).get(k, "")
        _part_b_lines.append(f"| {label} | {v} |")

    _report = f"""# Gap analysis: US Core for an RA monitoring dashboard

**Prepared by:** _(your name here)_
**Reviewed against:** US Core 6.1, Observation Lab profile (`hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab`)

## Summary

{summary_notes.value or '_(write a one-paragraph summary at the top of the notebook to fill this in)_'}

## Part A. US Core Observation Lab coverage of RA monitoring labs

| Must-support element | Coverage for RA monitoring |
|---|---|
{chr(10).join(_part_a_lines)}

## Part B. RA-specific gaps

| Gap | Resolution |
|---|---|
{chr(10).join(_part_b_lines)}

### Other gaps

{extras.value or '_(none noted; add free-text observations to the field above to fill this in)_'}

## Recommendation

If any Part B row is marked **"Need a new profile or extension"** or **"Need a fresh profile in a custom RA IG"**, the project should plan for a small RA-specific implementation guide layered on top of US Core. A reasonable scope for that IG would include:

- A profile for DAS28-CRP as an Observation with `component` slices for TJC, SJC, CRP, and PGA.
- A profile for joint-count assessments with structured `bodySite` slices.
- An extension on MedicationStatement (or a new profile) for treatment-line and prior-failure tracking.
- A profile for the treat-to-target plan as either a CarePlan or a Goal resource.

The tooling for publishing such an IG is the same as any HL7 IG: write profiles in FHIR Shorthand (FSH), compile with SUSHI, publish with the HL7 IG Publisher.
"""

    mo.vstack(
        [
            mo.md("### Your one-page gap analysis report."),
            mo.callout(mo.md(_report), kind="info"),
            mo.md(
                "Copy out the report above as your draft. Edit the summary paragraph and the gap details as your analysis sharpens. "
                "This is the kind of artifact a clinical informatics lead brings to a project kickoff so the engineering and clinical teams can argue from a shared list."
            ),
        ]
    )
    return


@app.cell
def _(mo):
    _reflection = mo.ui.text_area(
        placeholder="A few sentences. Think about what an IG can and can't do for a workflow whose needs aren't fully captured by published profiles.",
        rows=5,
        full_width=True,
        label=(
            "**Reflection.** If you were to actually publish an 'RA Monitoring IG' layered on top of US Core, what would the political/governance work look like? "
            "Who has to agree, what stakeholders would push back, and how would you frame the case to the people who don't already see why US Core isn't enough?"
        ),
    )
    mo.vstack(
        [
            _reflection,
            mo.callout(
                mo.md(
                    "_No answer key. A few moves worth thinking about: "
                    "(1) the ACR (American College of Rheumatology) likely cares about this and has its own informatics workgroup; "
                    "(2) HL7 has a CDS-IS workgroup that authorizes new IGs; "
                    "(3) interoperability cores at the bigger health systems would have opinions about adding more profile-conformance burden; "
                    "(4) most pushback won't be technical; it'll be \"we already have US Core conformance, why does this need to be its own IG?\", and the answer is exactly the gap analysis you just wrote._"
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

        - You put four ideas in place for reading and evaluating implementation guides: an **IG is a versioned package** of profiles plus extensions plus value sets plus narrative; the **anatomy of a profile** is differential plus snapshot plus must-support plus constraints; **must-support's meaning depends on IG narrative**, and "ambiguous must-support" is a real footgun in claimed conformance; **portability and interoperability** are not the same axis, and OMOP and FHIR target them differently.
        - You walked two real published profiles, **US Core Observation Lab** and **mCODE Primary Cancer Condition**, from their actual StructureDefinitions, named their differentials and their must-support lists, and traced the inheritance chain mCODE → US Core → FHIR.
        - You produced a one-page **gap analysis of US Core for rheumatology** as a structured report ready to take into a project kickoff.

        That gap analysis is what fluency in implementation guides actually looks like: less "what does US Core say?" and more "where does it match your workflow, where does it fall short, and what would you add."

        ## What's next.

        **Track 5: SMART on FHIR.** SMART is itself an implementation guide (the SMART App Launch IG), layered on top of US Core. Reading the SMART spec with this track's vocabulary in place (StructureDefinitions, must-support, capability statements, conformance) is what makes SMART feel boring instead of magical. The track-level capstone is a design concept for a SMART app for RA monitoring that uses the gap analysis you just wrote as the underlying data model.
        """
    )
    return


if __name__ == "__main__":
    app.run()
