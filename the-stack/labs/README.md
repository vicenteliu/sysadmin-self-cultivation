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
| [`04-backup-not-snapshot/`](04-backup-not-snapshot/) | [04 storage](../04-storage.md) | replication faithfully copies destruction; only an independent backup recovers you, up to its RPO | Python 3.8+ only |

## Planned (specs live in each chapter)

| Lab | Chapter | Sketch |
| --- | --- | --- |
| `01-failure-domains/` | [01 physical](../01-physical.md) | nested virt: a PXE-booted "fleet," two "racks," kill one and see what survives |
| `02-network-debug-ladder/` | [02 network](../02-network.md) | one 3-tier network built twice (Terraform on two clouds); break it 4 ways, fix with the debug ladder |
| `03-one-image-two-clouds/` | [03 compute](../03-compute-and-images.md) | Packer golden image + cloud-init to KVM and one cloud; sabotage the image, recover from the serial console |
| `06-see-the-request/` | [06 observability](../06-observability.md) | Prometheus + Grafana + an OTel trace; define an SLO and blow the error budget on purpose |
| `07-break-the-default/` | [07 security](../07-security.md) | misconfigure a bucket public, catch it with a posture scan, then make it impossible with policy-as-code |

Labs are added as chapters stabilize. The pure-local ones come first — evidence
should be cheap to reproduce.
