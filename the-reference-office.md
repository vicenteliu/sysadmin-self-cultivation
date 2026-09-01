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
| Where things run | Years, once written. What cannot leave the building changes slowly. |
| Reference build | Short. Dated, and meant to be replaced whole. |
| Cost shape | Medium, and relative only. No currency figures. |
| What this office does not yet say | Shortest. It is a ledger, and it empties. |

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
| Lease term | 5 years |

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
| Net growth | ~6 people a year | 100 to 130 across a 5-year term |
| Leavers | ~17 a year | 🧭 A mid-teens annual turnover rate on the average headcount of 115 |
| Joiners | ~23 a year | Leavers plus net growth — you hire the replacement *and* the addition |
| Joiners over the lease | ~116 | To grow by 30. And 216 people hold an account at some point, for 130 desks |

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

**A hundred people is a headcount, not a roster — and the roster is the thing IT
administers.** The file already sets growth *to about 130 without moving*; putting a term
under it turns a shape into a rate. Across five years that is about six net additions a
year, and net is the smaller half of the arithmetic. You do not hire six people. You hire
the six, **and** you hire a replacement for everyone who left.

**The turnover figure is the 🧭 part and it is the one to argue with.** A mid-teens annual
rate is the band professional-services and technology employers usually sit in, and this
file takes the middle of it rather than defending a decimal. On an average headcount of
about 115 across the term that is roughly seventeen leavers a year, so twenty-three
joiners: forty joiner-or-leaver events a year, **one about every six working days, for
five years running.** Move the turnover rate and every number in this paragraph moves with
it; the *structure* — joiners equals leavers plus growth — does not.

**The consequence is the number worth carrying away.** Over one lease this office
hires about a hundred and sixteen people **in order to grow by thirty**, and lets about
eighty-six go. Add the hundred who were already here and **roughly two hundred and sixteen
different people hold an account at some point — for a floor that never holds more than a
hundred and thirty of them at once.** The estate IT administers is not the office. It is
about one and seven tenths of the office, and the ratio grows with every year of the
lease.

Every one of those arrivals is an account, a device, a set of group memberships and a row
in an asset register; every departure is all of the same, in reverse, done by somebody who
no longer has a reason to care whether it finished.

That is why joiner-mover-leaver is
[a step of its own](build-out/15-joiner-mover-leaver.md) rather than a paragraph inside
identity, and it is why the estate-drift labs land the way they do. A hundred-person
office does not accumulate stale accounts and orphaned permissions because somebody was
careless. It accumulates them because **the population turns over faster than any review
cycle that runs annually**, which is most of them.

**The mover is the one this file will not give you a number for.** Internal moves — team
changes, promotions, secondments — are the least measured of the three and the most
consequential, because a mover keeps everything they had and gains what they need, and no
event fires that says *take the old thing away*. There is no published rate this file
trusts and no derivation available from anything above, so it states none. What it states
instead is that the mover is the leg with **no natural trigger**: a joiner has a start
date and a leaver has a last day, and the mover has a conversation.

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

## Where things run

⏳ **Not written yet, and it has two halves with two different entry conditions.**

**On premises.** [Step 02](build-out/02-the-building.md) shrank this room to *switches, an
access controller, a print device, a little lab gear*, because workloads left the
building; [step 04](build-out/04-devices-and-images.md) put the image with the OS vendor
rather than on-site. So the question this half answers is not *what should we run here* —
it is **what cannot leave**, and that list is currently unwritten because nothing has
needed it. *Entry condition: a build-out step or a lab needs something on this floor that
cannot be somebody else's service.*

**In a cloud.** Nothing in this repo has yet been forced to invent this office's cloud
numbers. Four labs anchor to *a hundred-person office* — [help desk
queue](cross-cutting/labs/help-desk-queue/), [asset
reconciliation](cross-cutting/labs/asset-reconciliation/), [permission
sprawl](cross-cutting/labs/permission-sprawl/) and [mail
authentication](cross-cutting/labs/mail-authentication-alignment/) — and not one of them
is about cloud. *Entry condition: a step or a lab is forced to invent a cloud number for
this office, and every line written here answers **why is this not in the IDF**.*

