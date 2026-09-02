---
kind: lab
axis: platforms
themes: [virtualization]
platforms: [vsphere]
marker: "🔨"
summary: "A cluster is sized right on the day it is built; then it grows one power-on at a time, and admission control is the only thing that notices N+1 stop being true. Six hosts, five hundred VMs, and the refusal that is the guarantee."
---
# Lab — N+1 is a number that decays

> 🌐 **Languages:** English (default) · [中文](../../../../docs/zh/platforms/vsphere/labs/n-plus-one-decays/README.md)

> **Inputs:** none · **Outputs:** which VMs restart and which stay down, under four cluster
> states · **Risk:** none — no vCenter, no ESXi, no credentials · **Root:** not needed

**Goal:** run the [architecture note](../../architecture.md)'s arithmetic forward in time.
Six hosts, not four, is what lets one host die while all five hundred VMs keep running at
78% — *and admission control is what makes that a guarantee instead of a hope.* The note
says it on the day the cluster is built. This drill is the year after: the cluster grows,
the guarantee refuses a power-on, somebody disables it, and the next host loss is the
outage N+1 was bought to prevent.

**You'll practise:** reading a refusal as the guarantee doing its job, sizing growth
against N+1 rather than against free memory, setting restart priority *before* the event
that uses it, and treating the swap lead time after a dead host as the exposure window
it is.

## Why this lab is pure-local

The [arc's third run](../README.md#run-03--watch-ha-restart-a-vm-failure-domains-made-tangible)
hard-powers a nested host and watches HA restart a VM, and you should do that — the
`VMHost` column changing under your eyes is the failure domain in your hands. But the
lesson underneath is capacity arithmetic over a year of growth, and a nested lab will not
show you a year. Hosts are dictionaries with a capacity; VMs are four gigabytes each with
a restart priority; HA is a loop that places the dead host's VMs on the least-loaded
survivor until there is no room. No vCenter, no credentials, no `pip install`. Python
stdlib, and CI runs it.

## Run it

```bash
python3 platforms/vsphere/labs/n-plus-one-decays/n_plus_one_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Sized right on day one.** Six hosts of 512 GB; admission control keeps one host
   back; five hundred VMs power on and use 65% of the cluster.

2. **A host dies, and that is HA working.** Its 83 VMs restart on the survivors, which
   now run everything at **78%** — the number in the architecture note, reproduced
   rather than quoted.

3. **The cluster grows, and the guarantee refuses you.** A hundred and fifty more VMs
   are requested; 140 power on and the 141st is refused, at exactly 2560 GB of 2560
   usable. That refusal is N+1, saying no.

4. **The standard click.** Admission control off, all 150 power on, the cluster shows
   85% of six hosts and plenty of free memory. The host dies again: 98 VMs restart and
   **10 have nowhere to go.** HA on paper is HA that ran out of room.

5. **Who stays down is a decision or an accident.** With restart priority set, the ten
   left down are the ten somebody ranked lowest. With no priorities, the same ten are
   `vm-440 … vm-494` — production VMs, chosen by the order HA happened to reach them.

6. **N+1 is one failure.** At the admission-control limit, the first host loss is
   absorbed. A second, before the first host is replaced, leaves **128 VMs down** with
   the guarantee on. The swap lead time is the exposure window, which is why the
   operations note calls the dead host the incident.

## Verify (don't take the script's word for it)

```bash
python3 n_plus_one_drill.py --break-it admission-off        # exit 1
python3 n_plus_one_drill.py --break-it ha-ignores-capacity  # exit 1
```

`admission-off` runs the cluster the way the click assumes — the refusal was a nuisance
and the memory was free — and two assertions break: the growth is no longer refused,
and the note's cluster no longer keeps its own promise. `ha-ignores-capacity` runs HA the
way the word *HA* is heard — everything comes back — and eight break, because a restart
that never checks room restarts VMs onto hosts that are already full, which is not a
restart.

Then drive the model yourself from this directory:

```bash
python3 -c '
from n_plus_one_drill import Cluster, fill
c = Cluster(6); print(fill(c, 700, "vm"), "of 700 accepted; refused from", c.refused[0])
'
```

Change `HOSTS` to seven in the file and rerun: the refusal moves by exactly one host's
worth of VMs, which is the whole of what buying a seventh host buys.

## The point

- **The refusal is the guarantee.** A power-on that admission control refuses is N+1
  telling you the cluster has reached the size it was built for. Disabling it does not
  add capacity; it removes the only thing that knew.
- **Free memory is not headroom.** 85% of six hosts is 102% of five, and five is what
  you have on the day that matters.
- **Restart priority is set on a quiet day.** After the event it is too late to say
  which VMs mattered; HA will have decided, in whatever order it reached them.
- **N+1 is one failure, and the swap lead time is the window.** [Operations](../../operations.md)
  calls the HA event HA working and the dead host the incident; this drill is the
  arithmetic of why: with the guarantee spent, the next loss is an outage until the
  shelf delivers a host.

## Teardown

None. The drill holds everything in memory and writes nothing.
