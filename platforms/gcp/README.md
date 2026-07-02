# Google Cloud Platform (GCP)

> 🚧 **Opening written; body in progress.** The framework below is complete —
> what this module will cover is fixed; the prose is being filled in. Follows the
> same four-part template as [`aws/`](../aws/) (the worked example) and
> [`azure/`](../azure/).

> The third cloud completes the story. Once AWS and Azure are mapped, GCP is
> mostly *"what's their word for it, and what's the one structural thing that's
> genuinely different?"* — and GCP has a real one: the **global VPC**.

GCP is where the operating model's promise gets its cleanest test: an experienced
admin who knows the [seven surfaces](../../00-the-operating-model.md) should be able
to ramp onto it fast, because the concepts are identical and only the names and a
few defaults change. This module maps those names — and flags the places GCP
genuinely diverges (global networking, custom machine types, project-based
structure) rather than pretending it's AWS with different logos.

## Planned coverage (the seven surfaces)

- **Identity** — Cloud Identity, IAM roles + bindings, service accounts (the
  workload-identity story), Workforce Identity Federation. Ties to
  [`cross-cutting/identity-iam.md`](../../cross-cutting/identity-iam.md).
- **Compute** — Compute Engine, machine types **plus custom machine types** (the
  dial, not just the menu), Managed Instance Groups, live migration.
- **Networking** — the **global VPC** (the structural outlier from
  [`the-stack/02`](../../the-stack/02-network.md)), regional subnets, VPC-level
  firewall rules, Cloud NAT, global anycast load balancing.
- **Storage** — Persistent Disk / Hyperdisk (zonal *or* regional), Filestore, Cloud
  Storage; the fewer-more-orthogonal-products design.
- **Provisioning** — gcloud, Terraform, Deployment Manager; project + org structure
  as the account model.
- **Observability** — Cloud Operations (Monitoring/Logging/Trace) with SLO tooling
  built in (the SRE-heritage advantage from [`the-stack/06`](../../the-stack/06-observability.md)).
- **Security** — Security Command Center, Org Policy guardrails, default-on
  encryption; the secure-by-default posture from [`the-stack/07`](../../the-stack/07-security.md).
- **GKE** — Google's Kubernetes, widely treated as the reference; see
  [`cross-cutting/kubernetes.md`](../../cross-cutting/kubernetes.md).

## Companion files

- [`skills-map.md`](skills-map.md) — the checkable competency list (Core/Working/Depth). 🚧
- [`ai-ramp.md`](ai-ramp.md) — the AI-assisted method to get competent fast. 🚧
- `labs/` — runnable exercises (planned; mirror the AWS lab shape).

## Honest boundaries

🧗 **honest ramp.** No production GCP operations claimed — this module is the
transferable model (AWS/Azure surfaces + on-prem depth) mapped onto GCP's names and
verified against current docs, exactly the ramp method [`WHY.md`](../../WHY.md)
argues for. The structural differences (global VPC, projects, custom machine types)
are called out precisely because they're where "GCP is just AWS" gets you burned.