**The two halves are one section because they are defined against each other.** A cloud
entry earns its place by naming what the on-premises side could not do, and the reverse.
Split apart, each would drift into a general tour of its side — which is
[`platforms/`](platforms/)' job, at `mixed` footing, and not this file's.

**What neither half may hold** is set by
[ADR-0015](docs/adr/0015-the-reference-office-consumes-services-and-operates-none.md):
this office consumes services and operates none. No traffic, no release cadence, no error
budget, no customers.

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

## What this office does not yet say

**Derived, not planned**, in the manner of [`build-out/GAPS.md`](build-out/GAPS.md). A
parameter earns a line here when **something else in this repo was already forced to
invent it** because this file is silent. Not a wish list: a domain nobody has needed is
not a gap, it is a ⏳ section with an entry condition — see *Where things run* above.

The distinction is the whole point. A ⏳ section says *named, and waiting to be asked*. A
line here says *asked already, and answered somewhere it should not have been*.

| Parameter | Who was forced to invent it | State |
|---|---|---|
| **Endpoints and spares** | [asset reconciliation](cross-cutting/labs/asset-reconciliation/) invented 97 devices; the store below is sized for *stock, spares and returns* and states no quantity | ⏳ open |
| **Identity shape** — teams, admin and service accounts, guests | [permission sprawl](cross-cutting/labs/permission-sprawl/) built two estates for *the same hundred people*; the plate carries four segments with no population behind them | ⏳ open |
| **SaaS estate** — how many, how many seats, who owns each, how many outside SSO | [permission sprawl](cross-cutting/labs/permission-sprawl/) again, and [mail authentication](cross-cutting/labs/mail-authentication-alignment/)'s sender inventory | ⏳ open |
| **Support load** — arrival rate by category, the support window | [help desk queue](cross-cutting/labs/help-desk-queue/) invented seven categories, their arrival rates and a fifty-hour window | ⏳ open |
| **Data and recovery** — what data exists, and the objective per category | [Step 09](build-out/09-backup-and-the-restore-drill.md) asks for *a recovery objective per category* and this file names no categories | ⏳ open |

**Every line here is the same failure.** A number this file should hold was invented
somewhere downstream instead, which is how a repo ends up with more than one
hundred-person office. It has one: *the reference office* is this file, and *a
hundred-person office* elsewhere is a generic phrase — a distinction now written into
[`CONTEXT.md`](CONTEXT.md).

**The table empties as they are written**, and a closed line moves below with what it
settled. An empty table is a state, not a finish: a parameter returns here the moment
something is forced to invent it again.

### Closed

✅ **People flow.** [Parameters](#parameters) gains a lease term as a scenario choice and
four derived rows; *Why these numbers* gains the rule. Joiners equal leavers plus growth,
which makes this office about twenty-three arrivals and seventeen departures a year — one
joiner-or-leaver event about every six working days. Across one lease that is a hundred
and sixteen hires **to grow by thirty**, and about two hundred and sixteen people holding
an account at some point for a floor that seats a hundred and thirty.

Two things came out of writing it that the ledger line did not predict. The **turnover
rate is 🧭** and is marked so in the parameter table: the structure of the derivation is
sound, the band it is fed is drawn from published employer figures rather than from this
author's payroll. And the **mover gets no number at all** — there is no rate here worth
trusting and none derivable from anything above, so the file says that plainly instead of
inventing one, and says the useful thing in its place: the mover is the only leg of JML
with no natural trigger.

**No conflict with [transcript retention](cross-cutting/labs/transcript-retention/).** The
ledger listed it as the source of demand, and on inspection the lab models *group*
membership — fifteen people joining one project group across three years — which is not
the company joiner rate and never was. The two are consistent rather than equal, and the
lab needed no change. What the office's numbers do is explain the lab: a population
turning over at this rate is why a group accumulates twenty-one readers while showing
eighteen members, and why the person the meeting was about can join on day 700 having
never been in the room.

## How interviews ask about this

⏳ **Not written yet.** When it exists it holds **questions and what each one is testing**,
and no model answers.

That boundary is not a style preference. Public material teaches you how to think; a
finished answer does the work for you, and the two do not belong in the same file. A
question plus what it probes is the first kind. A polished response is the second.
