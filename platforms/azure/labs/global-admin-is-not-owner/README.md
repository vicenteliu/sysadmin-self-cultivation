# Lab — Global Admin is not Owner (prove it in your own hands)

**Goal:** make Azure's signature access lesson from the [Azure support note](../../support.md)
tangible — **Azure has two separate identity planes: Microsoft Entra ID directory roles
govern the tenant, Azure RBAC governs resources, and they do NOT span each other. A
Global Administrator has no access to Azure resources; an Owner cannot manage users. The
one bridge is the elevation toggle → User Access Administrator at root `/` (assign, not
use), and the real fix for resource access is a scoped RBAC assignment.** You'll run a
faithful model of both planes and watch each cross-plane request get denied.

**You'll practice:** the reflex the note insists on — *before granting anything, decide
which plane you're in* — and reading `AuthorizationFailed` as "wrong plane / wrong
scope," not "make them Global Admin."

## Why this lab is pure-local

No tenant, no subscription, no credentials, no external packages — just Python 3.8+.
Entra directory roles and Azure RBAC roles are small dicts; the resource plane models the
**management-group → subscription → resource-group → resource** scope hierarchy with real
ARM-style paths, so inheritance (`Owner` on a subscription reaches a VM under it) and
isolation (nothing in another subscription) are exact.

(The role/action names are illustrative; the *behaviour* — two non-spanning planes,
additive scope inheritance, elevation = User Access Administrator at `/`, the fix is a
scoped RBAC assignment — is real.)

## Run it

```bash
python3 two_planes_drill.py
```

That's it — no install. Exit code `0` means every assertion held, so it doubles as a CI
check.

## What you'll see

Six narrated steps, each ending in a checked lesson:

```
=== 1. A Global Administrator tries to read a VM (an Azure resource) ===
  global-admin (Entra Global Administrator) → read vm1 → AuthorizationFailed
  ✓ Global Administrator has NO Azure RBAC → denied on the resource (LESSON 1)
=== 4. The one bridge: the elevation toggle → User Access Administrator at '/' ===
  global-admin can now assign access on the VM = True, can write it = False
  ✓ elevation grants User Access Administrator at '/' — ASSIGN roles, not USE resources
=== 6. Scope is everything: an Owner on S1 does nothing in S2 ===
  res-owner (Owner on /subscriptions/S1):  write S1 VM → OK,  write S2 VM → AuthorizationFailed
```

## Verify (don't take the script's word for it)

Drive the model yourself in a Python shell:

```python
from two_planes_drill import Principal, elevate, VM
ga = Principal("ga", entra_roles=["Global Administrator"])
print(ga.can_resource("read", VM))   # False — Global Admin has no RBAC
elevate(ga)                          # flip the "Access management for Azure resources" toggle
print(ga.can_resource("manage-access", VM))  # True — can now ASSIGN roles
print(ga.can_resource("write", VM))          # False — still can't USE the resource
```

Then break it deliberately — make the two planes span (an Entra role grants resource
access) — and re-run: the drill must exit **non-zero**. A self-verifier that can't fail
is worthless.

## The point

- **Two doors, one key never opens the other.** *Entra = who you are* (the directory);
  *Azure RBAC = what you can touch* (resources). Global Admin is the top of one plane and
  the bottom of the other.
- **The elevation toggle is break-glass, not a daily driver.** It grants **User Access
  Administrator at `/`** — the power to *assign* roles across the tenant, so you can
  bootstrap or recover access. It does not let you *use* resources, and you turn it back
  off after.
- **Fix resource access with a scoped RBAC assignment.** Not by handing out Global
  Administrator. A `Reader` on the resource group grants read (via inheritance) and *only*
  read — that's the point of scoped RBAC over a broad directory role.
- **Scope is the blast radius.** An assignment inherits down its scope and stops; an
  `Owner` on subscription S1 is nothing in S2. This is the mental model behind every
  `AuthorizationFailed`.

## Teardown

Nothing persistent is created — the drill writes no files. Nothing to clean up.
