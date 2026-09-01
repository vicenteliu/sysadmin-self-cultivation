---
kind: route-step
axis: build-out
themes: [security-compliance]
platforms: []
marker: "🔨"
summary: "🔨 hands-on — access governance, asset reconciliation, and audit automation Before: 03 identity · 06 tenant · 07 files · 08 endpoint · 09 backup · 11 assets."
---
# 14 · Compliance evidence — what an audit actually asks for

> 🌐 **Languages:** English (default) · [中文](../docs/zh/build-out/14-compliance-evidence.md)

> 🔨 hands-on — access governance, asset reconciliation, and audit automation
> **Before:** 03 identity · 06 tenant · 07 files · 08 endpoint · 09 backup · 11 assets. **After:** —

Its Before list is the longest in the series, and that is the point: **this step
produces almost nothing of its own.** It collects. If the preceding steps were done
with evidence in mind, this is assembly. If they were not, it is a quarter of
reconstruction that ends in findings anyway.

The scenario has a customer requiring SOC 2. That constraint has been shaping every
step — it is why identity, logging and asset records were called load-bearing rather
than nice-to-have.

## What this step produces

- A control-to-evidence map: for each thing you claim, **the artefact that proves it
  and the system it comes from**.
- Evidence that accrues on a schedule, retained, rather than screenshots gathered in
  the week before fieldwork.
- An access review that has happened, with a date and a reviewer, and a record of
  what was changed as a result.
- A written boundary for what is out of scope, agreed early. Scope creep during an
  audit is expensive and mostly avoidable.
- An owner for each control who is not "IT".

## Questions to ask first

- **For each control, what artefact proves it, and can you produce last quarter's?**
  This one question converts a policy library into a work list. Most gaps are not
  missing controls; they are controls with no retained evidence.
- **Is the evidence a screenshot or an export?** Screenshots prove a moment.
  Auditors ask about periods.
- **Who reviews access, how often, and what happens to the result?** A review with no
  recorded changes usually means it was not really performed.
- **What is in scope?** Systems, data, and which of the two sites. Say it before
  fieldwork, in writing.
- **Which controls are actually owned outside IT** — HR for onboarding, finance for
  vendor management? Naming them early prevents the audit becoming an IT project
  that IT cannot complete alone.
- **What is the evidence retention period, and does anything expire before the audit
  window closes?** Logs with 30-day retention cannot prove a quarter.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Trigger | regulated industry, or a very large customer | **a mid-size customer's procurement questionnaire** |
| Scope | systems you ran | systems you ran, plus every SaaS vendor holding your data |
| Evidence | screenshots, assembled at audit time | exports on a schedule, retained continuously |
| Vendor management | a filing cabinet | a real control — their SOC 2 report is part of yours |
| The hard part | writing the policies | **proving the policies were followed**, continuously |

**How much of that is AI: a genuine assist, tightly bounded.** Mapping controls to
evidence, spotting a control with no artefact, summarising an access review, and
drafting the narrative sections of a policy are all real uses that save real days.

What must not move is the attestation. **A control is either operating or it is not,
and someone signs their name to that claim.** A model can find the missing artefact;
it cannot assert that the control worked. That distinction is the same advisory /
authority line this series has drawn at every step, and here it has legal weight
rather than merely operational weight.

## Read deeper

- [`cross-cutting/itsm-and-assets.md`](../cross-cutting/itsm-and-assets.md) — access
  governance and proving least privilege, the core of this step
- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — least
  privilege, which most controls are restatements of
- [`the-stack/07-security.md`](../the-stack/07-security.md) — the controls themselves
- [`the-stack/06-observability.md`](../the-stack/06-observability.md) — because
  evidence and telemetry are the same pipeline, retained for different reasons
- [`cross-cutting/working-with-security.md`](../cross-cutting/working-with-security.md)

## Do it

- [`toolbox/patch-report/`](../toolbox/patch-report/) — patch state as retained data,
  which is exactly the shape evidence needs to be
- [`toolbox/baseline-check/`](../toolbox/baseline-check/) — an asserted baseline is an
  artefact; a described one is not
- [`toolbox/user-lifecycle/`](../toolbox/user-lifecycle/) — the leaver half of the
  most commonly failed control

## Getting it backwards

**Starting at the audit.** Every artefact is retrospective, several are impossible
to reconstruct, and the findings that result are about the process rather than the
security. The controls may have been operating perfectly; you cannot show it.

**Screenshots instead of exports.** They prove one moment and imply a period. The
follow-up question is always "and the other eleven weeks?"

**Access reviews with no outcome.** A review that never removes anything is not a
review, and an auditor reads a clean review with no changes across a year of
joiners and leavers as evidence that it did not happen.

**Log retention shorter than the audit window.** Discovered when the evidence is
requested, at which point it is gone. Retention is a setting; setting it wrong costs
nothing until the day it costs the entire control.
