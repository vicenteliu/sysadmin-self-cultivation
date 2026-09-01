---
kind: route-step
axis: build-out
themes: []
platforms: []
marker: "🧭"
summary: "🧭 verified ramp, not hands-on. This step is written as a question list, not as negotiating advice — a question list can be derived from first principles; negotiating cannot, and this author has not…"
---
# 00 · Questions to ask before the lease is signed

> 🌐 **Languages:** English (default) · [中文](../docs/zh/build-out/00-before-the-lease.md)

> 🧭 **verified ramp, not hands-on.** This step is written as a question list, not
> as negotiating advice — a question list can be derived from first principles;
> negotiating cannot, and this author has not sat on that side of the table.
> **Before:** nothing. **After:** 01 uplink · 02 the building

The reason this step exists at all is that **everything it covers becomes
unchangeable at signature**, and IT is usually not in the room. A building with
one carrier, no riser space, and a landlord who owns the rooftop is not a problem
you solve later — it is a constraint you inherit for the length of the lease.

The deliverable of this step is not a decision. It is **a page of questions
handed to whoever is deciding**, early enough to matter.

## What this step produces

- A written answer to each question below, from the landlord or broker, **before**
  signature — not a promise on a call.
- A named cost for each "no", so the rent comparison is honest. A cheaper building
  that needs its own fibre trench is not cheaper.
- A go/no-go note that survives being overruled: if the site is chosen anyway, the
  known constraints are on record and the schedule reflects them.

## Questions to ask first

**Carriers and entry**
- **How many carriers can actually serve this suite** — not the building, the suite?
  "Fibre in the building" often means fibre in a basement vault that another tenant
  controls.
- Where does service enter, and is there a **second entry on a different path**? Two
  circuits through one conduit is one circuit.
- Who owns the **riser**, and what does it cost to pull new cable through it?
- What is the **lead time** for a new circuit here? Three months is common and it is
  the number most likely to break a move-in date.

**Space and power**
- Is there a **dedicated room** for network gear that locks, or is the plan a closet
  shared with the janitor's supplies?
- What power is available to it, and is it on the same panel as the floor's HVAC?
- **What happens to cooling after hours?** Building HVAC that shuts off at 19:00 is
  the most common cause of a room that works in week one and fails in week six.
- Can a rack physically reach the room — door widths, lift capacity, turns?

**Building services and rights**
- Rooftop and riser **rights**: can you put an antenna, a second carrier's demarc, or
  a generator tie there, and at what cost?
- Who provides door access and does it have to be the landlord's system? This
  decides whether step 05 has a choice or an obligation.
- Is there existing cabling, and does anyone have documentation for it? Assume no.

**Timing**
- What is the **earliest date IT can get in** to build, relative to the date staff
  arrive? Every week of overlap is a week of doing the build with an audience.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Carrier diversity | important | **more** important — everything is off-site now, so the uplink is the whole business |
| On-site room | had to hold servers | holds network gear, and the few things that cannot leave (door access, print, lab) |
| Power/cooling need | sized for a server room | much smaller, and therefore much easier to under-plan and get away with until it fails |
| Lead times | slow | **still slow** — the one line item cloud did not compress |

**How much of that is AI: none.** Nothing in this step has changed because of AI.
Saying otherwise would be the clearest possible tell that the AI column is
decoration. It is here to be answered honestly, including with "no".

## Read deeper

- [`the-stack/01-physical.md`](../the-stack/01-physical.md) — the physical layer,
  and what every platform is hiding from you at it
- [`the-stack/labs/01-failure-domains/`](../the-stack/labs/01-failure-domains/) —
  why "two circuits, one conduit" is one failure domain, made runnable

## Do it

🔴 **Gap by nature, not by omission.** There is nothing runnable here and there
should not be — this is a conversation with a landlord. The honesty marker carries
the weight instead. Recorded in [`GAPS.md`](./GAPS.md) as a boundary.

## Getting it backwards

**Being invited after signature.** The usual sequence is that IT sees the building
when it is time to install. Every answer above then becomes a workaround with a
budget line, and several of them — riser rights, second entry, after-hours cooling
— have no workaround at any price.

**Trusting "fibre ready".** It is a marketing phrase with no defined meaning. The
question that has meaning is *which carriers currently terminate service in this
suite, and can you give me a contact at one of them*.
