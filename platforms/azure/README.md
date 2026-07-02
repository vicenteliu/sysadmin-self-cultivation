# Azure

> Same four-part template as [AWS](../aws/): **what it is → the admin skill map → the
> AI-assisted ramp → labs** — plus three deeper companion notes mirroring the AWS
> worked example: **[architecture](architecture.md)** (how it's structured),
> **[operations](operations.md)** (running it day-2, the ops-work breakdown, AI in the
> operating loop), and **[automation](automation.md)** (scripting the API). If you've
> read the AWS module, most of this is *"which of those concepts is renamed to what,
> and what's the Azure quirk?"* — which is exactly the point of the
> [operating model](../../00-the-operating-model.md).

## 1. What Azure is

Microsoft's cloud. Same idea as AWS — a rented data center you drive by API — with a
distinctly Microsoft flavor: identity is front-and-center (it grew out of Active
Directory), and resources live inside an explicit hierarchy.

**The org hierarchy is the first thing to internalize** (it has no clean AWS
equivalent):

```
Microsoft Entra ID tenant        (identity boundary — the directory)
└── Management Group             (policy / org grouping)
    └── Subscription             (billing + isolation boundary  ≈ an AWS account)
        └── Resource Group       (lifecycle container — NO AWS equivalent)
            └── Resources        (VMs, VNets, storage, ...)
```

Everything you create lives in a **resource group** inside a **subscription**. Get
that, and the rest maps onto the [seven surfaces](../../00-the-operating-model.md):

| Surface | Azure's word(s) | The one-liner |
| --- | --- | --- |
| **Identity & access** | **Microsoft Entra ID** (dir. identity) + **Azure RBAC** (resource access) + **Managed Identities** | Two systems, not one — Entra = *who you are*, RBAC = *what you can touch*. Confusing them is the classic mistake. |
| **Compute** | **Virtual Machines**, VM Scale Sets, **Azure Functions**, **AKS**, App Service | Where code runs. Start with a VM; graduate to AKS/Functions. |
| **Networking** | **VNet**, subnets, **NSGs**, route tables (UDRs), **Load Balancer / App Gateway**, **Azure DNS**, Private Endpoints | A VNet is the box; NSGs are the firewall rules. |
| **Storage & data** | **Storage Account** (Blob/File/Queue/Table), Managed Disks, **Azure SQL**, Cosmos DB | Blob storage is the default "where do I put this?" |
| **Provisioning & config** | **Bicep** / ARM templates, **Terraform**, **Azure CLI / PowerShell (Az)**, **Azure Policy** | Bicep is Azure-native IaC; Terraform is the cross-cloud choice. |
| **Observability** | **Azure Monitor** (metrics), **Log Analytics** + KQL (logs), App Insights (traces), **Activity Log** (audit) | KQL is the language you'll actually use to answer "what happened?" |
| **Security & compliance** | **Defender for Cloud**, **Key Vault**, **Azure Policy**, Entra Conditional Access / **PIM**, **Cost Management + Budgets** | Key Vault for secrets; Policy for guardrails; a Budget so you don't get surprised. |

## 2. The admin skill map

Full checklist in **[`skills-map.md`](skills-map.md)**. Headline capabilities:

- **Identity done right (two layers)** — Entra ID users/groups/service principals +
  Azure **RBAC** role assignments at the right scope (management group / subscription
  / resource group / resource); **Managed Identities** so nothing carries a secret.
- **A VNet you designed** — subnets, **NSGs** (and NSG vs. the old "allow all"
  default), route tables, and *why a VM can't reach out* — the Azure version of the
  #1 support question.
- **Compute you can run** — a VM from code with a managed identity and **no public IP
  + no open SSH** (reach it via **Azure Bastion** or `az ssh` over Entra).
- **Storage with safe defaults** — a Storage Account with public access disabled,
  encryption on, and least-privilege access via RBAC or a SAS you understand.
- **Everything from code** — the same stack in **Bicep** or **Terraform**, in version
  control, `what-if`/`plan`'d, and deletable (delete the resource group → it's gone).
- **You'd see it break** — Azure Monitor alerts, **KQL** in Log Analytics, and the
  Activity Log for "who changed this?"
- **Secure and within budget** — **Key Vault** instead of secrets in code; **Azure
  Policy** guardrails; a **Budget** alert.

## 3. The AI-assisted path to competence

Method in **[`ai-ramp.md`](ai-ramp.md)**. The short version for Azure specifically:
you now have two anchors — on-prem fundamentals *and*, once you've done the AWS
module, a full cloud mental model. So the fastest prompt isn't "teach me Azure," it's
*"I know AWS IAM/VPC/EC2/S3 and on-prem AD — map each onto its Azure equivalent, and
flag where Azure genuinely differs (RBAC vs. Entra roles, resource groups, managed
identities)."* Then generate the Bicep/Terraform and **verify against the docs** —
Azure's two-permission-systems split and its resource-provider quirks are exactly
where AI gets confidently wrong.

## 4. Labs

Runnable exercises in **[`labs/`](labs/)** — same shape as AWS: a scoped identity +
subscription inventory (Azure Resource Graph / CLI), then a minimal VNet + VM in
Terraform reachable without an open port, then Key Vault + managed identity, then a
Budget.

## 5. Going deeper — architecture, operations & automation

Three companion notes take Azure past "what the services are", mirroring the AWS set:

- **[`architecture.md`](architecture.md)** — how Azure is *structured*: the management-
  group → subscription → resource-group hierarchy as the blast-radius model, regions /
  zones / **paired regions**, the **two-permission-planes** gotcha (Entra ID roles vs.
  Azure RBAC) given real weight, shared responsibility, and a reference three-tier.
- **[`operations.md`](operations.md)** — *running* Azure day-2: the brief, the ops
  notes (public blob, NSG-at-subnet-or-NIC, the Entra-vs-RBAC denial), the recurring
  work **broken down by cadence**, and **how AI assists the operating loop** — leaning
  into KQL authoring for Log Analytics / Sentinel.
- **[`automation.md`](automation.md)** — **scripting the ARM API**: the
  `identity → client → API call` model, Azure's dual **CLI + first-class PowerShell**
  altitude ladder, **managed identity** / `DefaultAzureCredential` (never a secret in
  the script), the rules (`ItemPaged` pagination, **Resource Graph** for bulk),
  and the read-audit vs. remediation shapes.

## Honest boundaries

This is where the project's honesty policy earns its keep. **Identity is where I have
real hands-on** — I did the initial Microsoft Entra ID / Azure AD setup and ran
identity lifecycle at scale, so the Entra/RBAC surface isn't theory for me. The
**resource-management side at production scale** (large VNet designs, AKS in prod,
multi-subscription landing zones) is where I'm ramping — and this module documents
that ramp honestly rather than dressing it up. The claim is "strong identity
foundation + a fast, verifiable ramp onto the rest," not "10 years of Azure."
