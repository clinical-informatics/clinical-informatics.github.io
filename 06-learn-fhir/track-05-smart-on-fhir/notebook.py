"""Track 5: SMART on FHIR.

The final track of `06-learn-fhir`. SMART is itself an implementation
guide, layered on top of US Core; Track 4's vocabulary lets the
SMART spec read as another IG rather than as magic. The OAuth dance,
the two launch flavors, the scope vocabulary, and concept-level
introductions to CDS Hooks and Bulk Data are walked with one real
cached well-known/smart-configuration response from the SMART Health
IT sandbox.

Capstone (Socratic): design a SMART app concept for RA monitoring,
leaning on Track 4's gap analysis output as the underlying data
model. Six commit-and-reveal steps via shared.socratic, then an
assembled one-page design brief.

Cross-cell widgets have plain names; cell-internal vars are
underscore-prefixed. Quizzes that have options with shared prefixes
use exact-equality comparison.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import sys
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    # Absolute site path where this notebook's WASM export lives. See the
    # comment in load() below.
    _WASM_DATA_BASE = "/06-learn-fhir/track-05-smart-on-fhir/app"

    def load(filename):
        """Read a JSON file from this notebook's cache/ dir. Local + WASM.

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

    smart_config = load("smart-configuration.json")
    sample_token = load("sample-token-response.json")

    return (
        json,
        load,
        mo,
        pd,
        sample_token,
        smart_config,
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
        # Track 5: SMART on FHIR

        ## SMART is just another IG.

        Most introductions to SMART on FHIR start with OAuth, throw redirects and JWTs at the reader, and lose them in the first ten minutes. There is a simpler frame, and Track 4 built it for you: **SMART on FHIR is an implementation guide**, published at `hl7.org/fhir/smart-app-launch`, layered on top of US Core. Like every other IG, it has profiles, value sets (here, the scope vocabulary), a CapabilityStatement, and worked examples. The OAuth flow is the part that takes longest to describe; structurally, SMART is one more IG.

        By the end of this track:

        - You can name the two launch flavors (EHR launch vs standalone) and which to use when.
        - You can walk the OAuth authorization-code-with-PKCE flow in plain English, step by step.
        - You can read a SMART scope string and tell what it grants.
        - You can spot the "we requested `patient/*.*` for convenience" antipattern when evaluating a vendor.
        - You've drafted a design brief for a SMART app for RA monitoring, building on Track 4's gap analysis.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 1. Authentication is not authorization.

        Two terms that get used interchangeably and shouldn't be. Every SMART concept downstream of this one (OAuth, scopes, launch context, the token response) is doing one of these two jobs, and being clear about which is which is the move that makes the rest of the track land.

        **Authentication (authn) answers *who you are*.** The act of proving identity. "I am Dr. Bennett." The mechanism could be a password plus a second factor, a smart card, a biometric, or a digitally signed credential. The end product is the server being convinced that the entity on the other end is who they claim to be.

        **Authorization (authz) answers *what you're allowed to do*.** The act of granting access to specific resources or operations. "Dr. Bennett is allowed to read Ms. Reyes's chart." Authorization happens *after* authentication: the system first figures out who you are, then decides what you can do.

        Shorthand: **authn is who, authz is what.**

        The two are independent. A clinician can be authenticated (the system knows it's really Dr. Bennett) and still be unauthorized for a specific action (Dr. Bennett is on staff but isn't on this patient's care team, so reading the chart is blocked). The reverse also matters: an authenticated user might have broad authorization that the application doesn't need (Dr. Bennett's badge gets her into the whole chart, but the RA monitoring app should only be able to read what's relevant to RA).

        **Why SMART has to do both:**

        - A FHIR server holds patient data. Every request has to answer two questions: *who is asking?* (authn) and *what is this request allowed to read or write?* (authz).
        - SMART uses **OpenID Connect** (a thin layer on top of OAuth 2.0) for the *authn* answer. When your app requests the `openid fhirUser` scopes, the token response includes an `id_token` (a signed JWT) carrying claims about which user is logged in.
        - SMART uses **OAuth 2.0 scopes** for the *authz* answer. The access token, presented on every FHIR request as `Authorization: Bearer <token>`, encodes which resources and operations the bearer is allowed to perform.
        - **Launch context** is a third axis. Even within what's authorized, the launch context narrows the *current focus*. The token might authorize reading any patient the user can see, but the launch context says "this session is about Ms. Reyes specifically." Without launch context, the app would have to ask the user to pick a patient on every launch.

        A useful analogy for the three:

        - **Authentication** is the bouncer at the door checking your ID.
        - **Authorization** is the wristband saying which areas of the venue you can access.
        - **Launch context** is your seat assignment for tonight's show.

        The OAuth dance you're about to see is doing all three at once.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 2. Two launch flavors.

        A SMART app starts up in one of two ways. Most apps support one; some support both.
        """
    )
    return


@app.cell
def _(pd):
    flavors = pd.DataFrame(
        [
            {
                "Flavor": "EHR launch",
                "How it starts": "The clinician clicks a button inside the EHR (sidebar, chart widget, order-entry add-on). The EHR redirects the browser to the app's launch URL, passing `iss` (the FHIR base URL) and `launch` (a one-time launch token).",
                "Where context comes from": "The EHR knows the patient, the encounter, and the user. It packages them into the launch context that comes back in the token response.",
                "Typical use": "Clinical-workflow apps (chart viewers, decision support, order-entry helpers).",
                "Capability name": "`launch-ehr`",
            },
            {
                "Flavor": "Standalone launch",
                "How it starts": "The user (clinician or patient) starts at the app directly. The app knows which FHIR server to talk to and initiates the OAuth flow itself.",
                "Where context comes from": "The user authenticates during the flow; if they have access to multiple patients, they pick one during auth and that becomes the launch context.",
                "Typical use": "Patient-facing apps (`launch/patient` scope, MyChart-style portals), researcher tools, analytics dashboards.",
                "Capability name": "`launch-standalone`",
            },
        ]
    )
    flavors
    return (flavors,)


@app.cell
def _(mo):
    mo.md(
        r"""
        A SMART-enabled FHIR server lists which launch flavors it supports in its `/.well-known/smart-configuration` discovery document. The cached example below is from the SMART Health IT sandbox (`launch.smarthealthit.org/v/r4`), the canonical public SMART playground.
        """
    )
    return


@app.cell
def _(mo, smart_config):
    _caps = smart_config.get("capabilities", [])
    _scopes = smart_config.get("scopes_supported", [])
    _supports_ehr = "launch-ehr" in _caps
    _supports_standalone = "launch-standalone" in _caps

    mo.callout(
        mo.md(
            f"""
**SMART configuration from `{smart_config.get('issuer', '(no issuer)')}`:**

- **authorization_endpoint:** `{smart_config['authorization_endpoint']}`
- **token_endpoint:** `{smart_config['token_endpoint']}`
- **introspection_endpoint:** `{smart_config.get('introspection_endpoint', '(not advertised)')}`
- **grant types supported:** {', '.join(smart_config.get('grant_types_supported', []))}
- **response types supported:** {', '.join(smart_config.get('response_types_supported', []))}
- **PKCE code-challenge methods:** {', '.join(smart_config.get('code_challenge_methods_supported', []))}

This server supports **EHR launch:** {"yes" if _supports_ehr else "no"}; **standalone launch:** {"yes" if _supports_standalone else "no"}.

**Capabilities advertised** ({len(_caps)}): `{', '.join(_caps)}`.

**Scopes supported** ({len(_scopes)}): `{', '.join(_scopes)}`.

The authorization and token endpoints are what your SMART client points its OAuth library at. The capabilities list tells you which SMART features the server has implemented; `context-ehr-patient` for example means the server can return a `patient` context value in EHR-launch token responses. The scopes list is the SMART scope vocabulary the server accepts (we'll come back to it).
"""
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 3. The OAuth dance, in plain English.

        SMART uses OAuth 2.0's authorization-code-with-PKCE flow for authorization, with OpenID Connect layered on for authentication. Six steps that matter clinically. The cryptographic parts (PKCE, JWT signatures) are handled by libraries; the clinically interesting parts are the **scopes** and the **launch context**.

        1. **Discover.** The app fetches `<fhir-base>/.well-known/smart-configuration` (the document you just saw) and reads the `authorization_endpoint` and `token_endpoint` URLs.
        2. **Authorize.** The app redirects the browser to the authorization endpoint with a query string naming itself (`client_id`), the scopes it wants, where to redirect back to (`redirect_uri`), a state token (to prevent CSRF), and a PKCE code challenge (to prove later that the same app finishes the flow).
        3. **User consents (or the EHR auto-grants).** In EHR launch, the EHR usually auto-grants the scopes that match the existing user's permissions. In standalone launch, the user sees a consent screen and approves the scopes.
        4. **Authorization code returned.** The authorization endpoint redirects the browser back to the app's `redirect_uri` with a one-time `code` parameter.
        5. **Token exchange.** The app POSTs the `code`, its `client_id`, the `redirect_uri`, and the PKCE code verifier to the token endpoint. The server validates everything and returns a **token response** containing the access token, the granted scope, an expiration, optionally a refresh token, and the launch context (`patient`, `encounter`, etc.).
        6. **API calls.** The app makes FHIR requests against the FHIR base URL, passing the access token as `Authorization: Bearer <access_token>`. Every request is scoped by what the token allows.

        A representative token response (what step 5 returns) looks like the JSON below. This is the example shape from the SMART App Launch IG; a real production response has the same fields with real values.
        """
    )
    return


@app.cell
def _(json, mo, sample_token):
    _displayable = {k: v for k, v in sample_token.items() if k != "_note"}
    mo.vstack(
        [
            mo.md(
                f"""
```json
{json.dumps(_displayable, indent=2)}
```
"""
            ),
            mo.callout(
                mo.md(sample_token.get("_note", "")),
                kind="info",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Three things to notice in that token response.

        - **`patient`** is the launch context. Your app uses this value to scope every subsequent FHIR query: `GET /Observation?subject=Patient/<patient>&...`. Without it, the app has no idea which patient is in focus.
        - **`scope`** is what the server *granted*, not necessarily what the app *asked for*. An app that asked for `patient/*.write` might get back `patient/Observation.read patient/Condition.read` if the server narrowed the grant. Production apps have to handle this gracefully.
        - **`id_token`** is the OpenID Connect identity token. Decoded, it carries claims about the **launching user** (the clinician). The `fhirUser` claim is a relative reference to the user's Practitioner resource on the FHIR server. This is how the app knows which clinician is using it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 4. Scopes name what the app gets to see (this is the authorization layer).

        SMART scopes have three pieces.

        **Context scopes** request launch context fields.

        - `launch` -- EHR launch context (patient + encounter + whatever the EHR provides).
        - `launch/patient` -- standalone launch with a patient-picker step.
        - `launch/encounter` -- standalone launch with an encounter-picker step.
        - `openid fhirUser` -- the launching user's identity, returned as an OpenID Connect ID token.
        - `offline_access` -- the app wants a refresh token (persistent access after the user logs out).

        **Resource scopes** request FHIR resource access. Shape: `<context>/<ResourceType>.<operation>`.

        - `<context>` is `patient` (data for the launch-context patient only), `user` (data the launching user can see, across patients), or `system` (no user; for backend services).
        - `<ResourceType>` is a resource name or `*` for all.
        - `<operation>` is `read`, `write`, or `*`.

        **Granular scopes** (SMART v2) let you narrow further with query parameters: `patient/Observation.read?category=laboratory` requests only lab observations.

        A real app request typically combines context and resource scopes:

        ```
        launch openid fhirUser patient/Observation.read patient/Condition.read patient/MedicationStatement.read offline_access
        ```

        That's "EHR-launch context, plus the launching user's identity, plus read access to observations/conditions/medications for the launch-context patient, plus a refresh token for persistent access."
        """
    )
    return


@app.cell
def _(mo):
    scope_quiz = mo.ui.radio(
        options=[
            "`patient/Observation.read patient/Condition.read patient/MedicationStatement.read launch openid fhirUser`",
            "`patient/*.* user/*.* offline_access launch openid`",
            "`system/Observation.read system/Condition.read system/MedicationStatement.read`",
            "`launch patient/DiagnosticReport.read patient/AllergyIntolerance.write offline_access`",
        ],
        label=(
            "You're building a read-only chart-summary app that launches from inside an EHR, reads observations / conditions / medications for the patient in focus, and never writes back. "
            "Which scope request best matches \"the smallest scope that does the job\"?"
        ),
    )
    scope_quiz
    return (scope_quiz,)


@app.cell
def _(mo, scope_quiz):
    _v = scope_quiz.value
    _options = {
        "right": "`patient/Observation.read patient/Condition.read patient/MedicationStatement.read launch openid fhirUser`",
        "broad": "`patient/*.* user/*.* offline_access launch openid`",
        "system": "`system/Observation.read system/Condition.read system/MedicationStatement.read`",
        "wrong_resources": "`launch patient/DiagnosticReport.read patient/AllergyIntolerance.write offline_access`",
    }
    if _v is None:
        _r = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif _v == _options["right"]:
        _r = mo.callout(
            mo.md(
                "**Right.** Three resource scopes, all `read`, all `patient/` (scoped to the launch-context patient). Plus `launch` for EHR-launch context, `openid fhirUser` for the clinician's identity. No `offline_access` because a chart-summary app doesn't need persistent access beyond the user's session. This is the canonical principle of least privilege: ask for what the app needs and nothing more."
            ),
            kind="success",
        )
    elif _v == _options["broad"]:
        _r = mo.callout(
            mo.md(
                "**This is the antipattern.** `patient/*.*` plus `user/*.*` plus `offline_access` asks for read and write access to every resource type, both for the launch-context patient and across the launching user's whole patient panel, plus a refresh token. That's enormously more than a read-only chart-summary app needs. A vendor that requests this kind of scope for a feature that doesn't justify it is a real yellow flag. The right pattern is to enumerate the specific resource types and operations the app actually uses."
            ),
            kind="warn",
        )
    elif _v == _options["system"]:
        _r = mo.callout(
            mo.md(
                "**No.** `system/` scopes are for backend services authenticating with the SMART backend-services flow (no user context), used for population-scale data access like Bulk Data exports. For a user-launched chart-summary app, you want `patient/` scopes scoped to the launch-context patient, not system-level access."
            ),
            kind="warn",
        )
    else:
        _r = mo.callout(
            mo.md(
                "**Close, but mismatched.** The app needs Observation, Condition, and MedicationStatement (or MedicationRequest), not DiagnosticReport and AllergyIntolerance. And the app is read-only, so requesting `.write` on AllergyIntolerance is asking for more than the app needs. Match the scopes to the actual data the app reads."
            ),
            kind="warn",
        )
    _r
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 5. CDS Hooks, at concept level.

        CDS Hooks is a separate spec from SMART, but they often appear together. SMART is for **user-launched apps**; CDS Hooks is for **event-driven services**.

        A CDS Hooks service is a small web service the EHR calls at specific workflow moments. The three most common hooks:

        | Hook | When it fires | Typical use |
        |---|---|---|
        | `patient-view` | The clinician opens a patient's chart. Once per chart open. | Surface gaps in care, abnormal results that need attention, screening reminders. |
        | `order-select` | The clinician has started entering an order but hasn't signed it. Fires as the order is being composed. | Suggest alternative orders, surface drug-drug interactions, recommend lab monitoring. |
        | `order-sign` | The clinician is about to sign an order. Last chance before commit. | Final safety checks, hard stops for severe contraindications. |

        The EHR sends a JSON request to the CDS service's URL with the FHIR context (patient ID, encounter ID, the draft order). The service responds with a list of **cards**: small UI elements containing a summary, optional detail text, optional source links, and optional **suggestions** (proposed alternative actions the EHR can apply if the clinician accepts them).

        CDS Hooks uses FHIR resources as its data payload but isn't itself a FHIR API. The service typically reads from the EHR's FHIR server (often via a SMART scope granted to the service) to gather what it needs to decide what cards to return.

        Course 12 (Clinical decision support) walks CDS Hooks systematically. For Track 5 the concept-level pattern is enough: a hook fires, a service responds with cards, the EHR renders them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 6. Bulk Data ($export), at concept level.

        Where SMART App Launch scopes a request to one patient, **Bulk Data** is for "give me observations for everyone in this group, asynchronously." This is what powers most modern FHIR-based research and quality measurement.

        The flow, in four steps:

        1. **Authenticate** with `system/*` scopes via the SMART backend-services flow (no user, just a signed JWT proving the client is who it claims to be).
        2. **Issue `$export`** on a Group, Patient, or the system root: `GET /Group/<id>/$export?_type=Observation,Condition`. The server returns `202 Accepted` with a status-polling URL in the `Content-Location` header. This is async: the server doesn't return data right away.
        3. **Poll the status URL** until the server reports completion. The completed response is JSON listing one or more NDJSON file URLs, one per resource type.
        4. **Download the NDJSON files** and process them. Each file has one resource per line (newline-delimited JSON), which streams well at large scales.

        Bulk Data is what your research-cohort or quality-measurement pipeline uses to pull a population's worth of FHIR data without making 50,000 individual GET requests. The IG is at `hl7.org/fhir/uv/bulkdata`. For everyday clinical-app work, you won't write Bulk Data clients. For research and population health, you will.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capstone: design a SMART app for RA monitoring.

        You did the gap analysis in Track 4: US Core covers RA labs reasonably well, but leaves DAS28 composite scoring, joint-count assessments, biologic-line tracking, and treat-to-target as gaps that a custom IG would have to close. Now you're designing the SMART app that sits on top of that data model: an in-EHR rheumatology dashboard that gives a treating clinician the full picture for an RA patient on a single screen.

        Six commit-and-reveal steps. Each asks you to commit a written answer before the sample reveals. There are no single right answers; the point is that the design questions get answered explicitly and your reasoning is on paper. The final cell assembles your six answers into a one-page design brief you can copy out.
        """
    )
    return


@app.cell
def _(commit_text):
    cap_problem, cap_problem_ready = commit_text(
        "**Step 1. Problem statement.** What clinical problem does this app solve, who is the intended user, and what's the headline thing they should be able to do with it that they currently can't (or that takes them too many clicks)? One short paragraph.",
        min_chars=120,
    )
    cap_problem
    return cap_problem, cap_problem_ready


@app.cell
def _(cap_problem, cap_problem_ready, mo, reveal):
    mo.stop(
        not cap_problem_ready(),
        mo.md("_Commit your problem statement above. The sample unlocks when you do._"),
    )
    _sample = (
        "Rheumatologists managing patients on biologic DMARDs need to make treat-to-target decisions every visit, "
        "and the data that informs those decisions is scattered across the EHR: DAS28 components in flowsheets, "
        "CRP and ESR in lab results, current medications in the med list, treatment history in the chart, and the "
        "patient's own pain/global assessment usually nowhere structured. The app gives the treating rheumatologist "
        "a single screen, opened from inside the EHR for the patient in focus, that shows the four-year disease-activity "
        "trajectory (DAS28-CRP over time), the current regimen with biologic-line context, the current treat-to-target "
        "status, and the next steps the EULAR guideline implies. The clinician can capture this visit's joint counts "
        "and patient-global VAS directly into the app and have those values committed back to the EHR as structured "
        "Observations. The headline action: replace ten clicks across five EHR sections with one chart-glance plus one "
        "structured-capture form."
    )
    reveal(cap_problem.value, _sample, learner_label="Your problem statement")
    return


@app.cell
def _(commit_text):
    cap_launch, cap_launch_ready = commit_text(
        "**Step 2. Launch flavor.** Which SMART launch flavor (`launch-ehr` or `launch-standalone`) does the app use, and why? Mention whether the app also supports the other flavor for any specific use case.",
        min_chars=80,
    )
    cap_launch
    return cap_launch, cap_launch_ready


@app.cell
def _(cap_launch, cap_launch_ready, mo, reveal):
    mo.stop(
        not cap_launch_ready(),
        mo.md("_Commit your launch-flavor decision above. The sample unlocks when you do._"),
    )
    _sample = (
        "**Primary: EHR launch (`launch-ehr`).** The clinical workflow is \"clinician opens the patient's chart, clicks the rheumatology "
        "tab on the sidebar.\" The patient context is already established by the EHR; the app inherits it instantly, no second login. "
        "Token response carries `patient` and `encounter` so the app immediately knows whose record to render.\n\n"
        "**Secondary: standalone launch (`launch-standalone` with `launch/patient`)** is supported for two use cases: (1) the clinician on "
        "their iPad outside the EHR network during a home visit or telehealth, where they want the same view; (2) a research-time audit "
        "use case where the rheumatology QI lead wants to look up a specific patient's trajectory without going through the EHR's chart "
        "navigation. Both standalone paths require the user to pick a patient during auth; the app's UX for that step is identical to "
        "the EHR-launched view once a patient is selected."
    )
    reveal(cap_launch.value, _sample, learner_label="Your launch-flavor decision")
    return


@app.cell
def _(commit_text):
    cap_scopes, cap_scopes_ready = commit_text(
        "**Step 3. Scopes.** What scopes does the app request? List them as the actual scope strings, and justify each one in a few words. Be explicit about read vs write and about resource types.",
        min_chars=150,
    )
    cap_scopes
    return cap_scopes, cap_scopes_ready


@app.cell
def _(cap_scopes, cap_scopes_ready, mo, reveal):
    mo.stop(
        not cap_scopes_ready(),
        mo.md("_Commit your scope list above. The sample unlocks when you do._"),
    )
    _sample = (
        "Requested scope string:\n\n"
        "```\n"
        "launch openid fhirUser\n"
        "patient/Patient.read\n"
        "patient/Condition.read\n"
        "patient/Observation.read\n"
        "patient/MedicationStatement.read\n"
        "patient/MedicationRequest.read\n"
        "patient/AllergyIntolerance.read\n"
        "patient/Encounter.read\n"
        "patient/Observation.write\n"
        "```\n\n"
        "Justifications:\n\n"
        "- `launch openid fhirUser`: EHR launch context plus the launching clinician's identity (so the app can stamp the Observations it writes with the right `performer` reference).\n"
        "- Six `patient/*.read` scopes for the resource types the app reads. Notice this is narrower than `patient/*.read`: we enumerate exactly the seven resource types we touch. A reviewer can audit the scope string and know precisely what the app can see.\n"
        "- One `patient/Observation.write` because the app captures new joint-count, patient-global, and DAS28 Observations during the visit. We do NOT request `patient/*.write`; the only resource the app writes is Observation.\n\n"
        "Deliberately **not requested**:\n\n"
        "- `offline_access`: the app does not need persistent access after the clinician's session ends. A chart-summary view doesn't need a refresh token.\n"
        "- `user/*` scopes: the app reads only the launch-context patient, not the clinician's whole panel.\n"
        "- `system/*` scopes: this is a user-launched app, not a backend service."
    )
    reveal(cap_scopes.value, _sample, learner_label="Your scope list")
    return


@app.cell
def _(commit_text):
    cap_ui, cap_ui_ready = commit_text(
        "**Step 4. UI surface.** Name the two or three primary screens / states the app has, what each one shows, and which screen is the default the clinician sees right after launch. Keep it product-spec brief, two or three sentences per screen.",
        min_chars=150,
    )
    cap_ui
    return cap_ui, cap_ui_ready


@app.cell
def _(cap_ui, cap_ui_ready, mo, reveal):
    mo.stop(
        not cap_ui_ready(),
        mo.md("_Commit your UI surface above. The sample unlocks when you do._"),
    )
    _sample = (
        "**1. Disease activity timeline (default landing screen).** A single-page view with a four-year DAS28-CRP trajectory chart at the top (the chart from Track 2's capstone, adapted for one patient), the current regimen and biologic-line below it, and the most recent CRP / ESR / TJC / SJC / PGA values as a small grid on the right. The headline number is the most recent DAS28-CRP with EULAR category color-coded. The clinician sees this within a second of launch.\n\n"
        "**2. Today's visit capture form.** Reached by clicking \"capture today's visit\" on the timeline screen. A short form: TJC slider, SJC slider, patient-global VAS, and a notes field. As the clinician fills it in, the app calculates and displays DAS28-CRP live (using the most recent CRP from the timeline). Save commits four new Observations (TJC, SJC, PGA, DAS28-CRP) back to the EHR's FHIR endpoint with the encounter reference pre-populated. After save, the timeline screen refreshes to include the new point.\n\n"
        "**3. Regimen and history detail.** A drill-down from the timeline screen for the medication and treatment-history detail: full med list with start/stop dates, prior biologics, treatment-line numbers. Read-only; the app doesn't manage prescribing."
    )
    reveal(cap_ui.value, _sample, learner_label="Your UI surface")
    return


@app.cell
def _(commit_text):
    cap_data, cap_data_ready = commit_text(
        "**Step 5. FHIR data needs.** For each screen above, name the FHIR queries the app issues. Be specific about resource types, search parameters, and what gets done with the response. This is where Track 4's gap analysis pays off: name the gaps (DAS28 components, joint counts, treat-to-target) and how your app handles them given that US Core doesn't fully cover them.",
        min_chars=300,
    )
    cap_data
    return cap_data, cap_data_ready


@app.cell
def _(cap_data, cap_data_ready, mo, reveal):
    mo.stop(
        not cap_data_ready(),
        mo.md("_Commit your data inventory above. The sample unlocks when you do._"),
    )
    _sample = (
        "**Screen 1 (timeline). On launch, the app fires four parallel queries:**\n\n"
        "- `GET /Patient/<patient>` (one Patient by id) for demographics.\n"
        "- `GET /Observation?subject=Patient/<patient>&code=http://loinc.org|1988-5,4537-7,76374-2&_sort=-date&_count=200` for CRP, ESR, DAS28-CRP over time.\n"
        "- `GET /MedicationStatement?subject=Patient/<patient>&status=active` for current regimen, plus a follow-up paged search with status=`stopped` for treatment history.\n"
        "- `GET /Condition?subject=Patient/<patient>&category=problem-list-item` for the problem list (to confirm RA diagnosis and pick up any comorbidities).\n\n"
        "**Screen 2 (today's visit capture).** No additional reads beyond what the timeline already loaded. On save: a `transaction` Bundle POSTed to `/` with four Observation entries (TJC, SJC, PGA, DAS28-CRP), each with `subject` and `encounter` set to the launch context.\n\n"
        "**Screen 3 (regimen detail).** Reuses the MedicationStatement results from screen 1; no new query unless the user clicks an individual medication, which fires `GET /MedicationStatement/<id>` for the full resource.\n\n"
        "**Track 4 gap impact.** Three places where US Core doesn't cleanly cover what the app needs:\n\n"
        "- *DAS28-CRP composite scoring:* US Core doesn't define a profile that links a parent Observation (DAS28) to component Observations (TJC, SJC, PGA, CRP). The app's workaround is to write a parent DAS28-CRP Observation with the calculated value plus a `derivedFrom` reference to each of the four contributing Observations. Reviewers conforming strictly to US Core may not surface `derivedFrom` in their UI; this is an explicit known limitation of the design.\n"
        "- *Joint-count assessments with anatomic detail:* the app writes joint counts as a single integer (TJC28, SJC28) using a LOINC code, without the joint-by-joint structure. Capturing which joints were involved would require either an extension or a richer profile, both of which are deferred to a v2 of the app.\n"
        "- *Biologic-line tracking:* there's no FHIR field on MedicationStatement for \"this is the patient's third biologic.\" The app computes the line number client-side from the start/stop dates of past biologics, which is brittle. A v2 of the app would write the line number into an extension on MedicationStatement, defined in a small RA Monitoring IG layered on top of US Core."
    )
    reveal(cap_data.value, _sample, learner_label="Your data inventory")
    return


@app.cell
def _(commit_text):
    cap_hook, cap_hook_ready = commit_text(
        "**Step 6. CDS Hook integration (optional but recommended).** Does the app also register a CDS Hooks service alongside its SMART app? If yes, which hook does it register, what does the service do, and what cards does it return? If no, justify why a hook would add no value here.",
        min_chars=120,
    )
    cap_hook
    return cap_hook, cap_hook_ready


@app.cell
def _(cap_hook, cap_hook_ready, mo, reveal):
    mo.stop(
        not cap_hook_ready(),
        mo.md("_Commit your CDS Hooks decision above. The sample unlocks when you do._"),
    )
    _sample = (
        "**Yes; the app also registers a `patient-view` CDS Hooks service.**\n\n"
        "When the clinician opens any patient's chart, the EHR fires `patient-view` to the service. The service uses a SMART backend-services token (`system/Patient.read system/Condition.read system/Observation.read`) to look up: does this patient have a Condition with an RA code? If yes, does the patient have a DAS28-CRP measured within the last 90 days?\n\n"
        "If the patient has RA and no recent DAS28, the service returns a **card** with:\n\n"
        "- *summary:* \"This RA patient does not have a DAS28-CRP recorded in the last 90 days.\"\n"
        "- *indicator:* `info` (not `warning`, not `critical`).\n"
        "- *detail:* a one-line rationale (\"EULAR treat-to-target recommends DAS28-CRP every 3 months until target, then every 6.\")\n"
        "- A **suggestion** containing a `Launch Smart App` action that opens the SMART app directly to its visit-capture screen.\n\n"
        "If the patient has RA and a recent DAS28 in remission/low: the service returns no card. If DAS28 is moderate or high and not currently being escalated, the service returns a card suggesting the SMART app. The card never auto-launches; the clinician chooses to act on it.\n\n"
        "Why this works: the hook acts as the *entry point* for the SMART app for the patients who'd benefit from it most, while leaving the app available manually for everyone else. The app and the hook are both pieces of the same service from the clinician's perspective; they're two complementary technical integrations of the same RA-monitoring capability."
    )
    reveal(cap_hook.value, _sample, learner_label="Your CDS Hooks decision")
    return


@app.cell
def _(cap_data, cap_hook, cap_launch, cap_problem, cap_scopes, cap_ui, mo):
    _brief = f"""# SMART app design brief: RA monitoring dashboard

**Prepared by:** _(your name)_  **Date:** _(today)_  **Target environment:** any SMART-enabled FHIR R4 endpoint conforming to US Core.

## 1. Problem statement

{cap_problem.value or '_(not yet written)_'}

## 2. Launch flavor

{cap_launch.value or '_(not yet written)_'}

## 3. Scopes requested

{cap_scopes.value or '_(not yet written)_'}

## 4. UI surface

{cap_ui.value or '_(not yet written)_'}

## 5. FHIR data needs and known IG gaps

{cap_data.value or '_(not yet written)_'}

## 6. CDS Hooks integration

{cap_hook.value or '_(not yet written)_'}

---

**Next steps before build:**

- Run this design brief past a rheumatologist who isn't on the build team for a clinical sanity check (especially the workflow described in section 1 and the joint-count capture in section 4).
- Stand up a SMART-enabled FHIR sandbox (the SMART Health IT sandbox is the canonical free option) and prototype the launch flow with a stub UI before building the real screens.
- Decide whether to publish a small "RA Monitoring IG" layered on top of US Core to formalize the gaps identified in section 5 (DAS28 composite, joint-count details, biologic-line tracking). A small IG plus this app together is a cleaner story to take to other institutions than an app that uses extensions ad hoc.
"""

    mo.vstack(
        [
            mo.md("### Your one-page design brief."),
            mo.callout(mo.md(_brief), kind="info"),
            mo.md(
                "Copy the brief above out of the browser (Cmd/Ctrl + P → Save as PDF, or select-and-copy). This is the artifact you'd bring to a project kickoff or a sponsor review."
            ),
        ]
    )
    return


@app.cell
def _(mo):
    _reflection = mo.ui.text_area(
        placeholder="A paragraph. Think about what the design brief skips, what risks you'd flag for the security review, what assumptions about the EHR you're making.",
        rows=5,
        full_width=True,
        label=(
            "**Reflection.** If you took this design brief to your hospital's security review and clinical informatics committee, what's the *first* objection you'd expect, and how would you answer it? "
            "Bonus: what assumption about the EHR (Epic, Cerner, Athena, etc.) does your design depend on, and what happens if that assumption is wrong?"
        ),
    )
    mo.vstack(
        [
            _reflection,
            mo.callout(
                mo.md(
                    "_No answer key. A few likely objection lines: "
                    "(1) why does this need to be a separate app vs a built-in EHR feature? "
                    "(2) what data leaves the patient's record (any of it? logs?), where does it go, and how is it retained? "
                    "(3) the joint-count UI in screen 2 changes clinical documentation patterns -- has nursing leadership signed off? "
                    "(4) the CDS Hook fires on every chart open; what's the additional load on the FHIR endpoint and what happens if the service is slow or down? "
                    "(5) some EHR vendors implement SMART selectively or with constraints (Epic's App Orchard had its own dev-program requirements; Cerner's certification model is different) -- which vendor are we starting with, and what's the matrix of behavior changes across the others? "
                    "(6) the design assumes the EHR's FHIR endpoint exposes DAS28 sub-components as discrete Observations; some EHRs put DAS28 in a single text flowsheet field that doesn't make it through to FHIR. What's the migration path for those sites?_"
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

        - You put five ideas in place for SMART on FHIR: **authentication is who, authorization is what**, and SMART solves both via OpenID Connect plus OAuth 2.0 scopes plus launch context; SMART is **another implementation guide** layered on US Core; there are **two launch flavors** (EHR vs standalone) and the choice is workflow-driven; the **OAuth dance** is six steps with one fetch-discovery-and-redirect plus a token exchange; **scopes** are the contract for what the app can read and write, and "the smallest scope that does the job" is the right design instinct.
        - You picked up CDS Hooks and Bulk Data at the concept level: hooks are event-driven services that return cards into the EHR's workflow; Bulk Data is population-scale async data access via `$export`.
        - You wrote a one-page SMART app design brief for an RA monitoring dashboard, naming the problem, the launch flavor, the scopes, the UI surface, the FHIR data needs (with explicit reference to the Track 4 gap analysis output), and an optional CDS Hook integration that completes the story.

        That brief is what a clinical informaticist actually produces before any engineering work begins. The technical content of the rest of this course (Tracks 0 through 4) is what lets it be specific instead of decorative.

        ## What's next.

        **The course-level capstone (in `06-learn-fhir/capstone/`).** The capstone asks you to author and validate a complete FHIR record for Ms. Reyes on hapi.fhir.org, applying everything from Tracks 1 through 4. Track 3's authoring patterns scale up to her whole record; Track 4's profile awareness keeps the resources conformant. The capstone is the synthesis of the whole course.

        After this course, the curriculum continues: course 07 builds the OMOP and data-engineering layer (referenced via the forward callout in Track 4), course 09 brings AI evaluation into the picture, and course 12 deepens CDS Hooks into a full CDS course where the FHIR fluency you built here is the foundation.
        """
    )
    return


if __name__ == "__main__":
    app.run()
