---
kind: lab
axis: platforms
themes: [virtualization]
platforms: [openstack]
marker: "🧭"
summary: "The signature OpenStack incident, as a model you can wedge: a full message queue stops the API while nine instances keep answering, the tenant-only dashboard stays green, and the outage becomes the tenants' at the first change they need."
---
# Lab — the cloud is down and the VMs are up

> 🌐 **Languages:** English (default) · [中文](../../../../docs/zh/platforms/openstack/labs/the-cloud-is-down-the-vms-are-up/README.md)

> **Inputs:** none · **Outputs:** what the API, a ping and two health checks each say, across
> one incident · **Risk:** none — no DevStack, no cloud, no credentials · **Root:** not needed

**Goal:** make the [operations note](../../operations.md)'s signature incident something
you have already lived through. *A full message queue or a stuck database stops the API
while every already-running VM keeps humming untouched.* The note says to internalize
that before it teaches you, and to monitor the control plane itself, not just the
tenants. This drill wedges the queue, asks the API and the instances the same question,
and then does the thing the note's warning is really about: it lets a compute host die
while the queue is still full.

**You'll practise:** telling a control-plane outage from a tenant outage, asking the
day-2 health question in both halves — *tenants' VMs up, and is the control plane itself
up?* — and recognising the moment the first kind becomes the second.

## Why this lab is pure-local

The [arc's third run](../README.md) stops `n-api` on DevStack and pings a floating IP
while `openstack server list` errors, and you should do that — the API failing under
your hands while the instance answers is the lesson in one terminal. But DevStack is
one service on one node, and the finding is about what the whole control plane is a
path *for*. Here five services are a dictionary of booleans, three compute hosts carry
nine instances, an API call is a path through every service and a ping is a path
through none of them. No DevStack, no credentials, no `pip install`. Python stdlib, and
CI runs it.

## Run it

```bash
python3 platforms/openstack/labs/the-cloud-is-down-the-vms-are-up/control_plane_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **A healthy cloud.** `server list` returns nine instances on three hosts; nine pings
   answer; the health check is green.

2. **RabbitMQ fills up.** `server list` fails with *rabbitmq is down*. Nine pings still
   answer. **The cloud is down and the VMs are up** — the queue is on the API's path and
   on nobody else's.

3. **One question, two halves.** The tenants' dashboard is green: their instances
   answer. A health check that also asks whether the control plane is up is red. The
   first is what a monitor built from the tenants' side reports for the whole incident,
   which is exactly why it cannot be the monitor.

4. **The first change somebody needs.** `compute2` dies while the queue is still full.
   Three instances stop answering. `server evacuate` fails; a tenant's own
   `server reboot` fails. **Nothing can change** — and every change is an API call.
   This is the moment the control-plane outage becomes the tenants' outage.

5. **The queue drains.** One `server evacuate` moves the three instances; nine answer;
   the health check is green. The fix was always a control-plane fix.

6. **The imported instinct.** From a managed cloud, *API down* means *cloud down*: nine
   instances down. Reality: zero down, and every API call failing. Wrong in both
   directions — nothing was down, and nothing could be fixed.

## Verify (don't take the script's word for it)

```bash
python3 control_plane_drill.py --break-it control-plane-is-data-plane  # exit 1
python3 control_plane_drill.py --break-it green-is-healthy             # exit 1
```

`control-plane-is-data-plane` makes the instances die with the API — the managed-cloud
instinct, run as a model — and eight assertions break, starting with the one that says
the VMs are up. `green-is-healthy` makes the tenants' dashboard the whole of the health
question, and exactly two break: the check goes green with the control plane down, and
so does the one that says a monitor must ask both halves.

Then wedge a different service yourself from this directory:

```bash
python3 -c '
from control_plane_drill import Cloud, ControlPlaneDown
c = Cloud(); c.services["keystone"] = False
try: c.server_list()
except ControlPlaneDown as e: print("API:", e)
print("instances answering:", sum(c.ping(n) for n in c.instances), "of 9")
'
```

Every service gives the same shape — the API fails whole, the instances do not notice —
because the control plane is one path and the data plane is another.

## The point

- **A control-plane outage is not a tenant outage.** Running instances do not consult
  the API to keep running. That is what makes the incident survivable, and what makes
  it invisible to a monitor that only asks the tenants.
- **Ask the health question in both halves.** *Tenants' VMs up* and *control plane up*
  are different facts with different pagers. The operations note lists them as one
  bullet with two clauses; this drill is why the second clause is there.
- **The outage becomes the tenants' at the first change.** An evacuation, a reboot, a
  scale-out, an autoscaler's heal — every one is an API call, and a dead compute host
  during a wedged queue is three instances that stay down until the queue drains.
- **Fix the control plane; the workloads were never the problem.** Restarting
  computes, reimaging hosts and rebuilding instances are the instinct's remedies, and
  all of them are API calls too.

## Teardown

None. The drill holds everything in memory and writes nothing.
