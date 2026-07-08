# Google Cloud Platform (GCP) — the third cloud

> The template every platform module follows: **what it is → the admin skill map →
> the AI-assisted ramp → labs** — plus four deeper companion notes mirroring the AWS
> worked example: **[architecture](architecture.md)** (how it's structured),
> **[operations](operations.md)** (running it day-2, the ops-work breakdown, AI in
> the operating loop), **[automation](automation.md)** (scripting the API to
> manage and operate it), and **[support](support.md)** (the break-fix craft — GCP +
> GKE — and what an AWS admin must unlearn to inherit it). Follows the same shape as [`aws/`](../aws/) and
> [`azure/`](../azure/). GCP is where the ramp method gets its cleanest test — most
> of it is renamed AWS/Azure, with a few genuine structural differences to catch.

## 1. What GCP is

Google Cloud is a rented data center you drive by API — the same bargain as AWS and
Azure, on the fabric Google built to run Search and YouTube. For an admin who has
mapped the [seven surfaces](../../00-the-operating-model.md) on one cloud, GCP is
mostly a vocabulary exercise — *except* for a handful of places where Google made a
genuinely different design choice, and those are where "GCP is just AWS with
different logos" gets you burned. The headline difference: **the VPC is global**.

Mapped onto the seven surfaces:

| Surface | GCP's word(s) for it | The one-liner |
| --- | --- | --- |
| **Identity & access** | **Cloud IAM** (roles + bindings), service accounts, Cloud Identity | Roles bind to members on resources; service accounts are the workload-identity story. |
| **Compute** | **Compute Engine** (VMs), **Cloud Run** (serverless containers), **GKE** (Kubernetes), Cloud Functions | Where code runs. Machine types **plus a custom-size dial**; GKE is the reference Kubernetes. |
| **Networking** | **VPC (global!)**, regional subnets, firewall rules, Cloud NAT, Cloud Load Balancing (global anycast) | The structural outlier: one VPC can span the planet; subnets are regional. |
| **Storage & data** | **Cloud Storage** (object), **Persistent Disk / Hyperdisk** (block, zonal *or* regional), Filestore, Cloud SQL / Spanner | Fewer, more orthogonal products than AWS's sprawl. |
| **Provisioning & config** | **gcloud**, **Terraform**, projects + org hierarchy | Projects are the account/blast-radius unit; the org hierarchy is the guardrail surface. |
| **Observability** | **Cloud Operations** — Monitoring, Logging, Trace — with **native SLO tooling** | Google's SRE heritage shows: SLOs are built in, not bolted on. |
| **Security & compliance** | Cloud IAM, **Security Command Center**, Org Policy, default-on encryption, **Budgets** | Secure-by-default posture; Org Policy is the preventive guardrail. |

Know those service names and which surface each belongs to, and you can hold a real
GCP conversation. The map is nearly identical to AWS's — which is exactly the point.

## 2. The admin skill map

The concrete, checkable list of what a GCP administrator must be *able to do*. Full
checklist with proficiency tiers in **[`skills-map.md`](skills-map.md)**. The
headline capabilities, with the GCP-specific deltas called out:

- **IAM done right** — roles + bindings on the resource hierarchy; **service
  accounts** as workload identity (no keys on the box); the primitive-vs-predefined-
  vs-custom-role distinction.
- **A network you designed — remembering it's global** — one VPC, **regional
  subnets**, firewall rules targeting tags/service accounts; the multi-region design
  that's "just routes" here and needs peering elsewhere ([`the-stack/02`](../../the-stack/02-network.md)).
- **Compute you can run and scale** — Compute Engine from code, **custom machine
  types** (dial exact vCPU/memory), instance templates → Managed Instance Groups,
  live migration.
- **Storage with the right defaults** — Cloud Storage classes + access control;
  **regional Persistent Disk** as a cleaner HA primitive than AZ-locked block.
- **Everything from code** — Terraform against GCP; **projects and the org
  hierarchy** as the structure and blast-radius model.
- **You'd see it break** — Cloud Monitoring alerts, Cloud Logging queries, and the
  **built-in SLO tooling** ([`the-stack/06`](../../the-stack/06-observability.md)).
- **Secure and within budget** — a **budget alert first**, default-on encryption,
  **Org Policy** guardrails, Security Command Center ([`the-stack/07`](../../the-stack/07-security.md)).
- **GKE** — the reference managed Kubernetes; see [`cross-cutting/kubernetes.md`](../../cross-cutting/kubernetes.md).

## 3. The AI-assisted path to competence

The method — going from "knows AWS/Azure + on-prem" to "can operate GCP" in days —
is in **[`ai-ramp.md`](ai-ramp.md)**. In one paragraph:

GCP is the purest demonstration of this repo's thesis, because so much of it is a
*renaming* of surfaces already mapped elsewhere. Use AI to translate — *"I know AWS
VPCs and IAM; map GCP networking and IAM onto them and flag only the genuine
differences"* — and the ramp is mostly hunting the four structural outliers (global
VPC, project/org hierarchy, custom machine types, service-account-centric IAM).
Then verify every role name and API against current docs and run it in a sandbox
with a budget alert. AI writes the first draft; your judgment — earned on AWS/Azure
and on-prem — is the review gate.

