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
| 🥇 [10 · remote access](10-remote-access.md) | The failure paths: expired certificate, unreachable directory, captive portal, a more-specific route arriving from the tunnel | **Strongest candidate in the series.** It is the highest-volume ticket a help desk will ever see, the symptoms are identical across four unrelated causes, and every one of them can be reproduced locally with no vendor. |
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

Four of the six real gaps — remote access, mail authentication, permission sprawl,
reconciliation — are **the same shape**: two or more sources of truth that can
disagree, and a human decision about which one is right. That is also, in every
step's AI column, the exact place AI was said to be useful and the exact place it
was said not to be trusted.

If any single lab gets built, build [10](10-remote-access.md).
