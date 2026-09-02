---
kind: lab
axis: endpoint
themes: [endpoint, identity]
platforms: []
marker: "🔨"
summary: "The console says the policy reaches 3. It reaches 22. Three years later it reaches 30 and nobody edited it — because the group it is scoped to is populated by joiner-mover-leaver, and a blast radius is a function of time."
---
# Lab — the console says 3, the policy reaches 22, and in three years it reaches 30

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/endpoint/labs/policy-blast-radius/README.md)

> **Inputs:** none · **Outputs:** a per-step report of what the policy actually
> reaches, then and now · **Risk:** none — no MDM, no tenant, no device, no
> credentials · **Root:** not needed

**Goal:** answer the question [`endpoint/management.md`](../../management.md) says
should be answered before any policy ships — *how many devices does this reach, and
what is the worst thing it does to them* — and then show that the answer has an expiry
date nobody attaches to it.

**You'll practise:** resolving a scope rather than reading one, and the habit of
re-deriving a number you already signed off on.

## Why this lab is pure-local

Scoping is an *arithmetic* problem about set membership over time, not a vendor one.
Every management platform has the same shape underneath — a group, a nesting rule, an
exclusion, and devices attached to people — so it is fully expressible as a model.

The [spec this lab replaces](../../README.md) asked for a trial MDM and a spare device.
That is a **guided run**, not a lab ([`CONTEXT.md`](../../../CONTEXT.md) keeps those
words apart), and it would have taught the console rather than the problem — you cannot
watch three years pass on a trial tenant.

No MDM, no tenant, no device, no credentials, no `pip install`. Python stdlib, fully
deterministic, and CI can run it.

## Run it

```bash
python3 endpoint/labs/policy-blast-radius/blast_radius_drill.py
python3 endpoint/labs/policy-blast-radius/blast_radius_drill.py --break-it
```

Exit code `0` means every assertion about the lesson held.

## The office it models

Not invented — [the reference office's stated rates](../../../the-reference-office.md#parameters),
run forward for 1095 days: a hundred people across eight functions, about twenty-three
joiners and seventeen leavers a year, one device each with a three-year refresh, five
spares on the shelf.

One number in the model is **not** from the reference office and the drill says so in a
comment: **internal moves.** That file deliberately states no mover rate, because none is
derivable and none is worth inventing. This drill needs one to run, uses twelve a year,
and is the wrong place to look for that number's authority.

The policy is scoped to an access bundle that looks like every access bundle after
eighteen months: **one whole function nested in, plus three people added individually**
because somebody needed access once. An exclusion group protects a different function.

## What you'll see

1. **The console number and the real number are different on day one.** The screen shows
   **3** direct members. The policy reaches **22** enrolled devices. The gap is not a
   bug — nesting is not displayed, people hold a second machine after a refresh, and a
   spare on the shelf belongs to nobody and therefore matches no exclusion.

2. **Three years later it reaches 30, and nobody edited the policy.** A **+36%** drift
   produced entirely by joiners, leavers and movers arriving in and out of a nested
   group. There is no change record to review, because nothing changed.

3. **The exclusion drifts, and it drifts the wrong way.** Thirteen people were exempt on
   day zero and sixteen are exempt now — but only **five are the same people**. Eight
   lost an exemption nobody revoked, by moving team. Nothing fired, because
   [a mover has a conversation](../../../build-out/15-joiner-mover-leaver.md) and not an
   event.

4. **Eight enrolled devices have no holder at all** — five spares and three returns
   nobody wiped. They match the scope for a reason that is structural rather than
   careless: **exclusions are written about people, and these devices have none.**

5. **`--break-it` counts the way the console does**, and this is the part worth sitting
   with. It reports **3** on day zero and **3** on day 1095. The number is *stable*, it
   is *confidently displayed*, and it was only ever right about a question nobody asked.
   Three assertions break, and the third is the one that matters: **the method cannot
   tell you its answer has expired**, because it has no representation of time at all.

## Verify (don't take the script's word for it)

- **Change `MOVERS_PER_YEAR` to `0`** and re-run. The drift shrinks but does not vanish —
  what remains is joiners and leavers alone, which is the floor even in an office where
  nobody ever changes team.
- **Set `HORIZON` to `365`** and watch the drift at one year rather than three. It is
  already visible, which is the argument for a cadence rather than an annual review.
- **Remove the three individual grants** from `restricted-config` in `groups_on()` and
  re-run. The console number goes to zero while the policy still reaches most of a
  function — the pathological version of the same failure, and the one an estate reaches
  when every bundle is built purely from nested groups.
- **Add a spare** to the shelf loop and confirm it lands inside the reach. There is no
  policy language in the model that would have stopped it, which is the point.

## The point

**A blast radius is a function of time and it is reviewed as a constant.**

You compute it once, at authoring, from a screen that shows direct membership. From then
on the number lives in a change record that will never be reopened, while the actual
reach is recomputed continuously by a directory that turns over
[about forty times a year](../../../the-reference-office.md#why-these-numbers).

The remediation is not a better console. It is **re-deriving the number on a cadence and
alerting on the delta** — a policy whose target set grew by a third this quarter is
telling you something about the directory, not about the policy.

And the failure has the shape this repo keeps finding: nothing here is misconfigured,
nobody was careless, every individual grant was correct on the day it was made, and the
control that is missing was never an access control. It is a **re-derivation** — which
is the same answer [`transcript-retention`](../../../cross-cutting/labs/transcript-retention/)
reaches about expiry, arrived at from the other end.

## Teardown

None. Nothing was created outside the process.
