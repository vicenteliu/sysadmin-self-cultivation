#!/usr/bin/env python3
"""
two_planes_drill.py — prove, in your own hands, Azure's signature access lesson from
the Azure support note: there are TWO separate identity planes. Microsoft Entra ID
DIRECTORY ROLES (Global Administrator, User Administrator) govern the tenant — users,
apps, the directory. Azure RBAC (Owner, Contributor, Reader) governs Azure RESOURCES,
scoped on the management-group -> subscription -> resource-group -> resource hierarchy.
They do NOT span each other: a Global Administrator has, by default, no access to Azure
resources, and an Azure Owner cannot manage users. The single bridge is the "Access
management for Azure resources" elevation (Global Admin -> User Access Administrator at
root "/"), which lets you ASSIGN roles, not USE resources.

No cloud, no tenant, no credentials, no external dependencies. Pure Python stdlib.

We model both planes and run requests through them. A faithful (simplified) model — the
role/action names are illustrative; the behaviour (two non-spanning planes, additive
scope inheritance, elevation = User Access Administrator at "/", the fix is a scoped
RBAC assignment) is real.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass, field


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


# --- Plane 1: Microsoft Entra ID directory roles (govern the tenant) ---------------
ENTRA_ROLES = {
    "Global Administrator": {"user.manage", "app.manage", "elevate"},  # + can elevate
    "User Administrator": {"user.manage"},
}

# --- Plane 2: Azure RBAC roles (govern resources). Actions: read / write / manage-access
AZURE_ROLES = {
    "Owner": {"read", "write", "manage-access"},
    "Contributor": {"read", "write"},                    # manage, but not assign access
    "Reader": {"read"},
    "User Access Administrator": {"read", "manage-access"},  # assign roles, not use
}

# Scope hierarchy is expressed as ARM paths; "/" is the root above every subscription.
ROOT = "/"
SUB = "/subscriptions/S1"
RG = "/subscriptions/S1/resourceGroups/RG1"
VM = "/subscriptions/S1/resourceGroups/RG1/providers/Microsoft.Compute/virtualMachines/vm1"
OTHER_SUB_VM = "/subscriptions/S2/resourceGroups/RG9/providers/Microsoft.Compute/virtualMachines/vm9"


def scope_covers(assignment_scope, target_scope) -> bool:
    """An RBAC assignment applies to its scope AND everything beneath it (inheritance)."""
    if assignment_scope == ROOT:
        return True
    return target_scope == assignment_scope or target_scope.startswith(assignment_scope + "/")


@dataclass
class Principal:
    name: str
    entra_roles: list = field(default_factory=list)             # ["Global Administrator"]
    rbac: list = field(default_factory=list)                    # [("Reader", RG)] = (role, scope)

    def can_directory(self, action) -> bool:
        """Plane 1 — does an Entra directory role grant this tenant action?"""
        return any(action in ENTRA_ROLES[r] for r in self.entra_roles)

    def can_resource(self, action, scope) -> bool:
        """Plane 2 — does an Azure RBAC assignment grant this action at (or above) scope?"""
        return any(action in AZURE_ROLES[role] and scope_covers(assign_scope, scope)
                   for role, assign_scope in self.rbac)


def elevate(p: Principal):
    """The 'Access management for Azure resources' toggle: a Global Admin gains User
    Access Administrator at root '/'. It lets them ASSIGN roles — not use resources."""
    if p.can_directory("elevate"):
        p.rbac.append(("User Access Administrator", ROOT))
        return True
    return False


def run() -> int:
    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"  ✓ {ok_msg}")
        else:
            log(f"  ✗ {fail_msg}")
            failures.append(fail_msg)

    ga = Principal("global-admin", entra_roles=["Global Administrator"])   # tenant, no RBAC
    owner = Principal("res-owner", rbac=[("Owner", SUB)])                   # resources, no Entra
    analyst = Principal("analyst")                                         # nothing yet

    step(1, "A Global Administrator tries to read a VM (an Azure resource)")
    can = ga.can_resource("read", VM)
    log(f"  global-admin (Entra Global Administrator) → read {VM.split('/')[-1]} → "
        f"{'OK' if can else 'AuthorizationFailed'}")
    check(not can,
          "Global Administrator has NO Azure RBAC → denied on the resource (LESSON 1)",
          "a Global Admin could read the VM without any Azure RBAC — planes wrongly spanned")

    step(2, "An Azure Owner tries to create a user (a directory action)")
    can = owner.can_directory("user.manage")
    log(f"  res-owner (Azure Owner on {SUB}) → create user → "
        f"{'OK' if can else 'denied'}")
    check(not can,
          "an Azure Owner has NO Entra role → can't manage users — the reverse also holds (LESSON 2)",
          "an Azure Owner could manage users — the planes wrongly spanned")

    step(3, "Your instinct vs. reality — 'I'm Global Admin, I run Azure'")
    instinct = True                                    # the imported assumption
    reality = ga.can_resource("write", VM)             # not elevated
    log(f"  instinct: Global Admin ⇒ full Azure resource control = {instinct}")
    log(f"  reality:  global-admin can write the VM = {reality}")
    check(instinct != reality,
          "the 'Global Admin runs everything in Azure' instinct is WRONG (LESSON 3)",
          "instinct and reality agreed — the drill proved nothing")

    step(4, "The one bridge: the elevation toggle → User Access Administrator at '/'")
    elevated = elevate(ga)
    can_assign = ga.can_resource("manage-access", VM)   # can now assign roles
    can_write = ga.can_resource("write", VM)            # but still can't USE the resource
    log(f"  elevate 'Access management for Azure resources' → {elevated}")
    log(f"  global-admin can now assign access on the VM = {can_assign}, can write it = {can_write}")
    check(elevated and can_assign and not can_write,
          "elevation grants User Access Administrator at '/' — ASSIGN roles, not USE resources (LESSON 4)",
          "elevation behaved wrong (should grant assign-access at root, not resource use)")

    step(5, "The real fix: a SCOPED Azure RBAC assignment — not making them Global Admin")
    analyst.rbac.append(("Reader", RG))                 # what the elevated admin would grant
    can_read = analyst.can_resource("read", VM)         # inherited from RG down to the VM
    can_write = analyst.can_resource("write", VM)       # Reader is read-only
    log(f"  analyst gets Reader on {RG.split('/')[-1]}:  read VM → {'OK' if can_read else 'no'},"
        f"  write VM → {'OK' if can_write else 'AuthorizationFailed'}")
    check(can_read,
          "a scoped Reader assignment authorizes read via inheritance — the correct fix (LESSON 5)",
          "the scoped Reader assignment failed to authorize read")
    check(not can_write,
          "…and Reader does NOT grant write — RBAC is scoped, not all-or-nothing",
          "Reader wrongly granted write")

    step(6, "Scope is everything: an Owner on S1 does nothing in S2")
    here = owner.can_resource("write", VM)              # under S1 → inherited
    there = owner.can_resource("write", OTHER_SUB_VM)   # under S2 → not covered
    log(f"  res-owner (Owner on {SUB}):  write S1 VM → {'OK' if here else 'no'},"
        f"  write S2 VM → {'OK' if there else 'AuthorizationFailed'}")
    check(here and not there,
          "RBAC inherits down its scope and stops there — a grant on S1 is nothing in S2 (LESSON 6)",
          "scope inheritance/isolation did not hold")

    log("\n" + "=" * 70)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the lessons held:")
    log("  1. A Global Administrator (Entra) has no access to Azure resources.")
    log("  2. An Azure Owner (RBAC) cannot manage the directory — the planes don't span.")
    log("  3. 'Global Admin runs Azure' is false — two separate authorization systems.")
    log("  4. The elevation toggle = User Access Administrator at '/': assign, not use.")
    log("  5. You fix resource access with a scoped RBAC assignment, not a directory role.")
    log("  6. RBAC inherits down a scope and stops — scope is the blast radius.")
    log("")
    log("The instinct this drill retired:")
    log("  'I'm Global Admin, so I run Azure' — Entra says who you are; RBAC says what")
    log("  you can touch. They are two doors, and one key never opens the other.")
    return 0


def main():
    argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    sys.exit(run())


if __name__ == "__main__":
    main()
