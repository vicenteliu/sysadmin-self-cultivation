# Gaps the build-out found

> Derived, not planned. A step earns a line here when it **should** be able to point
> at a runnable lab or a `toolbox/` tool and the repo has none.
>
> ⚠ **Not a backlog of everything missing.** Material a 100-person office never
> touches is not a gap. This list stays useful exactly as long as it stays narrow.

Sixteen steps, **16 of 16 accounted for** (100%). Fifteen point at a runnable lab
or a `toolbox/` tool; [`00 · before the lease`](00-before-the-lease.md) points at
nothing and should — it is a conversation with a landlord, and the honesty marker
carries the weight instead.

The residue is empty. What follows is the record of what the scenario found, which
was always more interesting than the coverage number, because a scenario finds holes
a roadmap does not think to look for.

## Real gaps — a lab or tool should exist and does not

**None open.** All six the scenario found are built; see [Closed](#closed) below.

A step earns a line back into this table the moment it should be able to point at
something runnable and cannot. The table being empty is a state, not a finish.

## Boundaries — not holes, and they should not be filled

| Step | Why nothing runnable belongs here |
|---|---|
| [00 · before the lease](00-before-the-lease.md) | It is a conversation with a landlord. The honesty marker carries the weight instead, and inventing an exercise would misrepresent the step. |
| [02 · the building](02-the-building.md) | Commissioning a room from a shell is physical work with contractors. The rack-side habits are covered in [`platforms/self-host/`](../platforms/self-host/); the building-side is 🧗 and stays so. |
| [12 · rooms](12-meeting-rooms-av-and-uc.md) — AV half | Same reason. The data-governance half was the real gap and is now built at [`labs/transcript-retention/`](../cross-cutting/labs/transcript-retention/); the AV half stays here. |

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

✅ **Step 11 — 2026-08-22.**
[`cross-cutting/labs/asset-reconciliation/`](../cross-cutting/labs/asset-reconciliation/)
— procurement and the endpoint tool both report 97 devices, 97 exist, and three
records are wrong. The join key decides how much of the fleet is fiction: hostname
reports 104, serial 99, asset tag 98. Its `--break-it` reconciles on hostname, and
the assertion worth sitting with is the third — 12 of the 15 rows reaching the
advisory layer are phantoms the key invented, and it produces confident causes for
every one.

**All four same-shape gaps are now built** — remote access (10), permission sprawl
(07), mail authentication (06), reconciliation (11).

✅ **Step 12 (data half) — 2026-08-22.**
[`cross-cutting/labs/transcript-retention/`](../cross-cutting/labs/transcript-retention/)
— the last one, and the only one containing no mistake. A meeting transcript shared
to a group and to nothing else, exactly as lab 07 recommends: six people were in the
room, 21 have been able to read it, zero grants were ever made, and four access
reviews across three years all pass truthfully. The recording that could have checked
the summary's one misattributed line expired on day 30; the summary did not. The
person the meeting was about joins the project on day 700 and can read it.

Its `--break-it` governs by point-in-time access review — the control everyone
actually runs — and the four broken assertions all say the same thing in different
words: **it does not answer those questions wrongly, it has no question whose answer
is any of them.** The control that was missing was never an access control. It was
an expiry.

This is the one that most needed not to be written, and the check that decided it
was worth writing was whether it could say anything lab 07 could not. It has one
axis 07 does not have, and the axis is time.

✅ **Step 13 — 2026-08-22.**
[`cross-cutting/labs/help-desk-queue/`](../cross-cutting/labs/help-desk-queue/)
— the first closed gap that is *not* the same shape. Nothing here disagrees with
anything; the failure is a ratio being unfalsifiable. Seven categories, two worlds,
Erlang-C: automation removes 39% of tickets and 31% of the work while *raising*
mean handling time, one more agent is 21× better rather than twice, and steps 04,
08 and 15 are priced at 50 people of headroom on one desk.

Its `--break-it` is the quietest in the series and possibly the most useful: staffed
by the one-per-fifty ratio it returns **the same answer the model does**. It breaks
three assertions anyway — it cannot name its binding constraint, cannot say at what
population its answer expires, and returns the same headcount whether or not the
automation exists. **The ratio is not wrong at a hundred people; it is
unfalsifiable at a hundred people**, and it will go on producing a number long
after the number stops being true.

The lab deliberately computes a *floor* rather than a recommendation, and leaves
the ratio out of the comparison at scale — a ticket-load model set against a
headcount rule would read as "you are over-staffed", which it has no standing to
claim.

Read together they say something none of them says alone. Each began as *two or
more sources of truth that can disagree*, and in each the sabotage that breaks the
drill turned out to be **the standard procedure**: an access review that walks
groups, a checker that reads authentication results, a reconciliation joined on
hostname. None of those is a mistake anyone would flag in a review. They are what
"we already do that" means, and they are wrong in the same way — each answers a
smaller question than the one being asked, and answers it correctly, which is why
nothing looks broken.

The four also converge on the same boundary: what survives a competent check is a
residue whose cause is **not in any of the systems**. That is the advisory line the
build-out's AI columns keep landing on — a model can rank the candidates, and the
decision needs a person who knows something the records do not contain.
