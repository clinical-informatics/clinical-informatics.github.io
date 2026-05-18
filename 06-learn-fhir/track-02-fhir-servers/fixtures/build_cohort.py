"""Build the synthetic RA cohort fixture for Track 2.

Produces a single FHIR R4 Bundle of type `searchset` containing five
patients (Ms. Reyes plus four synthetic peers) and their CRP and ESR
observations at roughly three-month intervals. The bundle is the
shape a real FHIR server would return for a query like

    GET /Observation?code=http://loinc.org|1988-5,http://loinc.org|4537-7
        &_count=200
        &_include=Observation:patient

We use a single bundle so the notebook can demonstrate filtering by
patient and by code without orchestrating multiple HTTP calls. The
five patient trajectories were hand-crafted to give the cohort visual
variety: a moderate responder (Reyes), a slow non-responder on MTX
mono (Chen), a dramatic responder with a hold-and-flare event
(Williams), an aggressive case who failed three agents (Patel), and a
freshly diagnosed patient still titrating (Russo).

Re-run this script whenever the cohort design changes; it overwrites
`cohort.json` in this directory.
"""

from __future__ import annotations

import json
from pathlib import Path

PATIENTS = [
    {
        "id": "elena-reyes",
        "family": "Reyes",
        "given": ["Elena", "Maria"],
        "gender": "female",
        "birthDate": "1974-02-09",
        "label": "Moderate seropositive RA; MTX + adalimumab since 2024.",
        "treatment_arc": "MTX 2022, adalimumab added Jan 2024.",
    },
    {
        "id": "marcus-chen",
        "family": "Chen",
        "given": ["Marcus"],
        "gender": "male",
        "birthDate": "1965-08-23",
        "label": "Late-onset seropositive RA; MTX monotherapy, slowly worsening.",
        "treatment_arc": "MTX 2023; adalimumab added April 2026 for inadequate response.",
    },
    {
        "id": "aisha-williams",
        "family": "Williams",
        "given": ["Aisha"],
        "gender": "female",
        "birthDate": "1982-11-04",
        "label": "Seronegative RA; MTX + tofacitinib. Dramatic responder; flared during a 2024 dose hold.",
        "treatment_arc": "MTX 2022; tofacitinib added June 2023; brief hold March 2024 (travel).",
    },
    {
        "id": "david-patel",
        "family": "Patel",
        "given": ["David"],
        "gender": "male",
        "birthDate": "1969-04-17",
        "label": "Aggressive seropositive erosive RA; failed MTX + adalimumab + infliximab; controlled on rituximab.",
        "treatment_arc": "MTX 2022; adalimumab Oct 2022; infliximab April 2023; rituximab Oct 2023.",
    },
    {
        "id": "sofia-russo",
        "family": "Russo",
        "given": ["Sofia"],
        "gender": "female",
        "birthDate": "1987-01-29",
        "label": "Recently-diagnosed seropositive RA; titrating MTX.",
        "treatment_arc": "Presented June 2025; MTX titration in progress.",
    },
]

