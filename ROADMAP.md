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

## Build order (demand-driven)

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
