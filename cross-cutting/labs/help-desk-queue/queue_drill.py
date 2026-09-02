#!/usr/bin/env python3
"""
queue_drill.py — "one per fifty users" is a linear sentence about a non-linear
system, and it happens to be right here for a reason it cannot state.

Step 13 asks how many people a hundred-person office needs on the service desk.
The usual answer is a ratio. This models the queue instead: seven categories with
their own arrival rates and handling times, two worlds (the automation of steps
04, 08 and 15 built, or not), and Erlang-C over the support window.

Four things it measures rather than asserts:
  1. that automation removes TICKETS faster than it removes WORK, and raises the
     mean handling time of everything left
  2. how sharply wait time bends as utilisation rises — the thing a ratio cannot
     express
  3. what the earlier steps bought, stated as headroom: the population one person
     can carry before the target breaks
  4. which constraint is actually binding at 100 people — and it is not volume

WHAT THIS MODEL IS NOT. Erlang-C assumes Poisson arrivals, exponential handling
times, no abandonment, and agents who do nothing but take tickets. Real handling
times are more skewed than exponential and real agents have projects. So:
**the shape of the curve is robust and the exact minutes are not.** Utilisation
below 1 does not mean idle — it means time available for everything else the job
contains, which is where the project work lives. A queue model that is read as
"you are over-staffed" is being read wrong; it bounds the ticket load only.

No ticket system, no data export, no credentials, no external dependencies. Pure
stdlib. Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import math
import sys
from dataclasses import dataclass

METHOD = "queue"          # --break-it flips this to "ratio"

SUPPORT_HOURS_PER_WEEK = 50.0    # 08:00-18:00, Mon-Fri, stated rather than assumed
ONE_PERSON_HOURS = 40.0
P95_TARGET_HOURS = 4.0           # "answered the same working day"
RATIO_USERS_PER_AGENT = 50       # the rule this lab is arguing with


# --- the reporter — vendored, byte for byte, in every drill (ADR-0017) ------------
# check.py holds the canonical copy and fails a drill whose copy differs. Change it
# there and then everywhere; a drill imports nothing from this repo.

FAILURES = []


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


def check(cond, ok_msg, fail_msg):
    if cond:
        log(f"  ✓ {ok_msg}")
    else:
        log(f"  ✗ {fail_msg}")
        FAILURES.append(fail_msg)
    return cond


def verdict(held, broken=False):
    """What main() returns: 1 with every failure listed, or 0 with the lessons that
    held — one line each, in the drill's own words."""
    log("\n" + "=" * 70)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        if broken:
            log("\nThat is the point of --break-it. Re-run without it.")
        return 1
    log("PASSED — the lessons held:")
    for line in held:
        log(line)
    return 0

# --- end of the reporter ------------------------------------------------------------


# --- the estate --------------------------------------------------------------

@dataclass
class Category:
    name: str
    per_week_100: float   # tickets per week per 100 people, before automation
    minutes: float        # mean handling time
    removed_by: str       # which build-out step automates it away
    remaining: float      # fraction left once that step is built


CATEGORIES = [
    Category("password / unlock",     25, 6,  "08 identity + self-service", 0.12),
    Category("enrolment / imaging",    6, 50, "04 zero-touch devices",      0.17),
    Category("joiner / mover / leaver", 5, 35, "15 automated JML",          0.20),
    Category("access / permissions",  18, 22, "—",                          1.00),
    Category("remote connectivity",   10, 25, "—",                          1.00),
    Category("hardware",               7, 45, "—",                          1.00),
    Category("rooms / AV",             8, 15, "—",                          1.00),
]


def load(population, automated):
    """Tickets per week and mean handling time, for a population and a world."""
    scale = population / 100.0
    tickets = work_min = 0.0
    for c in CATEGORIES:
        n = c.per_week_100 * scale * (c.remaining if automated else 1.0)
        tickets += n
        work_min += n * c.minutes
    return tickets, work_min / 60.0, (work_min / tickets if tickets else 0.0)


# --- the queue ---------------------------------------------------------------

def erlang_b(c, a):
    b = 1.0
    for n in range(1, c + 1):
        b = (a * b) / (n + a * b)
    return b


def erlang_c(c, a):
    """Probability an arriving ticket has to wait at all."""
    b = erlang_b(c, a)
    denom = 1.0 - (a / c) * (1.0 - b)
    return b / denom if denom > 0 else 1.0


def p95_wait_hours(tickets_per_week, mean_minutes, agents):
    """The wait 95% of tickets beat. None if the queue is unstable."""
    lam = tickets_per_week / SUPPORT_HOURS_PER_WEEK          # arrivals per hour
    svc = mean_minutes / 60.0                                # hours per ticket
    a = lam * svc                                            # offered load, erlangs
    if agents <= a:
        return None                                          # never drains
    mu = 1.0 / svc
    pc = erlang_c(agents, a)
    drain = agents * mu - lam
    if pc <= 0.05:
        return 0.0
    return math.log(pc / 0.05) / drain


def utilisation(tickets_per_week, mean_minutes, agents):
    lam = tickets_per_week / SUPPORT_HOURS_PER_WEEK
    return (lam * (mean_minutes / 60.0)) / agents


