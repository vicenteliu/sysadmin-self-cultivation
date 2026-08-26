---
kind: index
axis: platforms
themes: []
platforms: []
summary: "One folder per platform. Every module follows the same four-part template so you can move between them without re-learning how to read…"
---
# platforms/

One folder per platform. Every module follows the **same four-part template** so you
can move between them without re-learning how to read them:

1. **`README.md`** — what it is (mapped to the seven surfaces) + the headline skill map + the AI-ramp summary.
2. **`skills-map.md`** — the full, checkable competency list (Core / Working / Depth).
3. **`ai-ramp.md`** — the AI-assisted method to get competent fast, and how to keep AI honest.
4. **`labs/`** — runnable, tear-down-able exercises.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../site/assets/diagrams/seven-surfaces.dark.svg">
  <img alt="A five-step ramp: what you know, then the seven surfaces, then the structural outliers, then a checkable skill map, then the honesty ledger" src="../site/assets/diagrams/seven-surfaces.light.svg">
</picture>

*Every `README.md` in this folder is step 02 of that ramp, filled in for one platform: the seven surfaces with that platform's words in them. The [`platform-ramp`](../.claude/skills/platform-ramp/SKILL.md) skill is the same method, invokable.*

These are the platforms an admin *operates end to end*. They're also five of the
seven compared layer-by-layer in [`the-stack/`](../the-stack/) (with OCI and
self-host as the other two) — the platform folder is the "operate this one" view; the
stack is the "compare them per layer" view.

These are the **seven platforms** compared layer-by-layer in
[`the-stack/`](../the-stack/) — every one now has a dedicated "operate it end to end"
module, and **all seven carry the deeper architecture · operations · automation trio.**

**Public clouds** — a rented data centre you drive by API:

| Platform | Status |
| --- | --- |
| **[aws/](aws/)** | ✅ worked example + architecture + operations + automation notes + 2 runnable labs (read this first) |
| **[azure/](azure/)** | ✅ worked-example depth — + architecture + operations + automation notes; labs planned. Entra/identity is the hands-on strength. |
| **[gcp/](gcp/)** | ✅ worked-example depth — + architecture + operations + automation notes (incl. GKE); labs specced. The global-VPC outlier is the thing to learn. |
| **[oci/](oci/)** | ✅ worked-example depth — + architecture + operations + automation — 🧭 ramp; the youngest hyperscaler (compartments, OCPU-vs-vCPU, bare-metal-first, cheap egress). |

**Private cloud / on-prem** — the platforms you run on your *own* hardware:

| Platform | Status |
| --- | --- |
| **[vsphere/](vsphere/)** | ✅ worked-example depth — + architecture + operations + automation — **🔨 hands-on depth**: regional vCenter admin, VCP6-DCV/NV. A strength, not a ramp. |
| **[openstack/](openstack/)** | ✅ worked-example depth — + architecture + operations + automation — 🧭 ramp, adjacent to real KVM/Proxmox 🔨; "you build the cloud", control-plane-as-product. |
| **[self-host/](self-host/)** | ✅ worked-example depth — + architecture + operations + automation — **🔨 hands-on depth**, the deepest root: PXE/image/cloud-init fleet at 100k+ scale, BMC/IPMI, DNS/BIND, RAID. The layer every cloud abstracts over. |

See [`../00-the-operating-model.md`](../00-the-operating-model.md) for the transferable
skeleton every module is organized around.
