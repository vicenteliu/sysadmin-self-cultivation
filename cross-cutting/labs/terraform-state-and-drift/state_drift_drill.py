#!/usr/bin/env python3
"""
Terraform drill — state is the source of truth, and drift is the enemy.

Pure-local, stdlib-only. Models the one thing an Ansible/config-management sysadmin
gets wrong about Terraform: it does NOT converge against the real world every run.
It plans against a STATE FILE — a persistent record of what it made — and the gap
between three worlds is where every Terraform surprise lives:

    config  (your .tf — the desired state)
    state   (terraform.tfstate — what Terraform BELIEVES exists)
    real    (the actual infrastructure)

    plan  = refresh state from real, then diff config vs state -> actions
    apply = make real match config, and update state to match

From that one model, six lessons fall out:
  1. empty state  -> plan wants to CREATE
  2. apply        -> state and real both converge to config
  3. drift        -> a hand-edit to real is detected and REVERTED ("Terraform fights you")
  4. immutable    -> changing a ForceNew attribute REPLACES (destroy+recreate), not in-place
  5. lost state   -> Terraform wants to re-CREATE a resource that already exists; `import` fixes it
  6. count vs for_each -> reordering a `count` list shifts indices and churns resources;
                          `for_each` keys are stable

Run clean and every lesson holds -> exit 0 (doubles as a CI check).
Run with --sabotage to break the model and watch the guarantees fall -> exit 1:
  --sabotage no-refresh  : plan stops refreshing from real -> drift goes undetected (step 3 fails)
  --sabotage mutable-all : nothing is immutable -> a ForceNew change looks in-place (step 4 fails)
"""

import argparse
import sys

# Attributes that force destroy+recreate when changed (the provider "ForceNew" flag).
# NOTE: for aws_instance these are genuinely ForceNew (changing them can't be done
# in place) — unlike instance_type or tags, which update in place. Getting this right
# matters: claiming instance_type forces replacement is a common and catchable error.
IMMUTABLE = {"ami", "availability_zone", "subnet_id"}


def log(msg=""):
    print(msg)


def step(n, title):
    log(f"\n[{n}] {title}")


def refresh(state, real, enabled=True):
    """Before diffing, `plan` refreshes state from the real world so it can SEE drift.
    Returns an effective-state view. A resource in state but gone from real is a 'ghost'
    (None) that will be recreated. --sabotage no-refresh skips this and plans blind."""
    if not enabled:
        return dict(state)  # blind to reality — the sabotage
    effective = {}
    for addr in state:
        effective[addr] = dict(real[addr]) if addr in real else None  # None = ghost
    return effective


def plan(config, state, real, refresh_enabled=True, honor_immutable=True):
    """Return a list of (addr, action, changed_attrs). action in:
    create | no-op | update | replace | destroy."""
    eff = refresh(state, real, refresh_enabled)
    actions = []
    for addr, want in config.items():
        have = eff.get(addr)
        if have is None:  # not tracked (or ghost) -> create
            actions.append((addr, "create", None))
        elif have == want:
            actions.append((addr, "no-op", None))
        else:
            changed = sorted(k for k in set(have) | set(want) if have.get(k) != want.get(k))
            forces = honor_immutable and any(k in IMMUTABLE for k in changed)
            actions.append((addr, "replace" if forces else "update", changed))
    for addr in eff:
        if eff[addr] is not None and addr not in config:
            actions.append((addr, "destroy", None))
    return actions


def apply(actions, config, state, real):
    """Make real match config and bring state in sync — the only step that mutates the world."""
    for addr, act, _ in actions:
        if act in ("create", "update", "replace", "no-op"):
            real[addr] = dict(config[addr])
            state[addr] = dict(config[addr])
        elif act == "destroy":
            real.pop(addr, None)
            state.pop(addr, None)


