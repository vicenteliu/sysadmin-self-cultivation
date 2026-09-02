---
kind: lab
axis: cross-cutting
themes: [identity, networking]
platforms: []
summary: "Four unrelated causes produce a byte-identical 'the VPN will not connect', so diagnosing from the symptom is guessing with extra steps. An ordered set of checks, each chosen for what it rules out, gets there every time with a bounded worst case."
---
# Lab — "The VPN won't connect" is four different problems

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/cross-cutting/labs/remote-access-four-causes/README.md)

**Goal:** make the most expensive habit in remote-access support tangible —
**four unrelated causes produce a byte-identical user report**, so diagnosing from
the symptom is guessing with extra steps. You will watch the reflex checks
("restart it", "is the tunnel up?") eliminate nothing, watch two causes masquerade
as each other, and watch an ordered set of checks — each chosen for what it *rules
out* — get there every time with a bounded worst case.

**You'll practise:** the discipline
[`toolbox/linux-triage`](../../../toolbox/linux-triage/) is built on and
[build-out step 10](../../../build-out/10-remote-access.md) names as its top ticket
— *every check has to eliminate something*.

The four, straight from that step:

1. an expired certificate on the gateway
2. the identity provider is unreachable
3. a captive portal is intercepting (hotel, cafe, airport)
4. the tunnel installs a more-specific route that does not carry auth traffic

## Why this lab is pure-local

Every one of the four is a *reasoning* failure before it is a network failure. What
makes the ticket expensive is not that the packets are hard to see — it is that the
symptom is the same in all four worlds and the obvious checks do not narrow
anything. That is fully expressible as a model: four world-states, a set of checks,
and the possibility set each one leaves behind.

No VPN, no gateway, no tenant, no credentials, no `pip install`. Python stdlib, and
CI can run it.

## Run it

```bash
python3 cross-cutting/labs/remote-access-four-causes/four_causes_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Four incidents, one report.** All four print the same sentence. The assertion
   is that the set of distinct symptoms has size one.
2. **The reflex checks eliminate nothing.** "Restart the client" and "is the tunnel
   connected?" leave all four causes possible, in every world. They feel like
   progress because they produce a *result*, not because they remove a possibility.
3. **The masquerade.** "Can I reach the identity provider?" returns the same answer
   for a genuine identity outage and for a captive portal. Exactly one observation
   separates them: whether DNS is answering *honestly* — a portal answers
   everything, and answers it with itself.
4. **The phase trap.** Cause #4 fails *after* the tunnel reports connected. It is
   the only world where "is it up?" says yes, which means the reflex check does not
   merely waste a step — it points away from the fault.
5. **Guessing vs. eliminating**, run over all four. Elimination resolves 4/4, worst
   case 3 checks. The habit order resolves 2/4 and runs out of checks with two
   causes still standing.

## Verify (don't take the script's word for it)

A self-verifier that cannot fail is worthless. Sabotage it:

```bash
python3 .../four_causes_drill.py --break-it   # exit 1
```

This replaces the DNS-honesty check with one that eliminates nothing — the same
mistake as never asking the question. Elimination immediately drops to 2/4, because
the portal and the real outage are now indistinguishable, and the drill exits `1`
naming the assertion that broke.

To go further, edit `ELIMINATION_ORDER` and move the certificate check last: the
answers stay correct and the cost rises, which is the quieter version of the same
lesson — ordering is not cosmetic.

## The point

**A check earns its place by what it eliminates, not by what it reports.**

The help desk will see this ticket more than any other, forever. Handled by
symptom, it is four different guesses with the same opening move. Handled by
elimination, the worst case is bounded by the number of causes — and the ordering
that achieves it is the deliverable, not the individual commands.

The two traps are the part worth carrying out of here:

- **Two causes can give the same answer to a reasonable question.** Finding the
  question that separates them is the actual skill.
- **A cause that fails after "connected" defeats every liveness check.** Being up
  is not being correct.

## Teardown

None. The drill holds everything in memory and writes nothing.
