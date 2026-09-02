#!/usr/bin/env python3
"""
silence_drill.py — prove, in your own hands, the failure chapter 06 warns about and
that no dashboard is shaped to show: **the outage that produces silence instead of a
page.**

Every alert in a normal monitoring stack is a predicate over data that arrived. That
is a sound design and it has one blind spot, which is the case where no data arrives:

    a threshold alert    fires when a number crosses a line
    no data              is not a number, so it crosses nothing
    a monitor inside     the failure domain it watches stops sending at the same
                         instant its target stops serving

So the estate that most needs to page you is the estate that goes quiet, and quiet is
indistinguishable from healthy in every UI ever built — green is the colour of both.

The drill runs one hour of an incident three ways and counts who was paged, when, and
by what. No cloud, no credentials, no dependencies. Pure Python stdlib. Exit code 0
means every assertion about the lesson held. Run it in CI.

    python3 silence_drill.py
    python3 silence_drill.py --break-it no-data-is-green
    python3 silence_drill.py --break-it cause-alerts-suffice
"""

import argparse
import sys

SABOTAGE = None
MINUTES = 60
OUTAGE_AT = 12          # the rack loses power at minute 12
SLO_BURN_AT = 14        # user-visible errors are unmistakable two minutes later


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


# --------------------------------------------------------------------------
# The estate. Two monitors watch the same service; one of them lives on the
# rack it is watching, which is the only difference between them.
# --------------------------------------------------------------------------

class Monitor:
    def __init__(self, name, domain, kind):
        self.name = name
        self.domain = domain     # the failure domain the monitor itself runs in
        self.kind = kind         # "cause" | "symptom"


SERVICE_DOMAIN = "rack-a"

MONITORS = [
    Monitor("cpu-in-rack",      "rack-a", "cause"),
    Monitor("errors-in-rack",   "rack-a", "symptom"),
    Monitor("errors-off-rack",  "rack-b", "symptom"),
]


def sample(monitor, minute):
    """What this monitor reports at this minute. `None` means no sample arrived —
    which is a different thing from a sample whose value is fine, and the entire
    subject of this drill."""
    monitor_is_dead = monitor.domain == SERVICE_DOMAIN and minute >= OUTAGE_AT
    if monitor_is_dead:
        return None
    if monitor.kind == "cause":
        # CPU on a healthy service is unremarkable, and on a dead one is unreported.
        return 0.35
    if SABOTAGE == "cause-alerts-suffice":
        # The sabotage: an estate that alerts on resources and calls it observability.
        # Every monitor now measures something that does not move when users suffer.
        return 0.001
    # A symptom monitor outside the domain sees the errors the users see.
    return 1.0 if minute >= SLO_BURN_AT else 0.001


def threshold_alert(monitor, minute):
    """The ordinary alert: a predicate over a value. It never sees a `None`, because
    there is nothing to evaluate."""
    v = sample(monitor, minute)
    if v is None:
        if SABOTAGE == "no-data-is-green":
            return False
        return False        # the honest model: absence is not a threshold crossing
    if monitor.kind == "cause":
        return v > 0.90
    return v > 0.05


def staleness_alert(monitor, minute, tolerance=3):
    """The dead-man's switch: fires on the ABSENCE of samples. It is the only
    predicate in this file whose input is not a value."""
    if SABOTAGE == "no-data-is-green":
        return False        # the sabotage: treat silence as health, as a UI does
    recent = [sample(monitor, m) for m in range(max(0, minute - tolerance), minute + 1)]
    return all(v is None for v in recent) and minute > tolerance


def first_page(predicate):
    for m in range(MINUTES):
        if predicate(m):
            return m
    return None


