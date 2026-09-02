#!/usr/bin/env python3
"""
exposure_drill.py — prove, in your own hands, what chapter 07's guided run is really
about: **"we caught it" is a statement about a window, and a posture scanner's job is
to make that window small, not to close it.**

A control matrix has one column for prevent and detect, so the two read as
alternatives of equal standing. They are not. They differ in a unit nobody puts on
the page:

    prevent   exposure = 0 minutes, for exactly the classes the policy names
    detect    exposure = (time to notice) + (time to fix), for every class
    and one finding does not end when you fix it at all

That last one is the leaked credential, and it is the reason detection-time is the
wrong metric to report for it. A bucket stops being public the moment you fix it. A
secret that was public for four hours is public forever until it is rotated, and
"remediated at 14:20" is a true sentence that measures nothing.

No cloud, no credentials, no dependencies. Pure Python stdlib. Exit code 0 means
every assertion about the lesson held. Run it in CI.

    python3 exposure_drill.py
    python3 exposure_drill.py --sabotage fixing-ends-exposure
    python3 exposure_drill.py --sabotage policy-covers-everything
"""

import argparse
import sys

SABOTAGE = None
HORIZON = 30 * 24 * 60          # thirty days, in minutes


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


# --------------------------------------------------------------------------
# A month of ordinary mistakes. Nothing exotic; each is a thing a competent
# person does on a Tuesday.
# --------------------------------------------------------------------------

class Finding:
    def __init__(self, name, cls, introduced, fix_minutes, ends_on_fix=True):
        self.name = name
        self.cls = cls                    # the class a guardrail would have to name
        self.introduced = introduced      # minute it was made
        self.fix_minutes = fix_minutes    # how long remediation itself takes
        self.ends_on_fix = ends_on_fix    # False = the damage outlives the fix


FINDINGS = [
    Finding("public-read on the backup bucket", "storage-public",     2 * 1440, 25),
    Finding("0.0.0.0/0 on the admin port",      "sg-world-open",      9 * 1440, 15),
    Finding("unencrypted volume on a restore",  "volume-unencrypted", 17 * 1440, 40),
    Finding("API key committed to the repo",    "secret-in-repo",     21 * 1440, 20,
            ends_on_fix=False),
]

# What the preventive guardrail actually names. This is the honest part: a policy
# is a list, and a list has an end.
POLICY_COVERS = {"storage-public", "sg-world-open"}


def covered(cls):
    if SABOTAGE == "policy-covers-everything":
        return True
    return cls in POLICY_COVERS


