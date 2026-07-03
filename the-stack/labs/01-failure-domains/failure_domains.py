#!/usr/bin/env python3
"""
failure_domains.py — prove, in your own hands, the central lesson of chapter 01:
a failure domain is the blast radius of a shared dependency, and "highly available"
means placing replicas so no single domain failure takes them all.

No cloud, no credentials, no dependencies. Pure Python stdlib. It models a small
fleet as hosts grouped into racks (each rack shares a top-of-rack switch + PDU = a
failure domain), places a service two ways, kills a rack, and checks what survives:

    naive placement      both replicas happen to land in the SAME rack
    anti-affinity        replicas are forced into DIFFERENT racks

Then it fails a rack and shows the naive service goes DOWN while the anti-affinity
service stays UP on its surviving replica — the whole point of "spread across fault
domains," made concrete.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


class Fleet:
    """A set of racks (failure domains), each holding hosts."""

    def __init__(self, racks):
        # racks: dict[rack_name] -> list[host_name]
        self.racks = {r: list(hosts) for r, hosts in racks.items()}

    def all_hosts(self):
        return [h for hosts in self.racks.values() for h in hosts]

    def rack_of(self, host):
        for rack, hosts in self.racks.items():
            if host in hosts:
                return rack
        return None

    def fail_rack(self, rack):
        """A TOR switch or PDU dies: the whole rack and its hosts go with it."""
        self.racks[rack] = []


def place_naive(fleet, replicas):
    """Naive placement: just take the first N hosts, wherever they land.
    On a fleet where the first hosts share a rack, both replicas end up in one
    failure domain — the mistake this lab exists to show."""
    return fleet.all_hosts()[:replicas]


def place_anti_affinity(fleet, replicas):
    """Anti-affinity placement: no two replicas in the same rack. Round-robin the
    racks so replicas are spread across distinct failure domains."""
    chosen = []
    used_racks = set()
    # first pass: one host from each distinct rack
    for rack, hosts in fleet.racks.items():
        if len(chosen) >= replicas:
            break
        if hosts and rack not in used_racks:
            chosen.append(hosts[0])
            used_racks.add(rack)
    if len(chosen) < replicas:
        raise RuntimeError(
            f"cannot place {replicas} replicas with anti-affinity across "
            f"{len(fleet.racks)} racks — need at least that many racks")
    return chosen


def service_is_up(fleet, placement):
    """A service is up if at least one of its placed replicas is on a host that
    still exists (its rack hasn't failed)."""
    live_hosts = set(fleet.all_hosts())
    survivors = [h for h in placement if h in live_hosts]
    return len(survivors) > 0, survivors


def build_fleet():
    # Three racks, two hosts each. The first two hosts (rack-a) are what a naive
    # "take the first N" placement grabs — landing both replicas in one domain.
    return {
        "rack-a": ["a1", "a2"],
        "rack-b": ["b1", "b2"],
        "rack-c": ["c1", "c2"],
    }


def run():
    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"  ✓ {ok_msg}")
        else:
            log(f"  ✗ {fail_msg}")
            failures.append(fail_msg)

    step(1, "Build the fleet — three racks, each a failure domain")
    racks = build_fleet()
    for r, hosts in racks.items():
        log(f"  {r}: {', '.join(hosts)}   (shares one TOR switch + PDU)")
    log("  A rack is the blast radius of its switch and power — lose either, lose all its hosts.")

    step(2, "Place a 2-replica service TWO ways")
    naive_fleet = Fleet(racks)
    aa_fleet = Fleet(racks)
    naive = place_naive(naive_fleet, 2)
    aa = place_anti_affinity(aa_fleet, 2)
    log(f"  naive placement      : {naive[0]} ({naive_fleet.rack_of(naive[0])}), "
        f"{naive[1]} ({naive_fleet.rack_of(naive[1])})")
    log(f"  anti-affinity        : {aa[0]} ({aa_fleet.rack_of(aa[0])}), "
        f"{aa[1]} ({aa_fleet.rack_of(aa[1])})")
    naive_same = naive_fleet.rack_of(naive[0]) == naive_fleet.rack_of(naive[1])
    aa_diff = aa_fleet.rack_of(aa[0]) != aa_fleet.rack_of(aa[1])
    check(naive_same,
          "naive put BOTH replicas in the same rack — a hidden single point of failure",
          "naive placement unexpectedly spread the replicas")
    check(aa_diff,
          "anti-affinity put the replicas in DIFFERENT racks",
          "anti-affinity failed to spread the replicas")

    step(3, "DISASTER — a top-of-rack switch dies, taking rack-a with it")
    naive_fleet.fail_rack("rack-a")
    aa_fleet.fail_rack("rack-a")
    log("  rack-a is gone: a1, a2 are unreachable.")

    step(4, "Assess — which service survived?")
    naive_up, _ = service_is_up(naive_fleet, naive)
    aa_up, aa_surv = service_is_up(aa_fleet, aa)
    check(not naive_up,
          "naive service is DOWN — both replicas were in rack-a (LESSON 1: co-located replicas share a fate)",
          "naive service unexpectedly survived")
    check(aa_up,
          f"anti-affinity service is UP on {aa_surv} — one replica survived in another rack (LESSON 2: spread survives)",
          "anti-affinity service unexpectedly went down")

    step(5, "Scale the lesson — 3 replicas across 3 racks tolerate one rack loss")
    big = Fleet(build_fleet())
    three = place_anti_affinity(big, 3)
    log(f"  placed 3 replicas: {', '.join(f'{h} ({big.rack_of(h)})' for h in three)}")
    big.fail_rack("rack-b")
    up, surv = service_is_up(big, three)
    check(up and len(surv) == 2,
          f"lost rack-b, {len(surv)} of 3 replicas still serving — N+1 across domains (LESSON 3)",
          "3-replica service did not tolerate a single rack loss")

    log("\n" + "=" * 68)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the three lessons held:")
    log("  1. Co-located replicas share a fate — 'two copies' in one rack is one copy.")
    log("  2. Anti-affinity across failure domains is what 'highly available' means.")
    log("  3. N replicas across N domains tolerate one domain failure.")
    log("")
    log("The rename that makes it transferable:")
    log("  a rack is a fault domain is an availability zone is a placement constraint.")
    log("  This is the same lesson whether you designed the rack or the cloud handed")
    log("  you the AZ — placement is always your job.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args()  # no options — the drill runs the same way every time
    rc = run()
    sys.exit(rc)


if __name__ == "__main__":
    main()
