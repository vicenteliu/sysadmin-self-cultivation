# cross-cutting/

The layers that transfer across **every** cloud. Learn these as concepts once and
you're mostly translating vocabulary on each platform. This is where a systems
admin's existing depth (Linux, networking, identity, automation) pays off the most.

**Dedicated notes** — themes best learned as one concept across all platforms:

| Note | What it covers | Status |
| --- | --- | --- |
| [`identity-iam.md`](identity-iam.md) | Least-privilege, roles vs. policies, short-lived credentials, lifecycle (JML), SSO/SAML/OIDC, SCIM — same discipline on AD, Entra, AWS IAM, Azure RBAC, GCP IAM, Okta. | ✅ |
| [`iac-and-config.md`](iac-and-config.md) | Provisioning (Terraform) vs. config management (Ansible/Puppet): state, modules, plan/apply/destroy, idempotence, drift. | ✅ |
| [`ci-cd.md`](ci-cd.md) | The deployment pipeline: CI/CD, build-once-promote, OIDC over keys, GitOps (pull vs. push), rollback. | ✅ |
| [`databases.md`](databases.md) | Operating the stateful hard part: availability, recoverability (backup/PITR), performance, self-run vs. managed. **✋** | ✅ |
| [`itsm-and-assets.md`](itsm-and-assets.md) | ITSM (incident/request/change), the CMDB, asset reconciliation, access governance & audit. **✋** | ✅ |
| [`saas-admin.md`](saas-admin.md) | Google Workspace & M365 administration, the identity spine, SCIM lifecycle — the productivity suite as a managed estate. | ✅ |
| [`kubernetes.md`](kubernetes.md) | The object model and operator's view, one layer deeper than the-stack/05; managed vs. self-run, the debugging reflex. | ✅ |
| [`cost.md`](cost.md) | Cost as a first-class operational control: budgets, alarms, right-sizing, the "forgotten GPU instance" problem. | ✅ |

**Covered by layer in [`the-stack/`](../the-stack/)** — cross-linked, not
duplicated (these read more naturally as layers than as standalone themes):

| Theme | Where |
| --- | --- |
| networking | [`the-stack/02-network.md`](../the-stack/02-network.md) |
| storage | [`the-stack/04-storage.md`](../the-stack/04-storage.md) |
| virtualization | [`the-stack/01-physical.md`](../the-stack/01-physical.md) |
| observability | [`the-stack/06-observability.md`](../the-stack/06-observability.md) |
| security & compliance | [`the-stack/07-security.md`](../the-stack/07-security.md) |

> The point of this folder: after AWS, most of Azure and GCP is *"which of these
> concepts is renamed to what, and what's the quirk?"* — a question that's fast to
> answer once the concept itself is solid. See [`../CONTENTS.md`](../CONTENTS.md)
> for how this folder fits the whole map.