def exposure(finding, regime):
    """Minutes this finding was live, under a given regime.

    A scan regime notices at the next scan boundary after the mistake; a preventive
    regime never lets the mistake exist at all, but only for a class it names."""
    if regime == "prevent" and covered(finding.cls):
        return 0
    if regime == "prevent":
        regime = 1440           # uncovered classes fall back to the daily scan
    noticed = ((finding.introduced // regime) + 1) * regime
    end = min(noticed + finding.fix_minutes, HORIZON)
    if not finding.ends_on_fix and SABOTAGE != "fixing-ends-exposure":
        # A credential that was readable is readable until it is rotated, and the
        # remediation ticket closed on the commit being removed.
        return HORIZON - finding.introduced
    return end - finding.introduced


def total(regime):
    return sum(exposure(f, regime) for f in FINDINGS)


def hours(m):
    return f"{m / 60:8.1f} h"


def run():
    failures = []

    def check(cond, ok, bad):
        if cond:
            log(f"  ✓ {ok}")
        else:
            log(f"  ✗ {bad}")
            failures.append(bad)

    log(__doc__.strip().split("\n\n")[0])

    # ---------------------------------------------------------------- 1
    step(1, "Four ordinary mistakes in thirty days, under three regimes")
    log(f"  {'finding':<36}{'daily scan':>12}{'hourly scan':>14}{'guardrail':>12}")
    for f in FINDINGS:
        log(f"  {f.name:<36}{hours(exposure(f, 1440)):>12}"
            f"{hours(exposure(f, 60)):>14}{hours(exposure(f, 'prevent')):>12}")
    log(f"  {'TOTAL':<36}{hours(total(1440)):>12}"
        f"{hours(total(60)):>14}{hours(total('prevent')):>12}")

    # ---------------------------------------------------------------- 2
    step(2, "Scanning faster is a real win, and it has a floor it cannot cross")
    daily, hourly = total(1440), total(60)
    saved = daily - hourly
    log(f"  daily -> hourly saves {saved / 60:.1f} hours of exposure across the month")
    log(f"  and still leaves {hourly / 60:.1f} hours, because a scan runs after the fact")
    check(0 < hourly < daily,
          f"a 24× faster scanner cut exposure by {100 * saved / daily:.0f}% and could not "
          "reach zero — detection is a window, and windows have a width (LESSON 1)",
          "the hourly scan reached zero exposure, which no detection regime can")

    # ---------------------------------------------------------------- 3
    step(3, "The guardrail takes two classes to zero and does nothing for the others")
    for f in FINDINGS:
        mark = "prevented" if covered(f.cls) else "NOT NAMED by the policy"
        log(f"  {f.cls:<22} {mark}")
    prevented = [f for f in FINDINGS if covered(f.cls)]
    check(all(exposure(f, "prevent") == 0 for f in prevented)
          and len(prevented) < len(FINDINGS),
          f"{len(prevented)} of {len(FINDINGS)} classes go to zero; the rest are still "
          "detect-only and the matrix has one word for both (LESSON 2)",
          "the policy covered every class, so 'prevent' stopped being a claim about a "
          "named list")
    log("  A guardrail is a list of named classes. Everything you did not think of is")
    log("  still on the detection path, and the control matrix records 'prevented'.")

    log("")
    log("  And read the totals again, because the third column is WORSE than the "
        "second:")
    log(f"    hourly scan, no guardrail : {hours(total(60)).strip()}")
    log(f"    guardrail + daily scan    : {hours(total('prevent')).strip()}")
    check(total("prevent") > total(60),
          "deploying the guardrail and relaxing the scan cadence LOST time overall — "
          "prevention covered two classes and the other two lost their fast detection "
          "(LESSON 2b)",
          "the guardrail regime beat the hourly scan, so the cadence trade is not real")
    log("  This is the trade nobody writes down: a guardrail retires a class, not a")
    log("  scanner. The two are not alternatives and the matrix format says they are.")

    # ---------------------------------------------------------------- 4
    step(4, "The finding whose exposure does not end when you fix it")
    secret = FINDINGS[3]
    fixed_at = ((secret.introduced // 60) + 1) * 60 + secret.fix_minutes
    log(f"  API key committed at minute {secret.introduced}, commit removed at "
        f"{fixed_at} — {(fixed_at - secret.introduced) / 60:.1f} h to remediate")
    log(f"  exposure actually counted: {exposure(secret, 60) / 60:.1f} h, and still running")
    check(exposure(secret, 60) > (fixed_at - secret.introduced) * 5,
          "the ticket closed in under two hours and the exposure is the rest of the "
          "month — removing a commit does not un-read a key (LESSON 3)",
          "removing the commit ended the credential's exposure")
    log("  Time-to-remediate is a true number here and it measures the wrong event.")
    log("  The number that matters is time-to-ROTATE, and no scanner reports it")
    log("  because rotation happens in a system the scanner cannot see.")

    # ---------------------------------------------------------------- 5
    step(5, "What to report, once you have the unit")
    log("  Not: '4 findings, all remediated, mean time to remediate 41 minutes.'")
    log(f"  But: '{hours(total(60)).strip()} of exposure this month. Two classes are "
        "prevented and")
    log("        cost zero. Two are detect-only. One of the four is a credential whose")
    log("        exposure has not ended, because it has not been rotated.'")
    detect_only = [f for f in FINDINGS if not covered(f.cls)]
    check(len(detect_only) == 2 and any(not f.ends_on_fix for f in detect_only),
          "the sentence names a window, a covered list and an unrotated key — three "
          "things 'all remediated' cannot say (LESSON 4)",
          "the reportable state collapsed back into a count of findings")

    # ---------------------------------------------------------------- verdict
    log("\n" + "=" * 70)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the lessons held:")
    log("  1. Detection is a window; a faster scanner narrows it and cannot close it.")
    log("  2. Prevention is zero exposure for exactly the classes a policy names.")
    log("  3. A leaked credential's exposure does not end when the finding is fixed.")
    log("  4. 'All remediated' is a count; exposure-minutes is the unit.")
    log("")
    log("The guided run in chapter 07 asks you to break a secure default, catch it")
    log("with the posture scanner, then make it impossible with policy-as-code. Do it.")
    log("This drill is the arithmetic underneath it: what catching it was worth, what")
    log("making it impossible was worth, and the one finding where neither number is")
    log("the one to report.")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage",
                    choices=["fixing-ends-exposure", "policy-covers-everything"],
                    help="break the model on purpose; the drill must then fail")
    args = ap.parse_args()
    global SABOTAGE
    SABOTAGE = args.sabotage
    if SABOTAGE:
        log(f"*** SABOTAGE: {SABOTAGE} — assertions are expected to fail ***")
    sys.exit(run())


if __name__ == "__main__":
    main()
