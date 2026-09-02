---
kind: guided-run
axis: platforms
themes: [virtualization]
platforms: [vsphere]
marker: "🔨"
summary: "Three guided runs against a lab vCenter (or nested ESXi) — on this platform, the honest note is that they already ran, in production, for years."
---
# vSphere — Guided runs

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/platforms/vsphere/labs/README.md)

Three guided runs against a lab vCenter (or nested ESXi). Reading about vMotion and
doing it are different skills — and on this platform, the honest note is that these
*already ran*, in production, for years.

**These are [guided runs](../../../CONTEXT.md), not labs.** Each needs a real environment,
so nothing here can assert that you did it and CI cannot run it. That is the whole of the
distinction and it is not a demotion — a guided run reaches real latency, real error
messages and real bills, which no model does.

> **Ground rules:** use a **lab/nested cluster**, snapshot before destructive steps,
> and clean up VMs when done. Never test on production hosts.

## Why the command line

vSphere has a great GUI — and the pros still automate with **PowerCLI** (or `govc`),
because the CLI is **faster** (no click-through on 200 VMs), **exact**, **repeatable**
(the same script every maintenance window), and **reviewable**. The GUI is for
one-offs and looking; PowerCLI is for operating a fleet. This is the platform where
that difference is most obvious: nobody clicks through a rolling host upgrade twice.

## The three-run arc

### Run 01 — Connect + inventory (the "list everything")

Connect to vCenter and inventory the estate from **PowerCLI** — the move you'd never
do by clicking on a real cluster:

```powershell
Connect-VIServer -Server vcenter.lab.local -User administrator@vsphere.local

# every VM, its host, power state, and resource use — one line
Get-VM | Select Name, PowerState, NumCpu, MemoryGB, VMHost | Sort-Object VMHost | Format-Table

# every host and its cluster/connection state
Get-VMHost | Select Name, ConnectionState, @{N='Cluster';E={$_.Parent}}, Version | Format-Table

# datastores + free space (a full datastore is a mass outage — watch this)
Get-Datastore | Select Name, @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}, @{N='CapGB';E={[math]::Round($_.CapacityGB)}} | Format-Table
```

**Verify:** the counts match the vCenter inventory view — and you got them in one
command instead of three tabs.

### Run 02 — Provision a VM from a template

Clone from a golden template with a customization spec — the image pipeline
([`the-stack/03`](../../../the-stack/03-compute-and-images.md)) on vSphere:

```powershell
# clone a VM from a template onto a chosen host + datastore
New-VM -Name lab-vm01 -Template "ubuntu-2204-template" `
  -VMHost (Get-VMHost esxi01.lab.local) -Datastore (Get-Datastore vsanDatastore) `
  -OSCustomizationSpec "linux-dhcp"

Start-VM -VM lab-vm01

# confirm placement + tools status
Get-VM lab-vm01 | Select Name, VMHost, PowerState, @{N='Tools';E={$_.ExtensionData.Guest.ToolsStatus}}
```

**Verify:** the VM boots on the host you named with the customized identity — cattle,
not a hand-built pet. **Teardown:** `Stop-VM lab-vm01 -Confirm:$false; Remove-VM lab-vm01 -DeletePermanently -Confirm:$false`.

### Run 03 — Watch HA restart a VM (failure domains, made tangible)

The [`the-stack/01`](../../../the-stack/01-physical.md) failure-domain lesson on the
platform it came from — plus the maintenance-mode evacuation every upgrade uses:

```powershell
# put a host into maintenance mode — DRS/vMotion evacuates its VMs with no downtime
Set-VMHost -VMHost esxi02.lab.local -State Maintenance -Evacuate

# ...confirm VMs moved off it
Get-VMHost esxi02.lab.local | Get-VM      # should be empty

# bring it back
Set-VMHost -VMHost esxi02.lab.local -State Connected

# (HA drill, lab-safe) hard-power a host and watch HA restart its VMs elsewhere:
#   in a nested lab, power off an ESXi node and run:
Get-VM lab-vm01 | Select Name, PowerState, VMHost   # VMHost changes as HA restarts it
```

**Verify:** VMs evacuate on maintenance mode with no downtime; on a simulated host
failure, HA restarts them on a surviving host — the failure domain, in your hands.

## Beyond the arc — a pure-local drill

The three-run arc above needs a lab vCenter. One more lab needs **nothing** — a
pure-local, stdlib-only, self-verifying drill tied to the [operations note](../operations.md):

### `n-plus-one-decays/` — N+1 is a number that decays ✅ built (pure-local)

Runs the architecture note's six-host cluster forward in time and proves that admission
control's refusal *is* the guarantee: growth is refused at exactly the point N+1 stops
being true, the click that disables it leaves ten VMs down at the next host loss, and a
second loss inside the swap window is an outage even with the guarantee on. See
**[`n-plus-one-decays/`](n-plus-one-decays/)**.

```bash
python3 n-plus-one-decays/n_plus_one_drill.py   # exit 0 = the lessons held; runs in CI
```

---

Honest note: this is the 🔨 platform — these labs are the production work written down,
not a ramp. The GUI/CLI point lands hardest here: at fleet scale, you *only* operate
via PowerCLI.
