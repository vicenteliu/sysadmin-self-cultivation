# linux-triage

> **Inputs:** none · **Outputs:** one triage report on stdout · **Risk:** read-only
> · **Root:** optional — journal errors and some counters say more with it

The first move of every incident: one command, one screen, the whole picture —
load vs. cores, top CPU/memory consumers, disk and inode pressure, interface
addresses, connection counts, failed systemd units, and the last 20 log errors.
Anything alarming is repeated as a `FLAG:` line and counted into the exit code, so
both a human and an automation can branch on "is something actually wrong here?"

## Usage

```bash
./linux-triage.sh            # unprivileged: full report, journal may be partial
sudo ./linux-triage.sh       # everything
```

Red-flag thresholds: load1 > 2× cores · disk or inode usage ≥ 90% · any failed
systemd unit.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | report produced, no red flags |
| 1 | red flags found (count printed in the verdict) |
| 2 | not Linux |

## Tested on

Ubuntu 24.04 container (unprivileged + root). Uses `/proc`, `ps`, `free`, `df`,
`ip`, `ss`, `systemctl`, `journalctl` — standard on any systemd distro; degrades
gracefully where a command is missing. Lab-verified, not production-hardened.
