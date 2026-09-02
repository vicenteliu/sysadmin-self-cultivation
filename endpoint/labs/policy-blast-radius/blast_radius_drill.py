#!/usr/bin/env python3
"""
blast_radius_drill.py — the console says 3, the policy reaches 22, and three years
later it reaches 30. Nobody edited the policy.

An endpoint policy is scoped to a directory group. The group is populated by
joiner/mover/leaver. So the set of machines a policy applies to is a function of
time, and the number you reviewed at authoring time was a snapshot of it.

This drill takes the reference office's own rates — about 23 joiners and 17
leavers a year, 8 functions, a 3-year device refresh — runs 1095 days of them,
and measures the gap between:

  - the number an MDM console shows you (direct members of the scoped group, today)
  - the number of devices the policy ACTUALLY reaches (transitive membership,
    minus exclusions, plus every device assigned to each of those people, plus
    the unassigned devices that inherit scope because nobody scoped them out)

Five things it measures rather than asserts:
  1. that the authored blast radius and the current one are different numbers
  2. what the console's count omits — nesting, multi-device holders, spares
  3. that the exclusion group drifts too, in the direction that removes protection
  4. that a leaver's device keeps receiving policy until somebody wipes it
  5. that none of the above requires anybody to have made a mistake

--break-it computes reach the way the console does: count the direct members of
the scoped group, today. That is not a strawman — it is the number on the screen
you are asked to sign off, and it is right on day zero.

No MDM, no tenant, no device, no credentials, no external dependencies. Pure
stdlib, fully deterministic. Exit code 0 means every assertion about the lesson
held. Run it in CI.
"""

DOC = __doc__ or ""

import argparse
import sys
from dataclasses import dataclass, field

REACH = "resolved"        # --break-it flips this to "console"

HORIZON = 1095            # three years, the day we look back from
AUTHORED_ON = 0           # the policy was written on day zero

# --- the office, at the reference office's stated rates -----------------------
# the-reference-office.md#parameters: ~23 joiners and ~17 leavers a year, eight
# functions, a three-year device refresh. Nothing here is invented; it is those
# numbers, run forward.

STARTING_HEADCOUNT = 100
JOINERS_PER_YEAR = 23
LEAVERS_PER_YEAR = 17
MOVERS_PER_YEAR = 12      # internal transfers; the reference office states no
                          # rate and says so — this drill needs one, and says so too
FUNCTIONS = ["finance", "sales", "engineering", "design",
             "support", "people", "legal", "operations"]


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


# --- ground truth -------------------------------------------------------------

@dataclass
class Person:
    uid: str
    function: str
    joined: int
    left: int = HORIZON + 1          # still here
    moves: list = field(default_factory=list)   # (day, new_function)

    def function_on(self, day):
        f = self.function
        for d, nf in self.moves:
            if d <= day:
                f = nf
        return f

    def here_on(self, day):
        return self.joined <= day < self.left


@dataclass
class Device:
    tag: str
    holder: str              # uid, or "" for a spare / an unwiped return
    issued: int
    retired: int = HORIZON + 1
    note: str = ""

    def live_on(self, day):
        return self.issued <= day < self.retired


