# Lab — IAM is deny-by-default (prove it in your own hands)

**Goal:** make the central lesson of the [AWS support note](../../support.md) tangible
— **IAM is deny-by-default, an explicit `Deny` always wins, and an SCP or a
permissions boundary caps even an "admin" — so "just give them `Allow *`" is not the
fix your on-prem instinct thinks it is.** You'll run a faithful (simplified) model of
AWS's real policy-evaluation logic and watch requests get denied for five distinct
reasons — the exact reasons behind most "Access Denied" tickets.

**You'll practice:** reading a decision as *"which layer said no?"* — implicit deny
(no allow), explicit deny, SCP intersection, permissions-boundary ceiling — and
seeing precisely where the on-prem *"the admin can do anything"* model is wrong.

## Why this lab is pure-local

No cloud, no credentials, no cost, no external packages — just Python 3.8+. The
"policies" are lists of `Statement` objects and the evaluator is a small, honest
implementation of AWS's real order of operations:

1. An explicit `Deny` in **any** applicable policy overrides everything.
2. Otherwise the request must be explicitly **allowed by an identity policy** — no
   matching Allow is an *implicit deny*.
3. If SCPs apply, the action must **also** be allowed by every SCP (**intersection**).
4. A **permissions boundary** can only **reduce** (a ceiling).
5. A **session policy** can only reduce.

(Resource-based policies and condition keys exist too; omitted so the deny-by-default
+ explicit-deny + intersection behaviour is undeniable, not buried.)

## Run it

```bash
python3 iam_eval_drill.py
```

That's it — no install. Exit code `0` means every assertion held, so it doubles as a
CI check.

## What you'll see

Six narrated steps, each ending in a checked lesson:

```
=== 3. Explicit Deny beats Allow — even 'Allow *' admin ===
  admin (Allow *) + an explicit Deny on s3:DeleteObject → Deny (explicit deny in identity policy)
  ✓ explicit Deny overrides the Allow * — an admin can be blocked (LESSON 2)
=== 4. An SCP caps even the admin — and lives where the account can't see it ===
  admin (Allow *) but org SCP allows only s3:* → ec2:RunInstances → Deny
  ✓ the SCP intersection denies it despite Allow * — 'grant them admin' fails (LESSON 3)
=== 6. Your on-prem instinct vs. AWS reality — where they disagree ===
  s3:DeleteObject    instinct=Allow ≠ reality=Deny    (capped by explicit Deny)
  ec2:RunInstances   instinct=Allow ≠ reality=Deny    (capped by an SCP)
  s3:PutObject       instinct=Allow ≠ reality=Deny    (capped by a boundary)
```

## Verify (don't take the script's word for it)

Open a Python shell next to the file and drive the evaluator yourself:

```python
from iam_eval_drill import evaluate, Statement, ADMIN
# Allow * admin, but an org SCP only permits S3 — try to launch an instance:
scp = [Statement("Allow", ["s3:*"])]
print(evaluate("ec2:RunInstances", "*", identity=ADMIN, scps=[scp]))
# → ('Deny', 'denied by SCP #1 (org guardrail does not allow the action)')
```

Then break it deliberately — delete the SCP check in `evaluate()` and re-run
`python3 iam_eval_drill.py`: it must exit **non-zero** with failed assertions. A
self-verifier that can't fail is worthless.

## The point

- **Deny-by-default is the inversion that breaks your instinct.** On-prem, admin is
  god and a firewall is an allow-list. On AWS, `Allow *` is the *start* of the
  evaluation, not the end — five layers can still say no.
- **An explicit `Deny` always wins.** Guardrails are written as Denies precisely
  because they must beat any Allow, including an admin's.
- **The blocker can be invisible from the account.** An SCP lives in AWS
  Organizations; the account whose request is denied often can't even read it — which
  is why "just add an allow" fails and the real skill is *reading which layer denied*.
- **This is the #1 support ticket.** "Why is this denied?" is answered by walking these
  layers — in the console with the IAM Policy Simulator, CloudTrail's `errorCode`, and
  IAM Access Analyzer. You just built the model those tools evaluate.

## Teardown

Nothing persistent is created — the drill writes no files. Nothing to clean up.
