# role: user_lifecycle

Declarative users: define the desired state, the role converges to it. The
Ansible counterpart of the [`user-lifecycle`](../../user-lifecycle/) script,
same law — **disabled ≠ deleted**.

## The `users` variable

A list; each entry:

```yaml
users:
  - name: alice
    state: present            # default if omitted
    groups: [sudo, docker]
    ssh_key: "ssh-ed25519 AAAA… alice@laptop"
  - name: carol
    state: present
  - name: bob
    state: disabled           # locked + expired, NOT removed
  - name: dave
    state: absent             # explicit deletion (see safety)
```

| `state` | Effect |
| --- | --- |
| `present` (default) | account exists, in `groups`, `ssh_key` deployed, unlocked |
| `disabled` | locked + expired — unusable, but home and audit trail preserved |
| `absent` | account **removed** (home kept unless `user_remove_home: true`) |

| Variable | Default | Notes |
| --- | --- | --- |
| `users` | `[]` | the desired-state list above |
| `user_remove_home` | `false` | on `absent`, also delete the home directory |

## Safety

- **`disabled` is the leaver default**, not `absent` — you almost never want to
  delete a departing user's files and break your audit trail on day one.
- `absent` deletes; it's opt-in per user, and home removal is a second opt-in.
- Run `--check --diff` to preview convergence.

## Usage

```bash
ansible-playbook -i inventory.ini ../playbooks/users.yml --check --diff
ansible-playbook -i inventory.ini ../playbooks/users.yml
```

Keep the `users` list in your inventory/group_vars so it's reviewable in Git —
joiner/mover/leaver as a pull request.

## Tested on

Ubuntu 24.04 container: `present` with groups + SSH key, **idempotent re-run
`changed=0`**, and `disabled` (lock + expire) all verified end to end. The
`absent` path uses the module's `state: absent` (not exercised in the container
run — deletion is opt-in per user). Uses `ansible.posix.authorized_key` (bundled
with the `ansible` package). Lab-verified, not production-hardened.
