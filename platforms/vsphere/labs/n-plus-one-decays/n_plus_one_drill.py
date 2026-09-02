#!/usr/bin/env python3
"""
n_plus_one_drill.py — N+1 is a number that decays, and admission control is the only
thing that notices.

The [architecture note](../../architecture.md) sizes the cluster for five hundred VMs at
six hosts, not four: six is what lets one host die while all five hundred keep running at
78% — "and admission control is what makes that a guarantee instead of a hope." The
[operations note](../../operations.md) says the HA event is HA *working*, and that the
incident is the dead host, "replaced before the cluster loses its N+1."

This drill is that arithmetic, run forward in time. A cluster is sized right on the day
it is built. Then it grows, one power-on at a time, and the only thing standing between
the growth and the guarantee is a refusal nobody enjoys — until somebody disables it.

Five things it measures rather than asserts:
  1. sized at N+1, a host loss restarts every VM, and the survivors sit at 78%
  2. growth is refused at exactly the point where N+1 would stop being true
  3. with admission control off, the same growth succeeds — and the next host loss
     leaves VMs down, in the order restart priority chose
  4. restart priority decides WHICH VMs stay down; without it, the order is accident
  5. N+1 is one failure: before the dead host is swapped, a second loss is an outage
     even with the guarantee on — the swap lead time is the exposure

    python3 n_plus_one_drill.py
    python3 n_plus_one_drill.py --break-it admission-off        # exit 1
    python3 n_plus_one_drill.py --break-it ha-ignores-capacity  # exit 1

--break-it runs the cluster the way the instinct assumes: the refusal is a nuisance and
the cluster has free memory, so admission control is off; or HA means every VM comes
back, so a restart never runs out of room. Neither is how a cluster behaves.

No vCenter, no ESXi, no credentials. Pure stdlib and deterministic. Exit code 0 means
every assertion about the lesson held.
"""

import argparse
import sys
from dataclasses import dataclass, field

BREAK = None   # --break-it sets one of the modes above; the cluster consults it


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



# --- the model: hosts, VMs, and the two decisions HA makes -----------------------

HOST_GB = 512            # memory per host; the unit of everything below
HOSTS = 6                # the architecture note's workload cluster
VM_GB = 4                # the average VM; five hundred of them is 2000 GB
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Host:
    name: str
    capacity: int = HOST_GB
    alive: bool = True
    vms: list = field(default_factory=list)

    def used(self):
        return sum(vm.gb for vm in self.vms)

    def free(self):
        return self.capacity - self.used()


@dataclass
class VM:
    name: str
    gb: int = VM_GB
    priority: str = "medium"
    host: str = None          # None means powered off, or down after an HA event


class Cluster:
    """Placement goes to the least-loaded live host, which is what DRS does and why
    every host carries a mix of everything. HA reserves one host's worth of capacity
    when admission control is on; a power-on that would eat into it is refused, which
    is the guarantee doing its job."""

    def __init__(self, hosts, admission_control=True):
        self.hosts = {f"esxi{i:02d}": Host(f"esxi{i:02d}") for i in range(1, hosts + 1)}
        self.admission_control = admission_control
        self.vms = {}
        self.refused = []

    # --- capacity ---
    def live(self):
        return [h for h in self.hosts.values() if h.alive]

    def total(self):
        return sum(h.capacity for h in self.live())

    def used(self):
        return sum(h.used() for h in self.live())

    def usable(self):
        """What admission control lets you fill: everything minus one host."""
        if self.admission_control and BREAK != "admission-off":
            return self.total() - HOST_GB
        return self.total()

    def utilisation(self):
        return self.used() / self.total()

    # --- the two decisions ---
    def power_on(self, vm):
        if self.used() + vm.gb > self.usable():
            self.refused.append(vm.name)
            return False
        host = min(self.live(), key=lambda h: h.used())
        if host.free() >= vm.gb:
            host.vms.append(vm)
            vm.host = host.name
            self.vms[vm.name] = vm
            return True
        self.refused.append(vm.name)
        return False

    def fail_host(self, name):
        """A host dies. HA restarts its VMs on the survivors, highest restart priority
        first, until there is no room — and then it stops, because there is no room."""
        host = self.hosts[name]
        host.alive = False
        orphans = sorted(host.vms, key=lambda v: (PRIORITY_ORDER[v.priority], v.name))
        host.vms = []
        restarted, down = [], []
        for vm in orphans:
            vm.host = None
            target = min(self.live(), key=lambda h: h.used())
            # The break: HA "brings everything back" — a restart never checks room.
            if BREAK == "ha-ignores-capacity" or target.free() >= vm.gb:
                target.vms.append(vm)
                vm.host = target.name
                restarted.append(vm)
            else:
                down.append(vm)
        return restarted, down


