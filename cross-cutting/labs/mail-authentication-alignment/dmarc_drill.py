#!/usr/bin/env python3
"""
dmarc_drill.py — "SPF passed" is not the same sentence as "DMARC passed".

A hundred-person office publishes SPF, DKIM and DMARC. Every checker returns
green. The domain is still fully spoofable, and two departments are one policy
change away from an outage nobody has warned them about.

Two sources of truth, and they disagree:
  - the SENDER INVENTORY — the list you wrote down, which became the SPF record
  - the DMARC AGGREGATE REPORT — the senders receivers actually saw

Neither is a superset of the other. The inventory contains a sender that stopped
mattering; the report contains two the office never listed and one that is not
theirs at all.

The mechanism underneath is one word: **alignment**. SPF authenticates the
envelope domain. DKIM authenticates the signing domain. DMARC asks a third
question neither of them answers — does the authenticated domain match the
From: header the human actually reads? A message can pass SPF, pass DKIM, and
fail DMARC. A spoofer can pass SPF on their own domain all day.

Four things this drill measures rather than asserts:
  1. what the green checker actually verified, and what it did not
  2. how far the inventory and the report disagree, in both directions
  3. how many spoofed messages `p=none` delivers
  4. what moving to enforcement would break — before you move

No tenant, no DNS, no credentials, no external dependencies. Pure stdlib.
Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass

FAILURES = []
CHECK_ALIGNMENT = True   # --break-it flips this: evaluate the way checkers do


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


# --- the model ---------------------------------------------------------------

DOMAIN = "northwind.example"


def aligns(auth_domain, header_from):
    """DMARC alignment — the question SPF and DKIM do not ask.

    Relaxed alignment, which is what almost every published record uses: a
    subdomain of the same organisational domain counts. `mail.northwind.example`
    aligns; `bounces.deskly.io` does not, no matter how legitimately it passed
    SPF. (Strict alignment demands an exact match and is a different, larger
    enumeration job — out of scope here.)"""
    if not auth_domain:
        return False
    return auth_domain == header_from or auth_domain.endswith("." + header_from)


@dataclass
class Sender:
    """One system that sends as your domain. The office's mail-flow diagram is
    supposed to be a list of these; in practice it is a list of the ones someone
    remembered."""
    name: str
    envelope_domain: str       # what SPF authenticates (Return-Path)
    dkim_domain: str           # what DKIM authenticates (d=), "" if unsigned
    in_spf_record: bool        # is this path published in the SPF record
    volume: int                # messages in the reporting window
    ours: bool                 # is this sender legitimately ours
    note: str = ""

    # --- what the receiver computes, in the order it computes it ---

    def spf_result(self):
        """SPF authenticates the ENVELOPE domain against that domain's record.
        A sender using their own envelope domain publishes their own SPF and
        passes it — including a spoofer."""
        if self.envelope_domain == DOMAIN:
            return "pass" if self.in_spf_record else "fail"
        return "pass"   # their domain, their record, their pass

    def dkim_result(self):
        return "pass" if self.dkim_domain else "none"

    def spf_aligned(self):
        return self.spf_result() == "pass" and aligns(self.envelope_domain, DOMAIN)

    def dkim_aligned(self):
        return self.dkim_result() == "pass" and aligns(self.dkim_domain, DOMAIN)

    def dmarc_result(self):
        """DMARC passes on ONE aligned, passing authentication. Not on two
        unaligned ones."""
        if not CHECK_ALIGNMENT:
            # --break-it: read the auth results and stop, which is what a mail
            # health checker reports and what most people read in a report.
            return "pass" if "pass" in (self.spf_result(), self.dkim_result()) else "fail"
        return "pass" if (self.spf_aligned() or self.dkim_aligned()) else "fail"


def build_senders():
    """The reporting window as receivers saw it — everything that sent as the
    domain, whether or not anyone at the office knows about it."""
    return [
        Sender("M365 tenant", DOMAIN, DOMAIN, True, 8420, True,
               "the one everybody tests with"),
        Sender("marketing tool", f"mail.{DOMAIN}", DOMAIN, True, 2200, True,
               "custom return-path + own-domain DKIM — configured properly"),
        Sender("ticketing system", "bounces.deskly.io", "deskly.io", False, 1960, True,
               "From: helpdesk@ the domain, authenticated as the vendor"),
        Sender("billing platform", DOMAIN, "", False, 310, True,
               "the one finance uses"),
        Sender("CI runner", DOMAIN, "", False, 145, True,
               "alerts, from a host nobody added to the record"),
        Sender("unknown bulk sender", "bulk-mailer-xyz.net", "", False, 640, False,
               "From: ceo@ the domain. Not yours."),
    ]


INVENTORY = ["M365 tenant", "marketing tool", "ticketing system", "old newsletter tool"]
#            ^ the list someone wrote down. Note what is missing, and what is not.

DMARC_RECORD = {"v": "DMARC1", "p": "none", "rua": "mailto:dmarc@northwind.example"}


def green_checker(record_published):
    """The industry-standard mail health check: are the three records there.
    It is a real check. It answers a smaller question than it appears to."""
    return {
        "SPF record found": record_published["spf"],
        "DKIM selector found": record_published["dkim"],
        "DMARC record found": record_published["dmarc"],
    }


def disposition(sender, policy):
    """What the receiver does with the message."""
    if sender.dmarc_result() == "pass":
        return "deliver"
    return {"none": "deliver", "quarantine": "junk", "reject": "bounce"}[policy]


# --- the drill ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", action="store_true",
                    help="evaluate on auth results alone, ignoring alignment — the "
                         "way mail health checkers report and the way reports are "
                         "actually read. The drill must FAIL.")
    a = ap.parse_args()

    global CHECK_ALIGNMENT
    if a.break_it:
        CHECK_ALIGNMENT = False
        log("!! running with --break-it: 'spf=pass' is now read as 'DMARC pass'\n")

    senders = build_senders()
    by_name = {s.name: s for s in senders}

    step(1, "The records are published and the checker is green")
    for k, v in green_checker({"spf": True, "dkim": True, "dmarc": True}).items():
        log(f"  ✓ {k}")
    log(f"\n  published policy: p={DMARC_RECORD['p']}   rua={DMARC_RECORD['rua']}")
    check(DMARC_RECORD["p"] == "none",
          "three green ticks, and the policy is p=none — the checker verified that "
          "the records EXIST, which is not the same claim as the domain being "
          "protected",
          "the fixture is not at p=none; the half-done job is not modelled")
    log("     this is the state most domains are in, and it is where the work stops.")

    step(2, "Two sources of truth, disagreeing in both directions")
    seen = [s.name for s in senders]
    log(f"  inventory (what was written down) : {len(INVENTORY)} senders")
    log(f"  aggregate report (what was seen)  : {len(seen)} senders")
    missing = [n for n in seen if n not in INVENTORY and by_name[n].ours]
    stale = [n for n in INVENTORY if n not in seen]
    foreign = [n for n in seen if not by_name[n].ours]
    log(f"\n  in the report, never listed  : {', '.join(missing)}")
    log(f"  listed, never seen sending   : {', '.join(stale)}")
    log(f"  in the report, not yours     : {', '.join(foreign)}")
    check(missing and stale,
          f"the two lists disagree in BOTH directions — {len(missing)} real senders "
          f"were never listed, and {len(stale)} listed sender no longer sends. "
          "Neither list is the truth; the report is only the more honest of the two",
          "the inventory and the report agree; there is nothing to reconcile")
    check(any(by_name[n].name == "billing platform" for n in missing),
          "and the missed one is finance's — which is the outcome step 06 names "
          "in advance, because finance buys tools without asking IT",
          "the missed sender is not the finance one; the fixture lost the point")

    step(3, "'Pass' and 'aligned' are different words")
    log(f"  {'sender':<22} {'spf':<6} {'dkim':<6} {'aligned':<9} {'DMARC':<6}")
    log(f"  {'-'*22} {'-'*6} {'-'*6} {'-'*9} {'-'*6}")
    for s in senders:
        al = "spf" if s.spf_aligned() else ("dkim" if s.dkim_aligned() else "—")
        log(f"  {s.name:<22} {s.spf_result():<6} {s.dkim_result():<6} {al:<9} "
            f"{s.dmarc_result():<6}")

    tick = by_name["ticketing system"]
    check(tick.spf_result() == "pass" and tick.dmarc_result() == "fail",
          "the ticketing system passes SPF, passes DKIM, and FAILS DMARC — both "
          "authentications are real and both are for the vendor's domain, not "
          "yours. Two green ticks, no alignment, no pass",
          "the ticketing system does not demonstrate an aligned/unaligned split")

    spoof = by_name["unknown bulk sender"]
    check(spoof.spf_result() == "pass",
          "the spoofer passes SPF too — on their OWN envelope domain, with their "
          "own published record. 'SPF passed' is a statement about a domain, and "
          "not necessarily about yours",
          "the spoofer fails SPF; the fixture makes spoofing look harder than it is")
    check(spoof.dmarc_result() == "fail",
          "alignment is what catches them: the authenticated domain is not the "
          "From: domain, so DMARC fails where SPF alone would have waved it through",
          "the spoofer passed DMARC")

    step(4, "What p=none does with all of that")
    delivered = {}
    for s in senders:
        d = disposition(s, DMARC_RECORD["p"])
        delivered.setdefault(d, []).append(s)
    for s in senders:
        log(f"  {s.name:<22} DMARC {s.dmarc_result():<5} → "
            f"{disposition(s, 'none'):<8} ({s.volume} messages)")
    spoofed_delivered = sum(s.volume for s in senders
                            if not s.ours and disposition(s, "none") == "deliver")
    check(len(delivered.get("deliver", [])) == len(senders),
          "every message is delivered — the passing ones, the misaligned ones, and "
          "the forged ones, identically. p=none does not act on the verdict it "
          "spent a quarter computing",
          "p=none did not deliver everything; the policy model is wrong")
    check(spoofed_delivered > 0,
          f"{spoofed_delivered} forged messages reached inboxes with the domain in "
          "the From: line, while the dashboard stayed green. That is the whole "
          "content of 'monitoring, not protection'",
          "no spoofed mail was delivered; there is nothing for enforcement to fix")

    step(5, "What enforcement would break — measured before you move")
    for policy in ("none", "quarantine", "reject"):
        broken = [s for s in senders if s.ours and disposition(s, policy) != "deliver"]
        stopped = sum(s.volume for s in senders
                      if not s.ours and disposition(s, policy) != "deliver")
        log(f"  p={policy:<11} legitimate senders broken: {len(broken)}   "
            f"forged messages stopped: {stopped}")
    broken_q = [s for s in senders if s.ours and disposition(s, "quarantine") != "deliver"]
    check(len(broken_q) > 0,
          f"moving to quarantine today breaks {len(broken_q)} legitimate senders "
          f"({', '.join(s.name for s in broken_q)}) — the risk people cite for "
          "deferring enforcement is real",
          "enforcement breaks nothing today; the deferral has no stated reason")
    check(set(s.name for s in broken_q) == set(missing) | {"ticketing system"},
          "and it is EXACTLY the senders the inventory got wrong — the un-listed "
          "ones and the unaligned one. The risk is not unknowable, it is the "
          "reconciliation you have not done",
          "the breakage does not match the inventory gap; the two are unrelated here")

    step(6, "Do the reconciliation first, then the policy is free")
    fixed = build_senders()
    for s in fixed:
        if not s.ours:
            continue
        if s.name == "ticketing system":
            s.envelope_domain, s.dkim_domain = f"bounces.{DOMAIN}", DOMAIN
            s.in_spf_record = True
        elif not s.in_spf_record:
            s.in_spf_record, s.dkim_domain = True, DOMAIN
    for s in fixed:
        log(f"  {s.name:<22} DMARC {s.dmarc_result():<5} → "
            f"{disposition(s, 'reject'):<8}")
    still_broken = [s for s in fixed if s.ours and disposition(s, "reject") != "deliver"]
    stopped_now = sum(s.volume for s in fixed
                      if not s.ours and disposition(s, "reject") != "deliver")
    check(not still_broken,
          "with every real sender enumerated and aligned, p=reject breaks nothing — "
          "the enumeration was the work, and the policy change is the easy part "
          "that gets treated as the hard one",
          "senders still break after the fix; the remediation model is wrong")
    check(stopped_now > 0,
          f"and now the policy earns its keep: {stopped_now} forged messages "
          "bounced instead of delivered",
          "enforcement stopped nothing after the fix")

    # --- verdict -------------------------------------------------------------
    log("\n" + "=" * 72)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        return 1

    log("PASSED — the lessons held.\n")
    log("  1. A green checker verifies that the records EXIST. It does not read")
    log("     the policy, and p=none protects nothing.")
    log("  2. SPF authenticates the envelope domain, DKIM the signing domain.")
    log("     DMARC asks whether either matches the From: line a human reads.")
    log("     'SPF passed' can be true of a message forging your domain.")
    log("  3. The inventory and the aggregate report disagree in both directions.")
    log("     The report is the more honest source, and it is still not a list of")
    log("     authorised senders — a person has to decide which ones are yours.")
    log("  4. Enforcement's risk is measurable before you take it. It is exactly")
    log("     the senders your inventory got wrong, which is a reconciliation you")
    log("     can do this week instead of a danger you defer indefinitely.")
    log("\n  Publishing the record is not the job. Enumerating who sends as you,")
    log("  and moving off p=none on a date you wrote down, is the job.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