def run():
    log(__doc__.strip().split("\n\n")[0])

    cpu, in_rack, off_rack = MONITORS

    # ---------------------------------------------------------------- 1
    step(1, "Minute 12: rack-a loses power. What each monitor reports at minute 20.")
    for mon in MONITORS:
        v = sample(mon, 20)
        shown = "no sample" if v is None else f"{v}"
        log(f"  {mon.name:<17} (runs in {mon.domain}, {mon.kind:<7}) -> {shown}")
    check(sample(in_rack, 20) is None,
          "the in-rack monitor stopped sending at the instant its target died — it "
          "shared the failure domain it was watching (LESSON 1)",
          "the in-rack monitor kept reporting after its own domain died")
    check(sample(off_rack, 20) == 1.0,
          "the off-rack monitor is reporting the errors users are actually seeing "
          "(LESSON 1b)",
          "the off-rack monitor is not measuring anything a user would notice")

    # ---------------------------------------------------------------- 2
    step(2, "Who got paged, and when")
    rows = [
        ("cpu-in-rack",     "threshold", first_page(lambda m: threshold_alert(cpu, m))),
        ("errors-in-rack",  "threshold", first_page(lambda m: threshold_alert(in_rack, m))),
        ("errors-off-rack", "threshold", first_page(lambda m: threshold_alert(off_rack, m))),
        ("errors-in-rack",  "staleness", first_page(lambda m: staleness_alert(in_rack, m))),
    ]
    for name, kind, when in rows:
        log(f"  {name:<17} {kind:<10} -> "
            + ("never fired" if when is None else f"paged at minute {when}"))
    in_rack_thr = rows[1][2]
    off_rack_thr = rows[2][2]
    in_rack_stale = rows[3][2]
    check(in_rack_thr is None,
          "the in-rack error alert NEVER FIRED — it is a predicate over data, and no "
          "data arrived (LESSON 2)",
          "the in-rack threshold alert fired despite receiving no samples")
    check(off_rack_thr == SLO_BURN_AT,
          f"the off-rack symptom alert paged at minute {off_rack_thr} — monitoring from "
          "outside the thing it watches is the whole of why (LESSON 3)",
          "the off-rack symptom alert did not page when users saw errors")

    # ---------------------------------------------------------------- 3
    step(3, "The cause alert, which is the one most estates actually have")
    log(f"  cpu-in-rack threshold -> "
        + ("never fired" if rows[0][2] is None else f"minute {rows[0][2]}"))
    log("  CPU was 0.35 right up to the power cut, and unreported after it. There is")
    log("  no value of the CPU threshold that would have caught this outage.")
    check(rows[0][2] is None,
          "a cause alert cannot fire on a cause it has no sample of — tuning it is not "
          "the fix and never was (LESSON 4)",
          "the cause alert fired during the outage")

    # ---------------------------------------------------------------- 4
    step(4, "The only control that catches an in-domain monitor is a staleness alert")
    log(f"  errors-in-rack staleness -> "
        + ("never fired" if in_rack_stale is None else f"minute {in_rack_stale}"))
    check(in_rack_stale is not None and in_rack_stale <= OUTAGE_AT + 4,
          f"the dead-man's switch paged at minute {in_rack_stale}, on the absence of "
          "samples — the one predicate whose input is not a value (LESSON 5)",
          "no staleness alert fired for a monitor that stopped sending entirely")
    log("  Every other alert in this file is a question about a number. This one is")
    log("  a question about whether there was a number, which is why it is the only")
    log("  one that survives its own subject dying.")

    # ---------------------------------------------------------------- 5
    step(5, "What a dashboard shows at minute 20, and why it is not lying")
    log("  errors-in-rack : last value 0.001  (from minute 11)")
    log("  cpu-in-rack    : last value 0.35   (from minute 11)")
    log("  Both panels are green. Both are showing the last thing they were told.")
    log("  The users have been getting errors for six minutes.")
    green_but_dead = sample(in_rack, 20) is None and threshold_alert(in_rack, 20) is False
    check(green_but_dead,
          "green and silent are the same colour, and no threshold in the estate "
          "distinguishes them (LESSON 6)",
          "the dashboard state distinguished silence from health without a staleness "
          "alert")

    # ---------------------------------------------------------------- verdict
    return verdict([
        "  1. A monitor inside the failure domain dies with its target.",
        "  2. A threshold alert cannot fire on data that never arrived.",
        "  3. A symptom alert from outside the domain pages on what users see.",
        "  4. No tuning of a cause alert fixes a missing sample.",
        "  5. A staleness alert is the only predicate whose input is absence.",
        "  6. Green and silent are the same colour on every dashboard ever built.",
        "",
        "Two things to carry out. Put the monitor in a different failure domain from",
        "the thing it watches — chapter 01's placement rule, applied to the thing that",
        "tells you about chapter 01. And alert on the absence of data, because the",
        "worst hour you will have is the one that produces no data at all.",
    ], broken=bool(SABOTAGE))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it",
                    choices=["no-data-is-green", "cause-alerts-suffice"],
                    help="break the model on purpose; the drill must then fail")
    args = ap.parse_args()
    global SABOTAGE
    SABOTAGE = args.break_it
    if SABOTAGE:
        log(f"*** SABOTAGE: {SABOTAGE} — assertions are expected to fail ***")
    sys.exit(run())


if __name__ == "__main__":
    main()
