# 08 · Endpoint security and patching

> ⚒️ hands-on — patch operations, baselines, and working alongside a security function
> **Before:** 03 identity · 04 devices. **After:** 14 compliance evidence

Patching is the step everyone agrees is important and nobody schedules. It is also
the step where the gap between *what people expected automation to do* and *what
they actually let it do* is widest and best documented — which makes it the most
honest place in this series to talk about what AI is currently permitted to touch.

## What this step produces

- A patch cadence with a **named exception process**, because there will be a machine
  that cannot take the update and pretending otherwise makes the policy fiction.
- Disk encryption on, with **escrowed recovery keys** — and a test that a key can
  actually be retrieved by someone who is not you.
- A baseline someone can assert against, not a document describing one.
- Endpoint detection deployed, with a written answer to **who looks at the alerts**.
  A tool with no reader is a licence, not a control.
- Evidence that accumulates: patch state over time, not a screenshot taken the week
  of the audit.

## Questions to ask first

- **What is the maximum age of a missing critical patch?** Pick a number. "As soon as
  possible" produces no schedule and no accountability.
- **What is the reboot policy, and who eats the interruption?** Most patch programmes
  fail here rather than at deployment — the update installs and nothing reboots for
  eleven weeks.
- **Who has local admin, and why?** Every exception should have a name and a reason.
  This is the question a security review opens with.
- **Where do the encryption recovery keys live, and has anyone retrieved one?**
- **Who reads the EDR alerts at 22:00 on a Saturday?** If the answer is nobody, say so
  out loud and decide whether that is acceptable — it may well be, at 100 people,
  but it should be a decision rather than a discovery.
- **What proves any of this to an auditor?** Not the console — an export, on a
  schedule, retained.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Patch scope | the servers you owned; workstations lagged | endpoints are the estate, and they are not on your LAN |
| Delivery | WSUS/SCCM, on-premises, on the network | cloud-delivered policy; the device patches wherever it is |
| Antivirus | signatures | behavioural detection, with a response capability attached |
| Disk encryption | a project | default, and the recovery key escrow is the actual work |
| The hard part | pushing the update | **the reboot**, the exception list, and proving state over time |

**How much of that is AI: less than the marketing suggests, and the numbers are
unusually clear.** In Action1's 2026 survey of more than 1,000 sysadmins, patch
management was the workflow that had been expected to automate most — around
two-thirds predicted full automation by 2026 — and roughly one in six had
implemented it. Server monitoring showed the same shape. Troubleshooting, which
asks AI only for hypotheses, was the one area that nearly closed its gap.

The authority split in the same survey is the part worth internalising: about half
would let AI assess patch severity and schedule a window, while the share willing
to let it decide independently when to patch production sits near a sixth, and
willingness to let it override policy near a tenth.

⚠ *Source note: Action1 sells patch management, so read the framing with that in
mind. The prediction-versus-implementation structure is still useful precisely
because it makes the vendor's own optimism the thing being measured.*

**The practical reading for this step: use it to decide what to patch first, and
what a change is likely to break. Do not use it to approve the change.**

## Read deeper

- [`endpoint/`](../endpoint/) — MDM model, imaging, patch and EDR, BYOD
- [`the-stack/07-security.md`](../the-stack/07-security.md) — defence-in-depth, and
  where endpoint sits in it
- [`cross-cutting/working-with-security.md`](../cross-cutting/working-with-security.md)
  — the operator's view of working with a security function
- [`cross-cutting/incident-response.md`](../cross-cutting/incident-response.md) — for
  the question about who reads the alert

## Do it

- [`toolbox/patch-report/`](../toolbox/patch-report/) — patch state as data you can
  keep, which is what "evidence over time" means in practice
- [`toolbox/baseline-check/`](../toolbox/baseline-check/) — assert the baseline
  instead of describing it
- [`toolbox/ansible/roles/patch/`](../toolbox/ansible/roles/patch/) and
  [`baseline_hardening/`](../toolbox/ansible/roles/baseline_hardening/) — the same
  two jobs, applied rather than checked

## Getting it backwards

**Patching without a reboot policy.** Compliance dashboards go green on install,
and the machines carry unapplied kernels for months. The gap is invisible unless
you specifically measure uptime against patch date.

**Local admin for everyone, temporarily.** It is granted during the build because
it makes the build faster. It is never removed, because removing it breaks
something for someone, and now every endpoint is one bad download from a bad day.

**Buying detection with nobody to read it.** The licence is the easy part. An alert
queue that nobody owns is worse than no queue, because it produces the belief that
someone is watching.

**Collecting evidence at audit time.** The auditor asks for patch state over the
last quarter. If you start collecting when they ask, the answer is that you cannot
produce it — and that finding is about the process, not the patching.
