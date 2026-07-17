# vm-migration-assess

> **Inputs:** a [`vsphere-inventory`](../vsphere-inventory/) JSON document
> (`--in FILE` or stdin) · **Outputs:** per-VM verdict report (or `--json`) ·
> **Risk:** read-only — assessment only, touches neither environment ·
> **Root:** not needed

Answer the first question of every VMware→Proxmox conversation: **which of
these VMs can actually move, and what will each one fight you on?** Feed it the
inventory JSON; every VM gets a verdict — `EASY` / `MODERATE` / `HARD` — with
the specific findings behind it, so the output reads as a work plan, not a score.

## The rule table

| Severity | Finding | Why it matters |
| --- | --- | --- |
| **hard** | RDM (raw device mapping) disk | no direct Proxmox equivalent — that storage needs a redesign |
| **hard** | end-of-life Windows guest (XP/2003/2000/NT) | virtio drivers unavailable; legacy-device workarounds only |
| moderate | snapshots present | chains don't convert — consolidate before export |
| moderate | modern Windows guest | virtio drivers must go in before/at cutover |
| minor | non-virtio NIC on Linux | model changes to virtio; the driver is already in-kernel |
| minor | EFI firmware | recreate as OVMF VM, check Secure Boot expectations |
| minor | > 2 TiB total disk | plan the transfer window |
| minor | virtual hardware older than vmx-10 | verify ancient-guest assumptions |
| info | powered on | schedule downtime or a re-sync cutover |
| info | thick-provisioned disks | they export at full size |

Verdict = the worst finding (info/minor → EASY). The rules are one readable
function — extend them where your estate needs it.

## Usage

```bash
./vm-migration-assess.py --in inventory.json          # human report
../vsphere-inventory/vsphere-inventory.py … | ./vm-migration-assess.py   # piped
./vm-migration-assess.py --in inventory.json --json   # machine-readable
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | assessed; no HARD VMs |
| 1 | assessed; at least one HARD VM (both humans and pipelines branch on this) |
| 2 | input isn't a readable inventory document |

## Tested on

macOS 26 (Python 3.14) and Ubuntu 24.04 container (Python 3.12): live chain
against vcsim (snapshot VM correctly MODERATE) plus a crafted fixture that
fires every rule (RDM→HARD, XP→HARD, Windows 2022 + EFI + 3 TiB + snapshots
→ MODERATE, clean Linux → EASY with zero findings). The rule *weights* encode
judgment, not measurements — lab-verified, and deliberately conservative.
