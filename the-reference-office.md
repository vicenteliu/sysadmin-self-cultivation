---
kind: note
axis: start-here
themes: []
platforms: []
summary: "Every step in the build-out says a hundred people."
---
# The reference office

Every step in the build-out says *a hundred people*. This file is where that stops being
a word and becomes numbers you can plan against.

It exists because the build-out teaches decisions, and a decision needs a situation. How
many uplinks, how many switch ports, how many rooms with a screen in them — none of those
questions have an answer until somebody says how big the place is. This file says how big.

> **What this is not.** It is not a bill of materials, and it is not a design you should
> copy. It is one plausible hundred-person office, written down so the rest of the repo
> has something concrete to point at. Your building will differ. The *derivations* are
> the transferable part, and they live in their own section for exactly that reason.

## How to read this file

The sections below age at very different speeds, so they are kept apart on purpose.

| Section | Expected shelf life |
|---|---|
| Parameters | Years. A hundred people need roughly this much room in most decades. |
| Why these numbers | Longest. These are the derivations, and they outlive any product. |
| Selection rules | Years. Criteria, deliberately without model names. |
| Reference build | Short. Dated, and meant to be replaced whole. |
| Cost shape | Medium, and relative only. No currency figures. |

**If you only read one section, read *Why these numbers*.** The rest is an instance. That
one is the method.

## Parameters

**Scenario choices** — set here, not derived from anything. Change these and the rest of
the file follows.

| | Value |
|---|---|
| Headcount | 100 |
| Working pattern | Hybrid, three days a week expected in office |
| Floors | One |
| Growth assumed over the lease | To about 130 without moving |

**Derived** — every one of these comes from a rule in the next section.

| | Value | Derived from |
|---|---|---|
| Peak-day attendance | ~65 | Midweek occupancy runs mid sixties percent |
| Desks | ~70 | 0.7 desks per employee, hybrid norm, plus a small cushion |
| Meeting rooms | 7 | One per 10 to 20, open-plan end of the range |
| Room mix | 1 large, 2 medium, 4 small | 80 percent of meetings are six people or fewer |
| Phone booths | 6 | One per 10 to 15 in-office, counted separately from rooms |
| Tea point | 1, seating ~16 | One per floor; seats sized on peak-day attendance, not headcount |
| Store | 1 | Stock, spares and deliveries have to land somewhere with a door |
| Service desk | 1 walk-up position | A staffed point people can walk to, sited on the circulation route |

## Why these numbers

**Size for the peak day, not for the payroll.** A hundred people on payroll is not a
hundred people in the building. Occupancy data across thousands of buildings puts midweek
attendance in the mid sixties percent, Monday in the low fifties, Friday in the high
thirties. The practical effect is that a hundred-person office behaves like a
sixty-five-person office on Tuesday and a thirty-person office on Friday. **Size for
Tuesday.** Sizing for a hundred buys space that is empty every day of the year; sizing for
Friday means Tuesday does not fit.

**Desks are not one per person any more.** Hybrid offices commonly provision 0.6 to 0.8
desks per employee. At 0.7 that is seventy desks for a hundred people, which comfortably
seats a sixty-five-person peak and leaves room for the days it runs over.

**Meeting rooms scale with layout, not just headcount.** The rule of thumb is one room per
ten to twenty employees, and where you land inside that range is decided by how open the
floor is. An all-open floor pushes toward one per ten, because people with no door need
somewhere to go. A floor full of private offices pushes toward one per twenty. This office
is open, so it sits near the dense end and gets seven.

**The mix is where most offices get it wrong, and it is measurable.** Sensor data across
173 buildings, 13 countries and more than 27,000 workspaces found that 80 percent of
meetings happen in rooms built for six or fewer, while boardrooms built for seventeen or
more sat at 12 percent utilisation. Build for the meetings you actually have. Roughly half
the rooms should seat two to four, a quarter should seat five to eight, and only one in
seven or eight needs to be large.

**Phone booths are not small meeting rooms.** They serve a different need, they get
provisioned at about one per ten to fifteen in-office people, and counting them as meeting
rooms is how a floor ends up with nowhere to take a call.

**Three support spaces are load-bearing and get left off plans anyway.** None of them is
derived from a ratio; each exists because a step of the build-out asks a question that has
no answer without it.

