#!/usr/bin/env python3
"""
mitigate_drill.py — mitigating first saves 9 minutes of mean downtime and costs 6 in
the tail, and the model can say exactly where the advice stops being true.

`incident-response.md` calls this "the one instinct that separates seniors": stop the
bleeding first, find the cause afterwards. That is a claim about outcomes, so it can
be measured rather than asserted — and the measurement is worth more than the slogan,
because **the instinct is not a law and the model finds its edge.**

Six causes with prior probabilities, each with a time to diagnose and a time to fix
once known. One generic mitigation — the failover, the rollback, the restart — that is
available immediately, works for some causes and not others, and occasionally makes
things worse.

Five things this drill measures rather than asserts:
  1. expected downtime under diagnose-first and under mitigate-first
  2. the TAIL, which moves the OTHER way — and by exactly the mitigation window
  3. the crossover: at what generic-mitigation success rate the advice inverts
  4. what a risky mitigation does to the answer — the case the slogan omits
  5. that adding responders stops helping, and where the incident commander comes in

--break-it runs diagnose-first, which is not a strawman. It is what a careful engineer
does, it is defensible in every post-mortem, and it is what you will do under pressure
unless you have decided otherwise in advance.

No systems, no services, no credentials, no external dependencies. Pure stdlib and
fully deterministic — every number is an exact expectation over the cause distribution,
not a simulation. Exit code 0 means every assertion about the lesson held.
"""

import argparse
import sys
from dataclasses import dataclass

STRATEGY = "mitigate-first"    # --break-it flips this to "diagnose-first"

# The generic mitigation: failover, roll back, restart. Available at minute zero.
MITIGATION_MINUTES = 6          # how long it takes to apply
MITIGATION_MAKES_IT_WORSE = 0.0  # probability it costs you; raised in step 4


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


@dataclass
class Cause:
    name: str
    prior: float          # how often this is what it turns out to be
    diagnose: int         # minutes to identify it, from the symptom
    fix: int              # minutes to apply the real fix once identified
    generic_works: bool   # does failover/rollback/restart restore service?


# A plausible spread for one service. The point is not these exact numbers; it is that
# the two strategies are compared over the SAME distribution, and that the crossover
# below is computed rather than assumed.
CAUSES = [
    Cause("bad deploy",            0.30,  8,  4, True),
    Cause("dependency degraded",   0.20, 14,  9, True),
    Cause("resource exhaustion",   0.18, 11, 12, True),
    Cause("expired certificate",   0.12,  9,  5, False),
    Cause("data / migration bug",  0.12, 26, 34, False),
    Cause("network path change",   0.08, 22, 16, True),
]


def downtime_diagnose_first(c: Cause) -> int:
    """Understand it, then fix it. Service is down for the whole of both."""
    return c.diagnose + c.fix


def downtime_mitigate_first(c: Cause, mitigation_minutes=MITIGATION_MINUTES) -> int:
    """Apply the generic mitigation immediately.

    If it works, the customer-visible incident ends there — diagnosis and the real fix
    still happen, but not on the clock that matters. If it does not, you have spent the
    mitigation window and still have the whole diagnose-and-fix ahead."""
    if c.generic_works:
        return mitigation_minutes
    return mitigation_minutes + c.diagnose + c.fix


def expected(fn, **kw):
    return sum(c.prior * fn(c, **kw) for c in CAUSES)


def worst(fn, **kw):
    return max(fn(c, **kw) for c in CAUSES)


