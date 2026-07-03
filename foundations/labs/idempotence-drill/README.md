# Lab — Idempotence & `set -euo pipefail` (fragile vs. safe, felt in bash)

**Goal:** make the central [foundations](../../README.md) lesson tangible — **an
idempotent script (safe to run twice) is infrastructure; a fragile one is a
liability, and `set -euo pipefail` is the line between a tool and a footgun.** You'll
run a drill that builds a fragile script and a safe one, runs each repeatedly, and
checks the difference.

**You'll practice:** spotting non-idempotent operations (the unconditional append,
the bare `mkdir`), why a missing `set -e` masks failures, and the safe pattern —
strict mode, a required-argument guard, `mkdir -p`, and check-then-append.

## Why this lab is pure-local

No dependencies beyond `bash` + coreutils, no cloud, no root. It works in a throwaway
`mktemp` directory and cleans up after itself. The point is the muscle memory: after
this, a non-idempotent line *looks* wrong to you.

## Run it

```bash
bash idempotence_drill.sh
```

Exit code `0` means every assertion held — it doubles as a CI check. Add `--keep` to
leave the workspace for inspection. What you'll see:

```
=== 1. The FRAGILE script — no safety, not idempotent ===
  ✓ the fragile script DOUBLED its config line on the 2nd run (LESSON 1)
  ✓ it reported SUCCESS (exit 0) despite mkdir failing — no set -e (LESSON 2)
=== 2. The SAFE script — set -euo pipefail + idempotent ===
  ✓ IDEMPOTENT — the line is present exactly once after 3 runs (LESSON 3)
  ✓ with no argument it FAILS FAST (the ${1:?} guard) (LESSON 4)
```

## The point

- **Non-idempotent operations double on re-run.** `echo x >> file` appends every
  time; `mkdir` (no `-p`) crashes the second time. The fragile script re-run leaves a
  duplicated config line — "run it twice" broke it.
- **Without `set -e`, a script masks its own failures** — the fragile script's
  `mkdir` failed on the second run, but it reported exit `0` and kept going, doing
  damage with a half-set state. That's how a "successful" script leaves a broken box.
- **The safe pattern converges.** `set -euo pipefail`, `${1:?...}` to refuse an empty
  argument, `mkdir -p`, and `grep -qxF ... || echo >>` to append only-if-absent —
  run it once or a hundred times, the state is identical.
- **This is what every IaC tool is built on.** Ansible's "the package is present" and
  Terraform's plan/apply are idempotence, productized. You just felt the raw version
  in bash — which is why the [iac chapter](../../../cross-cutting/iac-and-config.md)
  says if you internalized idempotence here, you already understand the core of every
  tool there.

## Teardown

The drill cleans up its `mktemp` workspace automatically. If you ran with `--keep`,
remove the printed path (`rm -rf /var/folders/.../tmp.XXXX`).
