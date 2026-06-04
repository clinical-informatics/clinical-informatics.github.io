"""Course 22: security in clinical informatics.

Marimo course menu. The course is currently scaffolded; track content will
be filled in as the curriculum builds out. The menu below lists the tracks
and a one-sentence description of what each one will cover.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 22: Security in clinical informatics

        ## The dedicated information-security course for clinical informaticists: the healthcare threat landscape, regulatory and compliance frameworks, identity and access management, cryptography and data protection, operational security and incident response, and application and AI security.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **The healthcare threat landscape** | Why healthcare is a target. The ransomware era. Cost of a breach. Patient-safety dimensions of cyber incidents. |
        | 02 | **Regulatory and compliance frameworks** | HIPAA Security Rule (with 2025 NPRM). NIST CSF 2.0. HITRUST CSF. SOC 2 and ISO 27001. 405(d) HICP. |
        | 03 | **Identity and access management (IAM)** | SSO, MFA, RBAC vs ABAC vs JIT, PAM, break-the-glass with auditing. |
        | 04 | **Cryptography and data protection** | Encryption at rest and in motion. TLS. Key management. Zero trust. DLP for PHI. |
        | 05 | **Operational security and incident response** | SOC, SIEM, EDR, vulnerability and patch management. IR lifecycle. BCP/DR. Clinical downtime procedures. |
        | 06 | **Application and AI security** | Secure SDLC. OWASP Top 10. Threat modeling. AI/ML-specific threats. Vendor security questionnaires. |

        ### Capstone

        **Tabletop incident-response exercise: a ransomware-style intrusion at 03:17 affecting the EHR cluster, the LIS, pharmacy, and CDS. Walk through the first 4 hours, the first 72 hours, and the post-incident review (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