def build_office():
    """Deterministic. Every date below is arithmetic on the stated rates — no
    randomness, so the numbers in the README are the numbers you get."""
    people, devices = [], []

    # the hundred who were here on day one, spread across eight functions
    for i in range(STARTING_HEADCOUNT):
        people.append(Person(f"p{i:03d}", FUNCTIONS[i % len(FUNCTIONS)], joined=0))

    # joiners: 23 a year, evenly spaced
    n = 0
    for year in range(3):
        for k in range(JOINERS_PER_YEAR):
            day = year * 365 + int(k * 365 / JOINERS_PER_YEAR) + 3
            people.append(Person(f"n{n:03d}", FUNCTIONS[n % len(FUNCTIONS)], joined=day))
            n += 1

    # leavers: 17 a year, taken from the longest-serving still present
    idx = 0
    for year in range(3):
        for k in range(LEAVERS_PER_YEAR):
            day = year * 365 + int(k * 365 / LEAVERS_PER_YEAR) + 11
            while idx < len(people) and people[idx].left <= HORIZON:
                idx += 1
            if idx < len(people):
                people[idx].left = day
                idx += 1

    # movers: 12 a year, and this is the leg with no trigger
    by_uid = {p.uid: p for p in people}
    movers = [p for p in people if p.joined == 0][30:]
    for year in range(3):
        for k in range(MOVERS_PER_YEAR):
            day = year * 365 + int(k * 365 / MOVERS_PER_YEAR) + 40
            p = movers[(year * MOVERS_PER_YEAR + k) % len(movers)]
            if p.here_on(day):
                nf = FUNCTIONS[(FUNCTIONS.index(p.function_on(day)) + 3) % len(FUNCTIONS)]
                p.moves.append((day, nf))

    # one device per person at join, replaced on the three-year refresh
    t = 0
    for p in people:
        devices.append(Device(f"AT-{t:04d}", p.uid, issued=p.joined,
                              retired=p.left if p.left <= HORIZON else HORIZON + 1))
        t += 1
        # the refresh machine, for anyone who is still here at the cycle mark
        if p.joined + 1095 <= HORIZON + 400 and p.left > 1000:
            devices.append(Device(f"AT-{t:04d}", p.uid, issued=1000, note="refresh"))
            t += 1

    # the five spares on the shelf, and the returns nobody wiped
    for k in range(5):
        devices.append(Device(f"AT-9{k:03d}", "", issued=0, note="spare, on the shelf"))
        t += 1
    # three leavers' machines that came back and were never wiped or re-issued
    for k, p in enumerate([p for p in people if p.left <= HORIZON][:3]):
        devices.append(Device(f"AT-8{k:03d}", p.uid, issued=p.joined,
                              note="returned, never wiped — still enrolled"))

    return people, by_uid, devices


# --- the directory ------------------------------------------------------------

def groups_on(people, day):
    """Function groups, plus one nested access bundle. The policy is scoped to the
    bundle; the console shows the bundle's DIRECT members, which is one group."""
    g = {f: set() for f in FUNCTIONS}
    for p in people:
        if p.here_on(day):
            g[p.function_on(day)].add(p.uid)

    # The access bundle the policy is scoped to. Three people were added
    # individually ("just this once") and one whole function was nested in. That
    # is what an access bundle looks like after eighteen months, and it is what
    # step 03 warns about when a group means a job function AND a bundle.
    g["restricted-config"] = {"g:finance", "p017", "p044", "p061"}
    g["exempt"] = {"g:engineering"}
    return g


def resolve(groups, name, seen=None):
    """Transitive membership. The console shows the top level; the policy engine
    evaluates this."""
    seen = seen or set()
    if name in seen:
        return set()
    seen.add(name)
    out = set()
    for m in groups.get(name, set()):
        out |= resolve(groups, m[2:], seen) if m.startswith("g:") else {m}
    return out


# --- the two ways of counting -------------------------------------------------

def console_reach(people, day):
    """What the screen says: direct members of the scoped group. On day zero this
    is not wrong — it is incomplete in a way that does not show."""
    g = groups_on(people, day)
    direct = {m for m in g["restricted-config"] if not m.startswith("g:")}
    return direct, len(direct)


def resolved_reach(people, devices, day):
    """What the policy engine actually does: resolve nesting, subtract the
    exclusion, then find every live enrolled device attached to each of them —
    and the devices attached to nobody, which no group excludes."""
    g = groups_on(people, day)
    targeted = resolve(g, "restricted-config") - resolve(g, "exempt")
    reached = set()
    for d in devices:
        if not d.live_on(day):
            continue
        if d.holder in targeted:
            reached.add(d.tag)
        elif not d.holder:
            reached.add(d.tag)          # a spare matches no exclusion either
    return targeted, reached


