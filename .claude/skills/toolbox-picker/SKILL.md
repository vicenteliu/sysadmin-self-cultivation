---
name: toolbox-picker
description: Given a sysadmin task or problem in plain language, pick the right toolbox tool or Ansible role, explain how to run it safely, and hand back the exact command. The navigator for this repo's toolbox. Use when the user describes a task ("I need to batch-create users", "check what needs patching", "find overlapping subnets") and isn't sure which tool fits, asks "what's in the toolbox", "is there a tool for X", or "怎么用工具箱做 X".
created: 2026-07-16
owner: Vicente Liu
---

# Skill: toolbox-picker

The navigator for [`toolbox/`](../../../toolbox/): the user describes what they
need in plain language, this skill picks the right tool or role, states its safety
level, and hands back the exact command — so the toolbox is usable without
memorizing what's in it.

## The map (task → tool)

Every job in the toolbox is either a **read-only script** (find/report, safe to
run anywhere) or an **Ansible role** (change state, idempotent). Most needs pair
one of each — audit then remediate.

| The user wants to… | Tool | Kind |
| --- | --- | --- |
| see if a host is healthy / triage an incident | [`linux-triage`](../../../toolbox/linux-triage/) | script (read-only) — or the **linux-triage** skill |
| know what needs patching / reboot | [`patch-report`](../../../toolbox/patch-report/) | script (read-only) |
| actually apply updates | [`patch` role](../../../toolbox/ansible/roles/patch/) | Ansible (changes state) |
| check hardening posture | [`baseline-check`](../../../toolbox/baseline-check/) | script (read-only) |
| fix hardening gaps | [`baseline_hardening` role](../../../toolbox/ansible/roles/baseline_hardening/) | Ansible — or the **harden-baseline** skill |
| batch create/disable users (one-off) | [`user-lifecycle`](../../../toolbox/user-lifecycle/) | script (dry-run by default) |
| manage users declaratively (in Git) | [`user_lifecycle` role](../../../toolbox/ansible/roles/user_lifecycle/) | Ansible |
| prove a backup actually restores | [`backup-restore-drill`](../../../toolbox/backup-restore-drill/) | script (read-only to your system) |
| find overlapping CIDR ranges | [`cidr-check`](../../../toolbox/cidr-check/) | script (read-only) |
| inventory a vSphere environment | [`vsphere-inventory`](../../../toolbox/vsphere-inventory/) | script (read-only, stdlib SOAP) |
| judge "can this VMware estate move to Proxmox?" | [`vm-migration-assess`](../../../toolbox/vm-migration-assess/) | script (assessment only; feed it vsphere-inventory JSON) |
| inventory a Proxmox cluster / compare after migration | [`pve-inventory`](../../../toolbox/pve-inventory/) | script (read-only, on-node or from captures) |

When two tools pair (audit + fix), name both and the order: **audit first, show
the result, remediate second.**

## Workflow

1. **Classify the ask.** Read-only look, or a change? If a change, is there an
   audit tool to run first? (Almost always yes — pair them.)
2. **Pick from the map.** If an Agent Skill exists for the flow (`linux-triage`,
   `harden-baseline`), prefer routing to it — it carries the interpretation and
   guardrails. Otherwise hand back the tool directly.
3. **State the safety level** before the command: read-only (run freely),
   dry-run-by-default (safe to preview), or state-changing (check-mode /
   confirmation first).
4. **Hand back the exact command**, with the tool's README linked for options and
   its `Tested on:` line for scope. Include the sudo/privilege note.
5. **If nothing fits**, say so plainly — the toolbox is a focused set, not a
   catch-all. Don't force a bad match; suggest the closest starting point or note
   it as a gap (a candidate for a future tool).

## Honesty (the repo's law)

- Every tool's README carries a `Tested on:` line — surface it, don't imply
  broader coverage than was verified.
- Read-only vs. state-changing is not a footnote; lead with it so the user (or an
  agent acting for them) never runs a change thinking it was a look.
- The toolbox is deliberately small. "There isn't a tool for that yet" is a
  correct, useful answer.

## What this skill is not

Not a doc dump of the whole repo — for learning the *why*, that's the-stack and
cross-cutting notes. This picks the *runnable* thing for a concrete task and gets
out of the way.
