#!/usr/bin/env python3
"""
control_plane_drill.py — the cloud is down and the VMs are up, until the first change
somebody needs.

The [operations note](../../operations.md) calls it the signature OpenStack incident: a
full message queue or a stuck database stops the API while every already-running VM
keeps humming untouched. "The cloud is down but the VMs are up" is the failure mode to
internalize before it teaches you — and it means monitoring the control plane itself,
not just the tenants. The note's first day-2 question has two halves for that reason:
*tenants' VMs up, and is the control plane itself up?*

This drill is that incident, as a model you can wedge. Five services, three compute
hosts, nine instances. The API is a path through the control plane; a ping is a path
that never touches it.

Four things it measures rather than asserts:
  1. with the control plane wedged, every API call fails and every instance answers
  2. a health check that asks only the tenants' question stays green the whole time
  3. the outage becomes the tenants' outage at the first change they need — a dead
     compute host that cannot be evacuated, a reboot that cannot be issued
  4. the imported instinct — API down means cloud down — is wrong in both directions:
     the VMs were never down, and the recovery they will need is not available

    python3 control_plane_drill.py
    python3 control_plane_drill.py --break-it control-plane-is-data-plane  # exit 1
    python3 control_plane_drill.py --break-it green-is-healthy             # exit 1

--break-it runs the model the way the instinct assumes: instances die with the API, or
the tenants' dashboard is the whole of the health question. Neither is how the platform
behaves, and the drill must then fail.

No DevStack, no cloud, no credentials. Pure stdlib and deterministic. Exit code 0 means
every assertion about the lesson held.
"""

import argparse
import sys
from dataclasses import dataclass, field

BREAK = None   # --break-it sets one of the modes above; the model consults it


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



# --- the model: a control plane, compute hosts, and two kinds of path --------------

CONTROL_PLANE = ["keystone", "rabbitmq", "database", "nova-api", "neutron-server"]


class ControlPlaneDown(Exception):
    """What the CLI shows you: a 503, a timeout, or a connection refused — the request
    never reached the service that would have acted on it."""


@dataclass
class Instance:
    name: str
    host: str
    state: str = "ACTIVE"          # what Nova last recorded


@dataclass
class ComputeHost:
    name: str
    alive: bool = True


class Cloud:
    def __init__(self):
        self.services = {s: True for s in CONTROL_PLANE}
        self.hosts = {f"compute{i}": ComputeHost(f"compute{i}") for i in (1, 2, 3)}
        self.instances = {}
        for i, host in enumerate(self.hosts, start=1):
            for j in (1, 2, 3):
                name = f"web-{i}{j}"
                self.instances[name] = Instance(name, host)
        self.log = []

    # --- the control plane: every API call is a path through all of it ---
    def control_plane_up(self):
        return all(self.services.values())

    def api(self, call):
        """One request to the API. Fails whole if any control-plane service is down —
        Keystone to authenticate, the queue to dispatch, the database to record."""
        down = [s for s, up in self.services.items() if not up]
        if down:
            raise ControlPlaneDown(f"{call}: {down[0]} is down")
        return True

    def server_list(self):
        self.api("server list")
        return sorted(self.instances)

    def server_reboot(self, name):
        self.api(f"server reboot {name}")
        self.instances[name].state = "ACTIVE"
        return True

    def server_evacuate(self, host):
        """Rebuild a dead host's instances elsewhere. Needs every service: the
        scheduler picks a host over the queue, Nova records it in the database."""
        self.api(f"server evacuate --host {host}")
        survivors = [h for h in self.hosts.values() if h.alive]
        moved = 0
        for inst in self.instances.values():
            if inst.host == host:
                inst.host = survivors[moved % len(survivors)].name
                inst.state = "ACTIVE"
                moved += 1
        return moved

    # --- the data plane: a path that never touches the control plane ---
    def ping(self, name):
        inst = self.instances[name]
        # The break: the instinct that an API outage takes the workloads with it.
        if BREAK == "control-plane-is-data-plane" and not self.control_plane_up():
            return False
        return self.hosts[inst.host].alive and inst.state == "ACTIVE"

    # --- two health questions ---
    def tenants_green(self):
        """The dashboard a tenant sees: are my instances answering?"""
        return all(self.ping(n) for n in self.instances)

    def healthy(self):
        """The operations note's first question has two halves. A monitor that asks
        only the first is the monitor that was green through the whole incident."""
        if BREAK == "green-is-healthy":
            return self.tenants_green()
        return self.tenants_green() and self.control_plane_up()