def volume_minimum(population, automated):
    """Fewest agents whose p95 wait meets the target. Volume only."""
    t, _, m = load(population, automated)
    for c in range(1, 21):
        w = p95_wait_hours(t, m, c)
        if w is not None and w <= P95_TARGET_HOURS:
            return c
    return None


def coverage_minimum():
    """A support window wider than one person's week is a second person, not a
    rota. Step 13 says this in one line; it is arithmetic, not preference.

    Note what this does NOT add: a third for the bus factor. At this size a bus
    factor of one is usually unavoidable, and step 13's position is that naming it
    is worth more than staffing it away."""
    return math.ceil(SUPPORT_HOURS_PER_WEEK / ONE_PERSON_HOURS)


def one_person_ceiling(automated):
    """The population at which one agent stops meeting the target."""
    p = 20
    while p <= 2000:
        if volume_minimum(p, automated) != 1:
            return p
        p += 5
    return None


def desk_floor(population, automated):
    """The FLOOR that the ticket load and the support window together imply —
    (headcount, what is binding, the one-person ceiling).

    Not a staffing recommendation, and that distinction is the whole reason
    this is safe to publish. The model sees tickets. It does not see project
    work, maintenance windows, desk-side interruptions, second-line
    escalation, extra sites or after-hours. A real desk is legitimately
    larger than this floor. What a floor can do, and a ratio cannot, is move
    when the estate moves."""
    if METHOD == "ratio":
        # --break-it: the industry default. It reads the headcount and nothing else.
        return math.ceil(population / RATIO_USERS_PER_AGENT), "ratio", None
    v, c = volume_minimum(population, automated), coverage_minimum()
    return max(v, c), ("volume" if v > c else "coverage"), one_person_ceiling(automated)


