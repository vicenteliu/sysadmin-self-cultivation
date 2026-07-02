# Self-Hosted / Bare Metal — The AI-Assisted Ramp

> Like the [vSphere note](../vsphere/ai-ramp.md), this one is inverted: self-hosting
> is a **strength, not a gap**, so AI's job isn't to teach the platform — it's to
> accelerate the software glue, and to stay entirely out of the physical layer it
> cannot touch. And it's the platform where a wrong AI answer costs the most, because
> bare metal has no undo and no provider to roll you back.

The repo's thesis ([`WHY.md`](../../WHY.md)) is that AI collapses the unknown-unknowns
for platforms you've never run. Bare metal is the opposite case: it's the ground the
judgment was *earned* on, so the discipline inverts to **you verify by default; AI
drafts the config files and scripts you already know how to check.**

## Where AI earns its keep

- **Config-file drafting** — a BIND zone file, a `dhcpd.conf`, a kickstart/preseed, a
  PXE menu, an Ansible playbook, a `udev` rule, an `fstab` line. AI writes the
  boilerplate fast; because you know the system, you catch the wrong syntax or the
  missing directive immediately. This is the best use: AI types, your expertise
  reviews.
- **Error decoding** — paste a `dmesg` tail, a failed systemd unit, a RAID
  controller log, an `strace` of a wedged process: *"what's this pointing at?"* A fast
  hypothesis you then test with the [debugging reflex](../../foundations/).
- **Cross-mapping outward** — *"I run PXE/image/cloud-init, BMC/IPMI, DNS/BIND, and
  RAID. What are the AWS/Azure equivalents, and where does the analogy break?"* —
  turning bare-metal depth into a fast ramp onto the clouds (the operating model in
  reverse, same as the vSphere note).

## Where AI cannot help — and where it's dangerous

- **The physical layer.** A flaky DIMM, a cable in the wrong port, a backplane fault,
  a BMC that won't answer, a disk mid-rebuild — none of it is a prompt away. This is
  the half of the job that stays entirely human.
- **Destructive commands with no undo.** On a cloud a bad `terraform destroy` is
  recoverable-ish; on bare metal, `mkfs` on the wrong device or `dd` to the wrong disk
  is *gone*. AI drafts destructive commands confidently and without the guardrails
  you'd add by instinct — read every one as if you're running it as root, because you
  are ([`foundations/`](../../foundations/)).
- **Hardware-specific detail.** AI mis-remembers RAID controller quirks, NIC driver
  behavior, and firmware specifics — the exact things a wrong answer breaks a host on.
  Verify against the vendor docs and the actual hardware.

## Why this note exists

Because honesty is the point of the repo. Writing self-hosting like a cloud module —
"here's how AI gets you competent fast" — would be false: this is the platform the
rest of the repo's competence *came from*. The truthful version is more useful: on the
platform you know deepest, **AI is a config-file drafter and a translation engine, not
a teacher — and the physical layer, plus the judgment about what's safe to run, is
exactly what no model provides.**
