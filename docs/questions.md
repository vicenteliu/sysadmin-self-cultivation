---
kind: questions
axis: meta
themes: [networking]
platforms: []
summary: "Questions asked of this repo that it cannot yet answer — open, answered, or deliberately out of scope, with the reason recorded for the last kind."
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

## Networking

| # | Question | Status | Where |
|---|---|---|---|
| 1 | What does a current office network look like, architecturally? | ✅ | [`site-network-design.md`](../cross-cutting/site-network-design.md) |
| 2 | How has office network architecture changed over fifteen years? | ⏳ | the evolution note |
| 3 | How have the network protocols changed over that span? | ⏳ | the evolution note |
| 4 | Firewalls: Palo Alto now — what came before, and what changed? | ⏳ | the evolution note, **as a signature, not a recommendation** — see [Boundaries](#boundaries) |
| 5 | What does an F5-class device actually do? | ⏳ | the evolution note; partly answered by the *LB signature* row in [`the-stack/02`](../the-stack/02-network.md) |
| 6 | How are access points deployed, and by what rule? | ✅ | [`Selection rules`](../the-reference-office.md#selection-rules) — 🧭 |
| 7 | How have wireless and its protocols changed? | ⏳ | the evolution note |
| 8 | How does a large office's network differ from a small one's? | ✅ | [`site-network-design.md`](../cross-cutting/site-network-design.md#when-the-size-changes-the-design) |
| 9 | How does a VPN actually land a user on the office network? | ⏳ | a VPN note of its own |
| 10 | What are the basic troubleshooting commands? | ⏳ | a debug-ladder companion — **per rung, not a reference** — see [Boundaries](#boundaries) |
| 11 | How do IPv4 and IPv6 coexist now, and how is it configured? | ✅ | [`the-stack/02`](../the-stack/02-network.md) |
| 12 | What changed about speed? It cannot still be gigabit everywhere. | ✅ current · ⏳ history | [`site-network-design.md`](../cross-cutting/site-network-design.md) + [`Selection rules`](../the-reference-office.md#selection-rules); the fifteen-year arc belongs to the evolution note |
| 13 | How is the low-voltage network actually wired? Show a topology. | ⏳ | the **floor**'s near register — MDF/IDF, riser, path to the edge — in [`walkthrough/`](../walkthrough/README.md); still **not the construction side**, see [Boundaries](#boundaries) |

**Five answered, eight open.** The eight are not a wish-list: each has a named
destination, which is what separates this from a list of things that would be nice.

## Boundaries

Three of the questions above arrived wanting something this repo has already decided
not to do. **None of them was refused.** Each was narrowed to the version that does
not break a rule — and in all three cases that version is also the more useful one,
which is worth noticing rather than treating as a consolation.

Recorded here so that the narrowing does not have to be rediscovered. *A question
answered halfway, with no record of which half was cut, gets asked again in full.*

| Asked | Kept | Cut, and why |
|---|---|---|
| **Which firewall should I buy?** (#4) | What you will *see* in a given environment, and what it replaced. | A buying recommendation. [ADR-0002](adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md) allows model names only in a dated `Reference build`, whose entry condition is that a build-out step needs one — and none does. *"Palo Alto replaced what?"* is history and transfers; *"buy Palo Alto"* is a two-year-old opinion. |
| **A troubleshooting command reference** (#10) | The command that verifies each rung of the debug ladder. | A command reference. The chapter's stated altitude is *decisions somebody has to make and own* — it trains running a network, not reading the wire. A per-rung command serves the ladder; a reference replaces it with recall. |
| **A low-voltage topology, including the construction side** (#13) | MDF/IDF, riser, path to the edge — the logical topology a network person owns. | Containment, tray, pull schedules, construction sequencing. [`build-out/GAPS.md`](../build-out/GAPS.md) already judged this: commissioning a room from a shell is *physical work with contractors*, and it stays 🧭. Drawing a cable tray would be inventing depth. |

## Adding to this file

**A question goes in when you want to know and the repo cannot say** — not when it
would be nice to cover something. The difference is whether somebody actually asked.

When a question is answered, change the status and link the answer; do not delete the
line. The list of what this repo did not know is more interesting than the list of
what it covers, and it is the only place that history survives.

**When to split.** This file becomes `docs/questions/` with one file per domain at
whichever comes first: a **third domain** appearing, or a **single domain passing
twenty-five questions**. Below that, a directory costs more structure than it saves.
