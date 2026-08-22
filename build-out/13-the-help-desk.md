# 13 · The help desk itself — and how many people this needs

> ✋ hands-on — service desk operations and ITSM practice
> **Before:** 04 devices · 10 remote access · 11 assets · 12 rooms. **After:** 15 joiner/mover/leaver

Twelve steps have described what to build. This one asks the question everything
else assumed had an answer: **who runs it, and how many of them are there?**

It sits here because the honest inputs only exist now. Staffing a service desk from
a headcount ratio is guessing; staffing it from the actual estate — how many
devices, how many sites, how many things that page someone — is arithmetic with a
margin.

## What this step produces

- A staffing number with **the reasoning attached**, including what it assumes about
  the automation in steps 04, 08 and 15.
- Support hours, stated. If it is business hours, say what happens outside them
  rather than leaving people to discover it.
- Two or three ticket categories that map to something you would act on.
- An escalation path with names, and a documented answer to what happens when the
  one person who knows a system is away.
- A small set of runbooks for the highest-volume requests — which you can now
  predict, because steps 04, 10 and 12 named them.

## Questions to ask first

- **What is actually being supported?** 100 people, ~110 devices, two sites, a
  handful of rooms, a SaaS estate, and the short list of local things from step 05.
  Write it down; it is the denominator for every staffing conversation.
- **What does the automation actually remove?** Zero-touch enrolment, automated JML
  and patch automation each take a category of work off the queue. If they are not
  built, the staffing number goes up — this is where the earlier steps get paid for.
- **What are the top three request types going to be?** Access ("I can't get into X"),
  remote access, and hardware. All three are predictable, which means all three can
  be pre-solved with a runbook rather than improvised at volume.
- **Business hours, or something more?** Coverage beyond a single shift is not a
  scheduling question, it is a second person.
- **What is the bus factor?** At this size it is usually one. Naming that honestly is
  worth more than a policy that pretends otherwise.
- **How does someone ask for help when the thing that is broken is how they ask?**
  Step 10's version of this question, generalised.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Ticket volume drivers | password resets, mapped drives, printers, imaging | access, remote connectivity, SaaS permissions, rooms |
| Password resets | a large share of the queue | mostly gone, absorbed by self-service and SSO |
| Imaging | a technician per device | approaching zero, if step 04 was done properly |
| Where work went instead | — | **access questions and integration failures** — harder, less repetitive, less automatable |
| The skill that matters | knowing the systems | **judgement about what is actually broken**, because the systems are now somebody else's |

**How much of that is AI: real, bounded, and worth stating precisely.** Draft
responses, suggested runbooks, retrieval over past tickets, and triage suggestions
all work today and measurably reduce time-to-first-response. What has not happened,
at this size, is unattended resolution.

The pattern from the rest of this series holds and is well documented: in a 2026
survey of over a thousand sysadmins by Action1 (a patch-management vendor — read the
framing accordingly), AI adoption clustered in the advisory tasks, around half for
log analysis and just under half for troubleshooting, while anything carrying
authority over a production change stayed far lower. Roughly a third said their
organisation now requires them to use AI, up from about one in seven in 2023 —
**the mandate is growing faster than the authority is**.

For this step the practical consequence is a staffing answer that is *slightly*
smaller and a queue that is *qualitatively harder*: the repetitive work is what
automation and AI take first, and what remains is the part that needed judgement all
along.

## Read deeper

- [`cross-cutting/itsm-and-assets.md`](../cross-cutting/itsm-and-assets.md) — the four
  things ITSM tracks, and the operational spine this step sits on
- [`cross-cutting/incident-response.md`](../cross-cutting/incident-response.md) —
  lifecycle, on-call and post-mortem, for when a request becomes an incident
- [`ai-workflow/how-i-use-ai-to-learn-and-operate.md`](../ai-workflow/how-i-use-ai-to-learn-and-operate.md)
  — the method, applied to daily operational work

## Do it

- [`toolbox/linux-triage/`](../toolbox/linux-triage/) — the shape a runbook should
  have: ordered checks, each one eliminating something

🔴 **Gap:** nothing models the queue itself — arrival rates, categories, and what
automating one category does to the others. Recorded in [`GAPS.md`](./GAPS.md).

## Getting it backwards

**Staffing from a ratio.** "One per fifty users" ignores whether enrolment is
zero-touch, whether JML is automated, and whether there are four sites or one. The
same headcount is either comfortable or underwater depending on decisions made in
steps 04 and 15.

**No runbook for the predictable three.** They are predictable. Solving them from
scratch each time, by whoever is free, produces three different answers and a user
population that learns to ask a specific person instead of the queue.

**A bus factor of one, undiscussed.** It is often unavoidable at this size. What is
avoidable is nobody having said it out loud, so that no documentation was prioritised
and no cover was arranged before the holiday.

**Buying a ticket system before knowing the categories.** The taxonomy gets designed
by the vendor's template, filled in at random, and reported on by nobody.