def coverage():
    return sum(c.prior for c in CAUSES if c.generic_works)


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").strip().split("\n")[0])
    ap.add_argument("--break-it", action="store_true",
                    help="diagnose first — understand the problem before acting on it")
    args = ap.parse_args()
    global STRATEGY
    if args.break_it:
        STRATEGY = "diagnose-first"

    log((__doc__ or "").strip().split("\n\n")[0])
    log(f"\nstrategy: {STRATEGY}"
        + ("   [--break-it: what a careful engineer does]" if args.break_it else ""))

    ed = expected(downtime_diagnose_first)
    em = expected(downtime_mitigate_first)
    mine = ed if STRATEGY == "diagnose-first" else em

    step(1, "Expected customer-visible downtime")
    log(f"  the generic mitigation covers {coverage() * 100:.0f}% of causes by probability")
    log(f"  diagnose-first : {ed:5.1f} min")
    log(f"  mitigate-first : {em:5.1f} min")
    log(f"  this strategy  : {mine:5.1f} min")
    check(STRATEGY == "mitigate-first",
          f"mitigating first saves {ed - em:.0f} minutes of mean downtime",
          f"diagnose-first spends {ed - em:.0f} more minutes with the service down, "
          f"every incident, on average")

    step(2, "The tail — and the trade the slogan does not mention")
    wd, wm = worst(downtime_diagnose_first), worst(downtime_mitigate_first)
    log(f"  worst case, diagnose-first : {wd} min")
    log(f"  worst case, mitigate-first : {wm} min   ({wm - wd:+d})")
    log("")
    log("  Mitigating first buys the MEAN and pays for it in the TAIL, and the price")
    log(f"  is exactly the mitigation window: {MITIGATION_MINUTES} minutes spent on a cause the")
    log("  generic mitigation was never going to cover. The worst incident you will")
    log("  have is, by definition, one of those.")
    log("")
    log("  That is a real trade and it is the right way round: you take a small,")
    log("  bounded, KNOWN cost on the rare incident to remove a large one from every")
    log("  common incident. A slogan that only mentioned the win would be selling.")
    check(wm - wd == MITIGATION_MINUTES,
          f"the tail costs exactly the mitigation window, {MITIGATION_MINUTES} minutes — bounded and known",
          f"the tail moved by {wm - wd:+d} rather than by the mitigation window, "
          f"so the cost of guessing wrong is not bounded by what you spent guessing")

    step(3, "Where the advice inverts — the crossover")
    log("  Vary how much of the probability mass the generic mitigation covers, and")
    log("  find where mitigate-first stops winning.")
    log("")
    log("   coverage   diagnose-first   mitigate-first   better")
    crossover = None
    for pct in range(0, 101, 10):
        # rebuild the same distribution with `pct` of the mass covered by the mitigation
        mass, covered = 0.0, []
        for c in CAUSES:
            covered.append(mass < pct / 100.0 - 1e-9)
            mass += c.prior
        em_p = sum(c.prior * (MITIGATION_MINUTES if cov
                              else MITIGATION_MINUTES + c.diagnose + c.fix)
                   for c, cov in zip(CAUSES, covered))
        better = "mitigate" if em_p < ed else "diagnose"
        if crossover is None and better == "mitigate":
            crossover = pct
        log(f"   {pct:>6}%   {ed:>13.1f}   {em_p:>14.1f}   {better}")
    log("")
    log(f"  crossover: the generic mitigation has to cover about {crossover}% of causes")
    log("  before mitigating first is the better call.")
    check(crossover is not None and 0 < crossover < 100,
          f"the answer is falsifiable — it inverts below about {crossover}% coverage",
          "no crossover found, which would make this advice unfalsifiable rather than true")

    step(4, "The case the slogan leaves out — a mitigation that can make it worse")
    log("  A failover that flaps, a rollback that corrupts, a restart that loses the")
    log("  queue. Model it as an extra penalty when the mitigation is attempted.")
    log("")
    log("   penalty   mitigate-first   vs diagnose-first")
    flip = None
    for penalty in (0, 5, 10, 15, 20, 25, 30):
        em_p = expected(downtime_mitigate_first) + penalty
        call = "still better" if em_p < ed else "WORSE"
        if flip is None and em_p >= ed:
            flip = penalty
        log(f"   {penalty:>5} min   {em_p:>14.1f}   {call}")
    log("")
    log(f"  a mitigation that costs more than about {flip} minutes when it goes wrong")
    log("  is not a mitigation. That is the sentence the slogan omits, and it is why")
    log("  the rehearsed failovers in the backup and database chapters matter: they")
    log("  are what makes this penalty small enough to ignore.")
    check(flip is not None,
          f"the instinct depends on a cheap mitigation, and inverts past ~{flip} minutes of risk",
          "no penalty inverts the answer, which would mean the mitigation's risk is free")

    step(5, "Why the incident commander is not overhead")
    log("  Responders do not add linearly: each one has to be told what is known, and")
    log("  the telling comes out of the same minutes as the fixing. Model coordination")
    log("  as a share of each responder's time that grows with the group.")
    log("")
    log("   responders   effective   time-to-mitigate")
    best_n, best_t = 1, float("inf")
    for n in range(1, 7):
        overhead = 0.12 * (n - 1)              # stated, not derived — see the README
        effective = n * max(0.0, 1 - overhead)
        t = MITIGATION_MINUTES / effective if effective else float("inf")
        if best_t is None or t < best_t:
            best_n, best_t = n, t
        log(f"   {n:>10}   {effective:>9.2f}   {t:>13.1f} min")
    log("")
    log(f"  adding responders stops paying after about {best_n}. What buys more after")
    log("  that is not another pair of hands — it is taking the coordination out of")
    log("  the responders' minutes, which is the whole job description of an IC.")
    check(best_n < 6,
          f"more hands stop helping at about {best_n} responders, which is what the IC role fixes",
          "responders scale linearly here, which no incident has ever done")

    return verdict([
        "Mitigate before you diagnose — and now you can say",
        "under what conditions that stops being true, which is the part worth having.",
    ], broken=args.break_it)


if __name__ == "__main__":
    sys.exit(main())
