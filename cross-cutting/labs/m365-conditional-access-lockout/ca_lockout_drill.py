#!/usr/bin/env python3
"""
ca_lockout_drill.py — prove, in your own hands, the most dangerous lesson of the
M365 support note: a Conditional Access policy scoped to "All users" is tenant-live
the instant you enable it — it blocks EVERYONE who doesn't satisfy the grant,
INCLUDING the admin who wrote it and the break-glass account (unless it's excluded).
report-only mode is how you find that out *before* the outage instead of during it.

No cloud, no tenant, no credentials, no external dependencies. Pure Python stdlib.

We model M365 sign-in evaluation under one Conditional Access policy, then:
  1. enable a naive "all users, require compliant device" policy and watch the
     admin lock themselves out ("it won't apply to me" is false);
  2. see the break-glass account get locked out too — no way back in;
  3. exclude break-glass and confirm the fire exit now exists;
  4. re-run the SAME policy in report-only and confirm it enforces nothing —
     the safe way to have shipped it.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass, field


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


# --- the model: users, a CA policy, and the sign-in evaluation ----------------

@dataclass
class User:
    name: str
    compliant_device: bool = False   # is the device Intune-compliant?
    mfa_registered: bool = True      # has the user registered an MFA method?
    break_glass: bool = False        # emergency-access account?


@dataclass
class CAPolicy:
    name: str
    state: str = "enabled"           # "enabled" | "report-only" | "disabled"
    all_users: bool = True           # scope: every user in the tenant
    included: set = field(default_factory=set)   # used when all_users is False
    excluded: set = field(default_factory=set)   # the exclusions that save you
    require_compliant_device: bool = False
    require_mfa: bool = False

    def in_scope(self, user: User) -> bool:
        return self.all_users or user.name in self.included


def evaluate_sign_in(user: User, policy: CAPolicy):
    """Return (allowed, reason) for one user under one CA policy — the same order
    the service applies: state → scope → exclusions → grant controls."""
    if policy.state == "disabled":
        return True, "policy disabled"
    if policy.state == "report-only":
        # evaluated and logged, but NOT enforced — the whole point of the mode
        return True, "report-only: logged, NOT enforced"
    if not policy.in_scope(user):
        return True, "out of policy scope"
    if user.name in policy.excluded:
        return True, "excluded from the policy (the fire exit)"
    # grant controls — the user must satisfy ALL required controls
    if policy.require_compliant_device and not user.compliant_device:
        return False, "BLOCKED: policy requires a compliant device, user has none"
    if policy.require_mfa and not user.mfa_registered:
        return False, "BLOCKED: MFA required but the user hasn't registered one"
    return True, "grant satisfied"


def naive_instinct():
    """The mental model an admin imports: 'I'm the admin — the policy I just wrote
    won't lock ME out.' The drill is about how false that is."""
    return True  # "I can always get in"


def report(users, policy):
    """Evaluate every user, print the outcome, return {name: allowed}."""
    outcome = {}
    for u in users:
        allowed, why = evaluate_sign_in(u, policy)
        outcome[u.name] = allowed
        tag = "sign-in OK " if allowed else "LOCKED OUT "
        log(f"  {u.name:<12} {tag} — {why}")
    return outcome


def run() -> int:
    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"  ✓ {ok_msg}")
        else:
            log(f"  ✗ {fail_msg}")
            failures.append(fail_msg)

    # the tenant: an admin on a personal (non-compliant) laptop, two staff, and a
    # cloud-only break-glass account (FIDO2, no Intune device — compliant=False).
    admin = User("admin", compliant_device=False)
    alice = User("alice", compliant_device=True)      # corporate, compliant
    bob = User("bob", compliant_device=False)         # personal laptop
    breakglass = User("breakglass", compliant_device=False, break_glass=True)
    users = [admin, alice, bob, breakglass]

    step(1, "Ship a naive policy: All users, require compliant device, ENABLED")
    naive = CAPolicy("Require compliant device", state="enabled", all_users=True,
                     require_compliant_device=True)
    out = report(users, naive)
    check(out["alice"] is True,
          "alice (compliant device) still signs in — the policy does its job for her",
          "alice was blocked — the model is wrong")
    check(out["admin"] is False,
          "the ADMIN who wrote it is locked out — 'it won't apply to me' is false (LESSON 1)",
          "the admin was not locked out — the all-users policy didn't apply to them")

    step(2, "The break-glass account is NOT excluded — so it's locked out too")
    check(out["breakglass"] is False,
          "break-glass is ALSO locked out — you now have NO way back in (LESSON 2)",
          "break-glass survived without being excluded — the model is wrong")
    log("  → with both the admin and break-glass blocked, recovery means a Microsoft")
    log("    support case. This is the outage the note warns about.")

    step(3, "The fix: EXCLUDE the break-glass account from the policy")
    fixed = CAPolicy("Require compliant device", state="enabled", all_users=True,
                     excluded={"breakglass"}, require_compliant_device=True)
    out = report(users, fixed)
    check(out["breakglass"] is True,
          "break-glass now signs in — the fire exit exists (LESSON 3)",
          "break-glass still blocked after exclusion — the fix didn't work")
    check(out["admin"] is False,
          "the admin is still blocked (as designed) — but now there's a way back in",
          "excluding break-glass unexpectedly changed the admin outcome")

    step(4, "The safe way to have shipped it: the SAME policy in REPORT-ONLY")
    report_only = CAPolicy("Require compliant device", state="report-only",
                           all_users=True, require_compliant_device=True)
    out = report(users, report_only)
    check(all(out[u.name] for u in users),
          "report-only enforces NOTHING — nobody is blocked, impact is only logged (LESSON 4)",
          "report-only blocked someone — it must never enforce")
    log("  → shipped report-only first, you'd have SEEN the admin+break-glass impact")
    log("    in the sign-in logs and fixed it before enabling. That's the workflow.")

    step(5, "Your instinct vs. reality — the admin under the enabled policy")
    instinct = naive_instinct()                      # "I can always get in"
    reality, _ = evaluate_sign_in(admin, naive)      # enabled all-users policy
    log(f"  instinct: admin can always get in = {instinct}")
    log(f"  reality:  admin under the enabled all-users policy = {reality}")
    check(instinct != reality,
          "the 'I'm the admin, it won't lock me out' instinct is WRONG",
          "instinct and reality agreed — the drill proved nothing")

    log("\n" + "=" * 70)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the lessons held:")
    log("  1. An enabled all-users policy is tenant-live and blocks the admin too.")
    log("  2. Break-glass is blocked unless it is explicitly EXCLUDED.")
    log("  3. Excluding break-glass restores a way back in — the fire exit.")
    log("  4. report-only enforces nothing — it shows impact before you enable.")
    log("")
    log("The habit this drill builds:")
    log("  never enable a tenant-wide CA policy without (a) excluding two break-glass")
    log("  accounts and (b) running it report-only first. One save, no outage.")
    return 0


def main():
    argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    sys.exit(run())


if __name__ == "__main__":
    main()
