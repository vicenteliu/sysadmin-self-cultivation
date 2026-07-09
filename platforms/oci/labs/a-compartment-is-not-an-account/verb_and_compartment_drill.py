#!/usr/bin/env python3
"""
OCI IAM drill — a compartment is not an account, and a verb is not a role.

Pure-local, stdlib-only. Models the two things a cross-lane admin (AWS/Azure/GCP)
gets wrong about OCI authorization:

  1. Policies are VERB SENTENCES with a cumulative hierarchy:
         inspect  (list)
           read   = inspect + get
           use    = read + act-on-existing (start/stop), but NOT create/delete
           manage = use + create/delete   (everything)
     "Allow group G to <verb> <resource-type> in compartment C".

  2. The COMPARTMENT is the scope/boundary — a tree inside ONE tenancy. A policy
     attached to a compartment INHERITS DOWN to its children, and does NOTHING in
     a sibling. No policy at all => the OCI signature error
     NotAuthorizedOrNotFound (an HTTP 404): the resource is invisible, not "denied".

Run clean and every lesson holds -> exit 0 (doubles as a CI check).
Run with --sabotage to flatten either the verb hierarchy or the compartment
scope and watch the assertions fail -> exit 1. That's the point: the model is
only meaningful because breaking it breaks the guarantees.
"""

import argparse
import sys
from dataclasses import dataclass, field

# --- the verb hierarchy: inspect ⊂ read ⊂ use ⊂ manage, built cumulatively ---
INSPECT = {"list"}
READ = INSPECT | {"get"}
USE = READ | {"start", "stop"}
MANAGE = USE | {"create", "delete"}
VERB_OPS = {"inspect": INSPECT, "read": READ, "use": USE, "manage": MANAGE}

# --- resource-type families (a policy on a family covers its members) ---
FAMILIES = {"instance-family": {"instance", "volume-attachment", "image"}}

# --- the compartment tree, one tenancy (paths are ':'-joined like OCI) ---
ROOT = "tenancy"
DEV = "tenancy:Dev"
DEV_APP = "tenancy:Dev:App"   # child of Dev
PROD = "tenancy:Prod"          # sibling of Dev


def log(msg=""):
    print(msg)


def step(n, title):
    log(f"\n[{n}] {title}")


def compartment_covers(policy_scope, resource_compartment, sabotage=False):
    """A policy attached at `policy_scope` covers that compartment and everything
    BELOW it in the tree. The root covers all. Sibling compartments are isolated."""
    if sabotage:
        return True  # sabotage: pretend every policy is tenancy-wide
    if policy_scope == ROOT:
        return True
    return (resource_compartment == policy_scope
            or resource_compartment.startswith(policy_scope + ":"))


def verb_grants(verb, operation, sabotage=False):
    """Does `verb` grant `operation`? Honors inspect ⊂ read ⊂ use ⊂ manage."""
    if sabotage:
        return True  # sabotage: every verb grants every operation
    return operation in VERB_OPS[verb]


def rtype_matches(policy_rtype, resource_rtype):
    if policy_rtype in ("all-resources", resource_rtype):
        return True
    return resource_rtype in FAMILIES.get(policy_rtype, set())


@dataclass
class Policy:
    group: str          # "Allow group <group> ..."
    verb: str           # inspect | read | use | manage
    rtype: str          # e.g. instance-family
    scope: str          # compartment the policy is attached to


@dataclass
class User:
    name: str
    group: str