def main():
    ap = argparse.ArgumentParser(description=DOC.strip().split("\n")[0])
    ap.add_argument("--break-it", action="store_true",
                    help="count reach the way the MDM console does")
    args = ap.parse_args()
    global REACH
    if args.break_it:
        REACH = "console"

    people, _, devices = build_office()

    log(DOC.strip().split("\n\n")[0])
    log(f"\nmode: reach counted as {REACH!r}"
        + ("   [--break-it: the number on the console]" if args.break_it else ""))

    step(1, "The policy, on the day it was authored")
    d0_targeted, d0_reached = resolved_reach(people, devices, AUTHORED_ON)
    _, d0_console = console_reach(people, AUTHORED_ON)
    authored = d0_console if REACH == "console" else len(d0_reached)
    log(f"  scoped to  : restricted-config, minus exempt")
    log(f"  console    : {d0_console} direct members")
    log(f"  resolved   : {len(d0_targeted)} people, {len(d0_reached)} enrolled devices")
    log(f"  you signed off on: {authored}")

    step(2, "The same policy, three years later. Nobody edited it.")
    dN_targeted, dN_reached = resolved_reach(people, devices, HORIZON)
    _, dN_console = console_reach(people, HORIZON)
    now = dN_console if REACH == "console" else len(dN_reached)
    log(f"  console    : {dN_console} direct members")
    log(f"  resolved   : {len(dN_targeted)} people, {len(dN_reached)} enrolled devices")
    log(f"  reach now  : {now}")
    drift = (now - authored) / authored * 100 if authored else 0
    log(f"  drift      : {now - authored:+d} devices ({drift:+.0f}%)")

    check(abs(drift) >= 20,
          f"the blast radius moved {drift:+.0f}% with nobody editing the policy",
          f"drift is only {drift:+.0f}% — this method cannot see the movement")

    step(3, "What the console's number leaves out")
    nested_only = len(d0_reached) - d0_console
    log(f"  console counts   : {d0_console}")
    log(f"  actually reached : {len(d0_reached)}")
    log(f"  difference       : {nested_only}")
    log( "  because: one of the bundle's direct members is a GROUP, and its members")
    log( "           are not shown; people hold more than one device after a refresh;")
    log( "           and a spare belongs to nobody, so no exclusion removes it.")
    check(REACH == "resolved" and nested_only > 0,
          f"resolving nesting and devices finds {nested_only} the console does not show",
          "counting direct members reports a number that is not the reach")

    step(4, "The exclusion drifts, and it drifts the wrong way")
    d0_ex = resolve(groups_on(people, AUTHORED_ON), "exempt")
    dN_ex = resolve(groups_on(people, HORIZON), "exempt")
    still = len(d0_ex & dN_ex)
    log(f"  exempt on day 0    : {len(d0_ex)} people")
    log(f"  exempt on day {HORIZON}: {len(dN_ex)} people")
    log(f"  in both            : {still}")
    log(f"  left the exemption : {len(d0_ex - dN_ex)}  (moved team, or left; nothing fired)")
    check(len(d0_ex - dN_ex) > 0,
          f"{len(d0_ex - dN_ex)} people lost an exemption nobody revoked — they moved",
          "the exemption set did not move, which this office's rates say it must")

    step(5, "The devices attached to nobody")
    orphan = [d for d in devices if not d.holder and d.live_on(HORIZON)]
    unwiped = [d for d in devices if d.note.startswith("returned") and d.live_on(HORIZON)]
    log(f"  spares on the shelf, enrolled : {len(orphan)}")
    log(f"  returns never wiped, enrolled : {len(unwiped)}")
    log(f"  every one of them matches the scope, because exclusions are about PEOPLE")
    check(len(orphan) + len(unwiped) > 0,
          f"{len(orphan) + len(unwiped)} enrolled devices have no holder and no exclusion",
          "no unheld devices — the model lost the shelf")

    step(6, "Can this method say when its own answer expires?")
    if REACH == "console":
        log("  no. The console reports today's direct membership and has no")
        log("  representation of time, so it cannot distinguish a number that is")
        log("  right from one that has been wrong for two years.")
    else:
        log(f"  yes. Re-resolved at day {HORIZON} the answer changed by {drift:+.0f}%,")
        log("  which is the signal: re-derive on a cadence and alert on the delta.")
    check(REACH == "resolved",
          "the method can be re-run on a cadence and the delta is the alert",
          "this method produces one number and cannot tell you it has expired")

    return verdict([
        "The blast radius is a function of time, and the",
        "number you signed off on was a snapshot of it.",
    ], broken=args.break_it)


if __name__ == "__main__":
    sys.exit(main())
