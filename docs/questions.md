---
kind: questions
axis: meta
themes: []
platforms: []
summary: "The index of questions asked of this repo across seven domains — open, answered, or deliberately out of scope, with the reason recorded for the last kind."
---
# Open questions

> Everything else here records what the repo **knows**. This records what it has
> been **asked** — including the questions it decided not to answer, and why.

A question earns a line the moment somebody wants to know and the repo cannot say.
It keeps that line until one of three things happens: an answer is written and
linked, the question is judged out of scope with a reason, or it turns out to have
been answered already and nobody could find it — which is a finding about the
index, not about the question.

**This is not [`interview/`](../cross-cutting/interview/README.md).** Those are
questions *other people ask you*, paired with what each one probes. These are
questions *you asked this repo*. The direction is opposite and so is the audience.

## Status

| Symbol | Meaning |
|---|---|
| ✅ | Answered. The link is where. |
| ⏳ | Open. Nobody has written it yet, and the destination is named where it is known. |

There is no symbol for *out of scope*, deliberately — those live in
[Boundaries](#boundaries) below, where a line has room for the reason. A symbol
would compress the only part of them worth keeping.

## The domains

Seven files, one per domain, and this page is their index. **The directory has no
`README.md` of its own** — an exception to how every other folder here is indexed, and
a deliberate one: two decision records
([0009](adr/0009-the-walkthrough-ships-its-script-not-its-audio.md) and
[0014](adr/0014-the-plate-stops-at-topology.md)) point at *this* path, and records are
not edited to follow a file that moved.

| Domain | Asked | Answered | Open |
|---|---|---|---|
| [Networking](questions/networking.md) | 13 | 11 | 2 |
| [Endpoint](questions/endpoint.md) | 4 | 4 | 0 |
| [Storage and data](questions/storage.md) | 4 | 4 | 0 |
| [Platforms and virtualisation](questions/platforms.md) | 2 | 2 | 0 |
| [Observability](questions/observability.md) | 3 | 3 | 0 |
| [Identity](questions/identity.md) | 2 | 2 | 0 |
| [Inventory and assets](questions/assets.md) | 2 | 2 | 0 |
| | **30** | **28** | **2** |

**The split happened when the rule below said it would.** This was one file with one
domain until seven more arrived at once; *a third domain appearing* was the stated
threshold and it was crossed by four. Recording that here rather than quietly
reorganising is the point — a threshold nobody notices being crossed is
[ADR-0008](adr/0008-a-count-is-not-a-bound.md)'s entire subject.

**Two open, and the shape of them is worth a sentence.** They are all networking, and
the six that used to point at *the evolution note* are now answered by one — which was
the argument for writing it before anything else on the list. The endpoint four sat on the
repo's **deepest** hands-on claim and its least-written axis — which was not a
coincidence about endpoint but what happens when the material somebody knows best is the
material they never had to look up. All four are now written, the fourth as a lab whose
inherited spec had to be replaced — it asked for a trial MDM and a spare device, which
is a *guided run*, and could not have taught its own lesson anyway.

## Boundaries

Four of the questions arrived wanting something this repo has already decided not to
do. **None of them was refused.** Each was narrowed to the version that does not break
a rule — and in all four cases that version is also the more useful one, which is worth
noticing rather than treating as a consolation.

Recorded here so that the narrowing does not have to be rediscovered. *A question
answered halfway, with no record of which half was cut, gets asked again in full.*

| Asked | Kept | Cut, and why |
|---|---|---|
| **Which firewall should I buy?** (#4) | What you will *see* in a given environment, and what it replaced. | A buying recommendation. [ADR-0002](adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md) allows model names only in a dated `Reference build`, whose entry condition is that a build-out step needs one — and none does. *"Palo Alto replaced what?"* is history and transfers; *"buy Palo Alto"* is a two-year-old opinion. |
| **A troubleshooting command reference** (#10) | The command that verifies each rung of the debug ladder. | A command reference. The chapter's stated altitude is *decisions somebody has to make and own* — it trains running a network, not reading the wire. A per-rung command serves the ladder; a reference replaces it with recall. |
| **How do AWS, GCP and Oracle Cloud each design their network services?** ([platforms #1](questions/platforms.md)) | Each platform's own network design, where it already lives — and the layer-by-layer comparison across seven platforms, where it already lives. | A fourth document comparing three clouds' networking. [`the-stack/02`](../the-stack/02-network.md) **is** the place this repo compares one layer across platforms; a three-way note would restate it at `mixed` footing, and restating a ramp does not deepen it. The narrowing is that the question was already answered twice and needed a pointer, not a page. |
| **A low-voltage topology, including the construction side** (#13) | MDF/IDF, riser, path to the edge — the logical topology a network person owns. | Containment, tray, pull schedules, construction sequencing. [`build-out/GAPS.md`](../build-out/GAPS.md) already judged this: commissioning a room from a shell is *physical work with contractors*, and it stays 🧭. Drawing a cable tray would be inventing depth. |

## Adding to this file

**A question goes in when you want to know and the repo cannot say** — not when it
would be nice to cover something. The difference is whether somebody actually asked.

When a question is answered, change the status and link the answer; do not delete the
line. The list of what this repo did not know is more interesting than the list of
what it covers, and it is the only place that history survives.

**The split has happened.** The stated threshold was a third domain appearing or a
single domain passing twenty-five questions; seven domains arrived at once and the first
condition was crossed by four. This page is now the index, and each domain is a file
under [`questions/`](questions/).

**The next threshold, since a rule that has fired needs replacing rather than
deleting.** A domain file passing **twenty-five questions** splits by sub-domain the same
way. And a domain whose questions are *all* answered does not get deleted — it stays,
because the list of what this repo did not know is the part that does not survive
anywhere else.