# (patient_id, date, crp_value, esr_value)
OBSERVATIONS = [
    # Ms. Reyes (from labs.csv)
    ("elena-reyes", "2022-02-14", 42.1, 58),
    ("elena-reyes", "2022-05-22", 28.4, 42),
    ("elena-reyes", "2022-08-18", 19.2, 31),
    ("elena-reyes", "2022-11-09", 16.8, 28),
    ("elena-reyes", "2023-02-15", 22.5, 34),
    ("elena-reyes", "2023-05-23", 31.6, 46),
    ("elena-reyes", "2023-08-21", 26.9, 39),
    ("elena-reyes", "2023-11-13", 33.4, 48),
    ("elena-reyes", "2024-01-08", 36.2, 51),
    ("elena-reyes", "2024-04-17", 18.7, 29),
    ("elena-reyes", "2024-07-22", 14.1, 24),
    ("elena-reyes", "2024-10-30", 11.4, 22),
    ("elena-reyes", "2025-02-04", 13.8, 25),
    ("elena-reyes", "2025-05-12", 16.5, 28),
    ("elena-reyes", "2025-08-19", 14.9, 24),
    ("elena-reyes", "2025-11-21", 18.2, 31),
    ("elena-reyes", "2026-02-10", 21.4, 33),
    ("elena-reyes", "2026-04-28", 19.8, 29),
    # Marcus Chen (slow worsening on MTX mono, biologic added at the end)
    ("marcus-chen", "2023-04-12", 38.2, 52),
    ("marcus-chen", "2023-07-18", 22.4, 36),
    ("marcus-chen", "2023-10-14", 18.1, 28),
    ("marcus-chen", "2024-01-09", 16.5, 26),
    ("marcus-chen", "2024-04-15", 14.2, 24),
    ("marcus-chen", "2024-07-19", 13.1, 22),
    ("marcus-chen", "2024-10-22", 15.4, 24),
    ("marcus-chen", "2025-01-21", 17.3, 26),
    ("marcus-chen", "2025-04-24", 19.6, 28),
    ("marcus-chen", "2025-07-25", 21.8, 32),
    ("marcus-chen", "2025-10-28", 23.5, 36),
    ("marcus-chen", "2026-01-23", 26.4, 41),
    ("marcus-chen", "2026-04-20", 18.2, 28),
    # Aisha Williams (dramatic responder, hold-and-flare)
    ("aisha-williams", "2022-09-08", 31.4, 44),
    ("aisha-williams", "2022-12-02", 18.6, 28),
    ("aisha-williams", "2023-03-10", 12.1, 22),
    ("aisha-williams", "2023-06-15", 6.4, 14),
    ("aisha-williams", "2023-09-18", 3.2, 8),
    ("aisha-williams", "2023-12-21", 4.1, 10),
    ("aisha-williams", "2024-03-14", 5.3, 12),
    ("aisha-williams", "2024-06-12", 22.4, 36),
    ("aisha-williams", "2024-09-09", 12.3, 22),
    ("aisha-williams", "2024-12-11", 6.2, 14),
    ("aisha-williams", "2025-03-17", 4.4, 10),
    ("aisha-williams", "2025-06-19", 3.1, 8),
    ("aisha-williams", "2025-09-22", 3.4, 9),
    ("aisha-williams", "2025-12-15", 3.9, 11),
    ("aisha-williams", "2026-03-19", 3.2, 9),
    # David Patel (failed three agents, controlled on rituximab)
    ("david-patel", "2022-01-25", 65.3, 78),
    ("david-patel", "2022-04-21", 48.2, 62),
    ("david-patel", "2022-07-19", 38.4, 51),
    ("david-patel", "2022-10-17", 28.2, 42),
    ("david-patel", "2023-01-23", 32.1, 46),
    ("david-patel", "2023-04-20", 35.4, 49),
    ("david-patel", "2023-07-18", 38.6, 52),
    ("david-patel", "2023-10-22", 22.4, 32),
    ("david-patel", "2024-01-15", 16.3, 24),
    ("david-patel", "2024-04-22", 12.1, 19),
    ("david-patel", "2024-07-15", 14.2, 21),
    ("david-patel", "2024-10-21", 11.4, 18),
    ("david-patel", "2025-01-13", 13.5, 20),
    ("david-patel", "2025-04-14", 14.6, 22),
    ("david-patel", "2025-07-21", 12.3, 19),
    ("david-patel", "2025-10-13", 10.8, 17),
    ("david-patel", "2026-01-19", 12.4, 19),
    ("david-patel", "2026-04-15", 11.6, 18),
    # Sofia Russo (recent diagnosis, titrating)
    ("sofia-russo", "2025-06-23", 58.1, 72),
    ("sofia-russo", "2025-09-15", 42.4, 58),
    ("sofia-russo", "2025-12-10", 32.3, 44),
    ("sofia-russo", "2026-03-16", 24.2, 36),
]

LOINC_CRP = "1988-5"
LOINC_ESR = "4537-7"
SYSTEM_LOINC = "http://loinc.org"
SYSTEM_UCUM = "http://unitsofmeasure.org"
SYSTEM_INTERP = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
SYSTEM_OBS_CATEGORY = "http://terminology.hl7.org/CodeSystem/observation-category"
SYSTEM_COND_CLINICAL = "http://terminology.hl7.org/CodeSystem/condition-clinical"
SYSTEM_COND_VER = "http://terminology.hl7.org/CodeSystem/condition-ver-status"
SYSTEM_COND_CATEGORY = "http://terminology.hl7.org/CodeSystem/condition-category"
SYSTEM_SNOMED = "http://snomed.info/sct"
SYSTEM_ICD10 = "http://hl7.org/fhir/sid/icd-10-cm"

REF_RANGE = {
    LOINC_CRP: {"low": 0, "high": 5, "unit": "mg/L"},
    LOINC_ESR: {"low": 0, "high": 20, "unit": "mm/h"},
}


