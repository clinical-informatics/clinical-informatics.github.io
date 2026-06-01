"""Track 03: CDS Hooks.

CDS Hooks is the standards-based delivery layer for CDS. A hook is a
defined workflow moment at which the EHR calls out to an external CDS
service and receives back a list of recommendation cards. The track
walks the architecture, the three load-bearing hooks (patient-view,
order-select, order-sign), the JSON request and response payloads, and
an end-to-end card-design exercise on a simulated Reyes adalimumab
order-sign.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import types

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "06": "Learn FHIR",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return json, mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: CDS Hooks

        ## The architecture

        CDS Hooks is the standards-based delivery layer for CDS. The architecture has four parts and one shared vocabulary.

        - **The EHR.** Whatever EHR the clinician is in.
        - **The hook trigger.** A defined workflow moment (the clinician opened a chart, the clinician selected a medication, the clinician is about to sign an order) implemented by the EHR vendor as a documented event.
        - **The CDS service.** An external service the institution has registered to listen at a particular hook. The service lives outside the EHR, communicates over HTTPS, accepts a structured JSON request, and returns a structured JSON response.
        - **The card.** The response payload. A card carries a summary, a detailed explanation, source attribution, and zero or more suggested actions the clinician can accept or reject inline.

        The hook-trigger event causes the EHR to send a request to each registered CDS service. Each service returns a (possibly empty) list of cards. The EHR aggregates the cards from all services and displays them at the appropriate place in the workflow.

        The architecture is the standards-based replacement for vendor-built-in alerts. Vendor-built-in alerts live inside the EHR's rules engine and are configured per-tenant; CDS Hooks services live outside the EHR and are configured per-institution. The institution that adopts CDS Hooks-based alerts replaces the vendor-internal rules-engine work with a registry of external CDS services it owns and can update independently of the EHR vendor.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The three load-bearing hooks

        The CDS Hooks specification names a dozen hooks. Three account for most production traffic.
        """
    )
    return


@app.cell
def _(pd):
    hooks_table = pd.DataFrame(
        [
            {
                "Hook": "patient-view",
                "When it fires": "When the clinician opens a patient's chart.",
                "What's in the request": "Patient ID, encounter ID, the user (clinician) identifier, optional FHIR prefetch resources (recent labs, current meds, problem list).",
                "Typical card content": "Information about the patient's overall state, gaps in care, risk-stratification flags. Cards at patient-view are typically informational, not action-required.",
                "Example": "RA patient with rising CRP trend across the last 3 visits. Card surfaces the trend and suggests considering a treatment escalation discussion at this visit.",
            },
            {
                "Hook": "order-select",
                "When it fires": "When the clinician selects a medication or test order, before signing.",
                "What's in the request": "The candidate order (drug, dose, route, frequency, indication) plus patient context.",
                "Typical card content": "Drug-drug interactions, dose adjustments, alternative-therapy suggestions, formulary information. Cards at order-select often carry suggested-action changes.",
                "Example": "Clinician selects adalimumab for an RA patient. Card surfaces the TB-screening-required prerequisite and offers to add a QuantiFERON order.",
            },
            {
                "Hook": "order-sign",
                "When it fires": "When the clinician is about to sign one or more orders.",
                "What's in the request": "The full batch of pending orders plus patient context.",
                "Typical card content": "Last-chance validations: missing required orders, dose checks against renal function, prerequisite-screening missing. Cards at order-sign typically carry suggested-action accepts that modify or add orders inline.",
                "Example": "Clinician about to sign methotrexate orders. Card surfaces the missing folic-acid order and offers to add it.",
            },
        ]
    )
    hooks_table.index = range(1, len(hooks_table) + 1)
    hooks_table.index.name = "row"
    hooks_table
    return (hooks_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations about hook selection.

        First, the right hook depends on when the clinician can act. An adalimumab-TB-screening recommendation should fire at order-select (so the clinician can add the screening before signing), not at patient-view (where there is nothing to act on) and not at order-sign (which is the last chance and adds friction).

        Second, the request payload differs by hook. The order-select and order-sign hooks include the order in the request; the patient-view hook does not. A CDS service has to declare which hook it listens at because the request shape differs.

        Third, multiple services can listen at the same hook. The EHR aggregates the cards across services. The institution registers the set of services it wants at each hook; the EHR is the one place that has to know all of them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The JSON request payload

        The CDS Hooks request is a JSON object with a fixed top-level shape: the hook name, a unique invocation ID, the user, the patient context, and (optionally) prefetched FHIR resources the CDS service told the EHR it would need.
        """
    )
    return


@app.cell
def _(json, mo):
    request_example = {
        "hook": "order-sign",
        "hookInstance": "d1577c69-dfbe-44ad-ba6d-3e05e953b2ea",
        "fhirServer": "https://ehr.example.org/fhir",
        "user": "Practitioner/maya-bennett",
        "context": {
            "userId": "Practitioner/maya-bennett",
            "patientId": "ER-001",
            "encounterId": "Encounter/2024-05-15-reyes",
            "draftOrders": {
                "resourceType": "Bundle",
                "type": "collection",
                "entry": [
                    {
                        "resource": {
                            "resourceType": "MedicationRequest",
                            "status": "draft",
                            "intent": "order",
                            "medicationCodeableConcept": {
                                "coding": [{
                                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                                    "code": "1657983",
                                    "display": "adalimumab 40 MG/0.4 ML Auto-Injector"
                                }]
                            },
                            "subject": {"reference": "Patient/ER-001"},
                            "authoredOn": "2024-05-15",
                            "dosageInstruction": [{
                                "text": "40 mg subcutaneously every 2 weeks"
                            }]
                        }
                    }
                ]
            }
        },
        "prefetch": {
            "tbScreening": "<inline FHIR Bundle with the patient's TB-screening Observation, if any>"
        }
    }
    mo.md(
        f"""
        ### Example order-sign request for Ms. Reyes's adalimumab start

        ```json
        {json.dumps(request_example, indent=2)}
        ```

        The CDS service receives this payload. The service's job is to read the draft order, check the patient's record for TB screening within the last 12 months (the standard prerequisite for any TNF-inhibitor start), and return a card if screening is missing or outdated.
        """
    )
    return (request_example,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The JSON response: cards

        The CDS service returns a JSON object with a `cards` array. Each card has the same shape: summary, detail, indicator, source, links, suggestions.
        """
    )
    return


