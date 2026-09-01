---
kind: note
axis: start-here
themes: []
platforms: []
summary: "Every step in the build-out says a hundred people."
---
# The reference office

> 🌐 **Languages:** English (default) · [中文](docs/zh/the-reference-office.md)

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
| Where things run | Years. What cannot leave the building changes slowly, and the refusals change more slowly still. Four rows and six refusals — the shortness is the finding. |
| Reference build | Short. Dated, and meant to be replaced whole. |
| Cost shape | Medium, and relative only. No currency figures — six relationships, each derived from a number above. |
| What this office does not yet say | Shortest. It is a ledger, and it empties. |
| How interviews ask about this | Long. Questions age slowly; the answers were never here. |

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
| Endpoint refresh | Every 3 years |
| Functions | 8 |
| Support window | 08:00–18:00, Mon–Fri — 50 hours |
| Restore drill | Once a year, performed and recorded |

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
| Endpoints in service | ~100, rising to ~130 | One primary device per person; sharing is the exception at this size |
| Spares held | ~5 | A month of joiners plus what breaks in that month, without a purchase order in the path |
| Replacements | ~38 a year | Average fleet of 115 on a 3-year refresh |
| Devices purchased | ~44 a year | Replacements plus net growth |
| Devices over the lease | ~220 | To hold about 115. The register's population is twice the fleet's |
| Privileged identities | ~3, plus 2 break-glass | Separate from the person's own account; break-glass count is [step 03](build-out/03-identity.md)'s |
| Devices needing an 802.1X credential | ~26 | The fixed population: room displays and systems, booths, printers, door controllers |
| Management interfaces | ~11 | Three access switches, a core, six APs, a controller |
| Registered guests | none | Guest is sized by the peak day, not by a register — that is what makes it guest |
| Services IT owns and can name | ~10 | One per thing the sixteen steps require: directory, tenant, files, MDM, EDR, backup, remote access, ITSM, conferencing, monitoring |
| Services the office actually uses | **Not derivable, and that is the parameter** | Eight functions buy their own; the number is unknown *to IT* by construction |
| Seats on the core services | ≈ headcount | Bought per person, reclaimed by the leaver flow — for the ten it reaches |
| Non-human identities | ~40 | 26 device credentials, ~12 service integrations, 2 break-glass. **None has a last day** |
| Tickets, before automation | ~79 a week | Seven categories at the rates the [help-desk drill](cross-cutting/labs/help-desk-queue/) models |
| Tickets, once the build-out is built | ~48 a week | Steps 04, 08 and 15 remove 39% of the volume |
| Largest surviving category | Access and permissions, ~37% | Nothing in the sixteen steps removes it, and [the reason is above](#why-these-numbers) |
| Places company state lives | 5 categories | The tenant · the endpoints · the directory · IT's own records · the services nobody listed |
| Categories that can have a recovery objective | 4 of the 5 | You cannot set an objective for a system you have not inventoried |
| Categories needing an **expiry** as well | 3 of the 5 | Anything holding a record of a person, a meeting or a decision |

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
  has laptops arriving in boxes — about forty-four a year, plus the thirty-eight going the
  other way. It needs a shelf rather than a room: five spares, the returns not yet wiped,
  and whatever is in transit. Stock, spares, returns and deliveries need somewhere that
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

**One device per person, and the interesting number is not that one.** At this size and
this kind of work a primary device per employee is the assumption to argue *against*, not
for; shared machines, second devices and desk-side hardware are exceptions that need a
reason. So the fleet is the headcount: about a hundred now, about a hundred and thirty by
the end of the term. That is the boring half.

**The refresh cycle is what actually drives the work, and it is bigger than hiring.** A
three-year replacement cycle across an average fleet of a hundred and fifteen retires and
replaces about thirty-eight machines a year. Against twenty-three joiners, that means
**fewer than four in ten device handovers happen because somebody joined.** The majority
are handovers to people who already work here, already have an account, and already had a
machine. An imaging and enrolment process designed around the first day misses most of its
own traffic — which is the argument [step 04](build-out/04-devices-and-images.md) is
making when it says the technician-per-machine model does not survive.

**Purchases are replacements plus growth**, so about forty-four a year, and about two
hundred and twenty across the lease **to hold about a hundred and fifteen at a time.** The
fleet is a hundred and fifteen; the *register* has to account for two hundred and twenty,
the way the directory has to account for two hundred and sixteen people rather than a
hundred and thirty. Both estates are roughly twice the office, and for the same reason:
**an office is a snapshot and a register is a history.**

**The spares number is small, and it is a lead-time calculation rather than a stock
policy.** Hold enough that a joiner starting on Monday and a machine that died on Friday
are both covered without a purchase order in the path — a month of joiners is about two,
and the failures and accidents in that month are a fraction of one on a fleet this size.
Five covers both with room for a loaner, which is why the store needs a shelf and not a
room. **The part of this that varies most by fleet is breakage**, and a place that issues
laptops to a field team should not take five from here.

**The four segments on the floor have populations, and they are already counted
elsewhere in this file.** The plate draws staff, guest, unpatchable and management; the
port table above says how many things are in each without ever using those words.

| Segment | What is on it | How many | How often it changes |
|---|---|---|---|
| **Staff** | The managed fleet, and the phones that come with the people | ~100 endpoints rising to ~130; about 130 associated on the peak day | 40 people events and 82 device events a year |
| **Guest** | Whatever a visitor brought | Unbounded and unregistered **by design** | Every day |
| **Unpatchable** | Room displays and systems, booth devices, printers, door controllers | ~26 by port count, about twenty by wireless association — the same permanent population counted two ways | Almost never |
| **Management** | Three access switches, a core, six access points, a controller | ~11 interfaces | When the network changes |

**Two of those four never churn, and that is the problem with them.** Staff turns over
forty times a year and every one of those events has an owner, a date and a ticket.
Unpatchable and management change almost never — and because
[Selection rules](#selection-rules) require 802.1X, each of those thirty-seven things holds
a credential. **Nothing in the calendar ever makes anyone look at them.** A leaver forces a
review of one person's access; nothing forces a review of a door controller's.

**Which is the same shape as the mover, one layer down.** A human identity has a leaver
event. **A service account does not.** The device credentials above, the integrations that
will arrive with the SaaS estate, the enrolment connector, the monitoring account — none
of them has a last day, a manager, or anybody who notices. The count of those is not in
this file yet because it depends on how many services the office buys, which is the next
line of the ledger; what is already fixed is that **the non-human half of the directory is
the half with no natural end.**

**The count of services has two answers, and the gap between them is the domain.** The
first is countable and this file gives it: the sixteen steps require a directory, a
productivity tenant, file and collaboration storage, device management, endpoint security,
backup, remote access, an ITSM tool, conferencing and something that watches all of it —
**about ten services IT owns and can name.** The second answer is *how many the office
actually uses*, and **this file will not give you a number, because no such number exists
on the IT side.** Eight functions buy their own tools, on a card, without asking. The
parameter is not a count; it is that **there is a count IT does not have.**

**That is not a lament and it is measurable from the other end.** The
[mail authentication drill](cross-cutting/labs/mail-authentication-alignment/) is exactly
this arithmetic run backwards: the written inventory lists four senders, receivers
actually saw six, and one of the four listed had stopped sending. **Wrong in both
directions at once** — a billing platform finance bought and a CI runner nobody added,
against a newsletter tool that was decommissioned and never struck off. The office does
not have a list of its services; it has a list of the services somebody remembered.

**Seats follow headcount for ten services and follow nothing for the rest.** The leaver
flow in [step 15](build-out/15-joiner-mover-leaver.md) reaches what IT administers, so on
the core ten a seat is reclaimed when somebody goes. For the tail there is no reclamation
rate to quote, because **no leaver event reaches those services at all** — the drift is
not a percentage, it is total. Across one lease that is eighty-six departures whose access
to department-bought tools nobody revokes, because nobody with a revocation duty knows the
tools are there.

**The non-human half of the directory can now be counted, and it is about forty.** Twenty-
six device credentials from [the segments](#why-these-numbers), roughly a dozen service
integrations across the core ten, and two break-glass accounts. Two in five identities in
this office are not a person — and where a human has a start date, a manager and a last
day, **not one of the forty has any of the three.** The privileged accounts are the
exception that proves it: there are about three, and they expire because the human behind
each one eventually leaves.

**The support window is a scenario choice and it is the one that decides staffing, not
the ticket count.** Eight to six, Monday to Friday, is fifty hours; one person works
forty. That gap is arithmetic, it has nothing to do with volume, and it is why
[the help-desk drill](cross-cutting/labs/help-desk-queue/) finds coverage rather than
demand to be the binding constraint at this size. **This file states the window and the
volume and deliberately states no headcount** — the drill computes a floor and explains at
what population its answer expires, which is a different and more honest thing than a
number in a parameter table.

**Two of the seven ticket categories can be checked against numbers derived earlier in
this file, and they hold.** Once [step 04](build-out/04-devices-and-images.md)'s zero-touch
provisioning is built, enrolment and imaging generate about fifty-three tickets a year —
against the **sixty-two device handovers** the refresh cycle and the joiner rate produce.
**About seven tickets for every eight handovers**, which is what zero-touch is supposed to
look like: most machines change hands and nobody files anything, and some do not.
Two independent derivations, one from ticket rates and one from fleet arithmetic, landing
on the same office.

**What the build-out removes, and what it cannot.** Steps 04, 08 and 15 take the weekly
load from about seventy-nine to about forty-eight. Lifecycle work — joiners, movers,
leavers, enrolment — falls from roughly a seventh of all tickets to about a
twenty-fifth. **Access and permissions does not move at all, and afterwards it is the
largest category left at better than a third of everything.**

**That is not a gap in the automation; it is [the estate](#parameters) showing up in the
queue.** Access requests are generated by an identity population where two in five
identities are not people and have no lifecycle, against a service estate whose size IT
does not know, changing about a hundred and twenty-three times a year in the asset
register alone. Automating a request path does not shrink that. **The categories the
sixteen steps remove are the ones with a deterministic answer; the one that survives is
the one that ends in a human deciding whether somebody should have something** — which is
the same boundary every AI column in the build-out lands on.

**[Step 09](build-out/09-backup-and-the-restore-drill.md) asks for a recovery objective
per category and this file never said what the categories were.** Everything above now
does. State lives in five places: the **tenant** the office works in, the **endpoints**
that should hold nothing but do, the **directory** everything else authenticates against,
**IT's own records** — the asset register and the ticket history that change a hundred and
twenty-three times a year — and **the services nobody listed**, which step 09 names
outright as *two or three line-of-business SaaS products* and which
[the estate above](#parameters) has already established the office cannot count.

**Four of the five can have an objective. The fifth cannot, and not because it is
hard.** *How much work can we afford to lose* is answerable for a system somebody has
written down. For the tail there is no bad answer available — there is **no question**,
because setting an objective requires knowing the system exists. The correct entry for
that category is not a number of hours; it is that the inventory is the deliverable and
everything else waits on it.

**And there is a second objective on the same axis, pointing the other way, that no step
asks for.** A recovery objective is a **floor** on retention: do not lose more than this.
What several of these categories also need is a **ceiling**: do not keep longer than
this. The two are not variants of one setting, they are opposite constraints, and backup
practice supplies only the first.

**The cost of having only the floor is measured in
[the transcript drill](cross-cutting/labs/transcript-retention/).** A meeting recording
expired on day thirty, exactly as the platform intended. The summary written from it had
no retention at all, so on day one thousand and ninety-five it was still there, still
readable, still carrying one misattributed line — **one thousand and sixty-five days after
the only artefact that could have checked it stopped existing.** Nothing was
misconfigured. Every access review passed truthfully. The control that was missing was
never an access control; it was an expiry, and no *recovery* objective would ever have
produced one.

So three of the five categories — the tenant, IT's own records, and whatever the tail
turns out to hold — need both numbers written down, and this file names the second one
rather than letting *retention* mean only the reassuring half.

**The two device numbers in this file are not in conflict, and it is worth saying why.**
The fleet is *~100 managed endpoints rising to ~130* — every employee, whether or not they
came in today. The wireless derivation is *~145 associated devices* — sixty-five people at
two devices each on the peak day, plus the fixed population. Different denominators: one
counts what the office owns, the other counts what is in the air on a Tuesday. A hundred
laptops and a hundred and forty-five associations are the same office.

**Put the two estates together and you get the reconciliation problem, not a description
of it.** Forty joiner-or-leaver events a year, forty-four purchases, thirty-eight
retirements: **about a hundred and twenty-three changes a year to the asset register, one
roughly every two working days.** Reconciling that annually means comparing two systems
that have each moved a hundred-odd times since anyone last looked. The residue is not a
sign that somebody was sloppy; it is what a two-day mutation rate does to a twelve-month
check.

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

**Two halves, two entry conditions, both now fired.** The on-premises half fired when
[`endpoint/`](endpoint/README.md)'s companions needed a staging ring. The cloud half
fired from an unexpected direction — not a cloud lab, but three places that began
assuming a scheduler exists without saying where it runs.

### On premises — what cannot leave

[Step 02](build-out/02-the-building.md) shrank this room to *switches, an access
controller, a print device, a little lab gear* because workloads left the building, and
[step 04](build-out/04-devices-and-images.md) put the image with the OS vendor rather
than on-site. So the question is never *what should we run here*. It is **what cannot
leave**, and a thing earns a place on this floor by satisfying at least one of three
tests:

1. **It acts on the building.** A door, a printer, a radio. There is no version of it
   that is somebody else's service, because the thing it does is physical and it is here.
2. **It has to work when the uplink does not** — and something on this floor genuinely
   depends on that.
3. **It is the thing you break on purpose.** A staging ring cannot be somebody else's
   production.

| What stays | Which test | Why, in one line |
|---|---|---|
| **Switching and the access layer** | 1 | The floor's own forwarding. Nothing about it is remote |
| **Door and access control** | 1, 2 | The doors have to open on a day the internet does not. The decision is made at the door, which is why the controller is on this floor and in the [unpatchable segment](#why-these-numbers) |
| **A print device** | 1 | The paper comes out here. The queue in front of it need not be here, and increasingly is not |
| **The wireless controller** | — | **A real choice, not a default.** [Selection rules](#selection-rules) ask for *controller or cloud management that one person can operate*; both pass, and the deciding question is which one a single administrator can still operate at three in the morning |
| **A staging ring — the *little lab gear*, made specific** | 3 | See below |

**Test 2 is the one that surprises people, because almost nothing passes it.** Ask what
must keep working in this office on a day the uplink is down, and the honest list is:
getting into the building, getting out of it, and the fire panel. Everybody's work is in
a tenant they cannot reach anyway. **A SaaS-first office does not need local continuity
for its work; it needs it for its doors.** That is a much smaller requirement than most
on-premises arguments assume, and it is worth saying because *what if the internet goes
down* is the most common reason given for keeping a server room that nothing else
justifies.

**The staging ring is the one this office genuinely needs, and it is new.**
[`endpoint/management.md`](endpoint/management.md) and
[`endpoint/provisioning.md`](endpoint/provisioning.md) both land on the same
non-negotiable: a policy or an image goes to your own machines first, then a friendly
team, then everyone. **You cannot stage a device policy on somebody else's fleet** — the
whole point is to break something, and it has to be enrolled in your real management
platform to be a real test.

So: a small hypervisor in the IDF for the Windows and Linux side, plus **physical Apple
hardware**, because that side cannot be virtualised on anything you would put in this
rack. Two or three machines' worth, drawn from the same shelf as the
[five spares](#parameters) rather than bought separately. It is the smallest thing in
this section and the only one that would otherwise have been an accident.

**What was considered and does not stay.** Recorded because a room's contents are
decided as much by refusals as by requirements, and an unrecorded refusal gets
re-litigated every eighteen months.

| Considered | Verdict | Where the reasoning lives |
|---|---|---|
| **A self-hosted database** | **No.** [ADR-0015](docs/adr/0015-the-reference-office-consumes-services-and-operates-none.md) says this office operates no service, so there is no application whose state would live in it. Every system that holds state here is bought | [questions · storage](docs/questions/storage.md) |
| **A general VM estate** | **No** beyond the staging ring above. With imaging at the vendor, files in a tenant, identity in a cloud and monitoring bought, the honest question is *what would run on it* — and at this size the answer is nothing that is not already somebody's service | [questions · platforms](docs/questions/platforms.md) |
| **A file server** | **No.** The suite holds the files, and the design question moves with them: it stops being *permissions on directories* and becomes *who can see this*, which is [`permission-sprawl`](cross-cutting/labs/permission-sprawl/)'s subject and a harder problem than the one it replaced | [questions · storage](docs/questions/storage.md) |

**None of those three is a rule for every office.** Each is the answer *at a hundred
people, consuming services and operating none*. The transferable part is the three tests
at the top, which is why they are stated before the list rather than after it.


### In a cloud

**The entry condition fired, and not from where it was expected.** It read: *a step or
a lab is forced to invent a cloud number for this office.* No lab about cloud ever
appeared. What happened instead is that **three separate places began assuming this
office runs scheduled automation, and none of them said where it runs**:

- [Mail authentication](cross-cutting/labs/mail-authentication-alignment/) invented a
  **CI runner** sending a hundred and forty-five messages a year as this domain,
  described in its own model as *a host nobody added to the record*. A lab was forced to
  invent a machine.
- [`endpoint/encryption-and-keys.md`](endpoint/encryption-and-keys.md) calls the
  escrow-to-register comparison **a quarterly query, not a project**.
- [`endpoint/management.md`](endpoint/management.md) asks for a policy's reach to be
  **re-derived on a cadence** with an alert on the delta.

Each of those needs a thing that wakes up on a schedule and talks to APIs. This office
has one, it has never been written down, and every entry below answers the same
question: **why is this not in the IDF?**

**What runs here, and why not downstairs**

| What | Why not in the IDF |
|---|---|
| **The automation host** — the scheduler behind the reconciliations, the lifecycle runs, and the alerting the sections above ask for | Three reasons and each is sufficient. It must run **when the floor is empty**, which is most of the time. What it talks to is **almost entirely cloud APIs** — the directory, the device management, the tenant, procurement — and almost never the floor. And it must **survive the building**: a job whose whole purpose is to reconcile the asset register cannot live on a machine that register is about |
| **The off-platform copy of anything backed up** | [Step 09](build-out/09-backup-and-the-restore-drill.md) requires backups to **leave the platform they protect**. For a floor whose only on-site dependency is one room with one door, the IDF is not *away* — it is the failure the copy exists to survive |

**Why the automation host is not the staging ring**, which is the nearest thing on the
other half and the obvious place to put it: **the staging ring exists to be broken.**
That is its entire function. An automation host that reconciles the estate must be the
most boring machine you own. Two workloads with opposite requirements do not share a
host, and noticing that is the whole reason these two halves are one section.

**What does not go here either.** The same discipline as the on-premises refusals, and
for the same reason.

| Considered | Verdict |
|---|---|
| **A jump host or bastion** | **No.** There is nothing to jump to. [The on-premises half](#on-premises--what-cannot-leave) holds no servers, and the staging ring is reached from the floor it sits on |
| **Anything hosting a service for anyone outside the building** | **No**, by [ADR-0015](docs/adr/0015-the-reference-office-consumes-services-and-operates-none.md). Not a sizing judgement — a statement about what this office *is* |
| **The bought services themselves** — the tenant, the directory, the device management, the escrow inside it | **Not here.** Those are the [SaaS estate](#parameters), which counts what the office *buys*. This half holds only what IT itself **operates**, which is why it is two rows long and the SaaS estate is about ten plus a tail nobody can count |

**Two rows is the finding.** An office that consumes services and operates none has
almost nothing of its own running anywhere — and the little it does have exists to
*check the things it bought*. Neither of those rows would appear on a diagram anybody
draws of this office, and both would be discovered during an incident.

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

**Relative relationships only, never figures.** Currency amounts date faster than
anything else here and vary by region more than they vary by decade, so this section
states what is bigger than what — every one of them derived from a number
[above](#parameters) rather than from a price list.

**1. The recurring beats the one-time, and it is not close.** Seats on
[about ten services](#parameters), at roughly headcount, every year for the term of the
lease. The fit-out is paid once. Any conversation that treats the network build as *the
IT budget* is looking at the smaller half.

**2. Inside the fit-out, the ceiling beats the desk.** [Power over ethernet, the radios
and the ports facing them](#wired--ports-then-the-two-things-that-get-under-specified)
are where the money and the constraint are — a switch's PoE budget varies by more than
a factor of two between models at the same port count. **The desk port is the cheap
tier and stays cheap**, and specifying it up is the most common way to spend this
budget in the wrong ceiling.

**3. Inside the recurring, the part that grows is the part nobody counts.** The named
ten scale with headcount, which is predictable. [The tail scales with
nobody watching](#parameters) — bought on a card, never in the leaver flow, never
reclaimed. It is the only line here whose growth is not a function of anything.

**4. Device spend is a cycle, not a growth line.** [Thirty-eight replacements a year
against twenty-three joiners](#why-these-numbers) means **roughly three in five machines
bought have nothing to do with headcount**. A budget modelled on hiring under-reads by
that much, every year, and the gap looks like an overrun rather than a model error.

**5. The service desk is a step function and the step is coverage.** Volume asks for
one person; a [fifty-hour support window against a forty-hour
week](#parameters) asks for two, and that second one is bought for *hours* rather than
for *tickets*. Anything that reduces ticket volume does not move it.

**6. The cheapest controls in this file cost a paragraph.** Reserving an address range
so a remote session is distinguishable from a desk; writing the blast radius down at
authoring time; giving a synchronised row a `fetched_at`. Each is one design decision,
none has a line item, and each is worth more later than something with a price.

**What this section will never hold:** a currency figure, a per-seat price, or a
vendor's quote. Those belong in a dated `Reference build` whose entry condition is not
met, and they would be wrong before the ink dried.

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

**None open.** All six the ledger found are written; see [Closed](#closed) below.

A parameter earns a line back here the moment something in this repo has to invent it
again. **The list being empty is a state, not a finish.**

**Every line it held was the same failure.** A number this file should have carried was
invented somewhere downstream instead, which is how a repo ends up with more than one
hundred-person office. It has one: *the reference office* is this file, and *a
hundred-person office* elsewhere is a generic phrase — a distinction now written into
[`CONTEXT.md`](CONTEXT.md).

**And the six did not divide evenly into corrections.** Five of the labs that forced a
parameter turned out to need no change at all: their numbers sat inside what this file
derives, and what the derivations did was explain *why* each lab's finding is structural
rather than contrived. One went the other way — the support load is the drill's arithmetic
and this file adopted it. [Q7's rule](#closed) — the derivation wins a real conflict — was
never needed, because there was never a real conflict. That was worth finding out rather
than assuming in either direction.


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

✅ **Endpoints and spares.** One device per person makes the fleet the headcount, which
is the dull half. The refresh cycle is the other one: thirty-eight replacements a year
against twenty-three joiners, so **fewer than four in ten device handovers are because
somebody joined**. About two hundred and twenty machines are bought across the lease to
hold a hundred and fifteen — the same roughly-twice-the-office shape the directory has,
because an office is a snapshot and a register is a history.

✅ **Identity shape.** The plate's four segments get their populations, and they were
already in the port table under other names: ~26 fixed devices on unpatchable, ~11
interfaces on management, the fleet on staff, and nothing at all on guest — **guest is
sized by the peak day and not by a register, which is what makes it guest.**

The finding is which segments *do not* move. Staff churns forty times a year and every
event has an owner and a date. Unpatchable and management change almost never, and because
[Selection rules](#selection-rules) require 802.1X, those thirty-seven things each hold a
credential **that nothing in the calendar ever makes anyone look at**. That is the mover's
problem one layer down, and it has a sharper form: a human identity has a leaver event and
**a service account does not**.

The count of non-human identities is deliberately *not* here. It depends on how many
services the office buys, which is the next open line — an example of the entry condition
working rather than a gap in this one.

✅ **SaaS estate.** Ten services IT owns and can name, one per thing the sixteen steps
require. The second number — how many the office *uses* — is deliberately absent, because
**the honest parameter is that no such number exists on the IT side.** Eight functions buy
their own, and the file says so rather than inventing a figure that would look sourced.

It also settles the count domain 3 deferred: **about forty non-human identities**, being
twenty-six device credentials, a dozen service integrations and two break-glass. Two in
five identities in this office are not a person, and where a human has a start date, a
manager and a last day, not one of the forty has any of the three.

✅ **Support load.** The window is now a scenario choice — fifty hours against a
forty-hour week — and it is the number that decides staffing, which is why this file
states it and states **no headcount**: the drill computes a floor and says at what
population the floor expires, and a headcount in a parameter table would quietly outlive
that caveat.

**This is the one domain where the office adopts the lab's numbers rather than the other
way round.** The seven categories and their arrival rates are the drill's, step 13 is 🔨
ground, and nothing in this file derives them independently. What this file adds is the
back-reference and one cross-check that was not available before: automated enrolment
comes to about fifty-three tickets a year against the **sixty-two device handovers**
[Endpoints and spares](#parameters) derives from the refresh cycle — seven tickets per
eight handovers, from two derivations that share no inputs.

The finding is which category survives. Steps 04, 08 and 15 take the load from
seventy-nine a week to forty-eight, and lifecycle work drops from a seventh of tickets to
a twenty-fifth. **Access and permissions does not move at all and ends up the largest
category left**, because it is generated by an identity population that is two-fifths
non-human with no lifecycle, against a service estate whose size IT does not know. The
automatable categories are the ones with a deterministic answer; the survivor ends in a
person deciding whether somebody should have something.

**No conflict with
[mail authentication](cross-cutting/labs/mail-authentication-alignment/), which turns out
to be this domain measured from the other end.** Its inventory lists four senders,
receivers saw six, and one of the listed four had stopped sending — wrong in both
directions at once, with a billing platform finance bought and a CI runner nobody added on
one side and a decommissioned newsletter tool on the other. That is not a contrived
scenario; it is what *there is a count IT does not have* looks like when a receiver
reports it back. The lab needed nothing changed.

**No conflict with [permission sprawl](cross-cutting/labs/permission-sprawl/).** Its
estate is a hundred people with a finance function of eight and a nested core of three,
which is what eight functions across a hundred people produces; nothing needed changing.
What this file adds is why its ninety-three-reader gap is structural rather than careless
— the estate holding that document is administered against a population that turns over
forty times a year, and a sharing link is the one grant path that no leaver event touches.

**No conflict with [asset reconciliation](cross-cutting/labs/asset-reconciliation/)
either, and the check was worth running.** Its ninety-seven is a snapshot of *a*
hundred-person office in the generic sense, not a claim about this one, and it sits inside
what this file derives — a hundred in service, less the joiners not yet issued and the
returns not yet re-imaged. Nothing needed correcting under
[Q7's rule](#what-this-office-does-not-yet-say).

What the numbers *do* to that lab is better than a correction. Its five anomalies are not
contrived cases; they are this office's event stream, at the rates above. *She left in
June and he has had the laptop since* is a leaver. The re-image wave is refresh. The
warranty swap is breakage. The disposal that was never filed is a retirement, and there
are thirty-eight of those a year. **A hundred and twenty-three register changes a year,
one every two working days, reconciled annually** — the lab's three wrong records are what
that arithmetic produces, not what carelessness produces.

✅ **Data and recovery.** [Step 09](build-out/09-backup-and-the-restore-drill.md) asked
for a recovery objective per category against a file that named no categories; the five
other domains named them without meaning to. State lives in the tenant, the endpoints, the
directory, IT's own records, and the services nobody listed.

**Four of the five can have an objective and the fifth cannot** — not because it is hard,
but because setting one requires knowing the system exists. For that category the
inventory *is* the deliverable.

The finding is a second objective, on the same axis, pointing the other way. A recovery
objective is a **floor** on retention: do not lose more than this. Three of these
categories also need a **ceiling**: do not keep longer than this. Backup practice supplies
only the first, and
[the transcript drill](cross-cutting/labs/transcript-retention/) already measured what the
missing second one costs — a summary still readable one thousand and sixty-five days after
the recording that could have checked it expired, with nothing misconfigured and every
access review passing truthfully. **The control that was missing was never an access
control; it was an expiry**, and no recovery objective would ever have produced one.

**No conflict with [transcript retention](cross-cutting/labs/transcript-retention/).** The
ledger listed it as the source of demand, and on inspection the lab models *group*
membership — fifteen people joining one project group across three years — which is not
the company joiner rate and never was. The two are consistent rather than equal, and the
lab needed no change. What the office's numbers do is explain the lab: a population
turning over at this rate is why a group accumulates twenty-one readers while showing
eighteen members, and why the person the meeting was about can join on day 700 having
never been in the room.

## How interviews ask about this

**Questions and what each one is testing. No model answers**, here or anywhere else in
this repo.

That boundary is not a style preference. Public material teaches you how to think; a
finished answer does the work for you, and the two do not belong in the same file. A
question plus what it probes is the first kind. A polished response is the second.

**Every question below is answerable from this file**, which is the other reason they
are here: an interviewer asking any of them is asking whether you size from a rule or
from a habit, and this file is the rule.

| Asked | What it is actually testing |
|---|---|
| *How many access points would you put in an office this size?* | Whether you [count twice and take the larger](#wireless--count-it-twice-and-take-the-larger) — and whether you know that below about a hundred and fifty people **the coverage floor usually wins**, which surprises people who were told density is what matters. A confident single method is the wrong answer whichever method it is |
| *How many desks for a hundred people?* | Whether you ask about the working pattern before answering. **A hundred is a payroll number**; the building question is the peak day |
| *How would you segment this network?* | Whether you say *trust levels* or *departments*. The follow-up that separates them: **what are you willing to block between two segments, and will you actually block it** — a segment with an any-any rule to staff is a VLAN wearing a control's name |
| *What is in the comms room?* | Whether you know **the answer changed**. Servers, storage and tape became switches, an access controller, a print device and a little lab gear — and the room got *more* critical rather than less, being the last single point of failure that is physically yours |
| *How many people do you need on the service desk?* | Whether you can name **the binding constraint**. At this size it is coverage, not volume — a fifty-hour window against a forty-hour week — and a ratio produces a number that happens to be right here and cannot say when it stops being |
| *What is your backup strategy?* | Whether *strategy* means a schedule or a **recovery objective per category**. The strong version asks which categories exist first, and notices that one of them cannot have an objective at all because nobody has inventoried it |
| *How do you onboard someone?* | Whether you start from **the trigger** or from the ticket. *What system decides whether a person is still an employee* is the question underneath, and an answer that begins with a form has already lost the automation |
| *How many laptops does a hundred-person company buy?* | Whether you model **the refresh cycle** or the headcount. Three in five purchases have nothing to do with hiring, and an answer of *a hundred* is a snapshot offered where a rate was asked for |
| *Would you self-host that?* | Whether you have a **test** or a preference. The three used here — does it act on the building, must it work when the uplink does not, is it the thing you break on purpose — and the willingness to answer *no, and here is why* |
| *What would you improve about this design?* | Whether you can find the seam. The honest answers are in this file and are marked: the [🧭 wireless arithmetic](#selection-rules), the turnover band, and the mover with no rate |

**The follow-up matters more than the question in every row above.** An interviewer
learns most from what happens when the first answer is challenged — which is the whole
premise of [`cross-cutting/interview/`](cross-cutting/interview/README.md), where the
same discipline is applied to questions other people ask you rather than to this file's
own numbers.
