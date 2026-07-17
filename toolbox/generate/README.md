# generate

> **Inputs:** a selection — `--profile NAME` or `--pick concern,concern` (+ optional
> `--platform`) · **Outputs:** a standalone toolbox pack written to `--out DIR` ·
> **Risk:** read-only towards the repo and your system — writes only inside `--out`,
> refuses a non-empty target without `--force` · **Root:** not needed

The customizable half of the toolbox: one command assembles the subset a given
shop actually needs — the matching scripts, their paired Ansible remediation
roles and playbooks, and every Agent Skill whose references are fully satisfied —
into a directory you can hand to a colleague or drop onto a jump host.

The pack keeps this repo's layout (`toolbox/…`, `.claude/skills/…`), so every
relative link and every documented command inside the copied files works
unchanged, and a generated top-level `README.md` says what's in the pack, how to
run it, and which conventions travel with it.

## Usage

```bash
./generate.py --list                                    # concerns, profiles, catalog
./generate.py --profile security-baseline --out ~/kit   # named scenario
./generate.py --pick triage,backup --out ./pack         # à-la-carte concerns
./generate.py --pick network --platform macos --out p   # platform filter
```

Profiles are just named concern sets — `linux-shop` (everything),
`security-baseline` (hardening + patching), `incident-response` (triage and the
fixes it routes to). Both live in [`catalog.json`](catalog.json), which is the
whole selection model: each tool/role carries concern + platform tags, each
skill lists what it requires. New tools join the catalog with one JSON entry.

## Honesty rules built in

- A skill ships **only when everything it references is in the pack** — a pack
  never contains a skill that points at a tool it doesn't carry.
- Docs that enumerate the whole toolbox (the charter, the Ansible line README)
  ship only with a full selection, for the same reason.
- Every copied tool keeps its own `Tested on:` line — the pack inherits the
  repo's honesty labels rather than re-asserting them.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | pack written (or `--list` shown) |
| 1 | bad selection: unknown concern/profile, or nothing matched |
| 2 | usage/environment: missing `--out`, non-empty target without `--force`, incomplete checkout |

## Tested on

Python 3.9+ stdlib only. Verified: macOS 26 (Python 3.14) and Ubuntu 24.04
container (Python 3.12) — generated `security-baseline`, `linux-shop`, and
platform-filtered packs; ran pack tools from the pack root and exercised the
refusal/unknown-selection paths. Lab-verified, not production-hardened.
