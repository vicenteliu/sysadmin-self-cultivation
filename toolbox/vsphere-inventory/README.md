# vsphere-inventory

> **Inputs:** `--server host[:port]`, `--user`, password via `VSPHERE_PASSWORD` ·
> **Outputs:** one JSON inventory document (stdout or `--out`), optional per-VM
> CSV · **Risk:** read-only — logs in, reads properties, logs out; changes
> nothing · **Root:** not needed (a read-only vSphere role is enough)

Inventory a vSphere environment with **nothing but Python's standard library** —
no pyvmomi, no SDK, no govc. The tool speaks the vim25 SOAP API directly (XML
over HTTPS via `urllib`): it is both a working migration-assessment input and a
demonstration that "the vCenter API" is just XML you can read.

Collects per VM: power state, vCPU/memory, guest OS, firmware (BIOS/EFI),
virtual hardware version, every disk (capacity, thin/thick, VMDK vs **RDM**),
every NIC (model, network, MAC), and the **snapshot count** — exactly the facts
[`vm-migration-assess`](../vm-migration-assess/) scores. Plus hosts, datastores,
and networks. The JSON schema is shared with
[`pve-inventory`](../pve-inventory/), so source and destination of a
VMware→Proxmox move compare field by field.

## Usage

```bash
export VSPHERE_PASSWORD='…'                     # keeps the secret off argv
./vsphere-inventory.py --server vcenter.lab --user readonly@vsphere.local \
    --out inventory.json --csv vms.csv
./vsphere-inventory.py --server 127.0.0.1:8989 --user user --insecure   # lab/vcsim
```

`--insecure` skips TLS verification for self-signed lab vCenters. A dedicated
read-only vSphere role is the right credential — the tool only ever reads.

Prefer a maintained CLI for daily interactive work? `govc` does all of this and
more. This tool exists where a zero-dependency, auditable, single-file collector
is worth having (jump hosts, agents, teaching).

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | inventory written |
| 1 | cannot reach the endpoint, or vCenter returned a fault (bad credentials, …) |
| 2 | usage: no password provided |

## Tested on

macOS 26 (Python 3.14) and Ubuntu 24.04 container (Python 3.12) against
**vcsim** (govmomi's official vCenter simulator, 4 VMs/4 hosts): full document
verified including snapshot counting (chained snapshots) and disk/NIC device
parsing; connection-refused and missing-password paths exercised. vSphere ✋
depth is real (VCP-level, production years); a run against a **real** vCenter
is still pending — treat output-shape details against production vCenter
versions as lab-verified, not production-proven.
