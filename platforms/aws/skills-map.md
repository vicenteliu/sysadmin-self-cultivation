# AWS — Admin Skill Map

A checkable competency list. Tiers:

- **Core** — you cannot administer AWS without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it from code and *explain* the failure modes — not
when you've read about it.

## Identity & access (IAM) — the front door

- [ ] **Core** — Explain user vs. role vs. policy vs. group; when to use each.
- [ ] **Core** — Write a least-privilege JSON policy for a specific task (e.g. read one S3 bucket).
- [ ] **Core** — Secure the root account: MFA, no access keys, break-glass only.
- [ ] **Working** — Assume-role / short-lived credentials (STS) instead of long-lived keys.
- [ ] **Working** — Instance profiles: give an EC2 box a role instead of baking keys into it.
- [ ] **Working** — IAM Identity Center (SSO) for human access; federation basics.
- [ ] **Depth** — Permission boundaries, SCPs (Organizations), and reading a denied request in CloudTrail.

## Networking (VPC) — the box everything lives in

- [ ] **Core** — Design a VPC: CIDR, public vs. private subnets across AZs.
- [ ] **Core** — Route tables, Internet Gateway, NAT — and trace *why a host can't reach the internet*.
- [ ] **Core** — Security groups vs. NACLs: stateful vs. stateless, and which to reach for.
- [ ] **Working** — Load balancing (ALB/NLB) and target groups.
- [ ] **Working** — Route 53 for DNS; public vs. private hosted zones.
- [ ] **Depth** — VPC peering / Transit Gateway; VPC endpoints (keep traffic off the internet); hybrid connectivity (VPN / Direct Connect).

## Compute — where code runs

- [ ] **Core** — Launch/stop/terminate EC2 from the CLI; pick instance types sanely.
- [ ] **Core** — Attach an IAM role to an instance; user-data bootstrap.
- [ ] **Working** — Auto Scaling groups + a load balancer + health checks.
- [ ] **Working** — Build/maintain an AMI (the cloud version of image building).
- [ ] **Depth** — Containers on ECS/EKS; Lambda for event-driven/serverless; Spot for cost.

## Storage & data — where state lives

- [ ] **Core** — S3 with encryption + block-public-access; bucket policies vs. IAM.
- [ ] **Core** — EBS volumes + snapshots; lifecycle basics.
- [ ] **Working** — RDS/Aurora in a private subnet; backups, parameter groups, failover.
- [ ] **Working** — S3 lifecycle rules + storage classes (cost).
- [ ] **Depth** — DynamoDB basics; EFS for shared file storage; cross-region replication.

## Provisioning & config — build from code, not clicks

- [ ] **Core** — Stand up a stack from **Terraform** or **CloudFormation** in version control.
- [ ] **Core** — Destroy it cleanly (no orphaned, billing resources).
- [ ] **Working** — Remote state + locking; modules / reusable stacks.
- [ ] **Working** — Systems Manager (SSM) for patching, run-command, Parameter Store.
- [ ] **Depth** — CI/CD for infrastructure; drift detection; policy-as-code guardrails.

## Observability — is it healthy, and who did what

- [ ] **Core** — CloudWatch metrics + an alarm that actually pages someone.
- [ ] **Core** — Ship and search logs in CloudWatch Logs.
- [ ] **Core** — CloudTrail: answer "who created/deleted this?"
- [ ] **Working** — Dashboards; log-metric filters; basic SLO thinking.
- [ ] **Depth** — Distributed tracing (X-Ray); centralized multi-account logging.

## Security & compliance — safe, provable, affordable

- [ ] **Core** — KMS encryption at rest; Secrets Manager / Parameter Store (no secrets in code).
- [ ] **Core** — A **Budget alarm** so a forgotten resource doesn't surprise you.
- [ ] **Working** — GuardDuty (threat detection), AWS Config (compliance rules).
- [ ] **Working** — Multi-account with Organizations; separate prod/dev blast radius.
- [ ] **Depth** — Landing-zone / guardrail design; incident response for a leaked key; cost anomaly detection.

## The "can you actually operate it" test

If you can do the **Core** boxes across all seven surfaces, from code, and debug the
common failures, you can honestly say you can administer AWS at a working level.
**Working** boxes make you genuinely useful on day one. **Depth** boxes are what a
strong candidate reaches for in the interview and what keeps a production account out
of trouble.