# --- the drill ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", action="store_true",
                    help="staff by the one-per-fifty ratio instead of the queue — "
                         "the industry default. The drill must FAIL.")
    a = ap.parse_args()

    global METHOD
    if a.break_it:
        METHOD = "ratio"
        log(f"!! running with --break-it: staffing by ratio "
            f"(1 per {RATIO_USERS_PER_AGENT} users)\n")

    POP = 100
    t_man, h_man, m_man = load(POP, automated=False)
    t_aut, h_aut, m_aut = load(POP, automated=True)

    step(1, "Automation removes tickets faster than it removes work")
    log(f"  {'category':<26} {'before':>8} {'after':>8}  {'min each':>9}  removed by")
    log(f"  {'-'*26} {'-'*8} {'-'*8}  {'-'*9}  {'-'*24}")
    for c in CATEGORIES:
        log(f"  {c.name:<26} {c.per_week_100:>8.0f} "
            f"{c.per_week_100 * c.remaining:>8.1f}  {c.minutes:>9.0f}  {c.removed_by}")
    log(f"\n  tickets / week        {t_man:>8.0f} {t_aut:>8.0f}   "
        f"({(t_aut/t_man - 1) * 100:+.0f}%)")
    log(f"  hours of work / week  {h_man:>8.1f} {h_aut:>8.1f}   "
        f"({(h_aut/h_man - 1) * 100:+.0f}%)")
    log(f"  mean handling (min)   {m_man:>8.1f} {m_aut:>8.1f}   "
        f"({(m_aut/m_man - 1) * 100:+.0f}%)")

    drop_t = 1 - t_aut / t_man
    drop_h = 1 - h_aut / h_man
    check(drop_h < drop_t,
          f"tickets fall {drop_t*100:.0f}% and work falls only {drop_h*100:.0f}%. "
          "Automation takes the SHORT categories first — a password reset is six "
          "minutes and a permissions question is twenty-two — so a ticket count is "
          "the one metric that overstates what you saved",
          "work fell at least as fast as ticket count; the fixture cannot show that "
          "tickets are not work")
    check(m_aut > m_man,
          f"and the mean handling time goes UP, {m_man:.1f} → {m_aut:.1f} minutes. "
          "What is left needed judgement all along; the queue got smaller and "
          "qualitatively harder at the same time",
          "mean handling time did not rise; the residual mix is not harder")

    step(2, "Wait time bends; a ratio is a straight line")
    log(f"  automated world, {POP} people, target p95 ≤ {P95_TARGET_HOURS:.0f}h\n")
    log(f"  {'agents':>7}  {'utilisation':>12}  {'p95 wait':>10}")
    log(f"  {'-'*7}  {'-'*12}  {'-'*10}")
    waits = {}
    for c in (1, 2, 3):
        w = p95_wait_hours(t_aut, m_aut, c)
        waits[c] = w
        u = utilisation(t_aut, m_aut, c)
        log(f"  {c:>7}  {u:>11.0%}  {('unstable' if w is None else f'{w*60:>7.0f} min'):>10}")
    check(waits[1] is not None and waits[2] is not None and waits[1] > 4 * waits[2],
          f"one agent to two takes p95 from {waits[1]*60:.0f} to {waits[2]*60:.0f} "
          f"minutes — {waits[1]/waits[2]:.0f}× better for one more person, because "
          "queue delay rises hyperbolically in utilisation, not linearly. This is "
          "the whole reason a ratio cannot be the argument",
          "the second agent did not produce a disproportionate improvement; the "
          "non-linearity is not visible in this fixture")
    log("\n  ⚠ utilisation here is ticket time only. 40% is not 60% idle — it is the")
    log("     room the projects, the maintenance and the interruptions live in.")

    step(3, "What steps 04, 08 and 15 bought, in people")
    ceil_man, ceil_aut = one_person_ceiling(False), one_person_ceiling(True)
    log(f"  one agent meets the target up to ...")
    log(f"    without the automation : {ceil_man} people")
    log(f"    with it                : {ceil_aut} people")
    log(f"  hours of ticket work removed per week: {h_man - h_aut:.1f}")
    check(ceil_man is not None and ceil_aut is not None and ceil_aut > ceil_man,
          f"the automation moves the one-person ceiling from {ceil_man} to {ceil_aut} "
          f"people — {ceil_aut - ceil_man} more people carried by the same desk. "
          "That is what the earlier steps are worth, stated in the unit the "
          "staffing conversation actually uses",
          "the automation did not move the ceiling; the earlier steps cannot be "
          "priced this way")

    step(4, "Which constraint is actually binding at 100 people")
    n_aut, bind_aut, ceil_reported = desk_floor(POP, automated=True)
    n_man, bind_man, _ = desk_floor(POP, automated=False)
    v_aut, cov = volume_minimum(POP, True), coverage_minimum()
    ratio_says = math.ceil(POP / RATIO_USERS_PER_AGENT)
    log(f"  volume needs   : {v_aut} agent(s)")
    log(f"  coverage needs : {cov} agents  "
        f"({SUPPORT_HOURS_PER_WEEK:.0f}h window > {ONE_PERSON_HOURS:.0f}h week, "
        "plus one person is a bus factor of one)")
    log(f"  floor          : {n_aut}, binding constraint = {bind_aut}")
    log(f"  the ratio says : {ratio_says}")
    check(bind_aut == "coverage",
          f"at this size the queue does not set the number — coverage does. The "
          f"ratio lands on the same {ratio_says}, for a reason it cannot state, "
          "which is why it cannot tell you where it stops landing there",
          f"the binding constraint came back as {bind_aut!r} rather than coverage — "
          "either volume binds at this size (and the lab's central claim fails in "
          "its own fixture) or the method has no concept of a binding constraint "
          "at all")
    check(ceil_reported is not None,
          f"and the method can say where its own answer expires: one agent to "
          f"{ceil_reported} people. A number that knows its own range is a "
          "different kind of object from a number that does not",
          "the method cannot name the population at which its answer changes — it "
          "has no model of the estate, so it cannot warn you when it has gone stale")

    step(5, "The floor moves with the estate. A ratio cannot.")
    log("  the same company, at each size, in both worlds:\n")
    log(f"  {'people':>7}  {'automated':>10}  {'manual':>7}")
    log(f"  {'-'*7}  {'-'*10}  {'-'*7}")
    diverged = []
    for p in range(100, 601, 50):
        na, _, _ = desk_floor(p, True)
        nm, _, _ = desk_floor(p, False)
        flag = "  ← differ" if na != nm else ""
        log(f"  {p:>7}  {na:>10}  {nm:>7}{flag}")
        if na != nm:
            diverged.append(p)
    first = diverged[0] if diverged else None
    log("\n  ⚠ the ratio is deliberately not a column here. Set against a FLOOR")
    log("     at scale it would read as 'you are over-staffed', and this model")
    log("     cannot support that — it prices tickets, and a desk is legitimately")
    log("     larger than its ticket load. The narrower claim is the one that")
    log("     survives: the floor responds to the estate; a headcount ratio has")
    log("     no input that could make it respond.")
    check(first is not None,
          f"the two worlds need different desks from {first} people onward — same "
          "company, same headcount, different answer depending on whether steps 04, "
          "08 and 15 were built. A number derived from headcount alone cannot "
          "represent that, because the input is not in it",
          "the automated and manual worlds never differ at any size — a staffing "
          "method that cannot tell them apart is not reading the estate")

    # --- verdict -------------------------------------------------------------
    return verdict([
        "  1. Ticket count is the metric that most overstates what automation saved.",
        "     The short categories go first, so the queue shrinks and the mean",
        "     handling time rises at the same time.",
        "  2. Wait time bends. Two agents are not twice one, and that is exactly",
        "     what a per-head ratio has no way of saying.",
        "  3. The earlier steps can be priced in people: they move the population",
        "     one desk can carry. That is the sentence step 04 was waiting for.",
        "  4. At a hundred people the binding constraint is coverage, not volume.",
        "     The ratio agrees by arithmetic accident, and it cannot tell you when",
        "     it stopped agreeing, because the estate is not one of its inputs.",
        "\n  A staffing number is not a number. It is a number, the estate it came",
        "  from, and the automation it assumed — and only the last two survive",
        "  contact with the next question.",
    ], broken=a.break_it)


if __name__ == "__main__":
    sys.exit(main())