## 4. Labs

Reading about a global VPC and building one are different skills. A **three-lab CLI
arc** (scoped identity + inventory → global-VPC network + instance → secure storage +
budget) is in **[`labs/`](labs/)** with real `gcloud` commands — the second lab is
where the global-VPC model visibly changes the commands vs. the AWS version.

## 5. Going deeper — architecture, operations, automation & support

Four companion notes take GCP past "what the services are", mirroring the AWS set:

- **[`architecture.md`](architecture.md)** — how GCP is *structured*: the resource
  hierarchy (Org → Folders → Projects) as the blast-radius unit, regions & zones, the
  **global-VPC outlier**, service-account-centric IAM, shared responsibility, and a
  reference three-tier showing every surface compose.
- **[`operations.md`](operations.md)** — *running* GCP day-2: the brief, the ops notes
  (what pages you), the recurring work **broken down by cadence**, and **how AI
  assists the operating loop** — including AI's GCP-specific trap of handing you
  AWS-shaped (regional-VPC) advice.
- **[`automation.md`](automation.md)** — **scripting the API**: the
  `identity → client → API call` model, the `gcloud`-vs-client-library-vs-Terraform
  altitude ladder, ADC and attached service accounts (never a key file in the
  script), the rules (iterate projects/regions/zones, Cloud Asset Inventory for bulk,
  idempotence, read-only-first), and the read-audit vs. remediation shapes.
- **[`support.md`](support.md)** — **the break-fix craft (GCP + GKE)**: what supporting
  GCP makes you responsible for, the recurring tickets and *where you look* (the
  `403 PERMISSION_DENIED` hierarchy walk, the global-VPC firewall, and the GKE
  deep-dive — the auth plugin, the **IAM-vs-RBAC two planes**, `IP_SPACE_EXHAUSTED`),
  and the load-bearing AWS instincts an admin must **unlearn** — with a runnable
  GKE-auth lab and a verified GitHub field kit.

## Honest boundaries

🧗 **honest ramp — and labeled as one.** No production GCP operations claimed: this
module is the transferable operating model (AWS/Azure surfaces + on-prem depth)
mapped onto GCP's names and verified against current docs — exactly the ramp method
[`WHY.md`](../../WHY.md) argues for. The structural differences (global VPC,
projects, custom machine types, service-account IAM) are called out precisely
because they're where the "GCP is just AWS" reflex fails. The claim isn't "years on
GCP"; it's "a transferable model plus a fast, verifiable ramp" — the same honest
position as every 🧗 module in this repo.