@app.cell
def _(json, mo):
    response_example = {
        "cards": [
            {
                "summary": "TB screening required before adalimumab start",
                "detail": "Adalimumab is a TNF inhibitor. Active or untreated latent TB must be excluded before initiation. This patient has no TB-screening result in the last 12 months. Consider ordering a QuantiFERON-TB Gold before signing this adalimumab order.",
                "indicator": "warning",
                "source": {
                    "label": "ACR 2021 RA Treatment Guideline (Section: Biologic Initiation Screening)",
                    "url": "https://www.rheumatology.org/Practice-Quality/Clinical-Support/Clinical-Practice-Guidelines/Rheumatoid-Arthritis"
                },
                "suggestions": [
                    {
                        "label": "Add QuantiFERON-TB Gold order",
                        "uuid": "f6a3a3b8-9b7a-4f6c-a18a-9b3b6a8b3e2d",
                        "actions": [
                            {
                                "type": "create",
                                "description": "Add QuantiFERON-TB Gold order",
                                "resource": {
                                    "resourceType": "ServiceRequest",
                                    "status": "draft",
                                    "intent": "order",
                                    "code": {
                                        "coding": [{
                                            "system": "http://loinc.org",
                                            "code": "71773-6",
                                            "display": "QuantiFERON-TB Gold Plus"
                                        }]
                                    },
                                    "subject": {"reference": "Patient/ER-001"}
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    mo.md(
        f"""
        ### Example response card

        ```json
        {json.dumps(response_example, indent=2)}
        ```

        Three properties of the card are load-bearing.

        First, the `indicator` field controls how the EHR renders the card visually. `info` (informational), `warning` (yellow-coded), and `critical` (red-coded) are the three values. Critical cards are typically hard stops; warning cards are typically soft alerts; info cards typically render as a banner.

        Second, the `source` field carries the attribution. The clinician can click through to the guideline that motivated the recommendation. This is the published-evidence trail the five-rights "right information" criterion requires.

        Third, the `suggestions` array carries the suggested actions. Each suggestion has an `actions` list; each action is a structured operation (create, update, delete) on a FHIR resource. The EHR renders the suggestion as an accept-or-reject control; accepting applies the action without requiring the clinician to navigate elsewhere.
        """
    )
    return (response_example,)


@app.cell
def _(xref):
    xref.callback(
        "12",
        "06",
        "FHIR resources as the CDS Hooks payload",
        "Course 06 introduced the FHIR Patient, Observation, MedicationRequest, and ServiceRequest resources. The CDS Hooks request includes FHIR resources as context; the CDS Hooks response includes FHIR resources as suggested actions. Fluency with the FHIR data model is the prerequisite for designing CDS Hooks cards.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Designing a card: an interactive exercise

        The controls below let the reader compose a card for the Reyes adalimumab order-sign scenario. The composed card is rendered as JSON below and as a clinician-facing-mockup preview to the right.
        """
    )
    return


@app.cell
def _(mo):
    card_summary = mo.ui.text(
        label="Card summary (one sentence)",
        value="TB screening required before adalimumab start",
        full_width=True,
    )
    card_detail = mo.ui.text_area(
        label="Card detail (the explanation, with the clinical rationale)",
        value="Adalimumab is a TNF inhibitor. Active or untreated latent TB must be excluded before initiation. This patient has no TB-screening result in the last 12 months.",
        rows=4,
        full_width=True,
    )
    card_indicator = mo.ui.radio(
        options=["info", "warning", "critical"],
        value="warning",
        label="Indicator level",
    )
    card_action_label = mo.ui.text(
        label="Suggested action label (what the clinician sees as the button text)",
        value="Add QuantiFERON-TB Gold order",
        full_width=True,
    )
    mo.vstack([card_summary, card_detail, card_indicator, card_action_label])
    return card_action_label, card_detail, card_indicator, card_summary


@app.cell
def _(card_action_label, card_detail, card_indicator, card_summary, json):
    composed_card = {
        "summary": card_summary.value,
        "detail": card_detail.value,
        "indicator": card_indicator.value,
        "source": {
            "label": "ACR 2021 RA Treatment Guideline",
            "url": "https://www.rheumatology.org/"
        },
        "suggestions": [
            {
                "label": card_action_label.value,
                "uuid": "f6a3a3b8-9b7a-4f6c-a18a-9b3b6a8b3e2d",
                "actions": [
                    {
                        "type": "create",
                        "description": card_action_label.value,
                        "resource": {
                            "resourceType": "ServiceRequest",
                            "status": "draft",
                            "intent": "order",
                            "code": {
                                "coding": [{
                                    "system": "http://loinc.org",
                                    "code": "71773-6",
                                    "display": "QuantiFERON-TB Gold Plus"
                                }]
                            },
                            "subject": {"reference": "Patient/ER-001"}
                        }
                    }
                ]
            }
        ]
    }
    composed_json = json.dumps({"cards": [composed_card]}, indent=2)
    return composed_card, composed_json


@app.cell
def _(card_action_label, card_detail, card_indicator, card_summary, mo):
    indicator_color = {"info": "info", "warning": "warn", "critical": "danger"}[card_indicator.value]
    mockup = mo.callout(
        mo.md(
            f"""
            **{card_summary.value}**

            {card_detail.value}

            _Source: ACR 2021 RA Treatment Guideline_

            **[ {card_action_label.value} ]**  _(suggested action; click to accept)_
            """
        ),
        kind=indicator_color,
    )
    mockup
    return indicator_color, mockup


@app.cell
def _(composed_json, mo):
    mo.md(
        f"""
        ### Composed JSON payload

        ```json
        {composed_json}
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## CDS Hooks vs the alternatives

        Three architectural alternatives appear in production today.

        - **Vendor-built-in rules engine.** The EHR vendor's own rules layer (Epic Best Practice Advisories, Cerner Discern). Highest performance, deepest EHR integration, but locked to the vendor. Per-institution rule maintenance.
        - **SMART on FHIR apps.** Course 06 Track 5 covered these. SMART apps are full clinician-facing applications launched from the EHR; useful for complex multi-step workflows. Heavier than a card; not the right architecture for a single-recommendation alert.
        - **CDS Hooks services.** The standards-based middle ground. Lightweight (a card, not an application), portable across EHRs, and externalized from the EHR vendor. The architecture this track covers.

        The three coexist in most production institutions. The choice for any specific intervention depends on the workflow weight (a card or an app), the integration depth (vendor-only or cross-vendor), and the institutional capacity to operate external services.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        CDS Hooks is the standards-based delivery layer for CDS. The architecture has four parts (EHR, hook trigger, CDS service, card) and a defined JSON request and response payload. The three load-bearing hooks (patient-view, order-select, order-sign) cover most production traffic; the right hook for a recommendation depends on when in the workflow the clinician can act on it. A card carries a summary, a detail explanation, an indicator level (info, warning, critical), source attribution, and suggested actions the clinician can accept inline.

        Track 04 takes up evaluation: how to know whether the alert a CDS Hooks card delivers is actually adding clinical value, with DCA (Course 11) at the alert threshold and before-and-after study designs from Course 04.
        """
    )
    return


if __name__ == "__main__":
    app.run()
