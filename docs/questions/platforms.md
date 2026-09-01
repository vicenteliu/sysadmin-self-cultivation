---
kind: questions
axis: meta
themes: []
platforms: []
summary: "Questions asked of this repo about cloud network design and about self-hosted virtualisation — one closed as out of scope, one open with runnable tools already built."
---
# Questions · Platforms and virtualisation

> The index, the status legend and the out-of-scope reasoning live one level up in
> [`docs/questions.md`](../questions.md).

| # | Question | Status | Where |
|---|---|---|---|
| 1 | How do AWS, GCP and Oracle Cloud each design their network services? | ✅ per platform · **closed** as a three-way note | [`platforms/aws`](../../platforms/aws/architecture.md) · [`azure`](../../platforms/azure/architecture.md) · [`gcp`](../../platforms/gcp/architecture.md) · [`oci`](../../platforms/oci/architecture.md), and [`the-stack/02`](../../the-stack/02-network.md) is already the place this repo compares one layer across seven platforms. A separate three-way note would repeat it at mixed footing — see [Boundaries](../questions.md#boundaries) |
| 2 | Self-hosting a VM estate: what actually differs between vCenter and Proxmox, and what are the options? | ✅ | [`vcenter-and-proxmox.md`](../../platforms/vsphere/vcenter-and-proxmox.md) — where each control plane lives and what you lose when it dies, and the finding that a hypervisor migration is a storage-and-guest-support project wearing a hypervisor costume |
