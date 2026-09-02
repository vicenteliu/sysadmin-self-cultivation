#!/usr/bin/env python3
"""
retention_drill.py — the estate that passed the permission lab is the one that
fails this one.

A meeting is recorded on day 0. The transcript is shared to the project group,
never to individuals — which is exactly what
`cross-cutting/labs/permission-sprawl/` recommends, and it is correct. No link is
left open. No individual grant is made. An access review run on any day of the
next three years returns "correctly permissioned", truthfully.

Three years later the conversation is readable by three times as many people,
including someone it was *about* who was not in the room, and the recording that
could have checked what it says expired in month one.

Nobody did anything wrong. There is no misconfiguration in this fixture at all.

WHERE THIS SITS. Lab 07 asks *who can see this* — a question about an instant, and
it answers it well. This asks the two questions an instant cannot hold:
  - who can see it over the artefact's LIFETIME, as a correct group grows
  - is what they are reading still checkable against anything

Four things it measures rather than asserts:
  1. how far readership drifts with zero grants made
  2. that a point-in-time review passes every single time it is run
  3. the window in which the transcript can be verified, against the window in
     which it can be read
  4. that the missing control was never an access control

No suite, no tenant, no credentials, no external dependencies. Pure stdlib.
Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass, field

GOVERNANCE = "lifetime"      # --break-it flips this to "point_in_time"

HORIZON = 1095               # three years, the day we look back from
RECORDING_RETENTION = 30     # platform default
TRANSCRIPT_RETENTION = None  # nobody set one


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


# --- the meeting -------------------------------------------------------------

ATTENDEES = ["dana", "raj", "mei", "tom", "sofia", "ken"]

# Someone the meeting was ABOUT, and who was not in it.
SUBJECT = "priya"

STATEMENTS = [
    ("dana",  "we are moving Priya off Atlas after the reorg"),
    ("raj",   "she has not been told yet, so keep this in here"),
    ("mei",   "the Q3 numbers are not her fault, the scope moved twice"),
    ("tom",   "legal wants the contractor conversation minuted separately"),
    ("sofia", "we should not put the headcount number in writing yet"),
    ("ken",   "agreed, and I will take the action on the vendor call"),
] + [("dana", f"routine planning point {i}") for i in range(8)]

# The summariser attributed one statement to the wrong speaker. Ordinary
# diarisation error rate; nothing exotic.
MISATTRIBUTED_INDEX = 2
MISATTRIBUTED_TO = "sofia"


@dataclass
class Group:
    """`project-atlas`. Group-based sharing, which is the correct pattern — and
    the reason this failure needs no mistake to occur."""
    name: str
    events: list = field(default_factory=list)   # (day, "+"/"-", person)

    def members_on(self, day):
        m = set(ATTENDEES)
        for d, op, who in self.events:
            if d > day:
                break
            m.add(who) if op == "+" else m.discard(who)
        return m

    def ever_by(self, day):
        """Everyone who could have read it at any point up to `day`. The set that
        matters for a conversation, and the one no permissions dialog displays.

        Bounded by the transcript's own life: joining the group after the document
        expired gives you nothing. That bound does no work at all while retention
        is unset — which is the point of setting one."""
        limit = day if TRANSCRIPT_RETENTION is None else min(day, TRANSCRIPT_RETENTION)
        seen = set(ATTENDEES)
        for d, op, who in self.events:
            if d > limit:
                break
            if op == "+":
                seen.add(who)
        return seen


def build_group():
    joins = [45, 120, 200, 260, 330, 410, 480, 540, 610, 700, 760, 830, 900, 970, 1040]
    names = [f"new{i:02d}" for i in range(len(joins))]
    # The person the meeting was about joins the project two years later. Routine,
    # correct, approved by whoever owns the group.
    names[9] = SUBJECT
    ev = [(d, "+", n) for d, n in zip(joins, names)]
    ev += [(300, "-", "tom"), (620, "-", "ken"), (880, "-", "new02")]
    return Group("project-atlas", sorted(ev, key=lambda e: e[0]))


# --- the artefacts -----------------------------------------------------------

def recording_alive(day):
    return day <= RECORDING_RETENTION


def transcript_alive(day):
    return TRANSCRIPT_RETENTION is None or day <= TRANSCRIPT_RETENTION


def verifiable(day):
    """Can anyone establish whether the summary is accurate? Only by going back to
    the source."""
    return recording_alive(day)


# --- the governance check ----------------------------------------------------

SHARING_POLICY = {"acl_type": "group", "individual_grants": 0, "open_links": 0}


def acl_state(group, day):
    """The sharing state of the transcript on `day`. It is set once, on day 0, and
    nothing in the next three years touches it — which is why every reading of it
    returns the same thing."""
    return {"acl": f"group:{group.name}", "acl_type": "group",
            "individual_grants": 0, "open_links": 0}


def review(group, day):
    """What an access review actually does: read the sharing state and compare it
    to the policy. A real evaluation of a real state — which passes, every time,
    because the state is genuinely correct and genuinely unchanged."""
    st = acl_state(group, day)
    ok = all(st[k] == v for k, v in SHARING_POLICY.items())
    return dict(st, day=day,
                verdict="correctly permissioned" if ok else "finding")


def governance_findings(group, day):
    """What the governance regime in force can SEE. Keyed by kind, so each beat of
    the drill can ask the regime rather than asking the model directly — the whole
    subject here is the difference between those two questions."""
    if GOVERNANCE == "point_in_time":
        # --break-it: this IS an access review, and it is not wrong. It reads a
        # correct state correctly. It simply has no way to express anything that
        # happened between two of its runs.
        r = review(group, day)
        return {} if r["verdict"] == "correctly permissioned" else {"acl": "finding"}

    out = {}
    day0, now = set(ATTENDEES), group.ever_by(day)
    if len(now) > len(day0):
        out["drift"] = f"readership grew {len(day0)} → {len(now)} with 0 grants made"
    if not verifiable(day) and transcript_alive(day):
        out["unverifiable"] = (f"unverifiable since day {RECORDING_RETENTION}; "
                               "still readable")
    if SUBJECT in now - day0:
        out["subject"] = f"{SUBJECT}, discussed by name and not present, can read it"
    if TRANSCRIPT_RETENTION is None:
        out["no_expiry"] = "no retention set on the transcript; exposure has no end date"
    return out


def detects(kind, group, day):
    """Does the regime in force surface this at all?"""
    return kind in governance_findings(group, day)


# --- the drill ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", action="store_true",
                    help="govern by point-in-time access review — the control every "
                         "organisation actually runs. The drill must FAIL.")
    a = ap.parse_args()

    global GOVERNANCE
    if a.break_it:
        GOVERNANCE = "point_in_time"
        log("!! running with --break-it: governing by point-in-time access review\n")

    g = build_group()

    step(1, "Day 0 is correct, and there is nothing in this fixture to find")
    log(f"  meeting          : Atlas — Q3 replan, {len(ATTENDEES)} attendees")
    log(f"  transcript shared: group:{g.name}   (not individuals, no link)")
    log(f"  individual grants: 0        open links: 0")
    r0 = review(g, 0)
    check(r0["verdict"] == "correctly permissioned" and r0["individual_grants"] == 0,
          "the transcript is shared to a group and to nothing else — the pattern "
          "lab 07 recommends, applied correctly. This lab contains no "
          "misconfiguration; everything that follows happens to an estate that is "
          "right",
          "the day-0 state is already wrong; this lab would just be lab 07 again")

    step(2, "The readership grows. Nobody grants anything.")
    log(f"  {'day':>6}  {'members':>8}  {'ever able to read':>18}  grants made")
    log(f"  {'-'*6}  {'-'*8}  {'-'*18}  {'-'*11}")
    for d in (0, 90, 365, 730, HORIZON):
        log(f"  {d:>6}  {len(g.members_on(d)):>8}  {len(g.ever_by(d)):>18}  {0:>11}")
    d0, dn = len(set(ATTENDEES)), len(g.ever_by(HORIZON))
    check(dn > d0,
          f"{d0} people were in the room; {dn} have been able to read what was said "
          f"in it. Every one of them arrived through a correct group membership "
          "approved by whoever owns the project — the transcript's own permissions "
          "were never touched",
          "the readership did not grow; the fixture has no drift to detect")
    check(detects("drift", g, HORIZON),
          "and the governance regime in force surfaces it — the number of people "
          "who have held access is a thing it can be asked for",
          "the regime in force cannot see the drift at all. It is not returning a "
          "wrong answer about readership; it has no question whose answer is "
          "readership-over-time")
    check(len(g.members_on(HORIZON)) < dn,
          f"and the group today has {len(g.members_on(HORIZON))} members, fewer than "
          f"the {dn} who have held access — leavers do not un-read. A membership "
          "list is a snapshot of a set that only ever accumulated",
          "current membership is not smaller than cumulative readership — either no "
          "leaver is modelled, or the transcript expired long enough ago that most "
          "of today's group joined after it was gone, which is the good case")

    step(3, "The review passes. Every time. Truthfully.")
    for d in (0, 365, 730, HORIZON):
        r = review(g, d)
        log(f"  day {d:>4}  acl={r['acl']:<22} individual={r['individual_grants']}  "
            f"links={r['open_links']}  → {r['verdict']}")
    passes = [review(g, d)["verdict"] for d in (0, 365, 730, HORIZON)]
    check(all(v == "correctly permissioned" for v in passes),
          "four reviews across three years, four clean results, none of them wrong. "
          "A control that is correct at every instant it is evaluated can still be "
          "wrong about the interval between them — and an access review has no "
          "syntax for an interval",
          "a review returned a finding; the point of this lab is that none of them "
          "can")

    step(4, "The source expires before the thing derived from it")
    log(f"  recording   retention {RECORDING_RETENTION:>4} days   → gone on day "
        f"{RECORDING_RETENTION + 1}")
    log(f"  transcript  retention {'none':>4}        → alive on day {HORIZON}, "
        "and after")
    log(f"  summary     retention {'none':>4}        → alive on day {HORIZON}, "
        "and after")
    speaker, text = STATEMENTS[MISATTRIBUTED_INDEX]
    log(f"\n  the summary attributes to {MISATTRIBUTED_TO}:")
    log(f"    \"{text}\"")
    log(f"  it was said by {speaker}.")
    verif_days = sum(1 for d in range(HORIZON + 1) if verifiable(d))
    read_days = sum(1 for d in range(HORIZON + 1) if transcript_alive(d))
    check(verif_days < read_days,
          f"the transcript can be read on {read_days} of the days modelled and "
          f"checked on {verif_days} of them — {verif_days / read_days:.0%}. The "
          "expensive artefact expires on a default and the cheap one does not, so "
          "the record that could settle an attribution is the one that goes first",
          "the source outlives the derivative; the asymmetry this lab is about does "
          "not exist in the fixture")
    check(detects("unverifiable", g, HORIZON),
          "and the regime in force flags that gap — an artefact still being read "
          "after the only thing that could check it expired is a reportable state",
          "the regime in force never notices that the source expired. Retention is "
          "set per artefact and reviewed by nobody who is looking at both")
    check(not verifiable(HORIZON) and transcript_alive(HORIZON),
          "so the error is not discovered and corrected — it becomes the account of "
          "what was said. Quiet failure, durable artefact, and no one is being "
          "careless at any point",
          "the durability claim does not hold at the horizon — either the source "
          "outlived the summary, or the transcript expired (which is the outcome "
          "this lab is arguing for, and means the fixture no longer demonstrates "
          "the failure)")

    step(5, "Who is reading it now")
    outsiders = g.ever_by(HORIZON) - set(ATTENDEES)
    log(f"  people who can read it and were not in the room: {len(outsiders)}")
    log(f"  among them: {SUBJECT} — named in it, discussed in the third person,")
    log(f"    joined the project on day "
        f"{[d for d, op, w in g.events if w == SUBJECT][0]} through ordinary onboarding")
    log(f"\n  what {SUBJECT} can now read about {SUBJECT}:")
    for i, (sp, tx) in enumerate(STATEMENTS[:3]):
        who = MISATTRIBUTED_TO if i == MISATTRIBUTED_INDEX else sp
        log(f"    {who}: \"{tx}\"")
    check(detects("subject", g, HORIZON),
          f"and the regime in force names {SUBJECT} — 'who can read this who was "
          "not in it' is a question it can answer",
          f"the regime in force cannot name {SUBJECT}. It sees a correct group on a "
          "correctly shared document, which is exactly what it is looking at")
    check(SUBJECT in outsiders,
          f"{SUBJECT} can read a conversation about {SUBJECT}, including one line "
          f"attributed to the wrong colleague. No grant was made, no policy was "
          "broken, no review would have flagged it, and the consent that covered "
          "the recording covered six people in a room three years ago",
          f"{SUBJECT} never gained access; the sharpest case is not in the fixture")

    step(6, "What the check would have to look at")
    found = governance_findings(g, HORIZON)
    if found:
        for kind, msg in found.items():
            log(f"  · [{kind}] {msg}")
    else:
        log("  (nothing)")
    check(len(found) >= 3,
          f"{len(found)} findings, none of which is a permissions finding. The "
          "control that was missing here was never an access control — it was an "
          "expiry. A transcript with a lifetime ends this entire failure, and no "
          "amount of reviewing the ACL does",
          "the governance check found fewer than three things — evaluated at an "
          "instant it cannot see readership drift, cannot see that the source "
          "expired, and cannot see who is reading; it is not wrong, it is silent")

    # --- verdict -------------------------------------------------------------
    return verdict([
        "  1. Doing it the way lab 07 recommends is what makes this happen. Group",
        "     sharing is correct, and a correct group grows.",
        "  2. A control evaluated at an instant cannot make a claim about an",
        "     interval. Every access review here passes, and every one is honest.",
        "  3. Retention defaults are set per artefact, so the source expires and",
        "     the summary derived from it does not. The checkable thing goes first.",
        "  4. Consent was given by six people in a room. It is now doing work it",
        "     was never asked to do, for readers nobody could have named.",
        "  5. The missing control is an expiry, not a permission. If the only",
        "     question you ask about a transcript is who can see it, you will keep",
        "     getting a correct answer while the exposure grows.",
        "\n  A recording is a decision about the next three years, taken by whoever",
        "  clicked the button, usually without knowing that is what it was.",
    ], broken=a.break_it)


if __name__ == "__main__":
    sys.exit(main())
