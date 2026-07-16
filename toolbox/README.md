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

## First wave (planned — ordered by how often the task shows up in real JDs)

| Tool | What it does | Origin |
| --- | --- | --- |
| `linux-triage` | one-shot health/triage report — CPU, memory, disk, network, recent log errors | new; the first move of every incident |
| `user-lifecycle` | CSV-driven batch user create/disable on Linux | new; identity is the densest JD cluster |
| `patch-report` | pending-updates inventory (apt/dnf) with reboot-required flags | new |
| `baseline-check` | read-only audit of a small hardening-baseline subset | new; Ansible remediation comes in the Ansible wave |
| `backup-restore-drill` | prove a backup by restoring it — a backup you haven't restored isn't one | grown from [the-stack lab 04](../the-stack/labs/04-backup-not-snapshot/) |
| `cidr-check` | detect overlapping CIDR ranges across network plans | grown from the multi-cloud lab |

Waves after this one: **Ansible roles** (hardening / patch orchestration / user
lifecycle, each lab-verified), then **user-side Agent Skills** wrapping the tools,
then a **generator** that assembles a per-shop subset of the toolbox.

## What this is not

Not a product, not production-hardened, not a replacement for your configuration
management. It is working material, published under the same honesty rules as
everything else here — if a tool hasn't been drilled somewhere real, its README
will tell you exactly where it *has* been.