- **A tea point, with tables people can eat at.** One per floor, sited away from the desks
  it would otherwise disrupt, and — the half that gets left off — **seated**. A counter and
  a kettle with nowhere to sit is a corridor, and it sends everyone out of the building at
  midday. Seats scale on peak-day attendance rather than headcount, at roughly a quarter of
  the peak eating on the floor at once: about sixteen here. The failure mode is not
  discomfort; it is that people leave the floor for lunch and the floor's occupancy numbers
  stop describing where anybody is.
- **A store, with a door that locks.** [Step 11](build-out/11-assets-and-tickets.md) asks
  the estate to be enumerated from device one; [step 04](build-out/04-devices-and-images.md)
  has laptops arriving in boxes. Stock, spares, returns and deliveries need somewhere that
  is not a desk, and an asset register whose physical counterpart is "the corner behind
  Dave" is a register that will disagree with reality inside a quarter.
- **A service-desk position.** [Step 13](build-out/13-the-help-desk.md) asks how many IT
  people a hundred people need and cannot answer it until the estate is known. It is also
  a *placement* question and that half is answerable now: a walk-up point on the
  circulation route, visible from the floor, near the store it draws stock from and near
  the IDF it is the first responder for. Put it in a back office and the walk-ups become
  tickets, which is a change in workload disguised as a change in furniture.

**Where these three sit is a network decision as much as a facilities one.** The store and
the service desk sit beside the IDF because that is the path a broken laptop takes; the
tea point sits away from all three because it is the one space whose job is noise.

**Those adjacencies are drawn, and the drawing stops where this repo's depth does.**
[`walkthrough/reference-office.plate.json`](walkthrough/README.md) carries the *topology*
of this floor — which space is next to which, and how you walk between them — and a
headless proof checks that every space is reachable from the lift lobby along circulation
without crossing a desk. It carries **no corridor widths, no egress distances, no sanitary
provision and no claim that the plan would pass anything**, because that is architecture
and [`build-out/GAPS.md`](build-out/GAPS.md) already judged the building side a 🧭 that
stays one. The reasoning is [ADR-0014](docs/adr/0014-the-plate-stops-at-topology.md).

**Room area follows the seat count.** A workable estimate is fifty square feet for the
room plus twenty-five per seated person, which is what turns *seven rooms* into a number a
landlord can quote against.

## Selection rules

Criteria only, never model names. **Written because three build-out steps needed a
number and could only give a criterion**: [01](build-out/01-uplink.md) wants *"a sizing
number with the reasoning attached"*, [02](build-out/02-the-building.md) says the load
moved to wireless density, and [05](build-out/05-network.md) asks how many people are in
the largest room on video without answering it. The scenario would want this if nothing
were ever filmed, which is the test.

The design decisions these quantities feed live in
[`cross-cutting/site-network-design.md`](cross-cutting/site-network-design.md). This is
the arithmetic; that is what you do with it.

### Wireless — count it twice and take the larger

The method, which outlives any radio generation:

1. **By client count.** Associated devices ÷ clients-per-AP. Plan around **25 active
   clients per radio, ~50 per AP** in a dense space — an airtime-fairness limit, not a
   spec-sheet one, which is why it has barely moved across generations.
2. **By throughput.** Active devices × per-client target ÷ usable per-AP throughput.
   Per-client targets: **video conferencing ~1.5 Mbps, HD video ~3 Mbps**, VoIP a
   rounding error. Size on the highest-bitrate application, not the average one.
3. **Take the larger, then check it against the coverage floor** — roughly **one AP per
   2,500–3,000 sq ft** of partitioned office. Below about a hundred and fifty people the
   coverage floor usually wins, which surprises people who have been told density is
   what matters.
4. **Then place them for the peak square metre**, not the mean. Uniform spacing serves a
   floor with meeting rooms worse than deliberate placement does.

**Worked, for this office.** ~65 on the peak day at roughly two devices each, plus seven
room systems, six booths and a handful of printers and controllers ≈ **145 associated
devices**.

| Calculation | Result |
|---|---|
| By client count | 145 ÷ 50 ≈ **3 APs** |
| By throughput | ~40% active at peak → 58 × 3 Mbps ≈ 174 Mbps → **1 AP** |
| Larger of the two | **3** |
| Coverage floor (~11,000 sq ft) | 11,000 ÷ 2,750 ≈ **4 APs** |
| Placement — the large room earns a dedicated radio | **5–6 APs** |

The number that binds is coverage and placement, not capacity. **That is the useful
finding**, and it refines rather than contradicts step 05: at a hundred people density
decides *where* the access points go, and coverage decides *how many*. Density starts
setting the count somewhere above this office's size.

### Wired — ports, then the two things that get under-specified

