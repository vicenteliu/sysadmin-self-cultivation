# pve-inventory

> **Inputs:** none on a PVE node (live `pvesh get` calls); or `--from DIR` with
> captured output · **Outputs:** one JSON inventory document (stdout or
> `--out`), same schema as [`vsphere-inventory`](../vsphere-inventory/) ·
> **Risk:** read-only — only `pvesh get`, never writes to the cluster ·
> **Root:** live mode runs where `pvesh` runs (a PVE node shell)

The destination side of a VMware→Proxmox move: inventory a Proxmox VE cluster
into the **same JSON schema** `vsphere-inventory` emits, so before/after
migration states compare field by field — VM by VM, disk by disk, NIC by NIC.

Collects per VM: power state, vCPU/memory, guest OS type, firmware
(SeaBIOS/OVMF → `bios`/`efi`), machine type, disks (capacity, qcow2/raw/
passthrough), NICs (model, bridge, MAC), snapshot count (the `current` marker
excluded). Plus nodes, storage, and the bridges the VM configs reference.

## Usage

```bash
# on a PVE node
./pve-inventory.py --out pve.json

# anywhere, from captured output — capture on the node with:
#   pvesh get /cluster/resources --output-format json > resources.json
#   pvesh get /version --output-format json > version.json
#   pvesh get /nodes/<node>/qemu/<vmid>/config   --output-format json > config-<vmid>.json
#   pvesh get /nodes/<node>/qemu/<vmid>/snapshot --output-format json > snapshot-<vmid>.json
./pve-inventory.py --from ./captured/
```

[`fixtures/`](fixtures/) holds a complete example capture (a PVE 8 node with a
Linux VM and an OVMF Windows 11 VM) — it documents the exact file shapes and
gives you a dry run: `./pve-inventory.py --from fixtures`.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | inventory written |
| 1 | `pvesh` missing/failed (live), or the capture directory is incomplete |
| 2 | usage error |

## Tested on

Parser and schema verified on macOS 26 (Python 3.14) and Ubuntu 24.04 container
(Python 3.12) against the bundled PVE-8-shaped fixtures (`--from`), including
cdrom/EFI-disk/TPM-state exclusion and `current`-snapshot handling. **A live
run on a real PVE node is still the operator's step** — the fixtures match
documented `pvesh` output shapes, but this line will be updated only after the
tool has run against real metal. Honest scope: home-lab Proxmox, not fleet
production experience.
