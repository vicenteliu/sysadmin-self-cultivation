# Gaps the build-out found

> Derived, not planned. A step earns a line here when it **should** be able to point
> at a runnable lab or a `toolbox/` tool and the repo has none.
>
> ⚠ **Not a backlog of everything missing.** Material a 100-person office never
> touches is not a gap. This list stays useful exactly as long as it stays narrow.

Sixteen steps, **15 of 16 point at something runnable** (94%). What follows is the
residue — and it is more interesting than the coverage number, because a scenario
finds holes that a roadmap does not think to look for.

## Real gaps — a lab or tool should exist and does not

| Step | What is missing | Why it counts |
|---|---|---|
| [06 · tenant and mail](06-tenant-and-mail.md) | Mail authentication: publish a record, read a DMARC aggregate report, watch a message fail alignment | Pure-local and self-verifying. The lesson — that `p=none` is monitoring and not protection — is exactly the kind that reads as obvious and is skipped anyway. |
| [07 · files](07-files-and-collaboration.md) | Permission sprawl: a synthetic set of spaces and links, and the job of finding the over-shared one | The lesson is structural, needs no vendor, and answers the question an auditor actually asks: *who can see this, and how do you know?* |
| [11 · assets](11-assets-and-tickets.md) | A reconciliation drill: two sources that disagree about the same fleet, and a diff to adjudicate | The step's whole claim is that the job is reconciling, not collecting — and nothing runnable makes that concrete. The ITSM note's own lab is still marked planned. |
| [13 · the help desk](13-the-help-desk.md) | A queue model: arrival rates, categories, and what automating one category does to the others | It is the only way to test the staffing argument instead of asserting it. |
| [12 · rooms](12-meeting-rooms-av-and-uc.md) | Governance of recordings and transcripts — where they land, who can read them | Partial: the AV half cannot be made runnable, but the *data* half is the same problem as step 07 and is currently unowned. |

## Boundaries — not holes, and they should not be filled

| Step | Why nothing runnable belongs here |
|---|---|
| [00 · before the lease](00-before-the-lease.md) | It is a conversation with a landlord. The honesty marker carries the weight instead, and inventing an exercise would misrepresent the step. |
| [02 · the building](02-the-building.md) | Commissioning a room from a shell is physical work with contractors. The rack-side habits are covered in [`platforms/self-host/`](../platforms/self-host/); the building-side is 🧗 and stays so. |
| [12 · rooms](12-meeting-rooms-av-and-uc.md) — AV half | Same reason. Only the data-governance half is listed above as a real gap. |

## What this list is telling you

Six real gaps, and **four of them are the same gap**: remote access, mail
authentication, permission sprawl, and reconciliation all reduce to *two or more
sources of truth that can disagree, and a human deciding which one is right*.

That is also, in every step's AI column, the exact place AI was said to be useful
and the exact place it was said not to be trusted. The shape is not a coincidence —
it is what is left over once the deterministic work has been automated away.

## Closed

✅ **Step 10 — 2026-08-22.** The one named here as the strongest candidate is built:
[`cross-cutting/labs/remote-access-four-causes/`](../cross-cutting/labs/remote-access-four-causes/)
— four causes, one byte-identical symptom, elimination resolving 4/4 where habit
resolves 2/4, and a `--break-it` flag that proves the self-check can actually fail.

It came out carrying the lesson all four of the same-shape gaps share — **a check
earns its place by what it eliminates, not by what it reports** — so the three that
remain have a worked example to copy rather than a spec to interpret.

**Next: [07 · permission sprawl](07-files-and-collaboration.md).** Same reason it was
listed — structural, no vendor needed, and it answers the question an auditor
actually asks.
