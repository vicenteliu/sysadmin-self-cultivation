---
kind: route-step
axis: build-out
themes: []
platforms: [self-host]
marker: "mixed"
summary: "🧭 for commissioning a new site; 🔨 for what happens in the rack afterwards (PXE/imaging fleets, BMC/IPMI, DNS and RAID at scale — see platforms/self-host/)."
---
# 02 · The building — riser, IDF, power, cooling, cable paths

> 🌐 **Languages:** English (default) · [中文](../docs/zh/build-out/02-the-building.md)

> 🧭 for **commissioning a new site**; 🔨 for **what happens in the rack afterwards**
> (PXE/imaging fleets, BMC/IPMI, DNS and RAID at scale — see
> [`platforms/self-host/`](../platforms/self-host/)). The distinction is deliberate:
> having operated machine rooms is not the same as having built one out of a shell.
> **Before:** 00 lease questions · 01 uplink. **After:** 04 devices · 05 network · 12 meeting rooms

This is the last step where physics is the constraint, and the only one where a
mistake is measured in construction rather than configuration. Everything after
this is software and can be redone on a Tuesday.

## What this step produces

- A room — locking, with its own power, and cooling that **does not stop when the
  building's does**.
- A documented cable plant: what runs where, terminated, labelled at both ends,
  tested. "Tested" means a certification report, not a laptop that got a link light.
- Enough spare capacity that the first unplanned need — an extra switch, a second
  UPS, someone's lab gear — does not require opening a wall.
- Photographs of everything before the ceiling goes back up. This costs ten minutes
  and is consulted for the length of the lease.

## Questions to ask first

- **What is in this room, honestly?** For a forced-hybrid 100-person office it is a
  small number of things — network gear, door access controller, print, and whatever
  lab equipment cannot leave. Sizing it for a 2015 server room wastes money; sizing
  it for "just a switch" leaves you stacking gear on a shelf by month four.
- **What happens to this room at 19:00 and on a Sunday in July?** Ask about the HVAC
  schedule specifically, in writing. This single question prevents the most common
  small-office room failure.
- **Is the power to this room on the floor's general circuit?** If yes, a space heater
  under someone's desk is now a network event.
- **How long does it need to survive without utility power** — a clean shutdown, or
  through a short cut? Those are different purchases, and the honest answer for most
  offices is the first one.
- **Who else has a key?** Cleaning, building maintenance, the landlord. A room
  anybody can enter is not a secure room, and some compliance evidence depends on
  that claim being true.
- **Where do the cable runs go, and how many spares?** Pulling spares during the
  build costs almost nothing; pulling one later costs a contractor and a ceiling.

## 2015 → today

| | 2015 | today |
|---|---|---|
| What the room holds | servers, storage, tape, UPS | switches, an access controller, a print device, a little lab gear |
| Power and cooling | a real engineering problem | small — and therefore easy to under-plan and get away with, until the first hot weekend |
| Cabling | to every desk, generously | still to every desk, but the load moved to **wireless density** and to APs needing PoE |
| Consequence of getting it wrong | contained, on-site | the room is now the only on-site dependency the whole office has |

**How much of that is AI: none.** The change here is that workloads left the
building — SaaS-ification and hosting, not models. The room got smaller and, in a
way that surprises people, more critical: it is the last single point of failure
that is physically yours.

## Read deeper

- [`the-stack/01-physical.md`](../the-stack/01-physical.md) — the physical layer
  compared across seven platforms; what an availability zone actually is
- [`platforms/self-host/architecture.md`](../platforms/self-host/architecture.md) and
  [`operations.md`](../platforms/self-host/operations.md) — the 🔨 material, from
  running fleets rather than commissioning buildings
- [`the-stack/labs/01-failure-domains/`](../the-stack/labs/01-failure-domains/)
- [the reference office's Selection rules](../the-reference-office.md#selection-rules)
  — how many access points and switch ports the floor above actually implies, since
  the cable and riser decisions here are made before anyone counts them

## Do it

- [`the-stack/labs/01-failure-domains/`](../the-stack/labs/01-failure-domains/) —
  the reasoning applies to a comms room as directly as it does to a region.

🔴 **Gap:** nothing here covers the build-out itself — no checklist for
commissioning a room from a shell. That is a boundary rather than a hole, and it
is marked so in [`GAPS.md`](./GAPS.md).

## Getting it backwards

**Sizing the room for what you are installing this month.** It is always exactly
big enough on day one. The first thing that does not fit ends up on a shelf, then
on the floor, and the room stops being a room and becomes a pile.

**Assuming building cooling is your cooling.** It runs on the building's schedule
and is designed for people, who go home. Equipment does not. The failure arrives
weeks after the install, which makes it hard to connect back to this decision.

**No documentation of the cable plant.** Every subsequent troubleshooting session
starts with tracing. Over a five-year lease that is a lot of hours, spent by people
who cost more than a labelling machine.
