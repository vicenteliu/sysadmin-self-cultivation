# Toolbox — take it with you

> The rest of this repo explains how things work. The toolbox is the part you can
> **run**: small, self-contained tools a sysadmin — or an AI agent working alongside
> one — can pick up and use in minutes.

## Why a toolbox

Reading proves understanding; running proves craft. This track evolves the repo from
*a thing you read* into *a thing you use* — and it is designed from day one to be
**agent-callable**: every tool is documented precisely enough that an AI assistant
can operate it safely on your behalf. That is the [`ai-workflow/`](../ai-workflow/)
chapter, made executable.

## Design rules (the conventions — every tool follows all six)

1. **One directory, self-contained.** `toolbox/<tool-name>/` holds the script(s) and
   a README stating purpose, usage, and exit codes. No tool depends on another.
2. **Safe by default.** Read-only or `--dry-run` is the default wherever a tool
   *could* change state; destructive actions require an explicit flag. A tool you
   can't run casually is a tool you won't run at all.
3. **Honest scope.** Every README carries a `Tested on:` line (e.g. *Ubuntu 22.04,
   RHEL 9 lab*). Lab-verified is not production-hardened, and the README says so —
   the repo's ✋/🧗 honesty layer, applied to code.
4. **Plain dependencies.** Bash and Python stdlib first; Ansible where orchestration
   genuinely earns it. No frameworks, no curl-piped installers.
5. **Agent-readable.** Each README opens with a short block stating inputs, outputs,
   and risk level, so an AI agent can call the tool without guessing. User-side
   Agent Skills that wrap these tools land in a later wave.
6. **Quiet success, loud failure.** Exit 0 and terse output when all is well;
   non-zero and an actionable message when it isn't — because both humans and
   agents branch on that.

## Layout

```
toolbox/
├── README.md            ← you are here: charter + conventions
└── <tool-name>/
    ├── README.md        ← purpose · usage · tested-on · risk level
    └── <tool>.sh|.py    ← the tool itself
```

## First wave (✅ shipped — ordered by how often the task shows up in real JDs)

| Tool | What it does | Origin |
| --- | --- | --- |
| [`linux-triage`](linux-triage/) | one-shot health/triage report — CPU, memory, disk, network, failed services, recent log errors | new; the first move of every incident |
| [`user-lifecycle`](user-lifecycle/) | CSV-driven batch user create/disable on Linux (dry-run by default) | new; identity is the densest JD cluster |
| [`patch-report`](patch-report/) | pending-updates inventory (apt/dnf) with reboot-required flags | new |
| [`baseline-check`](baseline-check/) | read-only audit of a small hardening-baseline subset | new; Ansible remediation comes in the Ansible wave |
| [`backup-restore-drill`](backup-restore-drill/) | prove a backup by restoring it — a backup you haven't restored isn't one | grown from [the-stack lab 04](../the-stack/labs/04-backup-not-snapshot/) |
| [`cidr-check`](cidr-check/) | detect overlapping CIDR ranges across network plans | grown from the multi-cloud lab |

## Ansible line (✅ shipped — the remediation half)

The scripts above *find*; the [`ansible/`](ansible/) roles *fix*, idempotently:

| Role | Remediates | Pairs with |
| --- | --- | --- |
| [`baseline_hardening`](ansible/roles/baseline_hardening/) | SSH posture, umask, sysctl, journald | `baseline-check` |
| [`patch`](ansible/roles/patch/) | apply updates (apt/dnf) + reboot orchestration | `patch-report` |
| [`user_lifecycle`](ansible/roles/user_lifecycle/) | declarative users (present / disabled) | `user-lifecycle` |

## Agent Skills (✅ shipped — drive the toolbox by sentence)

Three user-side [`.claude/skills/`](../.claude/skills/) wrap these tools so an AI
agent can run them for you: **linux-triage** (triage a host, route each flag to
its fix), **harden-baseline** (audit→remediate hardening, lock-out-aware), and
**toolbox-picker** (say the task, get the right tool + command). Install one on a
new box and drive the toolbox in one sentence — the "AI-assisted toolset" itself.

## Virtualization wave (✅ shipped — the hypervisor layer)

The first six tools look *inside* an OS; these three look at the platform under
it — and together they answer the season's question, "can this VMware estate
move to Proxmox?":

| Tool | What it does | Pairs with |
| --- | --- | --- |
| [`vsphere-inventory`](vsphere-inventory/) | read-only vSphere inventory over **pure-stdlib SOAP** (no SDK, no govc) | feeds `vm-migration-assess` |
| [`vm-migration-assess`](vm-migration-assess/) | verdict per VM — EASY/MODERATE/HARD — with the findings behind it | reads `vsphere-inventory` |
| [`pve-inventory`](pve-inventory/) | Proxmox inventory in the **same schema**, live on a node or from captures | the destination-side mirror |

## Generator (✅ shipped — the customizable toolbox)

[`generate`](generate/) assembles the subset a given shop actually needs — one
command, one standalone pack: the matching scripts, their paired Ansible roles,
and every Agent Skill whose references are fully satisfied (a pack never carries
a skill that points at a tool it doesn't have):

```bash
./toolbox/generate/generate.py --profile security-baseline --out ~/kit
```

Selection is concern + platform tags in [`generate/catalog.json`](generate/catalog.json);
a new tool joins the generator with one JSON entry.

## What this is not

Not a product, not production-hardened, not a replacement for your configuration
management. It is working material, published under the same honesty rules as
everything else here — if a tool hasn't been drilled somewhere real, its README
will tell you exactly where it *has* been.
