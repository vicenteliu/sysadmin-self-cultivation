# user-lifecycle

> **Inputs:** a CSV of `username,action[,groups]` · **Outputs:** the plan (dry-run)
> or per-user results (`--apply`) · **Risk:** **dry-run by default** — changes state
> only with `--apply` · **Root:** required for `--apply`

Joiner/mover/leaver at scale is a CSV, not fifty hand-typed `useradd` lines.
This applies a batch of user creates and disables from one file — the densest
skill cluster in real infrastructure JDs, done reproducibly.

Two safety choices worth knowing:

- **Dry-run is the default.** With no `--apply` it prints exactly what it would do
  and touches nothing. You always see the plan before it runs.
- **Disable ≠ delete.** A leaver is **locked, expired, and logged out**, never
  `userdel`'d — their files and your audit trail must survive. Deletion is a
  separate, deliberate decision. Created accounts are **locked with no password**;
  hand them an SSH key or a `passwd` reset out of band (no secrets on the CLI).

## CSV format

```
# username,action,groups
alice,create,sudo|docker
carol,create
bob,disable
```

`#` comments and blank lines are ignored; `groups` is optional and create-only.

## Usage

```bash
./user-lifecycle.sh users.csv              # dry-run — prints the plan
sudo ./user-lifecycle.sh users.csv --apply # execute
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | ok (planned, or applied with no failures) |
| 1 | one or more actions failed |
| 2 | usage error, bad CSV, or `--apply` without root |

## Tested on

Ubuntu 24.04 container (dry-run and `--apply` as root: create with/without groups,
idempotent re-run, disable, and missing-user cases). Lab-verified, not
production-hardened.
