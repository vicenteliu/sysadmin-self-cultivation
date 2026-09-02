#!/usr/bin/env python3
"""
reconcile_drill.py — both systems report 97 devices, 97 devices exist, and three
records are wrong.

A hundred-person office runs two systems that are live, automatic and maintained:
  - PROCUREMENT   — authoritative for who paid for it and who it belongs to
  - ENDPOINT MGMT — authoritative for what state it is in

Neither owns both, which is why "when they disagree, which one wins?" has no
global answer — and why answering it globally gets a different set of rows wrong
depending on which way you answer.

The totals agree. That is not reassurance; it is the reason nobody looks. A
re-image wave, one warranty swap, one disposal and one loaner net out to the same
number, and the only way to see it is to reconcile record by record.

Five things this drill measures rather than asserts:
  1. that equal totals hide unequal records
  2. what the reconciliation key costs you — hostname, serial, asset tag
  3. how many reported discrepancies are PHANTOMS the key invented
  4. that a single "which source wins" rule is wrong in both directions
  5. what survives a perfect key — and why that residue is a person's job

No CMDB, no agent, no credentials, no external dependencies. Pure stdlib.
Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass

RECONCILE_KEY = "asset_tag"   # --break-it flips this to "hostname"


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


# --- ground truth ------------------------------------------------------------

@dataclass
class Device:
    """What is physically true. NEITHER system has this view — that is the whole
    problem. The drill knows it only so it can score the reconciliation."""
    case: str
    asset_tag: str
    serial_bought: str      # serial as purchasing recorded it
    serial_now: str         # serial the machine reports today
    hostname_deployed: str  # hostname typed into the record at deployment
    hostname_now: str       # hostname the machine reports today
    owner_on_paper: str
    holder_actual: str
    in_procurement: bool    # procurement carries an active row
    in_endpoint: bool       # the endpoint tool sees it check in
    exists: bool            # is there a laptop


def build_fleet():
    f = []
    for i in range(88):
        t = f"AT-{i:04d}"
        f.append(Device("clean", t, f"SN{i:05d}", f"SN{i:05d}", f"LT-{i:04d}",
                        f"LT-{i:04d}", f"user{i:03d}", f"user{i:03d}",
                        True, True, True))
    # A re-image wave after the OS upgrade. Routine, and it renames the machine.
    for j in range(6):
        i = 200 + j
        t = f"AT-{i:04d}"
        f.append(Device("re-imaged", t, f"SN{i:05d}", f"SN{i:05d}", f"LT-{i:04d}",
                        f"LT-{i+900:04d}", f"user{i:03d}", f"user{i:03d}",
                        True, True, True))
    # The vendor replaced the mainboard under warranty. New serial, same sticker,
    # same name. Rare — which is why keying on serial feels safe.
    f.append(Device("warranty swap", "AT-0301", "SN00301", "SN99301", "LT-0301",
                    "LT-0301", "user301", "user301", True, True, True))
    # Sold three months ago. The disposal evidence was never filed, so the
    # procurement row is still open.
    f.append(Device("disposed, not retired", "AT-0302", "SN00302", "SN00302",
                    "LT-0302", "LT-0302", "user302", "—", True, False, False))
    # A vendor pilot loaner. Enrolled, working, never purchased.
    f.append(Device("never purchased", "AT-0303", "—", "SN00303", "—",
                    "LT-0303", "—", "user303", False, True, True))
    # She left in June; he has had the laptop since. Both systems are right about
    # the thing they own, and they disagree.
    f.append(Device("owner drift", "AT-0304", "SN00304", "SN00304", "LT-0304",
                    "LT-0304", "user304 (left in June)", "user401",
                    True, True, True))
    return f


def procurement_rows(fleet):
    """What purchasing knows. No live hostname — the hostname column was typed in
    at deployment and has not been touched since."""
    return [{"asset_tag": d.asset_tag, "serial": d.serial_bought,
             "hostname": d.hostname_deployed, "owner": d.owner_on_paper,
             "case": d.case}
            for d in fleet if d.in_procurement]


def endpoint_rows(fleet):
    """What the endpoint tool sees this morning. The asset_tag field is here only
    because somebody filled it in at enrolment — one column on one form."""
    return [{"asset_tag": d.asset_tag, "serial": d.serial_now,
             "hostname": d.hostname_now, "user": d.holder_actual,
             "case": d.case}
            for d in fleet if d.in_endpoint]


# --- the reconciliation ------------------------------------------------------

def reconcile(proc, endp, key):
    """Join the two sources on `key` and classify every row. This is the whole
    job; the inventory is not the work product, this diff is."""
    p_by = {}
    e_by = {}
    for r in proc:
        p_by.setdefault(r[key], []).append(r)
    for r in endp:
        e_by.setdefault(r[key], []).append(r)

    matched, only_p, only_e, owner_disagrees = [], [], [], []
    for k, rows in p_by.items():
        if k in e_by:
            matched.append((rows[0], e_by[k][0]))
            if rows[0]["owner"] != e_by[k][0]["user"]:
                owner_disagrees.append((rows[0], e_by[k][0]))
        else:
            only_p.extend(rows)
    for k, rows in e_by.items():
        if k not in p_by:
            only_e.extend(rows)
    return {"matched": matched, "only_procurement": only_p,
            "only_endpoint": only_e, "owner_disagrees": owner_disagrees}


def reported_device_count(rec):
    """How many distinct devices the reconciliation believes exist."""
    return len(rec["matched"]) + len(rec["only_procurement"]) + len(rec["only_endpoint"])


def discrepancies(rec):
    return (len(rec["only_procurement"]) + len(rec["only_endpoint"])
            + len(rec["owner_disagrees"]))


PHANTOM_CASES = {"re-imaged", "warranty swap"}


def phantom_count(rec):
    """Discrepancies that are not device problems — they are key problems. The
    device is fine; the join failed."""
    n = 0
    for r in rec["only_procurement"] + rec["only_endpoint"]:
        if r["case"] in PHANTOM_CASES:
            n += 1
    return n


def candidate_causes(row, side):
    """What AI is genuinely good for here: proposing why two records disagree.
    Note that several rows come back with more than one candidate and the data
    cannot separate them. That is the point at which it stops and a person
    starts."""
    if side == "only_procurement":
        return ["disposed, evidence never filed",
                "lost or stolen, never reported",
                "on a shelf, never enrolled"]
    if side == "only_endpoint":
        return ["loaner or vendor pilot, never purchased",
                "bought on a department card, outside procurement",
                "personal device enrolled by mistake"]
    return ["device re-assigned, paperwork not updated",
            "shared device, whoever logged in last",
            "procurement owner is a cost centre, not a person"]


# --- the drill ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", action="store_true",
                    help="reconcile on hostname instead of asset tag — the "
                         "intuitive key, the one both systems display, and the "
                         "one that changes. The drill must FAIL.")
    a = ap.parse_args()

    global RECONCILE_KEY
    if a.break_it:
        RECONCILE_KEY = "hostname"
        log("!! running with --break-it: reconciling on hostname\n")

    fleet = build_fleet()
    proc, endp = procurement_rows(fleet), endpoint_rows(fleet)
    physical = sum(1 for d in fleet if d.exists)

    step(1, "Both systems are live, both are automatic, and both agree on the total")
    log(f"  procurement rows (active) : {len(proc)}")
    log(f"  endpoint tool rows        : {len(endp)}")
    log(f"  laptops that exist        : {physical}")
    broken = [d for d in fleet
              if d.in_procurement != d.exists or d.in_endpoint != d.exists
              or (d.exists and d.owner_on_paper != d.holder_actual)]
    stale = [d for d in fleet if d.in_procurement
             and (d.hostname_deployed != d.hostname_now
                  or d.serial_bought != d.serial_now)]
    check(len(proc) == len(endp) == physical,
          f"all three numbers are {physical}. A count reconciles perfectly and "
          "tells you nothing — the re-image wave, the swap, the disposal and the "
          "loaner net out",
          "the totals differ; this fixture cannot show that equal totals hide "
          "unequal records")
    log(f"\n  devices whose records are actually wrong : {len(broken)}")
    log(f"  devices with a stale field in a record   : {len(stale)}")
    check(len(broken) > 0 and len(stale) > 0,
          f"{len(broken)} devices are genuinely mis-recorded and {len(stale)} more "
          "carry a field that has drifted since deployment. Neither shows up in a "
          "total. This is the 2026 failure mode — not a stale sheet, a live sheet "
          "that is still wrong, which is harder to notice because staleness has a "
          "smell and this does not",
          "the fixture has no mis-recorded or drifted devices; nothing to reconcile")

    step(2, "The key decides which failures become invisible")
    log(f"  {'key':<12} {'reported devices':<18} {'discrepancies':<15} {'of those, phantom'}")
    log(f"  {'-'*12} {'-'*18} {'-'*15} {'-'*17}")
    scores = {}
    for key in ("hostname", "serial", "asset_tag"):
        r = reconcile(proc, endp, key)
        scores[key] = r
        log(f"  {key:<12} {reported_device_count(r):<18} {discrepancies(r):<15} "
            f"{phantom_count(r)}")
    log(f"\n  laptops that actually exist: {physical}")

    h, s, t = (reported_device_count(scores[k]) for k in ("hostname", "serial", "asset_tag"))
    check(h > physical,
          f"keyed on hostname the reconciliation reports {h} devices against {physical} "
          f"that exist — {h - physical} machines that are not there. Every re-imaged "
          "machine became a new device and its old record never retired",
          "hostname keying did not inflate the count; the trap is not modelled")
    check(t < s < h,
          f"asset tag {t} < serial {s} < hostname {h}. The key is not a detail of "
          "the join, it is the thing that decides how much of the fleet is fiction",
          "the three keys do not separate; the comparison proves nothing")
    check(phantom_count(scores["asset_tag"]) == 0 and phantom_count(scores["hostname"]) > 0,
          f"and the difference is phantoms: hostname invents "
          f"{phantom_count(scores['hostname'])} discrepancies that are not device "
          "problems at all, asset tag invents none. A check earns its place by "
          "what it eliminates, not by what it reports",
          "the phantom counts do not separate the keys")
    check(phantom_count(scores["serial"]) > 0,
          f"serial is better and not clean either — the warranty swap changed the "
          "serial and left the sticker alone, so serial-keying splits one laptop "
          "into two records. Every key has a blind spot; the decision is which one "
          "you can live with, made before there is data",
          "serial keying has no blind spot here; the lab overclaims for serial")

    step(3, f"Reconciling on {RECONCILE_KEY}")
    rec = reconcile(proc, endp, RECONCILE_KEY)
    log(f"  matched                : {len(rec['matched'])}")
    log(f"  only in procurement    : {len(rec['only_procurement'])}")
    log(f"  only in endpoint tool  : {len(rec['only_endpoint'])}")
    log(f"  matched, owner differs  : {len(rec['owner_disagrees'])}")
    log(f"  → reports {reported_device_count(rec)} devices, {physical} exist")
    check(reported_device_count(rec) - physical <= 1,
          f"the reconciliation reports {reported_device_count(rec)} against {physical} "
          "physical — the one extra is the disposed laptop whose record is still "
          "open, which is a finding rather than an error",
          f"the reconciliation reports {reported_device_count(rec)} devices against "
          f"{physical} physical; the surplus is fiction, not findings")
    check(phantom_count(rec) == 0,
          "every discrepancy it reports is a real device problem — nothing here is "
          "the join failing",
          f"{phantom_count(rec)} of the reported discrepancies are phantoms — the "
          "key invented them, and someone will spend a week on them")

    step(4, "'Which source wins' has no global answer")
    drift = rec["owner_disagrees"][0] if rec["owner_disagrees"] else None
    if drift:
        p_row, e_row = drift
        log(f"  procurement says owner   : {p_row['owner']}")
        log(f"  endpoint says logged-in  : {e_row['user']}")
        log("\n  if procurement always wins → the owner stays a person who left in June;")
        log("     offboarding (step 15) chases a laptop she does not have.")
        log("  if the endpoint tool always wins → ownership follows whoever logged in;")
        log("     the cost centre changes when someone borrows a machine for a week.")
    check(drift is not None,
          "both systems are right about the thing they own and they disagree. "
          "Procurement owns who it belongs to, the endpoint tool owns what state "
          "it is in — a single-winner rule overwrites one of those with the other",
          "no owner disagreement survived to this step; the beat cannot be shown")
    log("\n     so the rule is per-field, not per-source — and it has to be written")
    log("     down before there is data: five minutes now, a political argument later.")

    step(5, "The residue is the work product")
    log("  what a perfect key leaves behind, and what each one needs from a person:\n")
    rows = ([(r, "only_procurement") for r in rec["only_procurement"]]
            + [(r, "only_endpoint") for r in rec["only_endpoint"]]
            + [(p, "owner_disagrees") for p, _ in rec["owner_disagrees"]])
    ambiguous = 0
    for r, side in rows:
        causes = candidate_causes(r, side)
        if len(causes) > 1:
            ambiguous += 1
        log(f"  {r['asset_tag']}  [{side}]")
        for c in causes:
            log(f"       · {c}")
    row_phantoms = sum(1 for r, _ in rows if r["case"] in PHANTOM_CASES)
    check(len(rows) > 0,
          f"{len(rows)} rows survive the join, and they are the whole reason the "
          "job exists. The inventory was never the work product — this diff is",
          "nothing survived; the reconciliation is not supposed to produce a clean "
          "sheet")
    check(row_phantoms == 0,
          "and every row handed to the advisory layer is a real device problem",
          f"{row_phantoms} of the {len(rows)} rows sent for explanation are phantoms "
          "the key invented — and the model below produced confident causes for "
          "every one of them. A bad key does not just cost a week; it feeds fiction "
          "to the thing you asked to explain it")
    check(ambiguous == len(rows),
          f"and every one of them has more than one candidate cause that the data "
          "cannot separate. This is exactly where AI is useful — proposing why two "
          "records disagree — and exactly where it must stop. It can rank these; "
          "it cannot know which is true, because the answer is not in either system",
          "some rows have a single mechanical cause; the advisory boundary is "
          "overstated here")

    # --- verdict -------------------------------------------------------------
    return verdict([
        "  1. Equal totals are not agreement. Two live systems can report the same",
        "     count, be automatically maintained, and still be wrong about which",
        "     laptops those are.",
        "  2. The reconciliation key decides how much of your fleet is fiction.",
        "     Hostname is the intuitive choice and it changes on re-image; the key",
        "     that survives costs one column on one form at device #1.",
        "  3. Most of what a bad key reports is phantoms. A check earns its place",
        "     by what it eliminates, not by what it reports.",
        "  4. 'Which source wins' is a per-field decision, not a per-source one.",
        "     Procurement owns ownership, the endpoint tool owns state, and a",
        "     global rule silently overwrites one with the other.",
        "  5. What a perfect key leaves is the actual job: rows whose cause is not",
        "     in either system. Let a model propose the why; let a person decide.",
        "\n  Collecting was the 2015 job. Reconciling is this one, and the diff —",
        "  not the inventory — is what you are paid for.",
    ], broken=a.break_it)


if __name__ == "__main__":
    sys.exit(main())
