---
kind: lab
axis: cross-cutting
themes: []
platforms: []
marker: "🔨"
summary: "Six of six kill-chain stages covered, resting on seven controls, one of which carries three stages alone — and the last stage is not prevented at all, it is survived. A control matrix cannot say any of the three."
---
# Lab — six of six covered, and EDR is doing three of them alone

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/cross-cutting/labs/one-control-three-stages/README.md)

> **Inputs:** none · **Outputs:** the matrix, then the four things it cannot express ·
> **Risk:** none — no tools, no scanners, no credentials · **Root:** not needed

**Goal:** do what [`working-with-security.md`](../../working-with-security.md) asks —
name the control you own at each kill-chain stage — and then **read the answer sheet
for what it hides**, which is a different exercise and the one that changes anything.

**You'll practise:** noticing that a control matrix is indexed by *stage* while every
question worth asking is about a *control*.

## Why this lab is pure-local

Coverage is set arithmetic: stages, controls, and which covers which. There is nothing
to scan, and scanning would not answer these questions anyway — a posture tool reports
per-resource findings, and the failure here is in the *shape of the summary*.

The spec this replaces said *no tools, just judgment*, and it was right. What it did
not say is that the judgement produces a table, and that **the table's format is the
trap**. That part is modellable, so it is modelled.

No tools, no scanners, no credentials, no `pip install`. Pure stdlib, fully
deterministic.

## Run it

```bash
python3 cross-cutting/labs/one-control-three-stages/coverage_drill.py
python3 cross-cutting/labs/one-control-three-stages/coverage_drill.py --break-it
```

Exit code `0` means every assertion about the lesson held.

## The estate it models

Ordinary and competent, not bad: a patch pipeline, mail filtering, EDR, MFA, a secret
manager, central logging, tested backups — **and two controls that exist in the design,
the diagram and the audit answer but not in the estate**: least privilege and network
segmentation. That last pair is the most realistic thing in the model.

## What you'll see

1. **Six stages of six have an answer.** Which is what the matrix was built to show,
   and it is true.

2. **Eleven filled rows rest on seven distinct controls.** A matrix has one row per
   stage, so a control that answers three stages is written three times and **counted
   three times**. The estate does not work that way. It fails once.

3. **EDR alone is the only preventive control at three stages** — execution, privilege
   escalation and lateral movement. If it fails, is bypassed, or is not installed on
   the host that matters, three of the six stages have nothing in the way at once.

   **Nothing in the matrix format asks this question**, because the matrix is indexed by
   stage and this is a question about a control. It is the single highest-value thing
   in the output and it takes one column that no template has.

4. **The last stage is not prevented. It is survived.** There are **three kinds** of
   control and the matrix has one column for all of them:

   | Kind | What the attacker experiences |
   |---|---|
   | **Prevent** | They do not get through |
   | **Detect** | They get through and you find out |
   | **Recover** | They get through, **it works**, and you come back afterwards |

   Tested backups are the third kind. They are one of the most valuable controls in any
   estate and they **do not prevent impact** — ransomware still runs, the data is still
   encrypted, and you restore. Writing *tested backups* in the impact row and calling
   the stage covered says the attacker fails there. They do not.

5. **The two unfinished controls explain the third finding.** Least privilege and
   segmentation would each have given a second control at two of EDR's three stages. So
   **on paper EDR was never carrying them alone** — which is precisely why nobody
   noticed that in the estate it is.

6. **`--break-it` scores per stage**, which is not a strawman. It is the format of every
   control matrix, every audit response and every security questionnaire, and it
   reports **6 of 6**. Two assertions break, and both are of the same kind: the scoring
   has no column for the question, so it cannot be wrong — it can only be silent.

## Verify (don't take the script's word for it)

- **Set `least privilege` to `in_place=True`** and re-run. EDR's blast radius drops
  from three stages to one, and it is the cheapest change in the file — which is the
  actual recommendation this lab produces.
- **Change `tested backups` to `kind="prevent"`** and watch step 4 report every stage
  prevented. That one edit is the whole of the error being described, and it is the
  edit a control matrix makes by default.
- **Add a second EDR-class control** covering execution only, and see the blast radius
  narrow without any stage's *coverage* changing. Coverage was never the variable.
- **Replace the estate with your own.** Nine controls and six stages is an afternoon,
  and the output is a sentence you can hand to a security team: *these are the stages,
  this is what carries each one, and this one control carries three.*

## The point

**A control matrix is indexed by the wrong thing.** It asks *is this stage covered*,
which has a reassuring answer, and never asks *what is this coverage resting on*, which
does not.

Three questions the format cannot express, all answerable in an afternoon:

- **Which control, failing, opens the most stages?** — the blast radius, which is a
  property of a control and has no row.
- **Prevent, detect, or recover?** — three different claims sharing one word.
- **Designed, or deployed?** — the two are indistinguishable in an audit answer and
  entirely distinguishable during an incident.

And the handoff the spec asked for gets better for it. *We have six of six covered* is
not useful to a SOC analyst. *EDR is our only preventive control at three stages, impact
is recovery-only, and least privilege is designed but not deployed* is the two sentences
they actually needed — and that **is** working with security.

## Teardown

None. Nothing was created outside the process.
