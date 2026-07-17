# role: baseline_hardening

Remediates the items [`baseline-check`](../../baseline-check/) audits — SSH
posture, default umask, a sysctl baseline, and persistent journald. Every item
is a switch; anything that can lock you out defaults to **off**.

## Variables (see [`defaults/main.yml`](defaults/main.yml))

| Variable | Default | Notes |
| --- | --- | --- |
| `harden_ssh` | `true` | manage sshd posture |
| `harden_ssh_permit_root` | `prohibit-password` | `no` or `prohibit-password` |
| `harden_ssh_password_auth` | `false` | **⚠️ set only when key auth already works** — `false` writes `PasswordAuthentication no` |
| `harden_umask` | `true` / `027` | `/etc/login.defs` default umask |
| `harden_sysctl` | `true` | writes `/etc/sysctl.d/99-baseline-hardening.conf` |
| `harden_journald_persistent` | `true` | creates `/var/log/journal` (takes effect at next journald restart / reboot — the role won't bounce journald and interrupt logging) |
| `harden_firewall` | **`false`** | ufw enable — off by default; allows OpenSSH first when on |

Each SSH change is validated with `sshd -t` before it's written, so a bad edit
never restarts a broken config.

## Safety

- **Run `--check --diff` first.** Every task supports check mode.
- `PasswordAuthentication no` will lock out anyone without a working SSH key —
  the reason it defaults to *keeping password auth* until you opt in.
- Firewall enable is opt-in and allows OpenSSH before switching the default
  policy to deny.

## Usage

```bash
ansible-playbook -i inventory.ini ../playbooks/harden.yml --check --diff
ansible-playbook -i inventory.ini ../playbooks/harden.yml
```

## Tested on

Ubuntu 24.04 container: config writes correct (`PermitRootLogin prohibit-password`,
`PasswordAuthentication no`, sysctl drop-in), **idempotent re-run `changed=0`,
`failed=0`**, and `--check` mode clean. Each SSH edit is validated with `sshd -t`
before the reload is queued.

The `reload sshd` handler issues a service reload, which needs a running init
system — it runs on real systemd hosts but can't execute in a bare container
(a common Ansible-in-container limitation), so the reload itself is exercised on
real machines, not in the container run above. Uses `community.general.ufw` for
the opt-in firewall path (bundled with the `ansible` package). Lab-verified, not
production-hardened.
