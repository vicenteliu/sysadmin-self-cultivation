# The Build-Out — one office, first day to open for business

> A **route through** the other axes, not another axis. Every step says what it
> produces, what must be true first, what depends on it — then points into
> `platforms/`, `the-stack/`, `cross-cutting/`, `foundations/`, `endpoint/` and
> `toolbox/` for the substance. **No step teaches a new page.**
> Decision: [`docs/adr/0001`](../docs/adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)

## 🚧 Status

Steps 03 and 11 are written. The rest are specified below and not yet drafted.

**The opening argument — why sequence is a useful way to cut this at all — is
deliberately not written yet.** It gets written after enough steps exist to know
whether the claim holds. Writing the manifesto first would weld the series to a
thesis nothing has tested.

## The scenario, pinned

Every step assumes the same company, so that no step has to answer "it depends":

| | |
|---|---|
| **Size** | 100 people |
| **Sites** | one main office, one small branch |
| **Hosting** | forced hybrid — a few things must stay local (door access, badge printing, lab gear) |
| **Compliance** | a customer requires SOC 2, which is what makes identity, logging and asset records load-bearing rather than nice-to-have |
| **Time** | today, with *"how the same step went in 2015"* carried alongside |

## The steps

Ordered by **dependency**, not by technical domain — what must be true before
what. That ordering is the only thing this series has that the axes do not.

| # | Step | ✋/🧗 | State |
|---:|---|:--:|---|
| 00 | Questions to ask before the lease is signed | 🧗 | spec |
| 01 | Uplink — carrier choice, bandwidth, redundancy | 🧗 | spec |
| 02 | The building — riser, IDF, power, cooling, cable paths | 🧗 | spec |
| **03** | **Identity — directory, groups, SSO** | **✋** | **written** |
| 04 | Devices and images — purchase, build, enroll | ✋ | spec |
| 05 | Network — VLANs, wireless, guest, printing, door access | ✋ | spec |
| 06 | Tenant and mail — domains, routing, SPF/DKIM/DMARC | ✋ | spec |
| 07 | Files and collaboration — where state lives, who can see it | ✋ | spec |
| 08 | Endpoint security and patching | ✋ | spec |
| 09 | Backup — and the restore drill | ✋ | spec |
| 10 | Remote access — VPN, or the thing that replaced it | ✋ | spec |
| 11 | **Assets and tickets — the record that starts at device #1** | **✋** | **written** |
| 12 | Meeting rooms, AV and UC — the orphan nobody owns | 🧗 | spec |
| 13 | The help desk itself — and how many people this needs | ✋ | spec |
| 14 | Compliance evidence — what an audit actually asks for | ✋ | spec |
| 15 | Joiner / mover / leaver, automated | ✋ | spec |

**Budget and procurement are a section inside each step, not a step of their
own** — money is decided at every one of these, and collecting it into one file
produces a finance chapter nobody reads.

## The shape of a step

```
# NN · <what this step is>
> ✋/🧗 · Before: <steps that must be done> · After: <steps that depend on this>

## What this step produces        something checkable, not a list of topics
## Questions to ask first          the house style of this series
## 2015 → today                    components and actions gained or dropped
##   how much of that is AI, and how much is SaaS-ification
## Read deeper                     into the axes — never restated here
## Do it                           a lab or a toolbox tool; if none, say "gap"
## Getting it backwards            what it actually costs to do this out of order
```

The last section is the one that matters. A handbook is dry because it only ever
describes the correct path; this series is allowed to say what the wrong one cost.
