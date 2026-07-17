---
name: harden-baseline
description: Close the audit→remediate loop on a Linux host — run the baseline-check script to find hardening gaps, explain each FAIL, then apply the baseline_hardening Ansible role safely (check-mode first, lock-out-aware). Use when the user says "harden this box", "check/fix the security baseline", "is this server hardened", "apply CIS basics", "加固这台机器", or wants the hardening gaps found and fixed. Pairs the read-only audit with its remediation.
created: 2026-07-16
owner: Vicente Liu
---

# Skill: harden-baseline

The toolbox's audit→remediate loop for host hardening, made invokable: find the
gaps with the read-only [`baseline-check`](../../../toolbox/baseline-check/)
script, explain each one, then converge them with the
[`baseline_hardening`](../../../toolbox/ansible/roles/baseline_hardening/) Ansible
role — **safely**, because hardening over SSH is exactly how people lock
themselves out.

## The premise

Anyone can run a hardening role. The judgment is in *not breaking access*: knowing
that `PasswordAuthentication no` locks out a box without working keys, that
enabling a firewall before allowing SSH is a self-inflicted outage, that you show
the diff before you converge. AI supplies the speed; this skill supplies the
guardrails.

## Workflow

### 1 — Audit (read-only, safe anywhere)

```bash
sudo ./toolbox/baseline-check/baseline-check.sh
```

Ten high-signal checks (SSH posture, firewall, UID-0 uniqueness, empty passwords,
world-writable under `/etc`, umask, IP forwarding, persistent journald, auto-
patching). Exit `0` = no FAILs, `1` = one or more FAILs. This is a **CIS-flavored
sample, not a compliance scanner** — say so; don't oversell a clean run.

### 2 — Explain each FAIL (don't just list)

For every `FAIL`, tell the user what it means and what the fix will change — e.g.
"`PasswordAuthentication yes` means the box accepts password logins; the fix
writes `no`, which requires everyone to have a working SSH key first." `INFO`
lines (e.g. IP forwarding on) may be intentional — ask before treating them as
defects.

### 3 — Pre-flight the lock-out risks (mandatory)

Before converging, confirm with the user:

- **SSH keys work** for everyone who needs in — *before* setting
  `harden_ssh_password_auth: false`. If unsure, leave password auth on this pass.
- **Firewall stays off unless asked** (`harden_firewall` defaults off). If enabling,
  the role allows OpenSSH first — confirm the SSH port is what you think it is.
- You are **not hardening yourself out of the only access path**.

### 4 — Converge with the role (check-mode first)

Always dry-run, show the diff, then apply:

```bash
cd toolbox/ansible
ansible-playbook -i inventory.ini playbooks/harden.yml --check --diff   # preview
ansible-playbook -i inventory.ini playbooks/harden.yml                  # apply
```

Every item is a `defaults/` switch; tune per host (see the
[role README](../../../toolbox/ansible/roles/baseline_hardening/README.md)). SSH
edits are `sshd -t`-validated before the config reloads (reload, not restart —
existing sessions survive).

### 5 — Re-audit to prove it

Run `baseline-check` again; the FAILs you fixed should now PASS. Closing the loop
*with evidence* is the whole point — "I ran a hardening role" is weaker than
"here's the before/after audit."

## Honesty (the repo's law)

- A clean `baseline-check` means the ten sampled basics hold — **not** "this host
  is compliant/secure." Never let the user hear the stronger claim.
- Show remediation diffs and get a yes before converging on a box you don't own.
- The `reload sshd` step needs a real init system; on a container/CI target it
  won't execute — note that rather than reporting a false success.

## What this skill is not

Not full CIS remediation, not a hardened-image replacement. The fast, safe,
loop-closing pass that gets the common gaps found, explained, and fixed — with the
before/after audit as proof.
