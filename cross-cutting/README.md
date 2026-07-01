# cross-cutting/

The layers that transfer across **every** cloud. Learn these as concepts once and
you're mostly translating vocabulary on each platform. This is where a systems
admin's existing depth (Linux, networking, identity, automation) pays off the most.

Planned notes (added as the platform modules mature):

| Note | What it covers |
| --- | --- |
| `identity-iam.md` | Least-privilege, roles vs. policies, short-lived credentials, lifecycle — the same discipline on AWS IAM, Azure RBAC, GCP IAM. |
| `networking.md` | Virtual networks, subnets, routing, firewalls, DNS, load balancing, private connectivity — cloud names for on-prem fundamentals. |
| `terraform-iac.md` | Infrastructure-as-code as the universal control plane: state, modules, plan/apply/destroy, review, drift. One tool, every cloud. |
| `kubernetes.md` | Containers + orchestration across EKS / AKS / GKE — the layer that's *most* portable between clouds. |
| `observability.md` | Metrics, logs, traces, alerts, SLIs/SLOs — "is it healthy, and how do I know," everywhere. |
| `security-compliance.md` | Encryption, secrets, hardening, audit, guardrails, policy-as-code — provable safety. |
| `cost.md` | Cost as a first-class operational control: budgets, alarms, right-sizing, the "forgotten GPU instance" problem. |

> The point of this folder: after AWS, most of Azure and GCP is *"which of these
> concepts is renamed to what, and what's the quirk?"* — a question that's fast to
> answer once the concept itself is solid.
