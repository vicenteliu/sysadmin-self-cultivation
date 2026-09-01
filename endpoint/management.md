---
kind: companion
axis: endpoint
themes: [endpoint, identity]
platforms: []
marker: "mixed"
summary: "What an MDM actually manages once the machine is in someone's hands — the rented management surface, why enrolled and managed are different claims, what you find in an Apple estate and what it tells you, and the scoping problem that has a time axis."
---
# What an MDM manages, and what it cannot

> [`provisioning.md`](provisioning.md) got the machine into somebody's hands. This note
> is the other half: **how it stays in a state you can describe, eighteen months later,
> after the person has had it.** The [README](README.md) draws the enrol-configure-
> comply-act loop; this is the design underneath it, and the places where the loop is
> quietly open.

**Footing, up front, because it changes inside this note.** 🔨 for the model and for two
dialects of it — **Jamf** and **Workspace ONE / UEM** operated hands-on across a fleet,
including owning testing and maintenance for one region on the Jamf side. 🧭 for
**Intune, Autopilot and ConfigMgr** — the same discipline through a console this author
has mapped rather than run — and 🧭 for **deep iOS and Android fleet compliance-profile
engineering**, where enrolment and lifecycle are 🔨 but fleet-profile mastery is the
ramp. The [README](README.md) has said this since it was written; it is repeated here
because a reader who arrives directly at this page would otherwise not see it.

## You are renting a management surface

The single most useful thing to understand about this layer: **an MDM can only manage
what the operating-system vendor has decided to expose.** It is not a general-purpose
agent that owns the machine. It is a client of a protocol whose surface somebody else
controls, and who controls it differs per platform.

That has three consequences that decide most designs:

- **The surface changes on the vendor's schedule, not yours.** Payloads get added,
  deprecated, and occasionally taken away. Something you rely on can become
  unsupported without your estate doing anything at all.
- **"Can the MDM do X" is a question about the OS, not about the MDM.** Two products
  will differ on ergonomics, reporting and scale; they will rarely differ on whether a
  setting is manageable. When they do, it is usually because one has shipped support
  for a payload the other has not yet.
- **Therefore the choice between products is not a capability comparison.** It is a
  question about the estate around them, which is the section below.

**This is why the vendor names in this repo are signatures and not recommendations**
([ADR-0002](../docs/adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)).
The transferable knowledge is the protocol and the discipline; the console is a dialect
you learn in a fortnight.

## Enrolled, managed, and compliant are three different claims

They get used interchangeably in status meetings and they are not the same, and the gap
between them is where estates rot.

| Claim | What it means | How it fails |
|---|---|---|
| **Enrolled** | The device has a management identity and a trust relationship | It is a one-time event; a device can be enrolled and then never check in again |
| **Managed** | The MDM currently holds a live relationship and can act on it | The device is off, off-network, or has silently lost its enrolment |
| **Compliant** | The device currently satisfies the policy you wrote | Nothing here says anybody *did* anything about it |

**The dangerous one is the third.** A compliance policy that reports and does not act is
a dashboard. This repo has a sentence for that, earned in a different lab: *a check
earns its place by what it eliminates, not by what it reports*
([`remote-access-four-causes`](../cross-cutting/labs/remote-access-four-causes/)). The
endpoint version is: **a device out of compliance with no attached action is a device
you have documented rather than fixed**, and the documentation makes it look handled.

The design question, therefore, is not *what should the policy check*. It is **what
happens automatically when it fails, and how long is the device allowed to stay
failing.** Both of those need an answer before the policy is written.

## The scoping problem has a time axis

This is the part that is genuinely hard and it is rarely stated.

