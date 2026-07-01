# AWS — The AI-Assisted Ramp

> How to get to *competent* on AWS in days instead of months — using AI as a
> co-pilot, and keeping it honest. The method generalizes to any platform.

The old way to learn a cloud was to grind a certification course front to back and
hope the relevant 20% stuck. The problem was never the material — it's that you
didn't yet know *which* 20% mattered for the job in front of you, so you couldn't
prioritize. That "unknown-unknowns" phase is exactly what AI collapses. But AI also
invents service names, mis-remembers API parameters, and writes confident,
plausible, *wrong* IAM policies. So the method is two disciplines held together:
**AI for speed, judgment for truth.**

## The loop

For any new area (say, VPC networking):

1. **Anchor to what you already know.** Don't ask "teach me VPCs." Ask *"I already
   understand Linux, TCP/IP, subnets, routing, and firewalls on-prem — map that onto
   an AWS VPC. What's the same, what's renamed, and what's genuinely different?"*
   You get a translation, not a lecture, and it lands in minutes.
2. **Get the 80/20.** *"Of everything in AWS networking, what's the 20% an admin
   uses daily, and what can I safely defer?"* Now you can prioritize.
3. **Generate the artifact.** *"Write a least-privilege IAM policy that lets this
   role read exactly one S3 bucket,"* or *"Terraform for a VPC with one public and
   one private subnet across two AZs, plus a NAT."* First draft in seconds.
4. **Verify — this is the non-negotiable step.** Cross-check every service name,
   parameter, and permission against the **official AWS docs**. AI's failure mode is
   *confident wrongness*: a policy action that doesn't exist, a default that changed,
   a resource argument it hallucinated. Assume the draft is 90% right and hunt the
   10%.
5. **Run it in a throwaway.** A sandbox/dev account with a **hard budget alarm**.
   Reality is the final reviewer — a plan that `terraform apply`s and a stack you can
   `destroy` cleanly is worth more than any explanation.
6. **Have AI review your work back.** *"Here's my Terraform / my security group —
   what's the security or cost risk I missed?"* It's a strong second set of eyes,
   as long as *you* remain the one who decides.

## Prompt patterns that pull their weight

- **The translator:** *"Explain X assuming I already know Linux/networking/IAM
  concepts — just the AWS-specific delta."* (Skips the beginner tax.)
- **The 80/20:** *"What's the minimum I must understand about X to be dangerous, and
  what's safe to defer?"*
- **The gotcha hunter:** *"What are the three things that most commonly break or
  surprise people with X, and how do I avoid them?"*
- **The least-privilege generator:** *"Write the tightest IAM policy that does
  exactly this and nothing more."* (Then tighten it further by hand.)
- **The reviewer:** *"Review this IaC / policy / architecture for security, cost, and
  reliability problems."*
- **The rubber duck:** paste an error, an `aws` CLI output, a denied request — *"walk
  me through what this means and how I'd debug it."*

## Where AI will burn you (so verify these hardest)

- **IAM policy actions & conditions** — it invents plausible-looking action strings.
- **Service defaults that changed** — e.g. S3 public-access and encryption defaults
  have shifted over the years; AI mixes eras.
- **Resource arguments in Terraform/CloudFormation** — wrong attribute names, deprecated ones.
- **Costs** — it will happily suggest an architecture that's correct and expensive.
- **Anything security-critical** — encryption, key policies, network exposure. Never
  ship these on trust; verify and test.

## Why this is a *sysadmin's* skill, not a shortcut around one

An AI can generate a VPC in seconds. It cannot tell you the request is denied
because the NACL is stateless and you only opened the inbound side. It cannot feel
that a security group is one line away from exposing a database to the internet. It
cannot own the 3 a.m. incident. The judgment — least-privilege instinct, "why can't
this reach that," reading the failure, weighing cost vs. reliability — is the
craft. AI just removes the months of rote lookup between *having* that judgment and
*applying* it to a platform you haven't touched yet.

That's the whole thesis of this project, on one platform: **the mental model is the
asset; AI is the accelerant; verification is the discipline that makes it safe.**
