#!/usr/bin/env python3
"""
coverage_drill.py — the matrix says six stages of six are covered. Seven controls are
doing it, EDR is doing three of them by itself, and the last stage is not prevented at
all — it is survived.

`working-with-security.md` asks you to name the control you own at each kill-chain
stage. That is the right exercise and it produces a row per stage, which is how every
control matrix and every audit checklist is filled in — and it is why nobody notices
that the same answer was written in three rows.

Six stages. Nine controls, each covering one or more stages, each of three KINDS —
prevent, detect, recover — and each in place or not. Exact set arithmetic over that.

Five things this drill measures rather than asserts:
  1. what stage-coverage says, and what it leaves out
  2. how many INDEPENDENT controls the coverage actually rests on
  3. which single control failing opens the most stages — the blast radius nobody scores
  4. which stages are only DETECTED or only RECOVERED FROM, where the attacker
     succeeds and you either find out or come back
  5. whether an end-to-end path exists with no preventive control in the way

--break-it scores coverage per stage: a stage with any control is covered. That is not
a strawman — it is the format of every control matrix, every audit response and every
security questionnaire, and it reports 6 of 6.

No tools, no scanners, no credentials, no external dependencies. Pure stdlib, fully
deterministic. Exit code 0 means every assertion about the lesson held.
"""

import argparse
import sys
from dataclasses import dataclass

SCORING = "independent"      # --break-it flips this to "per-stage"

# The operator's chain, as `working-with-security.md` draws it.
STAGES = ["initial-access", "execution", "privilege-escalation",
          "credential-access", "lateral-movement", "impact"]


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
class Control:
    """A matrix has one column for `control`. There are three kinds of them, and the
    difference is what the attacker experiences:

      prevent — they do not get through
      detect  — they get through and you find out
      recover — they get through, it works, and you come back afterwards
    """
    name: str
    covers: list             # which stages it is the answer for
    kind: str                # prevent | detect | recover
    in_place: bool = True

    @property
    def preventive(self):
        return self.kind == "prevent"


# One plausible estate. Nothing exotic — this is the answer sheet a competent operator
# fills in, and the point is what the answer sheet hides rather than what it gets wrong.
CONTROLS = [
    Control("patch pipeline",   ["initial-access"],                       "prevent"),
    Control("mail filtering",   ["initial-access"],                       "prevent"),
    Control("EDR",              ["execution", "privilege-escalation",
                                 "lateral-movement"],                     "prevent"),
    Control("MFA everywhere",   ["credential-access"],                    "prevent"),
    Control("secret manager",   ["credential-access"],                    "prevent"),
    Control("central logging",  ["credential-access", "lateral-movement",
                                 "impact"],                               "detect"),
    Control("tested backups",   ["impact"],                               "recover"),
    # Two that are in the design, the diagram and the audit answer, and not in the
    # estate. This is the ordinary state of a competent shop rather than a bad one.
    Control("least privilege",  ["privilege-escalation",
                                 "lateral-movement"],                     "prevent", False),
    Control("network segmentation", ["lateral-movement"],                 "prevent", False),
]


def live():
    return [c for c in CONTROLS if c.in_place]