def acts_of(actions):
    return {a for _, a, _ in actions}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage", choices=["no-refresh", "mutable-all"],
                    help="break the model: 'no-refresh' = plan stops refreshing from real "
                         "(drift undetected); 'mutable-all' = nothing forces replacement")
    args = ap.parse_args()
    refresh_on = args.sabotage != "no-refresh"
    immutable_on = args.sabotage != "mutable-all"
    if args.sabotage:
        log(f"  !! SABOTAGE ENABLED: {args.sabotage} !!")

    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"    OK  {ok_msg}")
        else:
            log(f"    XX  {fail_msg}")
            failures.append(fail_msg)

    WEB = "aws_instance.web"

    # 1. Empty state -> plan wants to CREATE.
    step(1, "Fresh config, empty state -> plan")
    config = {WEB: {"instance_type": "t3.small", "tags": "web", "availability_zone": "us-east-1a"}}
    state, real = {}, {}
    actions = plan(config, state, real, refresh_on, immutable_on)
    log(f"    plan: {actions}")
    check(acts_of(actions) == {"create"},
          "state is empty, so Terraform plans to CREATE the resource",
          "empty state should yield a CREATE")

    # 2. Apply -> state and real both converge to config.
    step(2, "apply -> the three worlds converge")
    apply(actions, config, state, real)
    log(f"    state={state}\n    real ={real}")
    check(state[WEB] == config[WEB] == real[WEB] and acts_of(plan(config, state, real, refresh_on, immutable_on)) == {"no-op"},
          "after apply, config == state == real, and re-plan is a clean no-op",
          "after apply the three worlds should match and re-plan should be no-op")

    # 3. Drift: someone hand-edits real out of band -> plan detects it and REVERTS.
    step(3, "Out-of-band change to real (the console hotfix) -> plan")
    real[WEB]["tags"] = "hand-edited-in-console"   # a human SSHes in / clicks the console
    actions = plan(config, state, real, refresh_on, immutable_on)
    log(f"    plan: {actions}")
    reverts = any(a == "update" and c and "tags" in c for _, a, c in actions)
    check(reverts,
          "plan refreshed from real, saw the drift, and will REVERT it back to config (Terraform fights you)",
          "plan should detect the hand-edit as drift and revert it")
    apply(actions, config, state, real)
    check(real[WEB]["tags"] == "web",
          "apply reverted the manual change — never hand-edit Terraform-managed infra",
          "apply should have reverted the drifted value back to config")

    # 4. Immutable attribute change -> REPLACE (destroy+recreate), not in-place.
    #    (availability_zone is genuinely ForceNew for aws_instance; instance_type is NOT.)
    step(4, "Change a ForceNew attribute (availability_zone) -> plan")
    config[WEB]["availability_zone"] = "us-east-1b"   # immutable (ForceNew) -> forces replacement
    actions = plan(config, state, real, refresh_on, immutable_on)
    log(f"    plan: {actions}")
    check(acts_of(actions) == {"replace"},
          "changing an immutable attr forces REPLACE (destroy+recreate) — READ THE PLAN before prod applies",
          "an immutable-attribute change should force REPLACE, not in-place update")
    apply(actions, config, state, real)

    # 5. Lost state -> Terraform wants to re-CREATE a resource that already exists; import reconciles.
    step(5, "State file lost -> plan (then `import`)")
    lost_state = {}                                # terraform.tfstate deleted/corrupted
    actions = plan(config, lost_state, real, refresh_on, immutable_on)
    log(f"    plan (state lost): {actions}")
    check(acts_of(actions) == {"create"},
          "with no state, Terraform wants to CREATE a resource that ALREADY EXISTS in real — a duplicate/clobber",
          "lost state should make Terraform want to (destructively) re-create the existing resource")
    lost_state[WEB] = dict(real[WEB])              # `terraform import` = teach state what real already is
    check(acts_of(plan(config, lost_state, real, refresh_on, immutable_on)) == {"no-op"},
          "`terraform import` reconciled state with real -> plan is a clean no-op again",
          "after import, plan should be a no-op")

    # 6. count vs for_each: reorder the list -> count churns, for_each is stable.
    step(6, "Remove the middle item: count (indexed) vs for_each (keyed)")
    #   count: addresses are numeric indices. Removing 'b' shifts 'c' from [2] to [1].
    cnt_state = {"r[0]": {"n": "a"}, "r[1]": {"n": "b"}, "r[2]": {"n": "c"}}
    cnt_real = {k: dict(v) for k, v in cnt_state.items()}
    cnt_config = {"r[0]": {"n": "a"}, "r[1]": {"n": "c"}}          # dropped 'b'; 'c' slid to index 1
    cnt_actions = plan(cnt_config, cnt_state, cnt_real, refresh_on, immutable_on)
    log(f"    count    plan: {cnt_actions}")
    #   for_each: addresses are keyed by name. Removing 'b' touches ONLY 'b'.
    fe_state = {'r["a"]': {"n": "a"}, 'r["b"]': {"n": "b"}, 'r["c"]': {"n": "c"}}
    fe_real = {k: dict(v) for k, v in fe_state.items()}
    fe_config = {'r["a"]': {"n": "a"}, 'r["c"]': {"n": "c"}}       # dropped 'b'
    fe_actions = plan(fe_config, fe_state, fe_real, refresh_on, immutable_on)
    log(f"    for_each plan: {fe_actions}")
    count_churns = sum(1 for _, a, _ in cnt_actions if a in ("update", "replace", "destroy"))
    foreach_touch = sorted(addr for addr, a, _ in fe_actions if a != "no-op")
    check(count_churns >= 2 and foreach_touch == ['r["b"]'],
          "count reordering churned the shifted resource(s); for_each destroyed ONLY the removed key",
          "count should churn shifted resources while for_each touches only the removed key")

    # verdict
    log("\n" + "=" * 70)
    if failures:
        log(f"XX FAIL — {len(failures)} lesson(s) broke:")
        for f in failures:
            log(f"    - {f}")
        if args.sabotage:
            log("\n(expected: --sabotage breaks the model, so the guarantees fall.)")
        log("=" * 70)
        return 1
    log("OK PASS — all six Terraform lessons held:")
    log("    Terraform plans against STATE, not the real world;")
    log("    a hand-edit becomes drift and gets reverted; immutable attrs REPLACE;")
    log("    lost state wants to re-create what exists (import reconciles);")
    log("    count shifts indices, for_each stays stable.")
    log("    State is the source of truth — respect it, lock it, never edit around it.")
    log("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
