---
kind: index
axis: platforms
themes: []
platforms: []
summary: "One folder per platform. Every module carries the same file set — README, skills map, AI-ramp, the architecture · operations · automation trio, a support note for the public clouds, and labs/ — so you can move between them without re-learning how to read them."
---
# platforms/

> 🌐 **Languages:** English (default) · [中文](../docs/zh/platforms/README.md)

One folder per platform. Every module carries the **same file set**, so you can move
between them without re-learning how to read them:

1. **`README.md`** — what it is (mapped to the seven surfaces) + the headline skill map + the AI-ramp summary.
2. **`skills-map.md`** — the full, checkable competency list (Core / Working / Depth).
3. **`ai-ramp.md`** — the AI-assisted method to get competent fast, and how to keep AI honest.
4. **`architecture.md` · `operations.md` · `automation.md`** — the deeper trio: how it is structured, what running it looks like, and how to drive it from code.
5. **`support.md`** — the break-fix craft, **for the four public clouds only.** A support note is for a platform you *inherit* rather than build: recurring tickets, the cross-lane experience gap, a lab. The three on-prem platforms are ones you run — two of them 🔨 ground — and their break-fix craft lives in `operations.md`; by that rule none of the three gets a support note.
6. **`labs/`** — a three-run CLI arc of guided runs against a real environment, and one lab that CI can run, owned by the note that teaches its lesson.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../site/assets/diagrams/seven-surfaces.dark.svg">
  <img alt="A five-step ramp: what you know, then the seven surfaces, then the structural outliers, then a checkable skill map, then the honesty ledger" src="../site/assets/diagrams/seven-surfaces.light.svg">
</picture>

*Every `README.md` in this folder is step 02 of that ramp, filled in for one platform: the seven surfaces with that platform's words in them. The [`platform-ramp`](../.claude/skills/platform-ramp/SKILL.md) skill is the same method, invokable.*

The platform folder is the *operate this one* view; [`the-stack/`](../the-stack/) is the
*compare them per layer* view of the same seven.

These are the **seven platforms** compared layer-by-layer in
[`the-stack/`](../the-stack/) — every one now has a dedicated "operate it end to end"
module, and **all seven carry the deeper architecture · operations · automation trio.**

**Public clouds** — a rented data centre you drive by API:

| Platform | Status |
| --- | --- |
| **[aws/](aws/)** | ✅ worked example + the trio + support + a lab (read this first) |
| **[azure/](azure/)** | ✅ worked-example depth — + the trio + support + a lab. Entra/identity is the hands-on strength. |
| **[gcp/](gcp/)** | ✅ worked-example depth — + the trio (incl. GKE) + support + a lab. The global-VPC outlier is the thing to learn. |
| **[oci/](oci/)** | ✅ worked-example depth — + the trio + support + a lab — 🧭 ramp; the youngest hyperscaler (compartments, OCPU-vs-vCPU, bare-metal-first, cheap egress). |

**Private cloud / on-prem** — the platforms you run on your *own* hardware:

| Platform | Status |
| --- | --- |
| **[vsphere/](vsphere/)** | ✅ worked-example depth — + the trio + a lab — **🔨 hands-on depth**: regional vCenter admin, VCP6-DCV/NV. A strength, not a ramp. |
| **[openstack/](openstack/)** | ✅ worked-example depth — + the trio + a lab — 🧭 ramp, adjacent to real KVM/Proxmox 🔨; "you build the cloud", control-plane-as-product. |
| **[self-host/](self-host/)** | ✅ worked-example depth — + the trio + a lab — **🔨 hands-on depth**, the deepest root: PXE/image/cloud-init fleet at 100k+ scale, BMC/IPMI, DNS/BIND, RAID. The layer every cloud abstracts over. |

See [`../00-the-operating-model.md`](../00-the-operating-model.md) for the transferable
skeleton every module is organized around.
