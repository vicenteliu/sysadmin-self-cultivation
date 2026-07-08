# Lab — Conditional Access self-lockout (prove it in your own hands)

**Goal:** make the most dangerous lesson of the [M365 support note](../../m365-support.md)
tangible — **a Conditional Access policy scoped to "All users" is tenant-live the
instant you enable it; it blocks everyone who doesn't satisfy the grant, including the
admin who wrote it and the break-glass account unless it's excluded — and `report-only`
is how you learn that *before* the outage instead of during it.** You'll ship a naive
policy, watch yourself get locked out, add the fire exit, and see report-only enforce
nothing.

**You'll practice:** the reflex the note insists on — **exclude two break-glass
accounts and run report-only first** — by feeling exactly what happens when you don't.

## Why this lab is pure-local

No tenant, no credentials, no cost, no external packages — just Python 3.8+. Four
`User`s and one `CAPolicy` model the tenant; `evaluate_sign_in()` applies the same
order the service does: **state → scope → exclusions → grant controls**. The break-glass
account is modelled the way the note prescribes — cloud-only, on a FIDO2 key, *not* an
Intune-compliant device — which is exactly why a "require compliant device" grant
catches it.

## Run it

```bash
python3 ca_lockout_drill.py
```

That's it — no install. Exit code `0` means every assertion held, so it doubles as a
CI check.

## What you'll see

Five narrated steps, each ending in a checked lesson:

```
=== 1. Ship a naive policy: All users, require compliant device, ENABLED ===
  admin        LOCKED OUT  — BLOCKED: policy requires a compliant device, user has none
  alice        sign-in OK  — grant satisfied
  ✓ the ADMIN who wrote it is locked out — 'it won't apply to me' is false (LESSON 1)
=== 2. The break-glass account is NOT excluded — so it's locked out too ===
  ✓ break-glass is ALSO locked out — you now have NO way back in (LESSON 2)
=== 4. The safe way to have shipped it: the SAME policy in REPORT-ONLY ===
  ✓ report-only enforces NOTHING — nobody is blocked, impact is only logged (LESSON 4)
```

## Verify (don't take the script's word for it)

Drive the model yourself in a Python shell:

```python
from ca_lockout_drill import User, CAPolicy, evaluate_sign_in
admin = User("admin", compliant_device=False)
enabled = CAPolicy("Require compliant device", state="enabled",
                   all_users=True, require_compliant_device=True)
print(evaluate_sign_in(admin, enabled))   # (False, 'BLOCKED: ... no compliant device')
enabled.excluded = {"admin"}
print(evaluate_sign_in(admin, enabled))   # (True, 'excluded from the policy (the fire exit)')
```

Then break it deliberately — make report-only enforce like enabled — and re-run: the
drill must exit **non-zero**. A self-verifier that can't fail is worthless.

## The point

- **"I'm the admin, it won't apply to me" is false.** An all-users policy has no
  special case for its author; the moment it's enabled it evaluates *you* too.
- **Break-glass survives only if you exclude it.** Two cloud-only emergency accounts,
  excluded from every CA policy, are the difference between a two-minute recovery and a
  Microsoft support case during an outage.
- **`report-only` is the safety valve.** It evaluates and logs impact without
  enforcing — ship every new tenant-wide policy this way first, read the sign-in logs,
  *then* enable. This drill shows the same policy going from "locked everyone out" to
  "enforced nothing" by flipping one field.
- **This is the tenant-wide blast radius, felt.** One policy, one save, everyone at
  once — the exact reason the note says never edit a tenant-wide policy without a pilot
  group and report-only.

## Teardown

Nothing persistent is created — the drill writes no files. Nothing to clean up.
