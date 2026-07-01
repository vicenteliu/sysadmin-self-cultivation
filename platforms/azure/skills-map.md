# Azure — Admin Skill Map

Same tiers as [AWS](../aws/skills-map.md): **Core** (can't admin without it),
**Working** (solid mid/senior), **Depth** (the differentiator). Check a box when you
can *do* it from code and *explain* the failure modes.

> If you did the AWS map first, read each line as *"what's the Azure equivalent, and
> the quirk?"* — most of these transfer directly.

## Fundamentals — the hierarchy (Azure-specific)

- [ ] **Core** — Explain tenant → management group → subscription → resource group → resource, and what each boundary is *for*.
- [ ] **Core** — Create/delete a resource group and understand it as a lifecycle boundary (delete the RG = delete its contents).
- [ ] **Working** — Move resources between RGs/subscriptions; understand what can't move.

## Identity & access — two systems, not one

- [ ] **Core** — **Entra ID vs. Azure RBAC**: directory identity vs. resource permissions. Know which is which.
- [ ] **Core** — Assign an RBAC role at the right **scope** (mgmt group / subscription / RG / resource); built-in roles (Reader/Contributor/Owner) and when *not* to use Owner.
- [ ] **Core** — Service principals / app registrations for automation.
- [ ] **Working** — **Managed Identities** (system- vs. user-assigned) so workloads carry no secret — the Azure "instance profile."
- [ ] **Working** — Entra groups for access; least-privilege custom RBAC role.
- [ ] **Depth** — Conditional Access, **PIM** (just-in-time privileged access), reading a denied action in the Activity Log.

## Networking (VNet)

- [ ] **Core** — Design a VNet: address space + subnets.
- [ ] **Core** — **NSGs** (stateful) on subnet/NIC; trace *why a VM can't reach out*.
- [ ] **Core** — No public IP + reach the VM via **Azure Bastion** (the "no open SSH/RDP" pattern).
- [ ] **Working** — Load Balancer vs. Application Gateway; Azure DNS zones.
- [ ] **Working** — **Private Endpoints** / service endpoints (keep storage/SQL off the public internet).
- [ ] **Depth** — VNet peering, UDRs + Azure Firewall / NVA, hybrid (VPN Gateway / ExpressRoute).

## Compute

- [ ] **Core** — Deploy/stop/delete a VM from CLI or IaC; attach a managed identity.
- [ ] **Core** — No public IP; connect via Bastion or `az ssh` over Entra.
- [ ] **Working** — VM Scale Sets + Load Balancer; custom images (Compute Gallery).
- [ ] **Depth** — AKS basics; Azure Functions (serverless); Spot VMs for cost.

## Storage & data

- [ ] **Core** — Storage Account with **public access disabled** + encryption; Blob containers.
- [ ] **Core** — Access via RBAC (preferred) vs. account keys vs. SAS — and why keys are a liability.
- [ ] **Working** — Azure SQL in a private setup; backups (Recovery Services Vault).
- [ ] **Depth** — Lifecycle management + storage tiers (cost); geo-redundancy options.

## Provisioning & config — build from code

- [ ] **Core** — Stand up a stack from **Bicep** or **Terraform**, in version control.
- [ ] **Core** — Delete it cleanly (RG delete / `terraform destroy`), nothing orphaned.
- [ ] **Working** — `what-if` / `plan` before apply; modules; remote state (Terraform) or deployment stacks.
- [ ] **Working** — **Azure Policy** to enforce/deny (e.g. "no public IPs", "encryption required").
- [ ] **Depth** — Landing zone / management-group design; policy-as-code; CI/CD for infra.

## Observability

- [ ] **Core** — Azure Monitor metric + an alert that pages someone.
- [ ] **Core** — Send logs to **Log Analytics**; write a basic **KQL** query.
- [ ] **Core** — **Activity Log**: answer "who created/deleted this?"
- [ ] **Working** — Dashboards; diagnostic settings routing logs centrally; App Insights.
- [ ] **Depth** — Cross-subscription central logging; SLO thinking; workbook dashboards.

## Security & compliance — safe, provable, affordable

- [ ] **Core** — **Key Vault** for secrets/keys/certs; access via managed identity (no secrets in code).
- [ ] **Core** — A **Budget** + cost alert so a forgotten VM/NAT/Bastion doesn't surprise you.
- [ ] **Working** — **Defender for Cloud** secure score + recommendations; Azure Policy guardrails.
- [ ] **Working** — Multi-subscription separation (prod/dev blast radius) via management groups.
- [ ] **Depth** — Landing-zone guardrails; incident response for a leaked key/secret; cost anomaly alerts.

## The "can you operate it" test

Core boxes across all surfaces, from code, plus debugging the common failures = you
can honestly administer Azure at a working level. On this platform specifically, the
**identity split (Entra vs. RBAC)** and the **resource-group hierarchy** are the two
things that trip up people coming from AWS — nail those and the rest follows.
