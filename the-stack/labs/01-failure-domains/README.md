# Lab 01 — Failure domains (place replicas so a rack loss survives)

**Goal:** make the central lesson of [chapter 01](../../01-physical.md) tangible — **a
failure domain is the blast radius of a shared dependency, and "highly available" means
placing replicas so no single domain failure takes them all.** You'll run a drill that
models a fleet as racks, places a service two ways, kills a rack, and watches which
placement survives.

**You'll practice:** thinking in failure domains (rack = TOR switch + PDU =
blast radius), the difference between naive and anti-affinity placement, and the
rename that makes it transferable — *a rack is a fault domain is an availability zone
is a placement constraint.*

## Why this lab is pure-local

No cloud, no credentials, no cost, no external packages — just Python 3.8+. Racks and
hosts are modeled in memory; "failing a rack" is removing it. The point isn't the
simulation — it's the **placement judgment**, which is identical whether you designed
the rack or the cloud handed you the AZ.

## Run it

```bash
python3 failure_domains.py
```

Exit code `0` means every assertion held, so it doubles as a CI check. What you'll
see:

```
=== 2. Place a 2-replica service TWO ways ===
  naive placement      : a1 (rack-a), a2 (rack-a)
  anti-affinity        : a1 (rack-a), b1 (rack-b)
...
=== 4. Assess — which service survived? ===
  ✓ naive service is DOWN — both replicas were in rack-a (LESSON 1)
  ✓ anti-affinity service is UP on ['b1'] — one replica survived (LESSON 2)
=== 5. Scale the lesson — 3 replicas across 3 racks tolerate one rack loss ===
  ✓ lost rack-b, 2 of 3 replicas still serving — N+1 across domains (LESSON 3)
```

## The point

- **Co-located replicas share a fate.** Two copies in one rack is one copy — the
  "highly available" service that both naive replicas landed in rack-a is a single
  point of failure hiding in plain sight.
- **Anti-affinity across failure domains is what HA *means*.** Forcing the replicas
  into different racks is the whole difference between surviving a rack loss and not.
- **N replicas across N domains tolerate one domain failure** — the N+1 idea, made
  concrete.
- **Placement is always your job.** The cloud gives you fault domains; it doesn't stop
  you from putting both replicas in one. This drill is that mistake, caught in code
  instead of during the outage.

This is the [chapter-01 lab spec](../../01-physical.md) in runnable form, and it's the
same discipline the [self-host](../../../platforms/self-host/) platform designs by hand
and every cloud's AZ/fault-domain model asks you to use.

## Teardown

Nothing persistent is created — the drill runs in memory and exits. Nothing to clean
up.
