# 22: Security in clinical informatics

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/22-security?quickstart=1)

**The dedicated information-security course for clinical informaticists: the healthcare threat landscape, regulatory and compliance frameworks, identity and access management, cryptography and data protection, operational security and incident response, and application and AI security.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

The course was added 2026-06-04 after a board-syllabus gap analysis identified information security (beyond the privacy material in Course 03) as a substantive missing area. The course covers the security discipline as it applies to clinical informatics: the healthcare-specific threat landscape, the compliance frameworks the field is governed by, and the operational practice of running secure clinical systems.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | The healthcare threat landscape | Why healthcare is a target. The ransomware era (Change Healthcare 2024, CommonSpirit, Ascension, Lurie). Cost of a breach. Patient-safety dimensions of cyber incidents. |
| 02 | Regulatory and compliance frameworks | HIPAA Security Rule (with the 2025 NPRM). NIST CSF 2.0. HITRUST CSF. SOC 2 and ISO 27001. 405(d) HICP guidance. |
| 03 | Identity and access management (IAM) | SSO, MFA (TOTP, push, FIDO2/WebAuthn). RBAC vs ABAC vs JIT. PAM. Break-the-glass with auditing. |
| 04 | Cryptography and data protection | Encryption at rest and in motion. TLS. Key management. Zero trust. Data classification and DLP for PHI. |
| 05 | Operational security and incident response | SOC and SIEM. EDR. Vulnerability and patch management. IR lifecycle. BCP/DR with RPO/RTO callback to Course 05. Clinical downtime procedures. |
| 06 | Application and AI security | Secure SDLC (cross-ref Course 13). OWASP Top 10. Threat modeling. AI/ML-specific threats: prompt injection, model extraction, training-data poisoning, adversarial examples. Vendor security questionnaires. |
| ... | **Capstone** | Tabletop incident-response exercise: a ransomware-style intrusion at 03:17 affecting the EHR cluster, the LIS, pharmacy, and CDS. Walk through the first 4 hours, the first 72 hours, and the post-incident review (Socratic). |

## What you'll find in this repo

```
22-security/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-threat-landscape/
├── track-02-regulatory-frameworks/
├── track-03-iam/
├── track-04-cryptography/
├── track-05-operations-incident-response/
├── track-06-application-ai-security/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
