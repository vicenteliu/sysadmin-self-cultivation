---
name: runnable-lab
description: Turn a concept into a pure-local, zero-dependency, self-verifying lab (exit code 0 = the lessons held), in the style of this repo's runnable drills. Prefers stdlib Python or bash so it needs no install and CI can run it. Use when the user says "make this a runnable lab", "turn this spec into code", "build a drill for X", "prove X in code", or wants to make a lab spec actually executable.
created: 2026-07-02
owner: Vicente Liu
---

# Skill: runnable-lab

Make a concept *tangible and self-proving* — a script someone runs to feel the lesson,
that asserts its own correctness. Modeled on this repo's runnable drills:
[backup-not-snapshot](../../../the-stack/labs/04-backup-not-snapshot/),
[failure-domains](../../../the-stack/labs/01-failure-domains/),
[idempotence-drill](../../../foundations/labs/idempotence-drill/),
[ci-cd-pipeline](../../../cross-cutting/labs/ci-cd-pipeline/). Read one before writing.

## What makes a good runnable lab (the bar)

- **Pure-local, zero-cost, zero-credential** — stdlib Python or bash, no cloud, no
  `pip install`, no root. Anyone can run it; CI can too.
- **Self-verifying** — it makes assertions and **exits 0 only if every lesson held**;
  non-zero with a clear message if not. It doubles as a test.
- **Teaches by *doing*, not describing** — it sets up a scenario, does the thing (or
  the wrong thing *and* the right thing side by side), and shows the difference.
- **Narrated** — prints numbered steps and ✓/✗ per assertion, so the run *is* the
  lesson.
- **Clean** — uses `mktemp` / in-memory / a `--keep`-gated workspace; leaves no stray
  artifacts (add the workspace dir to `.gitignore` if it writes to cwd).

## The pattern (the drills all share it)

1. **Set up** a small, honest model of the real thing (racks as dicts, a SQLite DB
   as "the database", two scripts as fragile-vs-safe).
2. **Do it two ways** where the lesson is a contrast (naive vs. anti-affinity;
   fragile vs. `set -euo pipefail`; replica vs. independent backup).
3. **Trigger the disaster** (kill a rack, `DROP TABLE`, re-run the fragile script).
4. **Assert the lessons** with a `check(cond, ok_msg, fail_msg)` helper that ✓/✗s
   and accumulates failures.
5. **Verdict** — print "PASSED — the lessons held" + the one-line takeaways, or
   "FAILED" + which assertions broke; `sys.exit(0/1)`.

## The workflow

1. **Pick the single lesson** the lab must make undeniable (e.g. "replication is not
   backup", "co-located replicas share a fate").
2. **Design the smallest model** that makes it visible, and the *contrast* that proves
   it (right vs. wrong).
3. **Write it** stdlib-only, with the narrated-steps + `check()` + verdict structure.
4. **Run it and confirm exit 0.** Then deliberately break the model to confirm it
   exits non-zero — a self-verifier that can't fail is worthless.
5. **Write a README** (goal / why pure-local / run command / what you'll see / the
   point / teardown), mirroring the existing lab READMEs.
6. **Wire it in:** flip the chapter's `## Lab` section from 🚧 spec to ✅ runnable with
   the exact run command; add a row to `the-stack/labs/README.md` if applicable.

## When the concept genuinely needs a cloud or a cluster

Some labs can't be pure-local (a real VPC, a kind cluster, a mesh). Then:
- Say so, and keep it **tear-down-able** with sandbox + budget-alarm ground rules
  (see [`platforms/aws/labs/`](../../../platforms/aws/labs/)).
- Still ship the *runnable* piece where possible — e.g. the CI/CD lab's tests run
  locally even though the pipeline runs on GitHub; a real, valid `ci.yml` kept out of
  the live workflows dir is a legitimate artifact.

## Guardrails

- Exit code is load-bearing: 0 = lessons held, non-zero = they didn't. Prove both.
- Clean up: no leftover files in git status after a run.
- Correctness over cleverness — the CLI commands / code must actually run, not look
  like they would. Run it before you call it done.