def instinct_api_down_means_cloud_down(cloud):
    """The mental model imported from a managed cloud, where the API and the
    workloads are one product: if the API is down, the cloud is down."""
    return 0 if cloud.control_plane_up() else len(cloud.instances)   # instances "down"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", choices=["control-plane-is-data-plane", "green-is-healthy"],
                    help="run the model the way the instinct assumes; the drill must then fail")
    args = ap.parse_args()
    global BREAK
    BREAK = args.break_it

    log((__doc__ or "").strip().split("\n\n")[0])
    if BREAK:
        log(f"\n  !! --break-it {BREAK} !!")

    cloud = Cloud()

    step(1, "A healthy cloud: the API answers, and so do nine instances")
    listed = cloud.server_list()
    answering = sum(cloud.ping(n) for n in cloud.instances)
    log(f"  server list → {len(listed)} instances on {len(cloud.hosts)} compute hosts")
    log(f"  ping → {answering}/{len(cloud.instances)} answer; healthy() = {cloud.healthy()}")
    check(len(listed) == 9 and answering == 9 and cloud.healthy(),
          "the baseline holds: control plane up, nine instances answering",
          "the baseline is already broken")

    step(2, "RabbitMQ fills up. The API stops. Nothing else does")
    cloud.services["rabbitmq"] = False
    try:
        cloud.server_list()
        api_state = "answered"
    except ControlPlaneDown as e:
        api_state = f"FAILED ({e})"
    answering = sum(cloud.ping(n) for n in cloud.instances)
    log(f"  server list → {api_state}")
    log(f"  ping → {answering}/{len(cloud.instances)} still answer")
    check(api_state.startswith("FAILED"),
          "every API call fails — the control plane is one path, and the queue is on it",
          "the API kept answering with the message queue down")
    check(answering == 9,
          "every instance keeps humming — the cloud is down and the VMs are up (LESSON 1)",
          f"only {answering} of 9 instances answer: the workloads went down with the API")

    step(3, "The monitor that asks one question is green through the whole incident")
    log(f"  tenants' dashboard: {'GREEN' if cloud.tenants_green() else 'RED'}"
        f"   (are my instances answering? yes)")
    log(f"  healthy(): {cloud.healthy()}   (tenants' VMs up AND the control plane up?)")
    check(cloud.tenants_green(),
          "the tenant-only view is green — which is exactly why it cannot be the monitor",
          "the tenant-only view went red on a control-plane outage, which the model does not predict")
    check(not cloud.healthy(),
          "a health check that asks both halves of the question is red — monitor the control plane itself (LESSON 2)",
          "health reported green with the control plane down — the check asked only the tenants' question")

    step(4, "The first change somebody needs: compute2 dies while the queue is still full")
    cloud.hosts["compute2"].alive = False
    lost = [n for n, i in cloud.instances.items() if i.host == "compute2"]
    answering = sum(cloud.ping(n) for n in cloud.instances)
    log(f"  compute2 lost: {', '.join(lost)} stop answering — {answering}/9 up")
    try:
        cloud.server_evacuate("compute2")
        evac = "moved"
    except ControlPlaneDown as e:
        evac = f"FAILED ({e})"
    try:
        cloud.server_reboot("web-11")
        reboot = "issued"
    except ControlPlaneDown as e:
        reboot = f"FAILED ({e})"
    log(f"  server evacuate --host compute2 → {evac}")
    log(f"  a tenant's own `server reboot web-11` → {reboot}")
    check(evac.startswith("FAILED") and reboot.startswith("FAILED"),
          "nothing can change: no evacuation, no reboot, no scale — the outage is now the tenants' (LESSON 3)",
          "an API-driven change succeeded with the control plane down")
    check(answering == 6,
          "the three instances on compute2 are down and will stay down until the control plane returns",
          f"{answering} instances answer, which does not match one dead host of three")

    step(5, "The queue drains. Now the evacuation the tenants were waiting for can run")
    cloud.services["rabbitmq"] = True
    moved = cloud.server_evacuate("compute2")
    answering = sum(cloud.ping(n) for n in cloud.instances)
    log(f"  rabbitmq back → server evacuate --host compute2 moved {moved} instances; {answering}/9 answer")
    check(moved == 3 and answering == 9 and cloud.healthy(),
          "with the control plane back, one command restores the tenants — the fix was always a control-plane fix",
          "the control plane returned and the evacuation still did not restore the instances")

    step(6, "The imported instinct: 'the API is down, so the cloud is down'")
    cloud.services["database"] = False
    said = instinct_api_down_means_cloud_down(cloud)
    real = sum(1 for n in cloud.instances if not cloud.ping(n))
    log(f"  instinct: database stuck ⇒ {said} of 9 instances down")
    log(f"  reality:  {real} of 9 instances down, and every API call fails")
    check(said != real,
          "the instinct is wrong in both directions — the VMs were never down, and the recovery they will need is not available (LESSON 4)",
          "instinct and reality agreed — the drill proved nothing")

    return verdict([
        "  1. A wedged queue or database stops the API; every running instance keeps humming.",
        "  2. A monitor that asks only 'are the tenants' VMs up' is green for the whole incident.",
        "  3. The outage becomes the tenants' at the first change they need — and every change is an API call.",
        "  4. 'API down means cloud down' is wrong both ways: nothing was down, and nothing can be fixed.",
        "",
        "The question a managed cloud never makes you ask:",
        "  is the platform alive? Ask it of the control plane, on its own, before a tenant",
        "  asks it of you — because by then the answer is a dead compute host nobody can evacuate.",
    ], broken=bool(BREAK))


if __name__ == "__main__":
    sys.exit(main())
