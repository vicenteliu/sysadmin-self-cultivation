# patch-report

> **Inputs:** none (`--quiet` for counts only) · **Outputs:** pending-updates report
> on stdout · **Risk:** read-only — never installs, never refreshes metadata ·
> **Root:** not needed for the report

What's waiting to be patched, and does the box need a reboot? One command answers
both, on either package family: apt (Debian/Ubuntu — `/var/run/reboot-required`
with the packages that caused it) or dnf/yum (RHEL family — `check-update`,
security-advisory count, `needs-restarting -r`).

Deliberate scope cut: this tool reports on the metadata the box **already has** —
it never runs `apt update`/`dnf makecache` itself, because a read-only report
should not be the thing that hits your mirrors. Refresh on your own schedule.

## Usage

```bash
./patch-report.sh            # full list
./patch-report.sh --quiet    # counts + verdict only — cron/agent friendly
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | fully patched, no reboot pending |
| 1 | updates pending and/or reboot required |
| 2 | no supported package manager / query failed |

## Tested on

Ubuntu 24.04 container (pending-updates, clean, and reboot-required cases).
dnf path verified on a Rocky Linux 9 container. Lab-verified, not
production-hardened.