def covering(stage, preventive_only=False):
    return [c for c in live()
            if stage in c.covers and (c.preventive or not preventive_only)]


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").strip().split("\n")[0])
    ap.add_argument("--break-it", action="store_true",
                    help="score coverage per stage, the way a control matrix does")
    args = ap.parse_args()
    global SCORING
    if args.break_it:
        SCORING = "per-stage"

    log((__doc__ or "").strip().split("\n\n")[0])
    log(f"\nscoring: {SCORING}"
        + ("   [--break-it: the format of every audit response]" if args.break_it else ""))

    step(1, "The matrix, filled in the usual way")
    log("   stage                    controls in place")
    covered = 0
    for s in STAGES:
        names = [c.name for c in covering(s)]
        covered += 1 if names else 0
        log(f"   {s:<24} {', '.join(names) if names else '— NONE —'}")
    log("")
    log(f"  stages with at least one control: {covered} of {len(STAGES)}")
    check(covered == len(STAGES),
          "every stage has an answer, which is what the matrix was built to show",
          "a stage has no control at all — fix that before reading further")

    step(2, "How many independent controls is that actually resting on?")
    used = sorted({c.name for s in STAGES for c in covering(s)})
    log(f"  rows in the matrix : {sum(len(covering(s)) for s in STAGES)}")
    log(f"  distinct controls  : {len(used)}  → {', '.join(used)}")
    log("")
    log("  A matrix has one row per stage, so a control that answers three stages is")
    log("  written three times and counted three times. The estate does not work that")
    log("  way: it fails once.")
    check(len(used) < sum(len(covering(s)) for s in STAGES),
          f"{sum(len(covering(s)) for s in STAGES)} filled rows rest on {len(used)} distinct controls",
          "every row is a different control, which no real estate has been")

    step(3, "Blast radius — which single control failing opens the most stages")
    log("   if this fails          stages left with NO preventive control")
    worst_name, worst_open = None, []
    for c in live():
        if not c.preventive:
            continue
        opened = [s for s in STAGES
                  if covering(s, preventive_only=True) == [c]]
        if opened:
            log(f"   {c.name:<22} {len(opened)}   {', '.join(opened)}")
        if len(opened) > len(worst_open):
            worst_name, worst_open = c.name, opened
    log("")
    log(f"  the widest is {worst_name}, at {len(worst_open)} stage(s).")
    log("  Nothing in the matrix format asks this question, because the matrix is")
    log("  indexed by stage and this is a question about a control.")
    check(SCORING == "independent" and len(worst_open) >= 1,
          f"one control failing would open {len(worst_open)} stage(s): {', '.join(worst_open)}",
          "scoring per stage cannot ask this question at all — it has no column for it")

    step(4, "Covered, observed, or survived?")
    log("   stage                    prevented?    otherwise covered by")
    detective_only = []
    for s in STAGES:
        prev = covering(s, preventive_only=True)
        det = [f"{c.name} ({c.kind})" for c in covering(s) if not c.preventive]
        if not prev:
            detective_only.append(s)
        log(f"   {s:<24} {'yes' if prev else 'NO ':<11}   {', '.join(det) if det else '—'}")
    log("")
    log("  A stage covered only by detection is a stage the attacker completes and you")
    log("  find out about. A stage covered only by RECOVERY is one where it works and")
    log("  you come back afterwards. Both are worth a great deal. Neither is the claim")
    log("  the word `covered` makes, and the matrix has one column for all three.")
    check(SCORING == "independent",
          f"{len(detective_only)} stage(s) are prevention-covered by nothing"
          if detective_only else "every stage has a preventive control",
          "per-stage scoring counts a detective control as coverage, which reports a "
          "stage as handled when the attacker gets through it")

    step(5, "Is there a complete path with nothing preventive in the way?")
    unpreventable = [s for s in STAGES if not covering(s, preventive_only=True)]
    if unpreventable:
        log(f"  stages with no preventive control: {', '.join(unpreventable)}")
        log("  An attacker does not need every stage to be open — they need a way")
        log("  through each one, and these are the ones where nothing is trying to")
        log("  stop them.")
    else:
        log("  No stage is preventively naked. Every stage has something in the way,")
        log("  which is the state the matrix believed it was describing.")
    log("")
    log("  And these are designed but not finished:")
    for c in CONTROLS:
        if not c.in_place:
            log(f"    {c.name} — would cover {', '.join(c.covers)}")
    log("  Each appears in the design, in the diagram and in the audit answer. Neither")
    log("  is in the estate, and the matrix has no cell for the difference. Note what")
    log("  they would have covered: both of EDR's three stages have a second control")
    log("  on paper, which is exactly why nobody noticed EDR was carrying them alone.")
    check(any(not c.in_place for c in CONTROLS),
          "the unfinished control is named separately from the ones that exist",
          "nothing distinguishes a designed control from a deployed one")

    return verdict([
        "Six of six covered, resting on seven controls, one of",
        "which carries three stages alone, one stage that is survived rather than",
        "prevented — and the matrix cannot say any of the three.",
    ], broken=args.break_it)


if __name__ == "__main__":
    sys.exit(main())
