# Lab — state is the source of truth (and drift is the enemy)

**Goal:** feel the one thing an **Ansible/config-management sysadmin gets wrong about
Terraform** — that it does *not* converge against the real world every run. It plans
against a **state file**, and the gap between three worlds is where every Terraform
surprise lives:

```
config   your .tf — the desired state
state    terraform.tfstate — what Terraform BELIEVES exists
real     the actual infrastructure
```

`plan` = refresh state from real, then diff **config vs state** → actions.
`apply` = make real match config, and update state to match.

What it drills — six lessons that fall out of that one model:
1. **Empty state → CREATE.** No state, so Terraform plans to create.
2. **apply → convergence.** config == state == real; re-plan is a clean no-op.
3. **Drift → revert.** A hand-edit to real (the console hotfix) is refreshed into state,
   detected, and **reverted back to config** on the next apply — *Terraform fights you.*
4. **Immutable → REPLACE.** Changing a `ForceNew` attribute forces **destroy+recreate**,
   not an in-place edit. You only catch it by reading the plan for `forces replacement`.
5. **Lost state → duplicate/clobber.** With no state, Terraform wants to *re-create* a
   resource that already exists; `terraform import` reconciles state with reality.
6. **`count` vs `for_each`.** Removing the middle item of a `count` list shifts indices and
   churns resources; `for_each` keys are stable and only the removed key is touched.

## Why local

No cloud account, no credentials, no `terraform apply` against real infrastructure, no
bill, no blast radius. The drill is a ~200-line model of Terraform's plan engine — the
config/state/real triangle, refresh, the replace-vs-update decision, and index-vs-key
addressing — so the *logic* is what you inspect, not a screen of HCL. Runs anywhere
Python does, and in CI.

## Run

```bash
python3 state_drift_drill.py
```

## What you'll see

Six narrated steps, each with an `OK`/`XX`: an empty-state CREATE; convergence after
apply; a console hotfix getting reverted; an immutable change forcing REPLACE; lost
state wanting to re-create an existing resource (then `import` fixing it); and `count`
churning a shifted resource while `for_each` leaves its neighbors alone. Ends with a
PASS verdict and `exit 0`.

## Verify (the important part)

Exit `0` = every lesson held; it doubles as a CI check. Now **break the model on
purpose** — two independent sabotage vectors:

```bash
python3 state_drift_drill.py --sabotage no-refresh    # plan stops refreshing from real -> drift undetected -> step 3 FAILS, exit 1
python3 state_drift_drill.py --sabotage mutable-all   # nothing is ForceNew -> a replace looks in-place -> step 4 FAILS, exit 1
```

If plans that ignore the real world still "passed," refresh wasn't doing anything; if a
ForceNew change still looked like an in-place edit, the immutable rule wasn't load-bearing.
The failures are the proof the model matters.

## The point

Two config-management reflexes get corrected here at once. First, **"just run it again,
it converges"** — Terraform's convergence is mediated by a *state file* that can drift,
lock, or be lost, and a blind re-run can *destroy*. Second, **"SSH in and fix it"** — a
manual hotfix becomes drift and gets reverted on the next apply. The discipline: change
the code, read the plan (especially for `forces replacement`), keep state remote +
locked, and never edit around Terraform. State is the source of truth. See the
[Terraform support note](../../terraform-support.md) for the full ticket catalog, and
[`iac-and-config.md`](../../iac-and-config.md) for where provisioning ends and
configuration begins.

## Teardown

None — it's a single self-contained script. Delete the folder to remove it.
