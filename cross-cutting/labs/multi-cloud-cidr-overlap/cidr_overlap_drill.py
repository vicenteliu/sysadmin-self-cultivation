#!/usr/bin/env python3
"""
Multi-cloud drill — overlapping CIDRs break the interconnect, and there is no central router.

Pure-local, stdlib-only. Models the #1 concrete blocker a single-cloud admin hits the day
they connect two clouds: you CANNOT peer / VPN networks whose address space overlaps
(verified in AWS, Azure CAF, and GCP docs — peering is refused if CIDRs overlap). Every
cloud's console nudges you to 10.0.0.0/16, so two clouds — or a cloud and on-prem — that each
defaulted to the same range cannot be joined: a destination IP is ambiguous.

    each cloud owns a CIDR      (AWS 10.0/16, Azure 10.1/16, ...)
    and keeps its OWN routes    (no central router; each side needs a route to the others)
    deliver(src, dst_ip)        routes only if the destination is unambiguous AND src has a route

Five lessons fall out of that one model:
  1. non-overlapping + routes both ways  -> traffic flows (round trip)
  2. overlapping CIDR                     -> the destination is AMBIGUOUS -> interconnect refuses
  3. missing route on one side            -> dropped (no central router; each cloud routes itself)
  4. asymmetric routing (one-way route)   -> half-open: the reply is dropped
  5. on-prem 10.0.0.0/8 swallows the clouds -> the hybrid overlap trap (plan IPAM across ALL of it)

Run clean and every lesson holds -> exit 0 (doubles as a CI check).
Run with --sabotage to break the model and watch the guarantees fall -> exit 1:
  --sabotage ignore-overlap  : pretend overlap is fine (pick one arbitrarily) -> steps 2 & 5 misroute
  --sabotage central-router  : assume a magic router with every route -> steps 3 & 4 miss the gap
"""

import argparse
import sys


def log(msg=""):
    print(msg)


def step(n, title):
    log(f"\n[{n}] {title}")


