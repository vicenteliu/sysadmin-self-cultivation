# Lab — a compartment is not an account (and a verb is not a role)

**Goal:** feel OCI's two signature access lessons the way you'll actually hit them in a
ticket — *by hand, with no cloud account* — so `NotAuthorizedOrNotFound` and the
`inspect/read/use/manage` verb hierarchy stop being trivia and become reflexes.

What it drills:
1. **No policy → `NotAuthorizedOrNotFound` (a 404, not a 403).** OCI returns the *same*
   error for "doesn't exist" and "you're not allowed to see it" — the resource is
   **invisible**, not visibly-forbidden. On this error, suspect a policy/compartment/region
   problem first, a missing resource second.
2. **Verbs are cumulative: `inspect ⊂ read ⊂ use ⊂ manage`.** `read` grants get/list but
   **not** delete; `use` can start/stop an existing instance but **can't create** one;
   `manage` does everything and subsumes the lower verbs.
3. **The compartment is the scope.** A policy attached to a **parent** compartment
   **inherits down** to its children; a policy scoped to one compartment does **nothing** in
   a **sibling**. Scope is the boundary — not a new account/subscription/project.

## Why local

No tenancy, no credentials, no OCID, no waiting on home-region propagation. The lab is a
~200-line model of OCI's policy evaluation — verb hierarchy, resource-type families,
compartment-tree inheritance, and the deliberate 404 ambiguity — so the *logic* is what you
inspect, not a screenful of Console. It runs anywhere Python does, and in CI.

## Run

```bash
python3 verb_and_compartment_drill.py
```

## What you'll see

Six narrated steps, each with a ✓/✗: carol (no policy) hits the 404; alice's Dev-scoped
`read` reaches the **child** compartment Dev:App (inheritance) but **can't delete** (verb
floor); dave's `use` starts an instance but **can't create**; bob's `manage` does everything;
and bob's Dev-scoped `manage` **can't touch the sibling** compartment Prod (isolation). Ends
with a PASS verdict and `exit 0`.

## Verify (the important part)

Exit `0` = every lesson held; it doubles as a CI check. Now **break the model on purpose** and
watch the guarantees fall — there are two independent sabotage vectors:

```bash
python3 verb_and_compartment_drill.py --sabotage verbs   # every verb grants everything -> steps 3 & 4 FAIL, exit 1
python3 verb_and_compartment_drill.py --sabotage scope   # policies go tenancy-wide     -> step 6 FAILS, exit 1
```

If flattening the verb hierarchy still "passed," the hierarchy wasn't doing anything; if
tenancy-wide scope still "passed," compartments weren't a boundary. The failures are the proof
the model is load-bearing.

## The point

Two AWS/Azure/GCP reflexes get corrected here at once. First, **"404 means it's gone"** — on
OCI it just as often means *you have no policy*. Second, **"I have access to this resource
type, so I can do anything to it"** — on OCI the **verb** caps what you can do and the
**compartment** caps where, and both are inherited down a tree inside a single tenancy. A
compartment is not an account; a verb is not a role. See the
[OCI support note](../../support.md) for the full ticket catalog.

## Teardown

None — it's a single self-contained script. Delete the folder to remove it.
