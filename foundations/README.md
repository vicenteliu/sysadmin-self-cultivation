# Foundations — Linux & scripting

> 🚧 **Opening written; body in progress.** The framework below is complete —
> what this module will cover is fixed; the prose is being filled in.

> The floor under every role in this repo. Every job posting that inspired this
> project *assumes* this and never lists it — which is exactly why it's worth
> making explicit. You don't get to the clouds without standing on this.

The roadmap leads with cross-cutting skills because they transfer; this module is
the thing *underneath* even those — the Linux command line and the scripting that
turns "I did it once by hand" into "it runs itself now." It's the most-requested,
least-taught skill in the whole demand signal, precisely because everyone assumes
you already have it. On the ✋/🧗 scale this is **✋ hands-on depth** — RHCE-level
Linux operated at fleet scale, with Python and Bash as daily tools over a decade.

## Planned coverage

- **The Linux mental model** — processes, the filesystem hierarchy, permissions,
  users/groups, systemd and the boot path, the `/proc` and `/sys` windows into the
  kernel. Not a command dictionary — the model that makes commands guessable.
- **The debugging reflex** — `strace`, `lsof`, `journalctl`, `dmesg`, `ss`, and the
  discipline of following the evidence instead of guessing (the same reflex the
  network debug ladder in [`the-stack/02`](../the-stack/02-network.md) formalizes).
- **Scripting that earns its keep** — Bash for glue, Python for anything with
  logic, and the line between them. Idempotence, error handling, and why a script
  you can't re-run safely is a liability.
- **PowerShell, honestly scoped** — real for Windows Server maintenance, not the
  primary tool; where it fits in a mostly-Linux fleet.
- **The AI-assisted ramp** — using AI to accelerate shell one-liners and script
  drafts *and* the verification habit that keeps a plausible-but-wrong command from
  running as root.

## Honest boundaries

✋ **hands-on depth.** Linux (RHEL/CentOS/Ubuntu) operated at fleet scale, RHCE
certified, Python and Bash as everyday automation tools across ten-plus years.
PowerShell is real but scoped (Windows Server maintenance). This is the module the
rest of the repo stands on, and it's the one written from the most direct
experience.
