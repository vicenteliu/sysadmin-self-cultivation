---
kind: lab
axis: the-stack
themes: []
platforms: []
summary: "\"We caught it\" is a statement about a window. A posture scanner makes the window small; a guardrail closes it for exactly the classes it names; and one finding's exposure does not end when you fix it at all."
---
# Lab 07 — detection is a window, and one finding never closes

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/the-stack/labs/07-detection-is-a-window/README.md)

> **Inputs:** none · **Outputs:** exposure-minutes per finding under three regimes ·
> **Risk:** none — no cloud, no scanner, no credentials · **Root:** not needed

**Goal:** put a unit on the thing [chapter 07](../../07-security.md)'s guided run is
really about. A control matrix gives prevent and detect one column each, so they read
as alternatives of equal standing. They are not, and they differ in a number nobody
puts on the page:

```
prevent   exposure = 0 minutes, for exactly the classes the policy names
detect    exposure = (time to notice) + (time to fix), for every class
and one finding does not end when you fix it at all
```

**You'll practise:** reporting exposure-minutes instead of a finding count, and
noticing which of your findings has an exposure that outlives its ticket.

## Why this lab is pure-local

The chapter's guided run misconfigures a real bucket, catches it with the native
posture scanner and then makes it impossible with policy-as-code. Do that — the
findings pane and the denied change are worth seeing. But the finding underneath it is
arithmetic over introduction times and scan boundaries, and thirty days of an estate is
not something a trial account will show you.

Four ordinary mistakes, thirty days, three regimes. No cloud, no scanner, no
credentials, no `pip install`. Python stdlib, and CI can run it.

## Where this sits, and why it is not `one-control-three-stages` again

[`one-control-three-stages`](../../../cross-cutting/labs/one-control-three-stages/) asks
what a control matrix **cannot express** — blast radius, and the prevent/detect/recover
collapse. It is a critique of the format.

This lab takes the same collapse and **prices it**. It is the arithmetic that turns *the
matrix has one column for two different claims* into *and here is what the difference
cost you in hours this month*. The first is why you should stop using the format; this
is what to write in the box instead.

## Run it

```bash
python3 the-stack/labs/07-detection-is-a-window/exposure_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Four ordinary mistakes, priced three ways.** A public backup bucket, an admin port
   open to the world, an unencrypted volume from a restore, an API key in a commit.
   Nothing exotic — each is a thing a competent person does on a Tuesday.

2. **Scanning faster is a real win with a floor it cannot cross.** Daily → hourly saves
   69 hours across the month and still leaves 220, **because a scan runs after the
   fact.** A 24× faster scanner cannot reach zero, and no scanner ever will.

3. **The guardrail takes two classes to zero and does nothing for the other two.** A
   policy is a list of named classes; everything you did not think of is still on the
   detection path, and the matrix records *prevented* for the row either way.

   **Then read the totals again, because the guardrail column is worse than the hourly
   one.** Deploying policy-as-code and relaxing the scan cadence *lost* time overall:
   prevention retired two classes and the other two lost their fast detection. **A
   guardrail retires a class, not a scanner.** The two are not alternatives, and the
   matrix format says they are.

4. **The finding whose exposure does not end when you fix it.** The API key was
   committed, noticed within the hour, and the commit removed 80 minutes later. The
   ticket says 1.3 hours. The exposure is 216 hours **and still running**, because
   removing a commit does not un-read a key. Time-to-remediate is a true number here
   and it measures the wrong event; the number that matters is **time-to-rotate**, and
   no scanner reports it because rotation happens in a system the scanner cannot see.

5. **What to report, once you have the unit.** Not *"4 findings, all remediated, MTTR
   41 minutes."* But *"220 hours of exposure this month; two classes prevented at zero
   cost; two detect-only; one of the four is a credential whose exposure has not ended,
   because it has not been rotated."*

## Verify (don't take the script's word for it)

```bash
python3 exposure_drill.py --sabotage fixing-ends-exposure     # exit 1
python3 exposure_drill.py --sabotage policy-covers-everything # exit 1
```

`fixing-ends-exposure` treats the credential like the bucket — the assumption behind
every *remediated* status in every findings pane — and exactly one assertion breaks,
which is the one that says a leaked key is a different kind of finding.

`policy-covers-everything` gives the guardrail an infinite list. Three assertions break,
and the second is the interesting one: with total coverage the cadence trade disappears,
so *the trade only exists because a policy is finite.* If your model of policy-as-code
has no uncovered classes in it, you are not modelling policy-as-code.

To go further, set the scan interval to 5 minutes and watch the first three findings
shrink toward zero while the fourth does not move at all. Everything a scanner can buy
you, it has bought by then — and the largest number on the page is still the one it
cannot touch.

## The point

**"We caught it" is a statement about a window.**

Three things to carry out:

- **Report exposure-minutes, not a finding count.** A count is the same for a mistake
  that lived four minutes and one that lived four weeks.
- **A guardrail retires a class; it does not retire the scanner.** If deploying policy
  is the reason the scan cadence relaxed, the estate went backwards, and the matrix
  records an improvement.
- **A leaked credential's clock does not stop at remediation.** For that one class the
  reportable number is time-to-rotate, and it is measured in a system nobody has wired
  to the findings pane.

## Teardown

None. The drill holds everything in memory and writes nothing.