@dataclass
class Tenancy:
    policies: list = field(default_factory=list)
    sabotage_scope: bool = False
    sabotage_verbs: bool = False

    def authorize(self, user, operation, resource_rtype, resource_compartment):
        """Return (allowed, error). OCI returns the SAME 404 for 'missing' and
        'unauthorized' — so a deny surfaces as NotAuthorizedOrNotFound, and the
        resource is invisible, not visibly-forbidden."""
        for p in self.policies:
            if p.group != user.group:
                continue
            if not rtype_matches(p.rtype, resource_rtype):
                continue
            if not compartment_covers(p.scope, resource_compartment, self.sabotage_scope):
                continue
            if verb_grants(p.verb, operation, self.sabotage_verbs):
                return True, None
        return False, "NotAuthorizedOrNotFound (HTTP 404)"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage", choices=["scope", "verbs"],
                    help="break the model: 'scope' = policies go tenancy-wide; "
                         "'verbs' = every verb grants everything")
    args = ap.parse_args()

    t = Tenancy(
        policies=[
            Policy("DevReaders", "read", "instance-family", DEV),
            Policy("DevOperators", "use", "instance-family", DEV),
            Policy("DevAdmins", "manage", "instance-family", DEV),
            # note: NO policy for group "Contractors"
        ],
        sabotage_scope=(args.sabotage == "scope"),
        sabotage_verbs=(args.sabotage == "verbs"),
    )

    alice = User("alice", "DevReaders")
    dave = User("dave", "DevOperators")
    bob = User("bob", "DevAdmins")
    carol = User("carol", "Contractors")   # in a group with no policy

    # the instance under test lives in Dev:App — a CHILD of Dev
    INST = "instance"
    log("Tenancy 'tenancy'  compartments: Dev > App, and sibling Prod")
    log("Policies:  DevReaders=read  DevOperators=use  DevAdmins=manage  (all on 'Dev')")
    log("Target:    an 'instance' in compartment Dev:App (a child of Dev)")
    if args.sabotage:
        log(f"\n  !! SABOTAGE ENABLED: {args.sabotage} !!")

    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"    ✓ {ok_msg}")
        else:
            log(f"    ✗ {fail_msg}")
            failures.append(fail_msg)

    # 1. No policy -> NotAuthorizedOrNotFound: invisible, not "denied".
    step(1, "carol (no policy) lists the instance")
    allowed, err = t.authorize(carol, "list", INST, DEV_APP)
    log(f"    -> allowed={allowed}, error={err}")
    check(not allowed and err and err.startswith("NotAuthorizedOrNotFound"),
          "no policy => NotAuthorizedOrNotFound (404): the resource is INVISIBLE, not 403-denied",
          "carol with no policy should get NotAuthorizedOrNotFound (404), not access")

    # 2. Compartment inheritance: a Dev-scoped policy reaches the child App compartment.
    step(2, "alice (read on Dev) gets the instance in the CHILD compartment Dev:App")
    allowed, _ = t.authorize(alice, "get", INST, DEV_APP)
    log(f"    -> allowed={allowed}")
    check(allowed,
          "a policy on a parent compartment INHERITS DOWN the tree to Dev:App",
          "alice's Dev-scoped read policy should reach the child compartment Dev:App")

    # 3. Verb floor: read grants get/list but NOT delete.
    step(3, "alice (read) tries to DELETE the instance")
    allowed, err = t.authorize(alice, "delete", INST, DEV_APP)
    log(f"    -> allowed={allowed}, error={err}")
    check(not allowed,
          "read grants get/list only — delete needs manage (inspect ⊂ read ⊂ use ⊂ manage)",
          "read should NOT grant delete")

    # 4. Middle verb: use can act on an existing instance but cannot create one.
    step(4, "dave (use) starts the instance, then tries to CREATE one")
    started, _ = t.authorize(dave, "start", INST, DEV_APP)
    created, _ = t.authorize(dave, "create", INST, DEV)
    log(f"    -> start allowed={started}, create allowed={created}")
    check(started and not created,
          "use = read + act-on-existing (start/stop), but NOT create/delete",
          "use should allow start but NOT create")

    # 5. Top verb: manage does everything and subsumes the lower verbs.
    step(5, "bob (manage) creates an instance, and can also get/list it")
    created, _ = t.authorize(bob, "create", INST, DEV)
    got, _ = t.authorize(bob, "get", INST, DEV_APP)
    listed, _ = t.authorize(bob, "list", INST, DEV_APP)
    log(f"    -> create={created}, get={got}, list={listed}")
    check(created and got and listed,
          "manage ⊃ use ⊃ read ⊃ inspect — the top verb includes every lower one",
          "manage should grant create AND the lower verbs (get/list)")

    # 6. Compartment isolation: a Dev policy does nothing in the sibling Prod.
    step(6, "bob (manage on Dev) tries to create an instance in the SIBLING compartment Prod")
    allowed, err = t.authorize(bob, "create", INST, PROD)
    log(f"    -> allowed={allowed}, error={err}")
    check(not allowed,
          "scope is the boundary: a policy on Dev does NOTHING in sibling Prod",
          "bob's Dev-scoped manage should NOT reach the sibling compartment Prod")

    # verdict
    log("\n" + "=" * 68)
    if failures:
        log(f"✗ FAIL — {len(failures)} lesson(s) broke:")
        for f in failures:
            log(f"    - {f}")
        if args.sabotage:
            log("\n(expected: --sabotage flattens the model, so the guarantees fall.)")
        log("=" * 68)
        return 1
    log("✓ PASS — all six OCI IAM lessons held:")
    log("    no policy => NotAuthorizedOrNotFound (invisible, 404 not 403);")
    log("    verbs nest inspect ⊂ read ⊂ use ⊂ manage;")
    log("    policies inherit DOWN the compartment tree and stop at siblings.")
    log("    A compartment is not an account, and a verb is not a role.")
    log("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
