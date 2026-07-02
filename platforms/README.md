# platforms/

One folder per platform. Every module follows the **same four-part template** so you
can move between them without re-learning how to read them:

1. **`README.md`** — what it is (mapped to the seven surfaces) + the headline skill map + the AI-ramp summary.
2. **`skills-map.md`** — the full, checkable competency list (Core / Working / Depth).
3. **`ai-ramp.md`** — the AI-assisted method to get competent fast, and how to keep AI honest.
4. **`labs/`** — runnable, tear-down-able exercises.

These are the platforms an admin *operates end to end*. They're also five of the
seven compared layer-by-layer in [`the-stack/`](../the-stack/) (with OCI and
self-host as the other two) — the platform folder is the "operate this one" view; the
stack is the "compare them per layer" view.

**Public clouds** — a rented data centre you drive by API:

| Platform | Status |
| --- | --- |
| **[aws/](aws/)** | ✅ worked example + architecture + operations + automation notes + 2 runnable labs (read this first) |
| **[azure/](azure/)** | ✅ worked-example depth — + architecture + operations + automation notes; labs planned. Entra/identity is the hands-on strength. |
| **[gcp/](gcp/)** | ✅ worked-example depth — + architecture + operations + automation notes (incl. GKE); labs specced. The global-VPC outlier is the thing to learn. |

**Private cloud / on-prem** — the platforms you run on your *own* hardware:

| Platform | Status |
| --- | --- |
| **[vsphere/](vsphere/)** | ✅ module written (what-it-is / skill map / ai-ramp) — **✋ hands-on depth**: AMS-region vCenter admin, VCP6-DCV/NV. The one platform here that's a strength, not a ramp. |
| **[openstack/](openstack/)** | ✅ module written (what-it-is / skill map / ai-ramp) — 🧗 ramp, adjacent to real KVM/Proxmox ✋; "you build the cloud", control-plane-as-product. |

See [`../00-the-operating-model.md`](../00-the-operating-model.md) for the transferable
skeleton every module is organized around.