Count the ports, then check the two budgets that are not port counts:

| Draw | For this office |
|---|---|
| Desks | 70 |
| Rooms — display + room system | 14 |
| Phone booths | 6 |
| Access points | 6 |
| Printers / MFDs | ~3 |
| Door controllers and access panels | ~3 |
| Signage, spares, unknowns | ~8 |
| **Active ports** | **~110** |
| **Plus growth to ~130 people** | **~135 → three 48-port switches** |

**Speed, per tier.** Three tiers, three answers — the reasoning for *why* they differ
is in [`site-network-design.md`](cross-cutting/site-network-design.md); this is what
this office needs.

| Tier | This office | Why not more |
|---|---|---|
| Desk ports | **1GbE** | A hybrid floor's load moved to wireless and to SaaS. Nothing at a desk here is starved; upgrading these first buys nothing. |
| AP-facing ports | **multi-gig** | Six access points whose radios can exceed a gigabit. A 1GbE drop makes the AP the bottleneck it was bought to remove. |
| Access-to-core uplink | **10GbE** | Three access switches aggregating ~110 ports. Sized against the sum of what lands on it, not against a round number. |

Note which tier is *not* upgraded. **The desk is the least starved link in the
building**, and specifying it up is the most common way to spend the budget in the
wrong ceiling.

- **PoE budget, not port count, often picks the switch.** Six access points plus room
  and booth devices plus access control lands near **500 W** of simultaneous draw here,
  and a 48-port switch's PoE budget varies by more than a factor of two between models
  at the same port count. Specify the watts, not the ports.
- **Uplink and stacking are the under-specified path.** Access-layer port count is easy
  to get right because it is easy to count. The path from access to core is not counted
  by anything and is where the design gets quietly capped.

### Requirements to specify, in criteria

- **Switching:** PoE budget in watts under simultaneous load · multi-gig access ports
  for AP-facing drops · uplink capacity sized past the access layer · L3 at the
  aggregation point if segments must route locally · 802.1X support, because
  [network authentication is an identity decision](cross-cutting/identity-iam.md).
- **Wireless:** current-generation radios · per-SSID VLAN mapping · client isolation on
  guest · controller or cloud management that one person can operate.
- **Both:** management interfaces reachable only from the management segment · firmware
  support life stated in years, since it decides when this becomes someone's project
  again.

*As of 2026, current-generation access points want PoE++ (802.3bt) and a 2.5GbE
access port; a design specifying PoE+ (802.3at) and 1GbE ports will meet the criteria
above and still constrain the radios it powers. That sentence is the part of this
section with a short shelf life — the criteria around it are not.*

**Where the wireless figures come from.** This section's radio arithmetic is 🧭 — drawn
from published vendor engineering guidance and checked for internal consistency, not
from having designed and then lived with an office wireless deployment. See
[`site-network-design.md`](cross-cutting/site-network-design.md#honest-boundaries) for
the boundary stated in full.

## Reference build

⏳ **Still not written, and the entry condition explains why.** It gets written when a
build-out step needs it — and **no step asks for a model**. Steps 01, 02 and 04 ask for
sizing numbers and for a hardware *policy* (how many laptop models to support); none of
them asks which switch. The criteria above answer every question the scenario actually
poses.

**Entry condition, and it is a hard one.** Every line here must survive the question
**could someone buy from this?** A switch model, a port count, an access point count all
pass. How a protocol behaves does not — that belongs somewhere else and this file stays
out of it.

When it is written it is a dated table and nothing else, replaceable whole without
touching a word of prose elsewhere in this file.


## Cost shape

⏳ **Not written yet.** Relative relationships only, never figures. Currency amounts date
faster than anything else here and vary by region more than they vary by decade.

## Where this office already lives

This file is parameters. Everything you would actually *do* with them is elsewhere, and
that is deliberate — it is written once, in one place.

- **The sixteen steps** in [`build-out/`](build-out/) — the route through the whole thing.
  Each step already carries a `Getting it backwards` section, which is where the failure
  modes live.
- **Runnable tooling** in [`toolbox/`](toolbox/) — the scripts, not descriptions of them.
- **Working with AI** in
  [`ai-workflow/`](ai-workflow/how-i-use-ai-to-learn-and-operate.md).

## How interviews ask about this

⏳ **Not written yet.** When it exists it holds **questions and what each one is testing**,
and no model answers.

That boundary is not a style preference. Public material teaches you how to think; a
finished answer does the work for you, and the two do not belong in the same file. A
question plus what it probes is the first kind. A polished response is the second.
