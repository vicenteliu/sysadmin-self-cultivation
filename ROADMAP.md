# Roadmap

> This project is built **demand-first**. The order below is set by how often each
> skill shows up in real **infrastructure / platform / IT-engineering job
> descriptions** — so the repo grows toward what the market actually asks for, not an
> arbitrary syllabus.

## The demand signal

Across a sample of ~40 recent US infra / platform / IT-engineering postings, the
most-requested technical skills clustered like this (roughly, by frequency):

| Cluster | Shows up as | ~How often |
| --- | --- | --- |
| **Linux + scripting** | Linux (RHEL/Ubuntu), Python, Bash | near-universal |
| **Identity & access** | AD, Entra/Azure AD, Okta, SSO/SAML/OIDC, SCIM, IAM/RBAC, least-privilege, joiner/mover/leaver | very high (the single densest cluster) |
| **Endpoint & MDM** | macOS, Windows, Jamf, Intune, PXE/imaging, patching | very high |
| **Networking** | TCP/IP, DNS, DHCP, routing/switching, firewalls (Palo Alto/Fortinet), VPN | high |
| **IaC & config mgmt** | Ansible, Terraform, Git/CI-CD, Puppet | high |
| **Security & compliance** | hardening/baselines, EDR/XDR, SIEM, zero-trust, SOC 2 / SOX / GDPR / FedRAMP | high |
| **Virtualization** | VMware/vSphere/ESXi, KVM, Proxmox | high |
| **Cloud** | AWS, Azure, GCP, OpenStack, OCI | medium–high |
| **Containers** | Kubernetes (EKS/AKS/GKE), Docker | medium |
| **Observability / SRE** | monitoring, SLIs/SLOs, incident response | medium |
| **Collaboration / SaaS** | Google Workspace, M365, ITSM, enterprise AI tooling | medium |

The takeaway that shapes this repo: the center of gravity for these roles is the
**operate-and-automate lane** — Linux + scripting + endpoint + **identity** +
config-management — with the clouds as one important surface among several. So the
roadmap leads with the **cross-cutting** skills that transfer across every platform,
and treats each cloud as a place to *prove* the model rather than the whole point.

## Status

