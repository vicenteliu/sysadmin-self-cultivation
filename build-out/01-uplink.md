---
kind: route-step
axis: build-out
themes: [networking]
platforms: []
marker: "mixed"
summary: "🧭 verified ramp for procurement and carrier negotiation; 🔨 for what the circuit is carrying and how it fails once it is live."
---
# 01 · Uplink — carriers, bandwidth, redundancy

> 🧭 **verified ramp** for procurement and carrier negotiation; 🔨 for what the
> circuit is carrying and how it fails once it is live.
> **Before:** 00 lease questions. **After:** 02 the building · 05 network · 10 remote access

For an office whose work lives entirely off-site, **the uplink is the business**.
That is a change worth stating plainly: in 2015 a dead circuit meant no email and
no internet, while the file server and the domain controller kept working in the
next room. Today a dead circuit means nobody can log in.

## What this step produces

- Two circuits from **two carriers**, entering on **two paths** — or a written
  acknowledgement of which of those three is being given up and what it costs.
- A sizing number with the reasoning attached, not a round number someone liked.
- A failover that has been **tested by unplugging something**, on a date, with the
  result written down.
- The branch office's link decided at the same time, because it fails the same way
  and nobody remembers it until it does.

## Questions to ask first

- **How many people, doing what?** 100 people on SaaS and video is a very different
  number from 100 people pushing large assets. Size from the two or three heaviest
  workflows, not from a per-seat rule of thumb.
- **What is the actual failure you are buying insurance against?** Carrier outage,
  fibre cut, or building event? They need different answers, and "redundancy" bought
  without naming one usually buys the least likely.
- **Is the second circuit truly diverse?** Different carrier, different entry,
  different last mile. Two resellers on the same physical fibre is a single circuit
  with two invoices — ask for the underlying carrier, not the logo on the contract.
- **What is the failover behaviour, precisely?** Does it re-establish sessions or drop
  them? A failover that drops every call and VPN tunnel is still worth having, but
  only if people know that is what will happen.
- **Who is called at 2am, and what is the contracted response?** An SLA with a credit
  and no response time is a discount, not a service.
- **What does the branch fail over to** — its own second circuit, or a tunnel over
  consumer broadband? Both are answers; not choosing is not.

## 2015 → today

| | 2015 | today |
|---|---|---|
| What breaks when it drops | email and browsing; local services keep running | **everything** — identity, files, phones, badge-in for some systems |
| Sizing driver | file transfer to HQ, VPN | video, SaaS sync, endpoint management traffic |
| Failover | often manual, often a router someone reconfigures | expected to be automatic, and expected to be tested |
| Second link | a nice-to-have justified with difficulty | the default; the argument now runs the other way |
| Branch office | a VPN tunnel and low expectations | expected to be a first-class site |

**How much of that is AI: none.** This is a straightforward consequence of work
moving off-premises — SaaS-ification, plus video becoming the default meeting.
The AI-driven traffic a 100-person office generates is not currently a sizing
factor worth naming.

## Read deeper

- [`the-stack/02-network.md`](../the-stack/02-network.md) — the network layer across
  seven platforms; the vocabulary this step is buying against
- [`the-stack/labs/01-failure-domains/`](../the-stack/labs/01-failure-domains/) —
  what "diverse" has to mean to count
- [`cross-cutting/incident-response.md`](../cross-cutting/incident-response.md) —
  because the 2am question above is really an on-call question
- [the reference office's Selection rules](../the-reference-office.md#selection-rules)
  — the sizing arithmetic, with the reasoning attached rather than a round number

## Do it

- [`the-stack/labs/01-failure-domains/`](../the-stack/labs/01-failure-domains/) —
  runnable, and the cheapest way to see why the two-circuits-one-conduit answer is
  wrong before you have paid for it.

## Getting it backwards

**Buying redundancy without diversity.** Two circuits, one conduit, one carrier
upstream, or one power feed to both terminating devices. The invoice says
redundant; the failure domain says one. It is discovered during the outage, which
is also when you discover the second circuit was never carrying traffic and its
configuration has drifted for a year.

**Never testing failover.** Untested failover fails at a rate close to one. The
test is disruptive, so it gets scheduled, then moved, then dropped. Do it during
the build — the one window where there is nobody to disrupt.

**Sizing for today's headcount.** 100 people is the number on the day you move in.
Circuits have lead times measured in months, and the upgrade conversation should
have a trigger written into it, not wait for complaints.
