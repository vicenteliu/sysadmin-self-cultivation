---
kind: lab
axis: the-stack
themes: []
platforms: [aws]
summary: "Runnable evidence for the layer series. Each chapter's \"Lab\" section is a spec; this folder is where those specs become code you can actually run and verify."
---
# The Stack — Labs

> 🌐 **Languages:** English (default) · [中文](../../docs/zh/the-stack/labs/README.md)

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
| [`02-first-match-and-longest-prefix/`](02-first-match-and-longest-prefix/) | [02 network](../02-network.md) | a routing table is order-independent and a ruleset is order-dependent; carrying one intuition into the other gives two mirror failures, and neither announces itself | Python 3.8+ only |
| [`03-one-image-is-not-one-image/`](03-one-image-is-not-one-image/) | [03 compute](../03-compute-and-images.md) | `latest` is a query answered at build time; the inventory records two machines as identical and is not lying | Python 3.8+ only |
| [`04-backup-not-snapshot/`](04-backup-not-snapshot/) | [04 storage](../04-storage.md) | replication faithfully copies destruction; only an independent backup recovers you, up to its RPO | Python 3.8+ only |
| [`06-no-data-is-not-healthy/`](06-no-data-is-not-healthy/) | [06 observability](../06-observability.md) | a monitor inside the domain it watches dies with it, and no threshold alert can fire on data that never arrived | Python 3.8+ only |
| [`07-detection-is-a-window/`](07-detection-is-a-window/) | [07 security](../07-security.md) | prevention is zero exposure for the classes a policy names; detection is a window; and a leaked credential's window does not close when the ticket does | Python 3.8+ only |

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
Running-but-not-Ready pod is pulled from the Service endpoints), and
[`cross-cutting/labs/multi-cloud-cidr-overlap/`](../../cross-cutting/labs/multi-cloud-cidr-overlap/)
(multi-cloud networking — why overlapping CIDRs can't be peered, and there's no central router
across clouds).

## What each chapter still asks you to do yourself

Every chapter also ends with a **[guided run](../../CONTEXT.md)** — Terraform on two
clouds, one Packer image booted on two, Prometheus and an OTel trace, a real bucket
broken and caught by a real posture scanner. Those are not labs and this folder will
never contain them: nothing here can assert that you did one, and CI cannot run it.
That is the whole of the distinction and it is not a demotion — a guided run reaches
real latency, real error messages and real bills, which no model does.

The five labs above are what was **modellable** in those specs: the reasoning failure
underneath each guided run, extracted and made to assert itself. Chapter 05 has no lab
because its argument — build versus rent — is a decision about your own estate rather
than a mechanism, and a model of it would be a model of the assumptions you fed it.

Labs are added as chapters stabilize. The pure-local ones come first — evidence
should be cheap to reproduce.
