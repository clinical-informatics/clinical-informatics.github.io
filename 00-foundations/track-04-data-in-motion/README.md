# Track 04: How computers move data

The lab analyzer is in the basement; the rheumatologist is on the third floor. The EHR is on a server in the building; the patient is on her phone at home. The clinical data warehouse is inside the firewall; the researcher who wants to query it is at a university in another state. Between rest and use is the network. This track names the network architecture clinical systems run on and where the boundaries that matter to the field actually sit.

The track moves through five short pieces.

1. **Client and server.** The single most useful piece of vocabulary in the track, taught through the restaurant analogy the curriculum reuses elsewhere. Every clinical system you interact with is implicitly one role or the other.
2. **The four network zones.** LAN (inside the building), firewall (the boundary), VPN (how the work-from-home rheumatologist gets back inside), public internet (everything else). What each zone allows and constrains.
3. **HTTP, REST, and APIs at concept level.** HTTP is the protocol the browser uses, REST is the convention modern APIs follow, an API is the documented menu of nouns and verbs a system accepts. Course 06 (`learn-fhir`) is the deep dive.
4. **On-prem versus cloud.** Where the server actually lives. On-prem (in the hospital's data center) was the older default; cloud and vendor-hosted are where most new clinical work happens. The trade-offs (control, latency, regulatory story, cost, scale) named on each side.
5. **The U.S. clinical security landscape.** HIPAA, HITECH, HITRUST, SOC 2. The pattern: every boundary clinical data crosses is matched with a contract and a technical control. Course 03 does this seriously; Track 04 names the landscape.

The track closes by walking Ms. Reyes's CRP from the lab analyzer to the LIS to the EHR to the CDW to the insurer to her phone to a research collaborator. Seven systems, three to five network boundaries, each authorized by a different combination of technical control and contractual control. The exercise makes the boundaries visible.

**Prerequisites:** Track 03 (data-at-rest is what data-in-motion is moving).

**How to start:** open `notebook.py` from the file tree on the left.

**What's next:** Track 05 (the American health system and its parts).
