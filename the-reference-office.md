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

**Room area follows the seat count.** A workable estimate is fifty square feet for the
room plus twenty-five per seated person, which is what turns *seven rooms* into a number a
landlord can quote against.

## Selection rules

⏳ **Not written yet.** This section takes criteria only, never model names.

**It gets written when a build-out step needs it** — not when a video needs it. The test
is whether the scenario would still want it if nothing were ever filmed.

## Reference build

⏳ **Not written yet.** When it exists it is a dated table and nothing else, replaceable
whole without touching a word of prose elsewhere in this file.

**Entry condition, and it is a hard one.** Every line here must survive the question
**could someone buy from this?** A switch model, a port count, an access point count all
pass. How a protocol behaves does not — that belongs somewhere else and this file stays
out of it.

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
