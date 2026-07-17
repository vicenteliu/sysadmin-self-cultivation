# snapshot-audit

> **Inputs:** one or more inventory JSON files ([`vsphere-inventory`](../vsphere-inventory/)
> and/or [`pve-inventory`](../pve-inventory/); stdin when none) · **Outputs:**
> hygiene report of flagged VMs (or `--json`) · **Risk:** read-only — flags only;
> deleting or consolidating stays a human decision · **Root:** not needed

A snapshot you forgot is a time bomb: it grows until the datastore chokes, it
drags I/O, and a deep chain is exactly what a migration trips over. This tool
reads inventory documents — **both hypervisors, one audit**, since
`vsphere-inventory` and `pve-inventory` share a schema — and flags every
snapshot that violates three thresholds:

| Threshold | Default | Why |
| --- | --- | --- |
| `--max-age-days` | 3 | VMware's own guidance: don't keep a snapshot past ~72 hours |
| `--max-depth` | 2 | deep chains hurt I/O and don't convert in migrations |
| `--max-count` | 3 | many snapshots on one VM usually means nobody owns cleanup |

A snapshot with no creation time is reported as `INFO` (age can't be judged),
and an inventory produced before snapshot detail existed gets an `INFO` telling
you to re-collect — the audit never guesses.

## Usage

```bash
./snapshot-audit.py inventory.json                      # one side
./snapshot-audit.py vsphere.json pve.json               # both sides, one audit
./snapshot-audit.py --max-age-days 7 --json inv.json    # your policy, machine-readable
../vsphere-inventory/vsphere-inventory.py … | ./snapshot-audit.py    # piped
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | audited; no hygiene warnings (INFO lines allowed) |
| 1 | at least one warning — something needs cleanup |
| 2 | input isn't a readable inventory document |

## Tested on

macOS 26 (Python 3.14) and Ubuntu 24.04 container (Python 3.12): a live
3-deep vcsim snapshot chain (depth warning) plus the bundled PVE fixtures
(~12-day-old snapshots → age warnings) audited in a single run; relaxed
thresholds go clean; detail-less legacy documents and unreadable input take
the INFO / exit-2 paths. Thresholds encode published guidance and judgment,
not measurements — tune them to your estate.
