# Track 02: DIKW and the lifecycle of clinical data

A CRP value of 36.2 mg/L on Ms. Reyes's lab tab is a number on a screen. It is not yet a diagnosis, a recommendation, or even a clinical fact about her; it is a fact about a tube of her blood that an analyzer ran on the morning of 2024-01-08. What turns that number into a clinical decision later in the visit is a series of steps that informatics has names for. This track names them.

The track works in two halves.

The first half presents the **DIKW pyramid** (data, information, knowledge, wisdom) layer by layer using Ms. Reyes's CRP. Each layer adds something specific: data is the raw signal plus its metadata; information is the signal in context with the flag that draws attention; knowledge is what the field has learned about signals like this one; wisdom is knowing whether and how to act in this specific patient at this specific moment. **Martin Frické's 2009 critique** of the strict hierarchy is cited honestly: the layers blur, the direction of flow is not strictly bottom-up, and the field treats DIKW as useful vocabulary rather than as a fixed sequence.

The second half follows the same CRP through the **lifecycle of clinical data**: capture, store, use, share, retire. Each stage has its own failure modes. The track names them at each step (mislabeled specimen, drifted copies, broken trend graph, stripped reference range, expired authorization). The closing exercise locates one common real-world failure (the patient alone with a context-stripped value at 11 p.m.) at the specific intersection of stage and layer where it actually lives.

**Prerequisites:** Track 01 (where Ms. Reyes is introduced and the working definition of the field is established).

**How to start:** open `notebook.py` from the file tree on the left.

**What's next:** Track 03 (how computers represent and store data).
