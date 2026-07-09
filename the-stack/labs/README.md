# The Stack — Labs

Runnable evidence for the layer series. Each chapter's "Lab" section is a spec;
this folder is where those specs become code you can actually run and verify.

> **Design bias:** these labs prefer **pure-local, zero-cost, zero-credential**
> exercises where the concept allows it — so anyone can run them, and CI can too.
> Where a lab genuinely needs a cloud or a hypervisor, it says so and stays
> tear-down-able (the platform-folder labs, e.g. [`platforms/aws/labs/`](../../platforms/aws/labs/),
> follow the sandbox-account + hard-budget-alarm ground rules).

## Built

| Lab | Chapter | What it proves | Needs |
| --- | --- | --- | --- |
| [`01-failure-domains/`](01-failure-domains/) | [01 physical](../01-physical.md) | co-located replicas share a fate; anti-affinity across failure domains is what "highly available" means | Python 3.8+ only |
| [`04-backup-not-snapshot/`](04-backup-not-snapshot/) | [04 storage](../04-storage.md) | replication faithfully copies destruction; only an independent backup recovers you, up to its RPO | Python 3.8+ only |

There are also runnable labs outside The Stack, same pure-local spirit:
[`foundations/labs/idempotence-drill/`](../../foundations/labs/idempotence-drill/)
(fragile vs. `set -euo pipefail`-safe scripting, bash),
[`cross-cutting/labs/ci-cd-pipeline/`](../../cross-cutting/labs/ci-cd-pipeline/) (a real
GitHub Actions pipeline + a tested app),
[`cross-cutting/labs/m365-conditional-access-lockout/`](../../cross-cutting/labs/m365-conditional-access-lockout/)
(a Conditional Access policy that locks the admin out — the tenant-wide blast radius,
felt), and
[`platforms/aws/labs/iam-deny-by-default/`](../../platforms/aws/labs/iam-deny-by-default/)
(AWS IAM policy evaluation — deny-by-default and why `Allow *` isn't the fix), and
[`platforms/gcp/labs/gke-iam-vs-rbac/`](../../platforms/gcp/labs/gke-iam-vs-rbac/)
(GKE's two auth planes — why "I'm Owner but kubectl says Forbidden"), and
[`platforms/azure/labs/global-admin-is-not-owner/`](../../platforms/azure/labs/global-admin-is-not-owner/)
(Azure's two identity planes — why a Global Admin is not an Owner), and
[`platforms/oci/labs/a-compartment-is-not-an-account/`](../../platforms/oci/labs/a-compartment-is-not-an-account/)
(OCI's verb hierarchy + compartment scope — why `NotAuthorizedOrNotFound` is a 404 and a
compartment is not an account), and
[`cross-cutting/labs/terraform-state-and-drift/`](../../cross-cutting/labs/terraform-state-and-drift/)
(Terraform's config/state/real triangle — why a hand-edit gets reverted, an immutable attribute
forces a destroy, and `count` churns where `for_each` stays stable), and
[`cross-cutting/labs/k8s-reconcile-loop/`](../../cross-cutting/labs/k8s-reconcile-loop/)
(Kubernetes' reconciliation loop — why a deleted pod comes back, an exec-fix vanishes, and a
Running-but-not-Ready pod is pulled from the Service endpoints).

## Planned (specs live in each chapter)

| Lab | Chapter | Sketch |
| --- | --- | --- |
| `02-network-debug-ladder/` | [02 network](../02-network.md) | one 3-tier network built twice (Terraform on two clouds); break it 4 ways, fix with the debug ladder |
| `03-one-image-two-clouds/` | [03 compute](../03-compute-and-images.md) | Packer golden image + cloud-init to KVM and one cloud; sabotage the image, recover from the serial console |
| `06-see-the-request/` | [06 observability](../06-observability.md) | Prometheus + Grafana + an OTel trace; define an SLO and blow the error budget on purpose |
| `07-break-the-default/` | [07 security](../07-security.md) | misconfigure a bucket public, catch it with a posture scan, then make it impossible with policy-as-code |

Labs are added as chapters stabilize. The pure-local ones come first — evidence
should be cheap to reproduce.