You scope a policy to a group. The group is populated from the directory. The directory
is maintained by joiner-mover-leaver. In [the reference
office](../the-reference-office.md#parameters) that is **about forty events a year**,
plus internal moves that nothing triggers at all.

So: **the set of machines a policy applies to changes without anyone editing the
policy.** You reviewed the blast radius on the day you wrote it. The blast radius is a
moving quantity and nobody reviews it again.

That is the endpoint form of the mover problem
([`build-out/15`](../build-out/15-joiner-mover-leaver.md)), and it has the same shape as
the finding in [`permission-sprawl`](../cross-cutting/labs/permission-sprawl/): a grant
made correctly on the day it was made, against a population that turned over
underneath it.

**What to do about it, in order of cost:**

1. **Write down the blast radius at authoring time** — the count, and the worst thing
   the policy does. This is free and almost nobody does it.
2. **Scope by compliance state or device attribute rather than by people-shaped group** wherever the
   policy is about the device rather than about the person. Device-shaped policies
   scoped to people-shaped groups are how a laptop in a drawer receives a
   configuration change.
3. **Re-derive the count on a cadence** and alert when it moves by more than you
   expected. A policy whose target set grew forty percent this quarter is telling you
   something about the directory, not about the policy.

## What you find in an Apple estate, and what it tells you

Read as **signatures** — what a thing's presence tells you about the organisation you
have walked into — and not as a shopping list. That distinction is a rule here, not a
disclaimer: naming a product to help someone recognise where they are transfers; naming
one to tell them what to buy expires.

**The two things that are not optional, whatever else you find:**

- **A device-registration channel** — the vendor-side record that says these serial
  numbers belong to this organisation. Without it there is no automated enrolment and
  no supervision, and the estate is doing the first column of
  [`provisioning.md`](provisioning.md) whether it means to or not.
- **Supervision.** Enrolment says the device is managed. **Supervision says the
  organisation owns it**, and it unlocks a materially different policy surface. An
  Apple estate where the fleet is enrolled but not supervised has usually grown out of
  a BYOD past, and that history explains most of what looks odd about it.

**What the management product itself tells you:**

| What you find | What it usually means |
|---|---|
| A **macOS-specialist platform** | Apple is a first-class platform here, not a tolerated one. Expect deep policy coverage, a scripting layer, and a team that knows the Apple release calendar. Often the sign of a design, engineering or research population |
| A **multi-OS UEM** | Somebody decided one console for all three matters more than depth in any one. Usually a large estate with a central endpoint team, and usually a compromise everyone knows about |
| The **Microsoft-estate default** | Identity and productivity are already Microsoft, and endpoint followed. The Apple support is real and improving and is rarely why the choice was made |
| An **Apple-only newer entrant** | A younger organisation that started on Apple and never had a Windows estate to unify with |
| **Two of the above, running** | A migration that stalled, or an acquisition. Find out which before proposing anything |

**The judgement, stated plainly:** the choice is decided by the estate around the
endpoints — which directory, which productivity suite, how many operating systems, and
whether Apple is a majority or a minority — and almost never by a capability the others
lack. An evaluation that produces a feature matrix has usually asked the wrong question.

## What an MDM cannot do

Worth stating because the loop diagram implies more than it delivers:

- **It cannot manage a device that does not check in.** Every number on the dashboard is
  a statement about the machines that reported. The interesting machines are the ones
  that did not.
- **It cannot make a policy retroactive to a device that was never enrolled.** The
  estate you can manage and the estate that exists are different sets, and the
  difference is [`inventory`](../CONTEXT.md) against the asset register again.
- **It cannot decide who should have something.** It applies a decision made elsewhere,
  which is why access and permissions remains the largest ticket category after every
  other kind of automation is built
  ([the reference office](../the-reference-office.md#parameters)).
- **It cannot substitute for the escrow design.** Enforcing encryption is one setting.
  What happens to the recovery key is a different problem entirely, and it is
  [`encryption-and-keys.md`](encryption-and-keys.md).

## Honest boundaries

🔨 **The model, and two dialects of it.** Jamf and Workspace ONE / UEM operated
hands-on across a real fleet — enrolment, configuration profiles, compliance policy,
targeted application distribution, and regional ownership of testing and maintenance
on the Jamf side. The enrolled-versus-managed-versus-compliant distinction and the
scoping-over-time problem are both operational scar tissue.

🧭 **Intune, Autopilot and ConfigMgr** — mapped, ramped and verified, not run.
🧭 **Deep iOS and Android fleet compliance-profile engineering** — enrolment and
lifecycle are 🔨; fleet-profile mastery is the ramp.

**Not claimed:** licensing economics, vendor contract negotiation, and any statement
about which product an organisation should buy.

## Read deeper

- [`endpoint/provisioning.md`](provisioning.md) — how the machine got here
- [`endpoint/encryption-and-keys.md`](encryption-and-keys.md) — the setting this note
  will not pretend is a setting
- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — the directory
  whose churn moves your policy targets
- [`build-out/08`](../build-out/08-endpoint-security-and-patching.md) — compliance with
  an action attached, and the reboot that is the actual hard part
- [`cross-cutting/labs/permission-sprawl/`](../cross-cutting/labs/permission-sprawl/) —
  the same failure one layer up: a correct grant against a population that moved
