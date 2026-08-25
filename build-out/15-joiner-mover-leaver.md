# 15 · Joiner / mover / leaver, automated

> 🔨 hands-on — JML at scale, directory automation, SCIM provisioning
> **Before:** 03 identity · 06 tenant · 11 assets · 13 the help desk. **After:** —

This is last because it consumes everything: a group model from 03, a tenant from
06, an asset record from 11, and a support process from 13. Automating it before
those exist automates a mess and makes it faster.

It is also the step that decides whether headcount growth costs ticket growth.
That is the difference between **scaling people and scaling tickets**, and it is the
single most-tested skill cluster in real infrastructure job descriptions.

## What this step produces

- A **trigger** — the event that starts each of the three flows, coming from a system
  rather than from someone remembering.
- Joiner: account, group membership by role, device assigned and recorded, ready on
  day one without a ticket.
- Mover: permissions added **and removed**. The removal half is the one that decides
  whether access reviews in 14 are survivable.
- Leaver: access revoked everywhere, on a clock, with a record — and the device
  recovery tracked in 11.
- A dry-run mode, and evidence of each run.

## Questions to ask first

- **What system emits the trigger?** HR is the right answer and often not the
  available one. If the trigger is a ticket somebody files, the process has a human
  single point of failure and Leaver will be late — sometimes by months.
- **Does Mover remove?** Almost every implementation adds correctly and removes
  nothing. Permission creep is not a slow drift; it is this specific missing
  operation.
- **What is the Leaver clock, and does it differ for a resignation and a
  termination?** They usually should. Decide before the first hard case, not during.
- **What happens to the person's data?** Mailbox, files, licence — 06 and 07 owed an
  answer here, and this is where it gets executed.
- **Where does the device recovery live?** In 11's record, or nowhere.
- **Can it be dry-run?** Anything that disables accounts in bulk must be able to show
  its plan before it acts. A JML script without a dry-run is a self-inflicted outage
  waiting for a bad CSV.
- **Who is excluded?** Break-glass accounts from 03 must not be swept up by
  automation that disables anything that looks stale.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Scope | one directory, a few systems | the directory plus every SaaS product |
| Mechanism | scripts against LDAP, or a person and a checklist | directory APIs and **SCIM** to downstream apps |
| Leaver completeness | knowable — you owned the systems | **the hard part** — a forgotten SaaS keeps access indefinitely |
| Growth cost | linear in tickets | flat, if this is built; still linear if it is not |
| Audit exposure | low | **the most commonly failed control** |

**How much of that is AI: none, and this is the clearest case in the series.** JML
is deterministic automation with an audit trail. Every property that makes it
valuable — repeatable, dry-runnable, provable — is a property a probabilistic system
does not have. The correct tool is a script and an API, and it has been for a
decade.

There is one legitimate adjacent use, and it belongs to 14 rather than here:
**finding the accounts that should have been caught** — orphans in a SaaS product
nobody wired into SCIM. Detection, again, not action.

## Read deeper

- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — the JML
  section, and SCIM as provisioning-by-API
- [`cross-cutting/saas-admin.md`](../cross-cutting/saas-admin.md) — the identity spine
  across the SaaS estate, which is where Leaver actually gets hard
- [`cross-cutting/itsm-and-assets.md`](../cross-cutting/itsm-and-assets.md) — access
  governance, and the device half of the leaver flow
- [`foundations/`](../foundations/) — scripting and the idempotence habit this needs

## Do it

- [`toolbox/user-lifecycle/`](../toolbox/user-lifecycle/) — joiner/mover/leaver from a
  CSV, **dry-run by default**, which is the property that matters most here
- [`toolbox/ansible/roles/user_lifecycle/`](../toolbox/ansible/roles/user_lifecycle/)
  — the same job as configuration rather than as a script
- [`foundations/labs/idempotence-drill/`](../foundations/labs/idempotence-drill/) —
  running it twice must be safe; for this step that is not a nicety

## Getting it backwards

**Automating before the group model is right.** Automation applies the model
faithfully. If groups mean both job function and access bundle (see 03), the
automation propagates that at machine speed to every new hire, and the mess is now
consistent and much larger.

**Mover that only adds.** Everyone builds this. It looks complete because joiners and
leavers both work. Two years and a few internal transfers later, the longest-serving
employees have the most access and no one can say why.

**Leaver driven by a ticket.** The manager forgets, or files it a week later, or
files it and misses the SaaS product their team bought directly. The account persists
and it is exactly what the auditor samples.

**No dry-run.** One malformed CSV, one column shifted, and the run disables people
who are still employed — during business hours, at scale, with the help desk from
step 13 receiving all of it at once.
