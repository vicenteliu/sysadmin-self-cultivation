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

✅ **Step 07 — 2026-08-22.**
[`cross-cutting/labs/permission-sprawl/`](../cross-cutting/labs/permission-sprawl/)
— two estates, same documents and people; the ACL difference is four names and the
real difference is 93 people, because a sharing link is a second grant path that no
access review walks. Its `--break-it` is the sharpest in the series: it makes the
audit ignore links, **which is how access reviews are actually performed**.

✅ **Step 06 — 2026-08-22.**
[`cross-cutting/labs/mail-authentication-alignment/`](../cross-cutting/labs/mail-authentication-alignment/)
— the sender inventory against the aggregate report, disagreeing in both
directions; a ticketing system that passes SPF, passes DKIM and fails DMARC; and a
spoofer who passes SPF on their own domain. Its `--break-it` reads the auth results
without comparing them to the `From:` line, which is what every mail health checker
reports — and under it `p=reject` still delivers the forged mail. The strictest
policy available, read the standard way, stops nothing.

**Three of the four same-shape gaps are now built.** Remaining: reconciliation (11).
It should copy the pattern these three established — model the two sources, let
them disagree, and make the *incomplete standard procedure* the sabotage mode.