| Area | Module | Status |
| --- | --- | --- |
| Thesis | [`00-the-operating-model.md`](00-the-operating-model.md) | ✅ |
| Thesis | [`WHY.md`](WHY.md) | ✅ |
| Method | [`ai-workflow/`](ai-workflow/) | ✅ |
| Platform | [`platforms/aws/`](platforms/aws/) | ✅ + 2 runnable labs |
| Platform | [`platforms/azure/`](platforms/azure/) | ✅ (labs planned) |
| Cross-cutting | [`cross-cutting/identity-iam.md`](cross-cutting/identity-iam.md) | ✅ |
| Layer series | [`the-stack/01-physical.md`](the-stack/01-physical.md) — physical layer, 7 platforms compared | ✅ |
| Layer series | [`the-stack/02-network.md`](the-stack/02-network.md) — network layer (covers Tier-1 item #2) | ✅ |
| Layer series | [`the-stack/03-compute-and-images.md`](the-stack/03-compute-and-images.md) — compute & the image pipeline | ✅ |
| Layer series | [`the-stack/04-storage.md`](the-stack/04-storage.md) — storage layer (block/file/object, backup) | ✅ |
| Layer series | [`the-stack/05-platform-services.md`](the-stack/05-platform-services.md) — platform services (build-vs-rent) | ✅ |
| Layer series | [`the-stack/06-observability.md`](the-stack/06-observability.md) — observability (3 pillars, SLI/SLO, OTel; covers Tier-3 #9) | ✅ |
| Layer series | [`the-stack/07-security.md`](the-stack/07-security.md) — security (shared-resp, defense-in-depth, CSPM/EDR/SIEM; covers Tier-2 #6) | ✅ |
| Layer series | **the-stack 01→07 complete** — 5 bottom-up layers + observability + security (two cross-cutting caps) | ✅ |
| Layer lab | [`the-stack/labs/04-backup-not-snapshot/`](the-stack/labs/04-backup-not-snapshot/) — runnable, pure-Python "replication is not backup" drill | ✅ |
| Framework | [`CONTENTS.md`](CONTENTS.md) + opening for every planned module (foundations/endpoint/iac/saas/k8s/cost/gcp) | ✅ |
| Foundations | [`foundations/`](foundations/) — Linux mental model, debugging reflex, scripting, honest scope (Tier-3 #10) | ✅ written |
| Endpoint | [`endpoint/`](endpoint/) — MDM model, imaging pipeline, patch/EDR, BYOD, Intune-as-ramp (Tier-2 #5) | ✅ written |
| SaaS admin | [`cross-cutting/saas-admin.md`](cross-cutting/saas-admin.md) — Google Workspace / M365, identity spine, SCIM lifecycle (Tier-3 #11) | ✅ written |
| IaC & config | [`cross-cutting/iac-and-config.md`](cross-cutting/iac-and-config.md) — provisioning vs. config, Terraform state, Ansible, drift (Tier-1 #3) | ✅ written |
| Cost | [`cross-cutting/cost.md`](cross-cutting/cost.md) — cost as an ops signal, shapes, surprises, right-sizing, anomaly alerts | ✅ written |

## Build order (demand-driven)

> **Note (2026-07):** the layer-first series [`the-stack/`](the-stack/) is now the
> vehicle for several items below — networking (#2) lands as
> `the-stack/02-network.md`, virtualization (#7) is carried from
> `the-stack/01-physical.md` onward, and OpenStack/OCI (#11) are compared in every
> chapter rather than getting late standalone folders.

### Tier 1 — highest ROI (highest demand, most transferable)

1. **`cross-cutting/identity-iam.md`** — ✅ *done.* The densest demand cluster
   (AD / Entra / Okta / SSO / SCIM / RBAC / lifecycle) and the most transferable
   surface across every platform.
2. **`cross-cutting/networking.md`** — the cloud/on-prem networking fundamentals every
   role assumes (TCP/IP, DNS, DHCP, routing, firewalls, load balancing).
3. **`cross-cutting/iac-and-config.md`** — Terraform + Ansible + Puppet as one
   universal control plane. (Ansible is one of the most-requested single tools.)
4. **`platforms/gcp/`** — completes the three-cloud story; structure mirrors AWS/Azure.

### Tier 2 — high demand, real depth

5. **`endpoint/`** — a first-class track for the endpoint/MDM lane (Jamf, Intune,
   PXE/imaging, patching, macOS/Windows fleet) — a very-high-demand area the platform
   folders don't cover.
6. **`cross-cutting/security-compliance.md`** — hardening/baselines, EDR/XDR, SIEM,
   zero-trust, and compliance-by-name (SOC 2 / SOX / GDPR / FedRAMP / ISO 27001).
7. **`cross-cutting/virtualization.md`** — VMware/vSphere, KVM, Proxmox.
8. **`cross-cutting/kubernetes.md`** — containers + orchestration across EKS/AKS/GKE.

### Tier 3 — round it out

9. **`cross-cutting/observability.md`** — metrics/logs/traces, SLIs/SLOs, incident response.
10. **`foundations/`** — Linux + scripting (Python/Bash/PowerShell) as the assumed base, made explicit.
11. **`cross-cutting/storage.md`**, SaaS admin (Google Workspace / M365), and additional platforms (OpenStack, OCI) as warranted.

## How this stays honest

Every module marks what's **hands-on depth** vs. an **honest ramp** — the roadmap is
weighted toward writing the strengths well *and* closing the common gaps visibly,
rather than pretending uniform expertise. See [`WHY.md`](WHY.md) for why that
distinction is the whole point.
