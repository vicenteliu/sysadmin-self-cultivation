---
name: linux-triage
description: Triage a Linux host with the toolbox's linux-triage script, read the result honestly, and route each red flag to its fix — patch, hardening, or a pointer. Use when the user says "check this box", "triage this server", "is this host healthy", "something's wrong with this machine", "帮我看看这台机器", or hands you a server that's misbehaving. The user-facing entry point to the toolbox.
created: 2026-07-16
owner: Vicente Liu
---

# Skill: linux-triage

The first move of every incident, made invokable: run the repo's read-only
[`toolbox/linux-triage`](../../../toolbox/linux-triage/) script, interpret the
report the way an experienced admin would, and — this is the point — route each
red flag to the right next step in the toolbox instead of leaving the user with a
wall of numbers.

## The premise

An AI can run a triage script and paraphrase its output. What earns trust is the
*judgment layer*: knowing that a load spike with idle CPU means I/O wait, that 90%
disk on `/var` is usually logs or a runaway container, that a failed unit is where
to look first. This skill supplies the routing; the human keeps the call.

## Workflow

### 1 — Run the triage

From the repo (or with the script copied to the host):

```bash
./toolbox/linux-triage/linux-triage.sh          # unprivileged
sudo ./toolbox/linux-triage/linux-triage.sh     # fuller: journal + shadow-adjacent
```

It's **read-only** — safe to run anywhere, no confirmation needed. Exit code: `0`
no red flags, `1` red flags found, `2` not Linux. Run with `sudo` when you can —
the journal-error and some counters are richer.

### 2 — Read the report (what each section is telling you)

- **host / load** — `load1 > 2× cores` is the flag. High load with *idle* CPU in
  the top-5 = I/O wait or lock contention, not CPU starvation. Say which.
- **cpu / memory top-5** — name the actual consumer, don't just report the percent.
- **disk** — `≥90%` on a filesystem, or **inodes ≥90%** (the sneaky one: space
  free but "No space left on device" — millions of tiny files).
- **network** — interface down, or a surprising listener/established count.
- **services** — any failed systemd unit is the highest-signal line in the report;
  start there.
- **recent log errors** — correlate with the failed unit or the resource flag.

### 3 — Route each flag to its fix (the toolbox loop)

This is the value. Don't stop at "here's what's wrong":

| Triage flag | Route to |
| --- | --- |
| Pending updates suspected / old kernel | [`toolbox/patch-report`](../../../toolbox/patch-report/) to inventory, then the [`patch`](../../../toolbox/ansible/roles/patch/) Ansible role to apply |
| Weak security posture (SSH, firewall off) | [`toolbox/baseline-check`](../../../toolbox/baseline-check/) to audit, then [`baseline_hardening`](../../../toolbox/ansible/roles/baseline_hardening/) to remediate — or invoke the **harden-baseline** skill |
| Disk ≥90% | investigate before deleting: `du -x -d1` from the mount; logs → check journald retention; a full `/var/lib/docker` → image/volume prune with the user's ok |
| Failed unit | `systemctl status <unit>` + `journalctl -u <unit> -n50`; fix the root cause, don't just restart |
| Unknown user accounts / lifecycle drift | [`toolbox/user-lifecycle`](../../../toolbox/user-lifecycle/) + the [`user_lifecycle`](../../../toolbox/ansible/roles/user_lifecycle/) role |

### 4 — Honesty (the repo's law, applied to a live box)

- Report what the tool observed, not what you assume. If a section was empty
  because a command was missing (no `ss`, no `journalctl`), **say so** — don't
  present a gap as "all clear".
- Never run a destructive fix off a triage flag without showing the user the
  remediation and getting a yes. Triage is read-only by design; keep that contract
  through to the fix.
- On a host you didn't provision, surface surprises rather than smoothing them
  over ("this box has IP forwarding on — intended router, or drift?").

## What this skill is not

Not a monitoring system and not a replacement for one — it's the *first look* when
you're staring at a box that's misbehaving, with a clear path from symptom to the
toolbox's fix. For a fleet, run it per host and aggregate the verdicts.
