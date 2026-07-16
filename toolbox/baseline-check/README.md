# baseline-check

> **Inputs:** none · **Outputs:** PASS/FAIL/INFO/SKIP per check + summary ·
> **Risk:** read-only, changes nothing · **Root:** optional — shadow and
> effective-sshd checks need it

A deliberately small, high-signal hardening audit — ten checks a reviewer would
look at first: SSH root-login and password-auth posture, an active firewall,
UID-0 uniqueness, empty password fields, world-writable files under `/etc`,
default umask, IP forwarding, persistent journald, and whether automatic patching
exists at all.

Honest scope: this is a **CIS-flavored sample, not a CIS scanner** — it tells you
whether the basics hold, not whether you're compliant. And it only *audits*:
remediation belongs to configuration management (the toolbox's Ansible wave), not
to a script making one-off edits.

## Usage

```bash
./baseline-check.sh          # unprivileged: some checks SKIP or read config files
sudo ./baseline-check.sh     # full: effective sshd -T values + shadow check
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | no FAILs (INFO/SKIP may still deserve reading) |
| 1 | one or more FAILs |
| 2 | not Linux |

## Tested on

Ubuntu 24.04 container (unprivileged + root; passing and deliberately-broken
configurations). Lab-verified, not production-hardened.
