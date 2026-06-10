# Track 05: Financial management for informaticists

The CFO needs the RA-CDS budget by Friday: what the deployment costs, and what Helios gets back. Answering well takes four instruments, and this track defines each one against the running scenario. The capital-vs-operating distinction decides which budget the money comes from, which committee approves it, and which calendar the request rides; the line-item budget states the one-time implementation cost (about $240K) and the ongoing annual cost (about $60K) that together make the 5-year total cost of ownership $540K, of which the visible build is the minority.

The return side is a model, and the track treats it as one: patients alerted per year, the share of alerts acted on, flares averted per acted-on alert, and the cost of a moderate-to-severe RA flare ($4K to $6K in additional utilization) combine into an annual gross benefit. ROI is net benefit over cost across an explicit horizon; NPV discounts each year's net cash flow at a stated rate (3% here) and sums them. The notebook's central interactive is a 5-year ROI calculator: seven sliders drive a year-by-year discounted cash-flow table, a cumulative-net-benefit chart with the break-even point marked, and a verdict line that restates the NPV, ROI, and payback period as the inputs move. The track closes with vendor contract economics (licensing models, the 18 to 22% annual maintenance fee, and the build-vs-buy comparison for the RA-CDS) and the distinction between this track's cost-benefit frame and Course 11's cost-effectiveness frame.

The artifact is the budget estimate with the 5-year ROI, which the capstone collects as the budget section of the implementation plan.

**Prerequisites:** Track 01 (the committees and roles that approve the spend) and Track 02 (the plan the budget pays for); Course 12 for the running scenario.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 06 (leadership and communication).
