# Ansible line — the remediation half

> The [scripts](../) *find* problems (read-only, safe to run anywhere). These
> Ansible roles *fix* them — idempotently, declaratively, one control plane.
> Together they close the loop: `baseline-check` reports, `baseline_hardening`
> remediates; `patch-report` inventories, `patch` applies; `user-lifecycle`
> plans, `user_lifecycle` converges.

## Roles

| Role | Fixes what | Pairs with |
| --- | --- | --- |
| [`baseline_hardening`](roles/baseline_hardening/) | SSH posture, umask, sysctl, persistent journald (per-item switches) | [`baseline-check`](../baseline-check/) |
| [`patch`](roles/patch/) | apply pending updates (apt/dnf) + reboot orchestration | [`patch-report`](../patch-report/) |
| [`user_lifecycle`](roles/user_lifecycle/) | declarative users: present / disabled (lock, never delete by default) | [`user-lifecycle`](../user-lifecycle/) |

## Conventions (same six as the toolbox charter, applied to Ansible)

1. **Idempotent.** A second run reports `changed=0`. Verified, not assumed.
2. **Safe by default.** Everything supports `--check` (dry-run). Genuinely
   dangerous switches (firewall enable, auto-reboot, user deletion) default
   **off** and are called out in each role's README.
3. **Honest scope.** Each role's README carries a `Tested on:` line. Lab-verified
   in containers is not production-hardened, and it says so.
4. **Plain dependencies.** Targets the full `ansible` package (bundles
   `ansible.posix`), not just `ansible-core`. No extra Galaxy roles.
5. **Readable variables.** Every behavior is a documented `defaults/` variable —
   nothing hidden in tasks.
6. **Converge quietly, fail loudly.** Standard Ansible reporting; handlers only
   restart what actually changed.

## Run

```bash
# check mode first — see what WOULD change, touch nothing
ansible-playbook -i inventory.ini playbooks/harden.yml --check --diff

# then for real
ansible-playbook -i inventory.ini playbooks/harden.yml
ansible-playbook -i inventory.ini playbooks/patch.yml
ansible-playbook -i inventory.ini playbooks/users.yml
```

Local smoke test against the control node itself:

```bash
ansible-playbook -i 'localhost,' -c local playbooks/harden.yml --check --diff
```

See [`inventory.example.ini`](inventory.example.ini) for the inventory shape.

## What this is not

Not a full CIS remediation, not a replacement for a hardened base image or your
existing configuration management. A focused, honest, loop-closing set — if a
role hasn't been converged somewhere real, its README tells you where it *has*.
