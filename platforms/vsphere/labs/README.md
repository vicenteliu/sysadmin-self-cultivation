# vSphere — Labs

Tear-down-able exercises against a lab vCenter (or nested ESXi). Reading about vMotion
and doing it are different skills — and on this platform, the honest note is the labs
*already ran*, in production, for years.

> **Ground rules:** use a **lab/nested cluster**, snapshot before destructive steps,
> and clean up VMs when done. Never test on production hosts.

## Why the command line

vSphere has a great GUI — and the pros still automate with **PowerCLI** (or `govc`),
because the CLI is **faster** (no click-through on 200 VMs), **exact**, **repeatable**
(the same script every maintenance window), and **reviewable**. The GUI is for
one-offs and looking; PowerCLI is for operating a fleet. This is the platform where
that difference is most obvious: nobody clicks through a rolling host upgrade twice.

## The three-lab arc

### Lab 01 — Connect + inventory (the "list everything")

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

### Lab 02 — Provision a VM from a template

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

### Lab 03 — Watch HA restart a VM (failure domains, made tangible)

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

---

Honest note: this is the ✋ platform — these labs are the production work written down,
not a ramp. The GUI/CLI point lands hardest here: at fleet scale, you *only* operate
via PowerCLI.
