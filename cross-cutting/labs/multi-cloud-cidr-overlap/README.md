# Lab — overlapping CIDRs break the interconnect (and there is no central router)

**Goal:** feel the #1 concrete blocker a single-cloud admin hits the day they connect two
clouds — you **cannot peer or VPN networks whose address space overlaps**. This is a hard
mechanical fact, verified in AWS, Azure (Cloud Adoption Framework), and GCP docs: peering is
*refused* if the CIDRs overlap. And every cloud's console nudges you toward `10.0.0.0/16`, so
two clouds — or a cloud and on-prem — that each took the default **cannot be joined**.

```
each cloud owns a CIDR     (AWS 10.0/16, Azure 10.1/16, ...)
and keeps its OWN routes   (no central router; each side needs a route to the others)
deliver(src, dst_ip)       routes only if the destination is unambiguous AND src has a route
```

What it drills — five lessons:
1. **Non-overlapping + routes both ways → traffic flows.** The interconnect works.
2. **Overlapping CIDR → ambiguous.** `10.0.0.5` is owned by *both* clouds, so the interconnect
   can't decide who owns it — peering/VPN is refused.
3. **Missing route on one side → dropped.** There's no central router; each cloud routes itself,
   so a forgotten route-table entry blackholes traffic.
4. **Asymmetric routing → half-open.** A forward route without a return route lets the request
   through but drops the reply.
5. **On-prem `10.0.0.0/8` swallows the clouds → the hybrid overlap trap.** A broad on-prem supernet
   overlaps every cloud's `10.x` range — plan non-overlapping address space across *all* of it.

## Why local

No cloud accounts, no VPN gateways, no bill. The drill is a ~150-line model of cross-cloud
routing — CIDR ownership, the ambiguity that overlap creates, and per-cloud (not central) route
tables — so the *logic* is what you inspect, not three consoles. Runs anywhere Python does, and
in CI.

## Run

```bash
python3 cidr_overlap_drill.py
```

## What you'll see

Five narrated steps, each with an `OK`/`XX`: a clean bidirectional interconnect; an overlapping
pair detected as ambiguous; a dropped packet from a missing route; a half-open connection from
asymmetric routing; and an on-prem supernet colliding with a cloud range. Ends with a PASS verdict
and `exit 0`.

## Verify (the important part)

Exit `0` = every lesson held; it doubles as a CI check. Now **break the model on purpose** — two
independent sabotage vectors:

```bash
python3 cidr_overlap_drill.py --sabotage ignore-overlap   # pretend overlap is fine -> steps 2 & 5 misroute, exit 1
python3 cidr_overlap_drill.py --sabotage central-router   # assume a magic router with every route -> steps 3 & 4 miss the gap, exit 1
```

If overlapping addresses can still be "routed," the ambiguity wasn't real; if a magic central
router always has a route, per-cloud route tables weren't load-bearing. The failures are the
proof the model matters.

## The point

Two single-cloud reflexes get corrected here at once. First, **"the cloud handles addressing and
routing for me"** — true *inside* one VPC/VNet, false *across* clouds, where you inherit the
on-prem discipline of enterprise IP address management (IPAM) spanning every cloud and on-prem.
Second, **"I'll just peer them later"** — you can't, if the ranges overlap, and re-IP-ing live
subnets is the one multi-cloud decision that's genuinely painful to reverse. Plan non-overlapping
CIDRs first. See the [multi-cloud support note](../../multi-cloud-support.md) for the full seam
catalog and [`the-stack/02-network.md`](../../the-stack/02-network.md) for the per-cloud
networking primitives.

## Teardown

None — it's a single self-contained script. Delete the folder to remove it.
