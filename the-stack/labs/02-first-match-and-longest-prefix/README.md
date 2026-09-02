---
kind: lab
axis: the-stack
themes: [networking]
platforms: []
summary: "A routing table and a firewall ruleset are both ordered lists of prefixes, and only one of them cares about the order. Neither file says which."
---
# Lab 02 — two files, two lookup disciplines, and nothing on the page says which

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/the-stack/labs/02-first-match-and-longest-prefix/README.md)

> **Inputs:** none · **Outputs:** the verdicts each file produces, shuffled and
> unshuffled · **Risk:** none — no network, no cloud, no credentials · **Root:** not
> needed

**Goal:** make undeniable a thing [chapter 02](../../02-network.md) states in two
separate sections and that almost nobody holds as **one** idea — a network path is
decided by two lookup disciplines that look identical on the page and are not.

```
a routing table   resolves by LONGEST PREFIX  — order-independent
a firewall ruleset resolves by FIRST MATCH     — order-dependent
```

**You'll practise:** asking which discipline a file uses *before* reading it, which is
the one question neither file answers.

## Why this lab is pure-local

The failure is a *reasoning* failure before it is a network failure. Both files are an
ordered list of lines with an address on each, both are read on a screen that shows
them in order, and the difference between them lives entirely in the resolver. That is
fully expressible as a model — two classes, one `max(prefixlen)` and one `hits[0]` —
and modelling it is what makes the contrast visible in one screen instead of across
two incidents a year apart.

No network, no cloud, no credentials, no `pip install`. Python stdlib, and CI can run
it.

## Run it

```bash
python3 the-stack/labs/02-first-match-and-longest-prefix/lookup_order_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Two files, printed side by side.** Same shape. Nothing in either one declares its
   resolver.

2. **Shuffle both twenty times.** Every verdict from the routing table is identical;
   eleven of twenty shuffles change a verdict from the ruleset. That is the whole
   difference, measured.

3. **The mirror error, first direction: "move the route up to prioritise it."** A
   ticket says a host is going out the wrong way, the line gets promoted to the top,
   and **nothing changes** — which the operator reads as *the route is not the
   problem*. It is the problem; the fix is a different prefix or next hop, and where
   the line sits was never going to matter.

4. **The mirror error, second direction: "add a broad allow at the top to unblock
   it."** One `allow 10.20.0.0/16 any` makes **three** rules below it inert, including
   a deliberate quarantine deny. The ruleset still *contains* the deny — a screenshot
   of it is truthful — and nothing in a console, a diff or an access review reports
   *never matches*.

5. **The asymmetry worth carrying.** A `/32` on the last line of a routing table beats
   a `/0` on the first. A `/32` on the last line of a ruleset loses to a `/16` on the
   first. **The same specific line wins in one file and loses in the other**, and that
   sentence is the lab.

## Verify (don't take the script's word for it)

A self-verifier that cannot fail is worthless. There are two independent sabotage
vectors, and each one implements the *mistaken model* so you can watch what it would
have predicted:

```bash
python3 lookup_order_drill.py --sabotage routes-first-match    # exit 1
python3 lookup_order_drill.py --sabotage rules-longest-prefix  # exit 1
```

If a first-match routing table still passed, longest-prefix was not deciding anything;
if a longest-prefix ruleset still passed, order was not. Both break three assertions,
and the third is the same one in each: specificity stops behaving differently in the
two files, which is exactly the confusion the drill exists to name.

To go further, add a fourth rule *below* the broad allow and re-run: the shadowed count
goes to four and no other output moves. The ruleset grows and the estate does not
change, which is how a rule file reaches forty lines of which nine can fire.

## The point

**Before you read either file, ask which discipline it uses.**

Three things to carry out:

- **Reordering a routing table is a no-op, and it reads as a ruled-out theory.** The
  danger is not the wasted minute; it is the false conclusion at the end of it.
- **A broad rule at the top is a silent mass-disable.** The rules below it still exist,
  still review clean, and never fire. Ask a ruleset which of its rules *can* match, not
  which of them are present.
- **Specificity is a tiebreaker in one file and irrelevant in the other.** Carrying the
  wrong intuition across produces two failures that are exact mirrors, and neither one
  announces itself.

## Teardown

None. The drill holds everything in memory and writes nothing.
