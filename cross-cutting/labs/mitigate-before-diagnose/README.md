---
kind: lab
axis: cross-cutting
themes: []
platforms: []
marker: "🔨"
summary: "Mitigating first saves nine minutes of mean downtime and costs six in the tail — and the model says at what mitigation coverage the advice inverts, which is the part a slogan cannot carry."
---
# Lab — mitigate before you diagnose, and the two places that stops being true

> **Inputs:** none · **Outputs:** expected and worst-case downtime under both
> strategies, the crossover, and the risk penalty that inverts it · **Risk:** none —
> no systems, no services, no credentials · **Root:** not needed

**Goal:** take [`incident-response.md`](../../incident-response.md)'s central claim —
*mitigate before you diagnose, the one instinct that separates seniors* — and **measure
it instead of repeating it.**

**You'll practise:** stating an operational instinct precisely enough that it could be
wrong, and then finding the conditions under which it is.

## Why this lab is pure-local

An incident is a decision under a distribution: some set of causes, each with a time to
find and a time to fix, and a generic mitigation that covers some of them. That is
fully expressible as arithmetic, and expressing it is what turns a slogan into a claim
with an edge.

The spec this replaces asked for a tabletop and a game-day. Both are worth doing and
neither is a lab — they are [guided runs](../../../CONTEXT.md), because nothing can
assert that you did them. What was modellable in the spec was the sentence underneath
it, and that is what this is.

No systems, no services, no credentials, no `pip install`. Pure stdlib, **fully
deterministic** — every number is an exact expectation over the cause distribution
rather than a simulation, so the figures below are the figures you get.

## Run it

```bash
python3 cross-cutting/labs/mitigate-before-diagnose/mitigate_drill.py
python3 cross-cutting/labs/mitigate-before-diagnose/mitigate_drill.py --break-it
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Mitigating first saves nine minutes of mean downtime**, on a distribution where
   the generic mitigation covers 76% of causes by probability. That is the slogan,
   confirmed — and it is the least interesting thing here.

2. **The tail moves the other way, by exactly six minutes.** The worst incident under
   diagnose-first is sixty minutes; under mitigate-first it is sixty-six. The extra is
   precisely the mitigation window, spent on a cause the generic mitigation was never
   going to cover — and **the worst incident you will have is, by definition, one of
   those.**

   That is the trade, and it is the right way round: **a small, bounded, known cost on
   the rare incident, to remove a large one from every common incident.** A version of
   this advice that only mentioned the win would be selling.

3. **The crossover: about 40%.** Below that coverage, diagnosing first is the better
   call. This is the number that makes the advice *falsifiable* rather than merely
   true, and it is the one worth carrying — because the honest question in a new estate
   is not *should I mitigate first*, it is **does my mitigation cover enough of what
   actually breaks here**.

4. **A mitigation that can make things worse inverts it at about ten minutes.** Past
   that expected penalty, mitigate-first is the wrong call. So the slogan quietly
   depends on a cheap, reliable mitigation — which is exactly what the
   [rehearsed restore](../../../the-stack/labs/04-backup-not-snapshot/) and a practised
   failover buy you. **They are not insurance against the incident; they are what makes
   this instinct correct.**

5. **Adding responders stops paying at about five**, because each one has to be told
   what is known and the telling comes out of the same minutes as the fixing. What buys
   more after that is not another pair of hands — it is **taking the coordination out
   of the responders' minutes**, which is the entire job description of an incident
   commander. The chapter calls the IC a coordinator who does not fix; this is why that
   is a role rather than an overhead.

6. **`--break-it` diagnoses first**, and it is not a strawman. It is what a careful
   engineer does, it is defensible in every post-mortem, and **it is what you will do
   under pressure unless you decided otherwise in advance.** One assertion breaks, and
   it is the plain one: nine more minutes down, every incident, on average.

## Verify (don't take the script's word for it)

- **Set `MITIGATION_MINUTES` to `1`** and watch the tail penalty shrink to one minute.
  The trade in step 2 is entirely the size of the window, which is the argument for
  making the mitigation fast rather than clever.
- **Flip `generic_works` to `False` on *bad deploy*** — the largest prior — and re-run.
  Coverage drops below the crossover and the advice inverts, in the direction the model
  said it would.
- **Change the distribution to your own estate's.** Six causes with priors is a thing
  you can write down from last year's incidents in an afternoon, and doing so replaces
  every number here with one that is about you.
- **Set the coordination coefficient to `0`** in step 5 and watch responders scale
  linearly. They never have. The coefficient is *stated rather than derived* and the
  README says so on purpose — the finding is that a ceiling exists, not where it is.

## The point

**An instinct you cannot falsify is a habit.** *Mitigate before you diagnose* is good
advice, and it is good advice **under conditions** — a mitigation that covers enough of
your causes and does not cost much when it fails. Both of those are properties of your
estate rather than of the advice, and both are measurable in an afternoon.

The senior instinct the chapter names is not really *mitigate first*. It is knowing,
before the pager goes off, **which one you are going to do and why** — because the
decision is not one you can make well at three in the morning while the graph is red.

## Teardown

None. Nothing was created outside the process.
