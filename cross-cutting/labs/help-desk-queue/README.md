---
kind: lab
axis: cross-cutting
themes: [itsm-saas]
platforms: []
summary: "Seven ticket categories with their own arrival rates and handling times, two worlds (that automation built, or not), Erlang-C over a stated support window."
---
# Lab — "one per fifty users" is right here, for a reason it cannot state

**Goal:** turn the staffing question into arithmetic you can argue with. Step 13
asks how many people a hundred-person service desk needs. The usual answer is a
ratio, and a ratio is a linear sentence about a system that is not linear.

**You'll practise:** what
[build-out step 13](../../../build-out/13-the-help-desk.md) asks for — a staffing
number **with the reasoning attached**, including what it assumes about the
automation built in steps 04, 08 and 15.

Seven ticket categories with their own arrival rates and handling times, two worlds
(that automation built, or not), Erlang-C over a stated support window. The ratio
and the model agree at a hundred people. They agree by accident, and the model can
say where the accident ends.

## What this model is, and is not

Erlang-C assumes Poisson arrivals, exponential handling times, no abandonment, and
agents who do nothing but take tickets. Real handling times are more skewed than
that and real agents have projects. So **the shape of the curve is robust and the
exact minutes are not.**

More important: what the drill computes is a **floor**, not a staffing
recommendation. It prices tickets. It does not see project work, maintenance
windows, desk-side interruptions, second-line escalation, extra sites or
after-hours, and a real desk is legitimately larger than its ticket load. Read as
"you are over-staffed", this model is being read wrong — and that is why the ratio
is deliberately absent from the comparison at scale.

Utilisation of 39% does not mean 61% idle. It means 61% of the week is available
for everything else the job contains.

## Why this lab is pure-local

Queueing is arithmetic. The whole argument is seven categories, two worlds and a
formula that has been in capacity planning since 1917. No ticket system, no data
export, no credentials, no `pip install`. Python stdlib, and CI can run it.

## Run it

```bash
python3 cross-cutting/labs/help-desk-queue/queue_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Automation removes tickets faster than it removes work.** Tickets fall
   **39%**, hours of work fall **31%**, and the mean handling time goes **up**,
   21.6 → 24.7 minutes. Password resets are six minutes and permissions questions
   are twenty-two; automation takes the short categories first. A ticket count is
   the single metric that most overstates what you saved.
2. **Wait time bends.** At a hundred people in the automated world:

   | agents | utilisation | p95 wait |
   |---|---|---|
   | 1 | 39% | 84 min |
   | 2 | 20% | 4 min |
   | 3 | 13% | 0 min |

   One more person is **21× better**, not twice better. Queue delay rises
   hyperbolically in utilisation. This is precisely the thing a per-head ratio has
   no way of expressing.
3. **The earlier steps priced in people.** One agent meets the target up to **135**
   people without the automation and **185** with it — the same desk carries 50
   more people, for **8.7** hours a week of ticket work removed. That is what steps
   04, 08 and 15 are worth, stated in the unit the staffing conversation actually
   uses.
4. **At a hundred people the binding constraint is coverage, not volume.** Volume
   needs 1 agent. A 50-hour support window against a 40-hour week needs 2. The
   ratio also says 2 — it lands on the right number without any input that could
   have told it so.
5. **The floor moves with the estate; a ratio cannot.** From **350** people the two
   worlds need different desks: same company, same headcount, different answer
   depending on whether the automation was built. A number derived from headcount
   alone cannot represent that, because the input is not in it.

## Verify (don't take the script's word for it)

```bash
python3 .../queue_drill.py --break-it   # exit 1
```

`--break-it` staffs by the one-per-fifty ratio instead of the queue. Note what does
*not* happen: it does not produce an absurd number. At a hundred people it produces
**the same 2** the model does. Three assertions break anyway, and they are the
interesting ones — the ratio cannot name its binding constraint, cannot say at what
population its answer expires, and returns the same headcount whether or not the
automation exists.

That is the failure worth internalising: **the ratio is not wrong here, it is
unfalsifiable here.** It will keep producing a number long after the number stops
being true, and nothing in it can tell you that has happened.

To go further, set `remaining` to `1.00` for the three automated categories — the
world where steps 04, 08 and 15 were never built. The one-person ceiling falls
185 → 135, and the drill exits `1` with **four** broken assertions rather than
quietly reporting a smaller number. That is correct and worth noticing: four of
this lab's five claims are claims *about the automation*, so deleting it does not
change a figure, it removes the thing being measured. The ratio's answer, of
course, does not move.

## The point

**A staffing number is not a number.** It is a number, the estate it came from, and
the automation it assumed — and only the last two survive contact with the next
question.

Three things to carry out:

- **Never quote the headcount without the two assumptions.** "Two people" is not an
  answer; "two people, at this estate, assuming zero-touch enrolment and automated
  JML" is, because it tells the next person what would change it.
- **Ticket count is the wrong success metric for automation.** Report hours removed
  and the change in mean handling time, or you will claim a 39% win for a 31% one
  and be surprised when the desk does not feel emptier.
- **Know which constraint is binding.** If it is coverage, more volume changes
  nothing until it suddenly changes everything, and the ratio you are using cannot
  see the crossover coming.

## Teardown

None. The drill holds everything in memory and writes nothing.
