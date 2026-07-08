# AWS — the worked example

> The template every platform module follows: **what it is → the admin skill map →
> the AI-assisted ramp → labs** — plus four deeper companion notes AWS gets as the
> worked example: **[architecture](architecture.md)** (how it's structured),
> **[operations](operations.md)** (running it day-2, the ops-work breakdown, and AI
> in the operating loop), **[automation](automation.md)** (scripting the API to
> manage and operate it), and **[support](support.md)** (the break-fix craft and what
> a strong sysadmin from another lane must unlearn to inherit it). AWS is done first
> and most thoroughly; read it end to end to see the shape.

## 1. What AWS is

Amazon Web Services is a rented data center you drive by API. You don't buy servers,
racks, switches, or storage arrays — you *request* them, pay by the hour/second/GB,
and give them back when you're done. The administrator's job shifts from *turning
screws* to *declaring intent* and keeping the result secure, reliable, and
affordable.

Mapped onto the [seven surfaces](../../00-the-operating-model.md):

| Surface | AWS's word(s) for it | The one-liner |
| --- | --- | --- |
| **Identity & access** | **IAM** (users, roles, policies), IAM Identity Center | The front door to everything. Roles + least-privilege policies are the whole game. |
| **Compute** | **EC2** (VMs), **Lambda** (serverless), **ECS/EKS** (containers), Auto Scaling | Where your code runs. Start with EC2; graduate to containers/serverless. |
| **Networking** | **VPC**, subnets, route tables, security groups, NACLs, **ELB**, **Route 53** (DNS) | Your private network in the cloud. A VPC is the box everything lives in. |
| **Storage & data** | **S3** (object), **EBS** (block), **EFS** (file), **RDS**/Aurora, DynamoDB | Where state lives. S3 is the default answer to "where do I put this?" |
| **Provisioning & config** | **CloudFormation**, **Terraform** (3rd-party), CDK, AMIs, Systems Manager | How you build it from code instead of clicks. |
| **Observability** | **CloudWatch** (metrics/logs/alarms), CloudTrail (audit), X-Ray (traces) | Is it healthy, and who did what? |
| **Security & compliance** | IAM, KMS (encryption), Secrets Manager, GuardDuty, Config, Organizations, **Cost Explorer / Budgets** | Is it safe, provable, and not on fire financially? |

If you know those ~25 service names and which surface each belongs to, you can hold
a real conversation about AWS. That's the map. Now the skills.

## 2. The admin skill map

The concrete, checkable list of what an AWS administrator must be *able to do* — not
"has heard of." Full checklist with proficiency tiers in
**[`skills-map.md`](skills-map.md)**. The headline capabilities:

- **IAM done right** — create scoped roles and least-privilege policies; understand
  the difference between a user, a role, and a policy; assume-role and short-lived
  credentials over long-lived keys; MFA and root-account hygiene.
- **A VPC you designed** — subnets (public/private), route tables, an internet
  gateway and a NAT, security groups vs. NACLs, and *why a thing can't reach the
  internet* (the #1 support question).
- **Compute you can run and scale** — launch EC2 from code, attach the right IAM
  role (never bake keys into an instance), basic Auto Scaling + a load balancer.
- **Storage with the right defaults** — S3 with encryption + block-public-access
  on by default; EBS snapshots; a managed RDS database in a private subnet.
- **Everything from code** — the same stack in Terraform or CloudFormation, in
  version control, reviewable, and destroyable.
- **You'd see it break** — CloudWatch alarms, CloudTrail for "who did that,"
  and the muscle memory to debug a connectivity or permissions failure.
- **Secure and within budget** — KMS/Secrets Manager instead of secrets in code;
  a Budget alarm so a forgotten GPU instance doesn't cost $4,000.

## 3. The AI-assisted path to competence

The method — how to go from "knows Linux/networking" to "can operate AWS" in days,
not months, using AI as a co-pilot **and keeping it honest** — is in
**[`ai-ramp.md`](ai-ramp.md)**. In one paragraph:

Use AI to collapse the *unknown-unknowns* — "given I already know Linux, networking,
and IAM concepts, what's the 20% of AWS that covers 80% of an admin's job?" — then
have it generate the least-privilege policy, the Terraform, the CLI command. **Then
verify every claim against the docs and run it in a throwaway account.** AI writes
the first draft; your judgment is the review gate. The sysadmin's value in 2026
isn't knowing every flag — it's knowing when the machine is confidently wrong.

## 4. Labs

Reading about a subnet and configuring one are different skills. The runnable,
tear-down-able exercises live in **[`labs/`](labs/)** — starting with a
least-privilege IAM role + a `boto3` script that inventories your account (the cloud
version of a classic "list everything" admin script), then a minimal VPC + EC2 in
Terraform.

## 5. Going deeper — architecture, operations, automation & support

Four companion notes take AWS past "what the services are":

- **[`architecture.md`](architecture.md)** — how AWS is *structured*: the
  account/organization model as the blast-radius unit, regions & AZs, the
  global-vs-regional split, the shared-responsibility line, Well-Architected as a
  review lens, and a reference three-tier that shows every surface composing into one
  system.
- **[`operations.md`](operations.md)** — what *running* AWS looks like: the day-2
  brief, the ops notes (what pages you), the recurring ops work **broken down by
  cadence** (continuous / daily / weekly / monthly / quarterly / on-incident), and
  **how AI assists the operating loop** — distinct from the learning ramp, with the
  guardrail that AI touches signals and drafts while you touch production.
- **[`automation.md`](automation.md)** — **scripting the API** to manage and operate
  AWS: the `identity → client → API call` model, the CLI-vs-boto3-vs-Terraform
  altitude ladder, the credential chain (never a key in the script), the rules that
  separate a working script from a footgun (paginate, iterate regions, handle errors,
  be idempotent), and the read-audit vs. remediation shapes — grounded in the
  runnable [inventory lab](labs/01-scoped-identity-inventory/).
- **[`support.md`](support.md)** — **the break-fix craft**: what supporting AWS makes
  you responsible for, the recurring tickets and *where you look* (the `AccessDenied`
  grammar, timeout-vs-refused, S3-403 layers, ALB 5xx, the cost surprises), and the
  load-bearing on-prem/cloud instincts a strong sysadmin must **unlearn** to inherit
  it — the ramp made concrete, with a verified GitHub field kit.

## Honest boundaries

Written in the spirit of the whole project: this documents a **method and a
competency map**, and the labs are real. Where deep production experience on a
specific AWS service is still ahead of me, the notes say so rather than bluffing —
that honesty is the point. The claim here isn't "15 years of AWS"; it's "a
transferable operating model plus an AI-augmented ramp that gets to competent, fast,
and can be verified in this repo."