def patient_resource(p):
    return {
        "resourceType": "Patient",
        "id": p["id"],
        "name": [{"use": "official", "family": p["family"], "given": p["given"]}],
        "gender": p["gender"],
        "birthDate": p["birthDate"],
    }


def condition_resource(p):
    return {
        "resourceType": "Condition",
        "id": f"{p['id']}-ra",
        "clinicalStatus": {"coding": [{"system": SYSTEM_COND_CLINICAL, "code": "active"}]},
        "verificationStatus": {"coding": [{"system": SYSTEM_COND_VER, "code": "confirmed"}]},
        "category": [
            {"coding": [{"system": SYSTEM_COND_CATEGORY, "code": "problem-list-item"}]}
        ],
        "code": {
            "coding": [
                {"system": SYSTEM_ICD10, "code": "M05.79"},
                {"system": SYSTEM_SNOMED, "code": "239791008", "display": "Seropositive rheumatoid arthritis"},
            ],
            "text": "Rheumatoid arthritis",
        },
        "subject": {"reference": f"Patient/{p['id']}"},
    }


def observation_resource(patient_id, date, loinc, value):
    if loinc == LOINC_CRP:
        display = "C reactive protein [Mass/volume] in Serum or Plasma"
        unit = "mg/L"
    else:
        display = "Erythrocyte sedimentation rate"
        unit = "mm/h"
    rng = REF_RANGE[loinc]
    flag = "H" if value > rng["high"] else ("L" if value < rng["low"] else "N")
    obs_id = f"{patient_id}-{loinc.replace('-', '')}-{date.replace('-', '')}"
    return {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "category": [
            {"coding": [{"system": SYSTEM_OBS_CATEGORY, "code": "laboratory"}]}
        ],
        "code": {"coding": [{"system": SYSTEM_LOINC, "code": loinc, "display": display}]},
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": f"{date}T08:30:00-05:00",
        "valueQuantity": {
            "value": value,
            "unit": unit,
            "system": SYSTEM_UCUM,
            "code": unit,
        },
        "referenceRange": [
            {
                "low": {"value": rng["low"], "unit": unit, "system": SYSTEM_UCUM, "code": unit},
                "high": {"value": rng["high"], "unit": unit, "system": SYSTEM_UCUM, "code": unit},
            }
        ],
        "interpretation": [
            {"coding": [{"system": SYSTEM_INTERP, "code": flag}]}
        ],
    }


def build_bundle():
    entries = []
    base = "https://hapi.fhir.org/baseR4"
    for p in PATIENTS:
        pr = patient_resource(p)
        entries.append({
            "fullUrl": f"{base}/Patient/{p['id']}",
            "resource": pr,
            "search": {"mode": "include"},
        })
        cr = condition_resource(p)
        entries.append({
            "fullUrl": f"{base}/Condition/{cr['id']}",
            "resource": cr,
            "search": {"mode": "include"},
        })
    for patient_id, date, crp_val, esr_val in OBSERVATIONS:
        for loinc, value in ((LOINC_CRP, crp_val), (LOINC_ESR, esr_val)):
            obs = observation_resource(patient_id, date, loinc, value)
            entries.append({
                "fullUrl": f"{base}/Observation/{obs['id']}",
                "resource": obs,
                "search": {"mode": "match"},
            })

    bundle = {
        "resourceType": "Bundle",
        "id": "ra-cohort-search-2026",
        "meta": {
            "lastUpdated": "2026-05-12T14:00:00-05:00",
            "tag": [
                {
                    "system": "http://clinical-informatics.example/tags",
                    "code": "synthetic",
                    "display": "Synthetic teaching data. Not real patients.",
                }
            ],
        },
        "type": "searchset",
        "total": len(entries),
        "link": [
            {"relation": "self",
             "url": f"{base}/Observation?_include=Observation:patient&code=http://loinc.org|1988-5,http://loinc.org|4537-7&_count=200"},
        ],
        "entry": entries,
    }
    return bundle


def main():
    out_path = Path(__file__).parent / "cohort.json"
    bundle = build_bundle()
    with open(out_path, "w") as fh:
        json.dump(bundle, fh, indent=2)
    obs_count = sum(1 for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation")
    print(f"Wrote {out_path}")
    print(f"  Total entries: {len(bundle['entry'])}")
    print(f"  Patients: {sum(1 for e in bundle['entry'] if e['resource']['resourceType'] == 'Patient')}")
    print(f"  Conditions: {sum(1 for e in bundle['entry'] if e['resource']['resourceType'] == 'Condition')}")
    print(f"  Observations: {obs_count}")


if __name__ == "__main__":
    main()