def fill(cluster, count, prefix, priority="medium"):
    """Power on `count` VMs; return how many the cluster accepted."""
    accepted = 0
    for i in range(count):
        accepted += cluster.power_on(VM(f"{prefix}-{i:03d}", priority=priority))
    return accepted


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", choices=["admission-off", "ha-ignores-capacity"],
                    help="run the cluster the way the instinct assumes; the drill must then fail")
    args = ap.parse_args()
    global BREAK
    BREAK = args.break_it

    log((__doc__ or "").strip().split("\n\n")[0])
    if BREAK:
        log(f"\n  !! --break-it {BREAK} !!")

    step(1, "Sized right on day one: six hosts, five hundred VMs, admission control on")
    c = Cluster(HOSTS)
    on = fill(c, 500, "vm")
    log(f"  {HOSTS} hosts × {HOST_GB} GB = {c.total()} GB; admission control keeps {HOST_GB} GB back")
    log(f"  powered on {on} of 500 VMs → {c.used()} GB used, {c.utilisation():.0%} of the cluster")
    check(on == 500, "five hundred VMs fit under the guarantee — the note's arithmetic holds",
          "the note's own cluster refused its own five hundred VMs")

    step(2, "A host dies. HA restarts its VMs elsewhere — that is HA working")
    restarted, down = c.fail_host("esxi03")
    log(f"  esxi03 lost with {len(restarted) + len(down)} VMs; HA restarted {len(restarted)}, "
        f"{len(down)} stayed down")
    log(f"  the five survivors now run everything at {c.utilisation():.0%}")
    check(not down, "every VM is back — one host loss was the failure N+1 was sized for (LESSON 1)",
          f"{len(down)} VMs stayed down after a single host loss at the sized load")
    check(round(c.utilisation(), 2) == 0.78,
          "the survivors sit at 78% — the number in the architecture note, reproduced",
          f"the survivors sit at {c.utilisation():.0%}, not the note's 78%")

    step(3, "Months later the cluster has grown. The guarantee is the thing that refuses you")
    c = Cluster(HOSTS)
    fill(c, 500, "vm")
    more = fill(c, 150, "new")
    log(f"  150 more VMs requested; admission control accepted {more}, refused {150 - more}")
    log(f"  the first refusal is at VM {c.refused[0] if c.refused else '—'}: "
        f"{c.used()} GB used of {c.usable()} GB usable")
    check(more < 150 and c.used() + VM_GB > c.usable(),
          f"growth stopped at exactly the point where N+1 would stop being true (LESSON 2)",
          "the cluster accepted growth that N+1 cannot survive — nothing refused it")

    step(4, "The standard click: disable admission control, because the VM has to run")
    loose = Cluster(HOSTS, admission_control=False)
    fill(loose, 500, "vm")
    lows = fill(loose, 150, "batch", priority="low")
    log(f"  admission control off: the same 150 power on ({lows}/150), cluster at "
        f"{loose.utilisation():.0%} of six hosts — plenty of free memory, on paper")
    restarted, down = loose.fail_host("esxi03")
    log(f"  esxi03 lost: HA restarted {len(restarted)}, and {len(down)} VMs have no host to go to")
    check(lows == 150, "with the guarantee off, the growth that was refused now succeeds — the instinct works",
          "admission control was off and the cluster still refused the growth")
    check(len(down) > 0,
          f"…and the next host loss leaves {len(down)} VMs down: HA on paper is HA that ran out of room (LESSON 3)",
          "HA restarted every VM on a cluster that no longer had room for them")

    step(5, "Restart priority decides who stays down. Without it, accident does")
    only_low = down and all(vm.priority == "low" for vm in down)
    log(f"  the {len(down)} VMs still down are: "
        + ", ".join(sorted({vm.priority for vm in down})) + " priority")
    unranked = Cluster(HOSTS, admission_control=False)
    fill(unranked, 500, "vm")
    fill(unranked, 150, "batch")            # same growth, nobody set a priority
    _, down2 = unranked.fail_host("esxi03")
    names = sorted(vm.name for vm in down2)
    log(f"  the same cluster with no priorities set: the {len(down2)} down are "
        + (f"{names[0]} … {names[-1]} — whoever HA reached last" if names else "nobody"))
    check(only_low, "the VMs left down are the ones somebody ranked lowest (LESSON 4)",
          "VMs of higher priority stayed down while low-priority ones restarted")
    check(down2 and any(vm.name.startswith("vm-") for vm in down2),
          "with no priorities, production VMs are among the ones left down — the order was accident",
          "with no priorities set, HA still happened to spare every production VM")

    step(6, "N+1 is one failure. The swap lead time is the exposure window")
    c = Cluster(HOSTS)
    fill(c, 500, "vm")
    fill(c, 150, "new")                      # up to the guarantee, then refused
    at_limit = len(c.vms)
    c.fail_host("esxi03")
    _, down_second = c.fail_host("esxi05")   # before esxi03 was replaced
    log(f"  at the admission-control limit ({at_limit} VMs), esxi03 dies and HA holds")
    log(f"  esxi05 dies before esxi03 is replaced: {len(down_second)} VMs down — the guarantee "
        f"covered one failure, and the second arrived inside the swap window")
    check(len(down_second) > 0,
          "a second loss inside the swap window is an outage even with the guarantee on — "
          "N+1 was one failure, and the incident is the dead host (LESSON 5)",
          "two host losses at the N+1 limit left nothing down, which is not what N+1 means")

    return verdict([
        "  1. Sized at N+1, one host loss restarts every VM — that is HA working.",
        "  2. Growth is refused at exactly the point where N+1 would stop being true.",
        "  3. Admission control off: the growth succeeds, and the next loss leaves VMs down.",
        "  4. Restart priority chooses who stays down; without it, the order is accident.",
        "  5. N+1 is one failure. The swap lead time after a host dies is the exposure.",
        "",
        "The instinct this drill retired:",
        "  'the cluster has free memory, so the refusal is wrong' — the refusal IS the",
        "  guarantee. A cluster that never refuses is a cluster that will not survive",
        "  the failure it was sized for, and nothing will tell you until it happens.",
    ], broken=bool(BREAK))


if __name__ == "__main__":
    sys.exit(main())