def ip2int(ip):
    a, b, c, d = (int(x) for x in ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def cidr_contains(cidr, ip):
    net, bits = cidr.split("/")
    bits = int(bits)
    mask = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF if bits else 0
    return (ip2int(ip) & mask) == (ip2int(net) & mask)


def host_in(cidr):
    """A representative host IP inside a CIDR (network address + 5)."""
    net = cidr.split("/")[0]
    a, b, c, d = (int(x) for x in net.split("."))
    return f"{a}.{b}.{c}.{d + 5}"


def deliver(src, dst_ip, nets, detect_overlap=True, central_router=False):
    """Route a packet from network `src` to `dst_ip`. Returns a status:
    delivered | ambiguous-overlap | no-route | no-destination."""
    owners = [name for name, n in nets.items() if cidr_contains(n["cidr"], dst_ip)]
    if not owners:
        return "no-destination"
    if len(owners) > 1 and detect_overlap:
        return "ambiguous-overlap"          # the interconnect can't decide which cloud owns it
    target = owners[0]
    if target == src:
        return "delivered"                  # local traffic
    if central_router or any(cidr_contains(r, dst_ip) for r in nets[src]["routes"]):
        return "delivered"
    return "no-route"                       # src has no route to the destination cloud


def round_trip(a, b, nets, **kw):
    """A connection needs BOTH directions to work."""
    fwd = deliver(a, host_in(nets[b]["cidr"]), nets, **kw)
    rev = deliver(b, host_in(nets[a]["cidr"]), nets, **kw)
    return fwd, rev


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage", choices=["ignore-overlap", "central-router"],
                    help="break the model: 'ignore-overlap' = don't detect ambiguous CIDRs; "
                         "'central-router' = assume a magic router that has every route")
    args = ap.parse_args()
    kw = dict(detect_overlap=(args.sabotage != "ignore-overlap"),
              central_router=(args.sabotage == "central-router"))
    if args.sabotage:
        log(f"  !! SABOTAGE ENABLED: {args.sabotage} !!")

    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"    OK  {ok_msg}")
        else:
            log(f"    XX  {fail_msg}")
            failures.append(fail_msg)

    # 1. Non-overlapping address space + a route on each side -> traffic flows both ways.
    step(1, "AWS 10.0/16 <-> Azure 10.1/16, non-overlapping, routes both ways")
    nets = {
        "aws":   {"cidr": "10.0.0.0/16", "routes": ["10.1.0.0/16"]},
        "azure": {"cidr": "10.1.0.0/16", "routes": ["10.0.0.0/16"]},
    }
    fwd, rev = round_trip("aws", "azure", nets, **kw)
    log(f"    aws->azure={fwd}, azure->aws={rev}")
    check(fwd == "delivered" and rev == "delivered",
          "non-overlapping CIDRs + a route on each side -> the interconnect works both ways",
          "non-overlapping networks with routes both ways should deliver")

    # 2. Overlapping CIDR -> the destination is ambiguous -> peering/VPN is refused.
    step(2, "AWS 10.0/16 <-> Azure 10.0/16, OVERLAPPING")
    nets = {
        "aws":   {"cidr": "10.0.0.0/16", "routes": ["10.0.0.0/16"]},
        "azure": {"cidr": "10.0.0.0/16", "routes": ["10.0.0.0/16"]},
    }
    status = deliver("aws", "10.0.0.5", nets, **kw)
    log(f"    aws -> 10.0.0.5 : {status}")
    check(status == "ambiguous-overlap",
          "10.0.0.5 is owned by BOTH clouds -> ambiguous -> you cannot peer/VPN overlapping CIDRs",
          "an address inside two overlapping CIDRs must be detected as ambiguous, not routed")

    # 3. Non-overlapping, but a route is missing on one side -> dropped (no central router).
    step(3, "Non-overlapping, but AWS has no route to GCP")
    nets = {
        "aws": {"cidr": "10.0.0.0/16", "routes": []},          # forgot to add the remote route
        "gcp": {"cidr": "10.2.0.0/16", "routes": ["10.0.0.0/16"]},
    }
    status = deliver("aws", host_in(nets["gcp"]["cidr"]), nets, **kw)
    log(f"    aws -> {host_in(nets['gcp']['cidr'])} : {status}")
    check(status == "no-route",
          "each cloud routes itself — a missing route-table entry drops traffic (there is no central router)",
          "traffic to a cloud the source has no route to should be dropped")

    # 4. Asymmetric routing: forward route exists, return route does not -> half-open.
    step(4, "Asymmetric: AWS->Azure route exists, Azure->AWS does not")
    nets = {
        "aws":   {"cidr": "10.0.0.0/16", "routes": ["10.1.0.0/16"]},
        "azure": {"cidr": "10.1.0.0/16", "routes": []},          # no return route
    }
    fwd, rev = round_trip("aws", "azure", nets, **kw)
    log(f"    aws->azure={fwd}, azure->aws(reply)={rev}")
    check(fwd == "delivered" and rev == "no-route",
          "the request flows but the REPLY is dropped — routes must exist in BOTH directions",
          "asymmetric routing should let the request through but drop the reply")

    # 5. Hybrid overlap: an on-prem 10.0.0.0/8 swallows every cloud's 10.x range.
    step(5, "On-prem 10.0.0.0/8 + cloud 10.x -> the hybrid overlap trap")
    nets = {
        "onprem": {"cidr": "10.0.0.0/8",  "routes": ["10.0.0.0/8"]},   # a /8 covers all of 10.*
        "aws":    {"cidr": "10.0.0.0/16", "routes": ["10.0.0.0/8"]},
    }
    status = deliver("onprem", "10.0.0.5", nets, **kw)
    log(f"    onprem -> 10.0.0.5 : {status} (both the /8 and the /16 claim it)")
    check(status == "ambiguous-overlap",
          "a broad on-prem range overlaps the cloud ranges -> plan non-overlapping CIDRs across ALL of it (IPAM)",
          "an on-prem supernet overlapping a cloud range must be detected as ambiguous")

    # verdict
    log("\n" + "=" * 74)
    if failures:
        log(f"XX FAIL — {len(failures)} lesson(s) broke:")
        for f in failures:
            log(f"    - {f}")
        if args.sabotage:
            log("\n(expected: --sabotage breaks the model, so the guarantees fall.)")
        log("=" * 74)
        return 1
    log("OK PASS — all five multi-cloud networking lessons held:")
    log("    overlapping CIDRs make the destination ambiguous -> no peering/VPN;")
    log("    there is no central router (each cloud needs its own routes, both ways);")
    log("    and an on-prem supernet can swallow the clouds.")
    log("    Plan non-overlapping address space across every cloud AND on-prem — first.")
    log("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
