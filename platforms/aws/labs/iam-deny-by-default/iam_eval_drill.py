#!/usr/bin/env python3
"""
iam_eval_drill.py — prove, in your own hands, the central lesson of the AWS
support note: IAM is DENY-BY-DEFAULT, an explicit Deny always wins, and an SCP or
a permissions boundary can cap even an "admin" — so "just give them Allow *" is
not the fix your on-prem instinct thinks it is.

No cloud, no credentials, no external dependencies. Pure Python stdlib.

We implement a faithful (simplified) model of AWS's real policy-evaluation logic —
identity policy + Organizations SCPs + a permissions boundary + a session policy —
and then run requests through it, asserting the four behaviours that break an
on-prem admin's instinct. Alongside it we run the naive on-prem model
("I have admin, therefore I can do anything") and prove exactly where the two
disagree — that gap is the lesson.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass, field


ALLOW, DENY = "Allow", "Deny"


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


# --- the model: statements, policies, and AWS's evaluation logic --------------

def matches(pattern: str, value: str) -> bool:
    """AWS-style wildcard match for an action or resource ('*' or a '…*' prefix)."""
    if pattern == "*":
        return True
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    return pattern == value


@dataclass
class Statement:
    effect: str            # "Allow" | "Deny"
    actions: list          # e.g. ["s3:GetObject"], ["s3:*"], ["*"]
    resources: list = field(default_factory=lambda: ["*"])

    def applies(self, action, resource) -> bool:
        return (any(matches(a, action) for a in self.actions)
                and any(matches(r, resource) for r in self.resources))


# a "policy" is just a list of Statements
def has_allow(policy, action, resource) -> bool:
    return any(s.effect == ALLOW and s.applies(action, resource) for s in policy)


def has_explicit_deny(policy, action, resource) -> bool:
    return any(s.effect == DENY and s.applies(action, resource) for s in policy)


def evaluate(action, resource, *, identity, scps=None, boundary=None, session=None):
    """A faithful, simplified model of AWS IAM's decision for a single-account
    request. Returns (decision, reason). The rules, in AWS's real order:

      1. An explicit Deny in ANY applicable policy overrides everything.
      2. Otherwise the request must be explicitly Allowed by an identity policy —
         no matching Allow is an *implicit deny*.
      3. If SCPs apply, the action must ALSO be allowed by every SCP (intersection).
      4. If a permissions boundary applies, the action must ALSO be allowed by it.
      5. If a session policy applies, the action must ALSO be allowed by it.
    (Resource-based policies and condition keys exist too; omitted for clarity —
    the lesson is the deny-by-default + explicit-deny + intersection behaviour.)
    """
    scps = scps or []

    # 1. explicit Deny anywhere wins
    named = [("identity policy", identity), ("permissions boundary", boundary),
             ("session policy", session)]
    named += [(f"SCP #{i+1}", scp) for i, scp in enumerate(scps)]
    for name, pol in named:
        if pol is not None and has_explicit_deny(pol, action, resource):
            return DENY, f"explicit deny in {name}"

    # 2. must be allowed by the identity policy — else implicit deny
    if not has_allow(identity, action, resource):
        return DENY, "implicit deny (no identity-based policy allows the action)"

    # 3. SCPs are boundaries: the action must be allowed by ALL of them
    for i, scp in enumerate(scps):
        if not has_allow(scp, action, resource):
            return DENY, f"denied by SCP #{i+1} (org guardrail does not allow the action)"

    # 4. permissions boundary can only reduce
    if boundary is not None and not has_allow(boundary, action, resource):
        return DENY, "denied by permissions boundary (it does not allow the action)"

    # 5. session policy can only reduce
    if session is not None and not has_allow(session, action, resource):
        return DENY, "denied by session policy (it does not allow the action)"

    return ALLOW, "allowed"


def onprem_instinct(is_admin: bool):
    """The mental model an on-prem admin imports: 'the admin can do anything.'
    Deliberately naive — the whole drill is about where this is WRONG on AWS."""
    return ALLOW if is_admin else DENY


ADMIN = [Statement(ALLOW, ["*"], ["*"])]  # the "just give them Allow *" reflex


def run() -> int:
    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"  ✓ {ok_msg}")
        else:
            log(f"  ✗ {fail_msg}")
            failures.append(fail_msg)

    step(1, "Deny-by-default — a principal with no policy is denied")
    dec, why = evaluate("s3:GetObject", "arn:aws:s3:::reports/q3.csv", identity=[])
    log(f"  request s3:GetObject with an empty identity policy → {dec} ({why})")
    check(dec == DENY,
          "no matching Allow = implicit deny — nothing is permitted until granted (LESSON 1)",
          "an empty policy somehow allowed the action — model is wrong")

    step(2, "An explicit Allow grants it (the baseline that works)")
    scoped = [Statement(ALLOW, ["s3:GetObject"], ["arn:aws:s3:::reports/*"])]
    dec, why = evaluate("s3:GetObject", "arn:aws:s3:::reports/q3.csv", identity=scoped)
    check(dec == ALLOW, "a scoped Allow permits exactly that action",
          "a scoped Allow failed to permit its own action")

    step(3, "Explicit Deny beats Allow — even 'Allow *' admin")
    with_guardrail = ADMIN + [Statement(DENY, ["s3:DeleteObject"], ["*"])]
    dec, why = evaluate("s3:DeleteObject", "arn:aws:s3:::reports/q3.csv",
                        identity=with_guardrail)
    log(f"  admin (Allow *) + an explicit Deny on s3:DeleteObject → {dec} ({why})")
    check(dec == DENY,
          "explicit Deny overrides the Allow * — an admin can be blocked (LESSON 2)",
          "explicit Deny did not override Allow — the #1 rule is broken")

    step(4, "An SCP caps even the admin — and lives where the account can't see it")
    scp_s3_only = [Statement(ALLOW, ["s3:*"], ["*"])]  # org guardrail: S3 only
    dec, why = evaluate("ec2:RunInstances", "*", identity=ADMIN, scps=[scp_s3_only])
    log(f"  admin (Allow *) but org SCP allows only s3:* → ec2:RunInstances → {dec}")
    log(f"    reason: {why}")
    check(dec == DENY,
          "the SCP intersection denies it despite Allow * — 'grant them admin' fails (LESSON 3)",
          "the SCP did not cap the admin — intersection is broken")

    step(5, "A permissions boundary can only REDUCE, never expand")
    boundary_get_only = [Statement(ALLOW, ["s3:Get*"], ["*"])]
    dec, why = evaluate("s3:PutObject", "arn:aws:s3:::reports/new.csv",
                        identity=ADMIN, boundary=boundary_get_only)
    log(f"  admin (Allow *) but boundary allows only s3:Get* → s3:PutObject → {dec}")
    check(dec == DENY,
          "the boundary caps the admin to read-only — a boundary is a ceiling (LESSON 4)",
          "the permissions boundary failed to reduce the admin's access")

    step(6, "Your on-prem instinct vs. AWS reality — where they disagree")
    log("  on-prem model: 'this user has admin, therefore the request is allowed.'")
    log("  AWS reality:   evaluate() with the guardrails above.\n")
    cases = [
        ("s3:DeleteObject", with_guardrail, {}, "explicit Deny"),
        ("ec2:RunInstances", ADMIN, {"scps": [scp_s3_only]}, "an SCP"),
        ("s3:PutObject", ADMIN, {"boundary": boundary_get_only}, "a boundary"),
    ]
    disagreements = 0
    for action, identity, extra, capped_by in cases:
        instinct = onprem_instinct(is_admin=True)          # says ALLOW every time
        reality, _ = evaluate(action, "*", identity=identity, **extra)
        differ = instinct != reality
        disagreements += differ
        mark = "≠" if differ else "="
        log(f"  {action:<18} instinct={instinct:<5} {mark} reality={reality:<5}"
            f"   (capped by {capped_by})")
    check(disagreements == len(cases),
          "the on-prem 'admin can do anything' instinct is WRONG in every capped case",
          "the instinct and reality agreed somewhere they shouldn't have")

    log("\n" + "=" * 70)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the lessons held:")
    log("  1. Deny-by-default: no matching Allow means denied.")
    log("  2. An explicit Deny overrides any Allow — including Allow *.")
    log("  3. An SCP intersects: it caps even an admin, from a policy the account can't see.")
    log("  4. A permissions boundary is a ceiling — it only reduces.")
    log("")
    log("The instinct this drill retired:")
    log("  'give them admin and it'll work' — on AWS, Allow * is the START of the")
    log("  evaluation, not the end of it. Debugging 'why is this denied' is reading")
    log("  which of these five layers said no.")
    return 0


def main():
    argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    sys.exit(run())


if __name__ == "__main__":
    main()
