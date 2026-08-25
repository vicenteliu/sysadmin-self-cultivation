# The Build-Out — one office, first day to open for business

> A **route through** the other axes, not another axis. Every step says what it
> produces, what must be true first, what depends on it — then points into
> `platforms/`, `the-stack/`, `cross-cutting/`, `foundations/`, `endpoint/` and
> `toolbox/` for the substance. **No step teaches a new page.**
> Decision: [`docs/adr/0001`](../docs/adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)

## Why sequence is a useful cut

*(Written after the sixteen steps existed, not before — the claim had to survive
being tried.)*

The six axes answer *what is this?* very well. Not one of them can answer **what
has to be true before this?**, because dependency is not a property of a topic. It
is a relation *between* topics, and a taxonomy has nowhere to put it.

That sounds abstract until you price it. Three things fell out of writing these
steps that no amount of reading the axes would have surfaced:

- **[Identity](03-identity.md) has an empty `Before` list.** It is the only step in
  a build-out with no physical prerequisite — it can start before there is a
  building, and eight later steps attach to it. Put it after the hardware and you
  have not sequenced badly, you have committed to re-imaging every desk.
- **[Assets](11-assets-and-tickets.md) is numbered eleventh and must start at device
  one.** The number is honest about dependency and a lie about time. A reader
  following the numbers as a schedule would get this exactly wrong, which is why the
  step says so in its first line.
- **[Staffing](13-the-help-desk.md) is unanswerable until step twelve.** "How many
  IT people does 100 people need" has no honest answer until the estate is
  enumerated and you know which categories of work steps 04, 08 and 15 removed.

The dependency graph across the sixteen is acyclic and fully symmetric — every
`Before` has its matching `After`. That is checkable, and it is checked. An ordering
that survives that is a real structure rather than a narrative convenience.

**What this series is not:** new material. It teaches no page the axes do not
already hold. If a step starts explaining how SCIM works, it has failed and the
explanation belongs upstream.

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

Ordered by **dependency** — what must be true before what — not by technical domain.

| # | Step | ⚒️/🧭 |
|---:|---|:--:|
| 00 | [Questions to ask before the lease is signed](00-before-the-lease.md) | 🧭 |
| 01 | [Uplink — carriers, bandwidth, redundancy](01-uplink.md) | 🧭 / ⚒️ |
| 02 | [The building — riser, IDF, power, cooling, cable paths](02-the-building.md) | 🧭 / ⚒️ |
| 03 | [**Identity** — directory, groups, SSO](03-identity.md) | ⚒️ |
| 04 | [Devices and images — purchase, build, enroll](04-devices-and-images.md) | ⚒️ |
| 05 | [Network — VLANs, wireless, guest, printing, door access](05-network.md) | ⚒️ |
| 06 | [Tenant and mail — domains, routing, SPF/DKIM/DMARC](06-tenant-and-mail.md) | ⚒️ |
| 07 | [Files and collaboration — where state lives, who can see it](07-files-and-collaboration.md) | ⚒️ |
| 08 | [Endpoint security and patching](08-endpoint-security-and-patching.md) | ⚒️ |
| 09 | [Backup — and the restore drill](09-backup-and-the-restore-drill.md) | ⚒️ |
| 10 | [Remote access — VPN, or the thing that replaced it](10-remote-access.md) | ⚒️ |
| 11 | [**Assets and tickets** — the record that starts at device #1](11-assets-and-tickets.md) | ⚒️ |
| 12 | [Meeting rooms, AV and UC — the orphan nobody owns](12-meeting-rooms-av-and-uc.md) | 🧭 |
| 13 | [The help desk itself — and how many people this needs](13-the-help-desk.md) | ⚒️ |
| 14 | [Compliance evidence — what an audit actually asks for](14-compliance-evidence.md) | ⚒️ |
| 15 | [Joiner / mover / leaver, automated](15-joiner-mover-leaver.md) | ⚒️ |

**Budget and procurement are a section inside each step, not a step of their own** —
money is decided at every one of these, and collecting it into one file produces a
finance chapter nobody reads.

Gaps the scenario surfaced: [`GAPS.md`](GAPS.md).

## The shape of a step

```
# NN · <what this step is>
> ⚒️/🧭 · Before: <steps that must be done> · After: <steps that depend on this>

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

## On the AI column

Most steps answer *"how much of this is AI?"* with **almost none**, and say so
plainly — the 2015→today change in identity, mail, files and provisioning is
SaaS-ification, and crediting a model for it invites the first correct objection.

[Step 12](12-meeting-rooms-av-and-uc.md) is the exception, and it exists partly to
prove the column is measuring rather than asserting: live transcription, attribution
and summarisation are genuinely model-driven and genuinely new. **A series that
always gives the same answer is not measuring anything.**

Where AI does appear, it is on one side of a line that every step draws the same
way: **let it find the thing; do not let it change the thing.** That line is not an
opinion here — it is what practitioners actually authorise, and
[step 08](08-endpoint-security-and-patching.md) carries the numbers.
