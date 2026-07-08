# Contents — the whole map

> The detailed index: every module, what it is, and where it lives.
> [`README.md`](README.md) is the front door and the shape; [`ROADMAP.md`](ROADMAP.md)
> says what to build *next and why*; this page is the table of contents.

The project crosses the same material along **four axes** — you enter from whichever
matches your question, not front to back. Everything the roadmap planned is now
**written** (✅); what remains is more runnable labs, Chinese mirrors, and deepening.

| # | Axis | Read it when you want to… |
| --- | --- | --- |
| **I** | **Start here** | understand the philosophy and the method |
| **II** | **Foundations** | shore up the Linux + scripting base |
| **III** | **The Stack** | compare all seven platforms layer by layer |
| **IV** | **Platforms** | operate one platform end to end |
| **V** | **Cross-cutting** | learn a transferable skill |

---

## I. Start here — the thesis and the method

| Module | What it is | Status |
| --- | --- | --- |
| [`WHY.md`](WHY.md) | Why this exists; where the craft is heading in the AI era | ✅ |
| [`00-the-operating-model.md`](00-the-operating-model.md) | The transferable skeleton — three moves, seven surfaces | ✅ |
| [`ai-workflow/`](ai-workflow/) | How AI is used to learn and operate — and kept honest | ✅ |

## II. Foundations — the base everything assumes

| Module | What it is | Status |
| --- | --- | --- |
| [`foundations/`](foundations/) | Linux + scripting (Python/Bash/PowerShell) — the floor under every role | ✅ |

## III. The Stack — read by layer, bottom-up (✅ complete, 01→07)

Seven platforms compared at every layer, written from the machine room up. The
project's most distinctive axis. See [`the-stack/`](the-stack/).

| Chapter | Covers | Status |
| --- | --- | --- |
| [`01-physical`](the-stack/01-physical.md) | data centers, hardware, hypervisors, failure domains | ✅ |
| [`02-network`](the-stack/02-network.md) | underlay/overlay, VPC models, the egress meter, the debug ladder | ✅ |
| [`03-compute-and-images`](the-stack/03-compute-and-images.md) | compute shapes, the image pipeline, bake vs. fry, cloud-init | ✅ |
| [`04-storage`](the-stack/04-storage.md) | block/file/object, the backup fear · **+ runnable [lab](the-stack/labs/04-backup-not-snapshot/)** | ✅ |
| [`05-platform-services`](the-stack/05-platform-services.md) | containers, serverless, managed DBs, build-vs-rent | ✅ |
| [`06-observability`](the-stack/06-observability.md) | metrics/logs/traces, SLI/SLO, OpenTelemetry | ✅ |
| [`07-security`](the-stack/07-security.md) | shared responsibility, defense in depth, CSPM/EDR/SIEM | ✅ |

## IV. Platforms — read by platform (all seven)

Every module is `README` (what-it-is + skill map + AI-ramp summary) · `skills-map` ·
`ai-ramp` · a **3-lab CLI arc** in `labs/`; the public clouds add the deeper
**architecture · operations · automation** trio. All seven platforms compared in The
Stack have a module. See [`platforms/`](platforms/).

**Public clouds** — a rented data centre you drive by API:

| Platform | What's there · honesty |
| --- | --- |
| [`aws/`](platforms/aws/) | ✅ worked example + [architecture](platforms/aws/architecture.md)/[operations](platforms/aws/operations.md)/[automation](platforms/aws/automation.md) + labs (**2 runnable** + 3-lab CLI arc). Read first. · 🧗 |
| [`azure/`](platforms/azure/) | ✅ + [architecture](platforms/azure/architecture.md)/[operations](platforms/azure/operations.md)/[automation](platforms/azure/automation.md) + 3-lab CLI arc. · 🧗, **Entra/identity ✋** |
| [`gcp/`](platforms/gcp/) | ✅ + [architecture](platforms/gcp/architecture.md)/[operations](platforms/gcp/operations.md)/[automation](platforms/gcp/automation.md) + 3-lab CLI arc. Global-VPC is the outlier. · 🧗 |
| [`oci/`](platforms/oci/) | ✅ + [architecture](platforms/oci/architecture.md)/[operations](platforms/oci/operations.md)/[automation](platforms/oci/automation.md) + 3-lab CLI arc. Youngest hyperscaler — compartments, OCPU, bare-metal-first, cheap egress. · 🧗 |

**Private cloud / on-prem** — the platforms you run on your *own* hardware:

| Platform | What's there · honesty |
| --- | --- |
| [`vsphere/`](platforms/vsphere/) | ✅ + [architecture](platforms/vsphere/architecture.md)/[operations](platforms/vsphere/operations.md)/[automation](platforms/vsphere/automation.md) + 3-lab CLI arc (PowerCLI). AMS-region vCenter admin, VCP6-DCV/NV. · **✋ hands-on depth — a strength, not a ramp** |
| [`openstack/`](platforms/openstack/) | ✅ + [architecture](platforms/openstack/architecture.md)/[operations](platforms/openstack/operations.md)/[automation](platforms/openstack/automation.md) + 3-lab CLI arc (DevStack). "You build the cloud"; control-plane-as-product. · 🧗 (KVM-adjacent ✋) |
| [`self-host/`](platforms/self-host/) | ✅ + [architecture](platforms/self-host/architecture.md)/[operations](platforms/self-host/operations.md)/[automation](platforms/self-host/automation.md) + 3-lab CLI arc. PXE/image fleet 100k+, BMC/IPMI, DNS/RAID. · **✋ hands-on depth — the deepest root** |

## V. Cross-cutting — read by theme (the transferable surfaces)

The layers that transfer across every platform. Some are **dedicated notes**; some
read more naturally *by layer* in The Stack and are **cross-linked, not duplicated**.
See [`cross-cutting/`](cross-cutting/).

| Theme | Home | Status |
| --- | --- | --- |
| [`identity-iam`](cross-cutting/identity-iam.md) | dedicated note | ✅ |
| [`iac-and-config`](cross-cutting/iac-and-config.md) | dedicated note (Terraform/Ansible/Puppet) | ✅ |
| [`ci-cd`](cross-cutting/ci-cd.md) | dedicated note (CI/CD pipelines, GitOps, rollback) | ✅ |
| [`databases`](cross-cutting/databases.md) | dedicated note (backup/PITR, replication, self-run vs managed) — **✋** | ✅ |
| [`itsm-and-assets`](cross-cutting/itsm-and-assets.md) | dedicated note (ITSM, CMDB, asset reconciliation, access governance) — **✋** | ✅ |
| [`endpoint/`](endpoint/) | dedicated track (Jamf/Intune/PXE/patching) | ✅ |
| [`saas-admin`](cross-cutting/saas-admin.md) | dedicated note (Google Workspace / M365) | ✅ |
| [`m365-support`](cross-cutting/m365-support.md) | dedicated note (M365 break-fix craft + the cross-lane transition) — **✋** | ✅ |
| [`kubernetes`](cross-cutting/kubernetes.md) | dedicated note (deeper than the-stack/05) | ✅ |
| [`service-mesh`](cross-cutting/service-mesh.md) | dedicated note (service discovery + mesh; and when not to) | ✅ |
| [`web-and-tls`](cross-cutting/web-and-tls.md) | dedicated note (reverse proxy, TLS/cert lifecycle) — **✋** fundamentals | ✅ |
| [`incident-response`](cross-cutting/incident-response.md) | dedicated note (incident lifecycle, on-call, blameless post-mortem) | ✅ |
| [`working-with-security`](cross-cutting/working-with-security.md) | dedicated note (working with InfoSec/SOC + ATT&CK awareness for operators) — **✋** ops-security | ✅ |
| [`cost`](cross-cutting/cost.md) | dedicated note (cost as a control) | ✅ |
| networking | → [`the-stack/02`](the-stack/02-network.md) | ✅ in The Stack |
| storage | → [`the-stack/04`](the-stack/04-storage.md) | ✅ in The Stack |
| virtualization | → [`the-stack/01`](the-stack/01-physical.md) | ✅ in The Stack |
| observability | → [`the-stack/06`](the-stack/06-observability.md) | ✅ in The Stack |
| security-compliance | → [`the-stack/07`](the-stack/07-security.md) | ✅ in The Stack |

---

## Agent Skills — the method, made invokable

The repo ships four [`.claude/skills/`](.claude/skills/) that package its methodology
as AI workflows: [`platform-ramp`](.claude/skills/platform-ramp/SKILL.md) (ramp onto
any platform, honestly), [`honesty-audit`](.claude/skills/honesty-audit/SKILL.md)
(classify claims ✋/🧗/overclaim), [`author-module`](.claude/skills/author-module/SKILL.md)
(write a new note in the repo's voice), and
[`runnable-lab`](.claude/skills/runnable-lab/SKILL.md) (turn a concept into a
self-verifying drill).

## The honesty layer (applies everywhere)

Every module marks **✋ hands-on depth** vs. **🧗 verified ramp** per
[`WHY.md`](WHY.md) — and the marking is load-bearing, not decoration. Two of the seven
platforms are **✋**: [vSphere](platforms/vsphere/) (a production vCenter estate,
VCP6-DCV/NV) and [self-host](platforms/self-host/) (a 100k+ device fleet), alongside
the cross-cutting strengths — Linux, [endpoint](endpoint/),
[identity](cross-cutting/identity-iam.md), [SaaS admin](cross-cutting/saas-admin.md),
and the automation discipline. The public clouds, OpenStack's control plane, and deep
Kubernetes are honest **🧗** ramps — mapped, verified, and runnable, never bluffed.
That distinction is the whole point ([`WHY.md`](WHY.md) explains why it matters more in
the AI era, not less).
