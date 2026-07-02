# Infrastructure-as-Code & Configuration Management

> 🚧 **Opening written; body in progress.** The framework below is complete —
> what this module will cover is fixed; the prose is being filled in.

> The universal control plane. Move #3 of the [operating model](../00-the-operating-model.md)
> — *drive the platform through its API and codify it* — made into its own
> discipline. Master this once and every platform becomes a thing you describe in a
> file and version in git, instead of a console you click and forget.

Infrastructure-as-code is what separates "I set it up" from "it's defined, reviewed,
reproducible, and disposable." This note covers the two halves that get conflated —
**provisioning** (Terraform: create the resources) and **configuration management**
(Ansible/Puppet: make the resources consistent) — and the discipline that makes
either one trustworthy: state, idempotence, review, and drift.

## Planned coverage

- **Provisioning vs. configuration** — the distinction that matters: Terraform
  *creates* the VPC and the VM; Ansible *configures* what's on the VM. Using one
  for the other's job is a common and expensive mistake.
- **Terraform as the universal plane** — state (and why remote state + locking are
  non-negotiable on a team), modules, `plan`/`apply`/`destroy`, and reading a plan
  before trusting it. One tool, every cloud in this repo.
- **Ansible** — agentless config management, playbooks, idempotence, and where it's
  the right tool over Terraform (mutating existing hosts, orchestration, the
  fry-half of [`the-stack/03`](../the-stack/03-compute-and-images.md)'s bake-vs-fry).
- **Puppet / the pull model** — where declarative, agent-based config still fits,
  and how it compares to Ansible's push model.
- **Drift** — the gap between what the code says and what reality is, how to detect
  it, and why manual console changes are how drift starts.
- **The AI-assisted ramp** — AI drafts HCL and playbooks fast and gets the syntax
  mostly right; it invents resource arguments and permissive defaults, so every
  generated plan gets read and every `apply` gets a dry run first.

## Honest boundaries

Mixed. **Ansible** and the automation discipline are ✋ (Python/Bash/Ansible
operated for real fleet automation); **Terraform** is a 🧗 ramp — the concepts
(state, plan/apply, modules) are solid and mapped, not claimed as years of
production module authoring. Puppet is conceptual. The transferable claim is a deep
automation instinct plus a fast, verified ramp onto any specific IaC tool — the
[`platforms/aws/labs/02`](../platforms/aws/labs/02-minimal-vpc-ec2-terraform/) lab
is where the Terraform ramp gets proven in code.
