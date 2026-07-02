# OpenStack — The AI-Assisted Ramp

> How to get to *competent-to-reason* on OpenStack fast — and an honest line about
> where AI stops. OpenStack is a clean demonstration of the ramp method **and** of its
> limit: the concepts translate in minutes, but the platform's real difficulty is
> operational, and that part you earn by running it.

The premise of [`WHY.md`](../../WHY.md): an experienced admin plus AI can reason about
a never-run platform in days. OpenStack rewards this — its surfaces map cleanly onto
things a virtualization-and-Linux background already knows (KVM, VLANs/overlays,
Ceph-style storage, IAM). But it also marks the boundary the whole repo is honest
about: **AI can teach you the architecture; it cannot give you the 3 a.m. Neutron
incident.**

## The loop (OpenStack-flavored)

1. **Anchor to what you already know.** *"I run KVM and Proxmox, I know VLANs and
   overlays, Ceph-style storage, and IAM. Map Nova, Neutron, Cinder, and Keystone onto
   that — what's the same, what's renamed, what's genuinely new?"* Because the
   hypervisor (KVM) is already yours, the mapping lands fast.
2. **Get the 80/20.** *"Of all the OpenStack projects, which handful does an operator
   touch daily, and which are optional?"* (Keystone/Nova/Neutron/Cinder/Glance are the
   core; the long tail can wait.)
3. **Generate the artifact.** *"The `openstack` CLI commands to create a project, a
   flavor, a tenant network with a router, and launch a cloud-init instance."* First
   draft in seconds.
4. **Verify against the docs** — service names, CLI flags, and API microversions drift
   across releases; assume the draft is 90% right and hunt the 10%.
5. **Run it in DevStack.** A single-node all-in-one OpenStack in a VM is the throwaway
   account of this platform — reality is the reviewer, and here it's free.
6. **Have AI review it back** — *"what's the security or capacity risk in this
   network/quota design?"*

## Where AI earns its keep

- **The concept translation** — Nova↔EC2, Neutron↔VPC, Cinder↔EBS, Keystone↔IAM,
  Glance↔AMI — AI maps the whole component set onto clouds you (or the reader) already
  know in one prompt.
- **CLI/Heat drafting** — the `openstack` commands and Heat templates, as a first
  draft you verify.
- **Decoding errors** — paste a failed `server create` or a Neutron trace: *"what does
  this point at?"*

## Where AI burns you (verify hardest)

- It **mixes OpenStack releases** — CLI flags, API microversions, and project names
  change; AI blends eras confidently.
- It **invents `openstack` subcommands and Heat resource types** that don't exist.
- It **under-weights the control plane** — AI will help you *use* OpenStack and stay
  quiet about the operational burden of *running* it (the queue, the DB, Ceph health),
  which is the actual hard part.

## The honest limit

This is the platform where the repo's honesty policy is most visible. AI ramps you to
*reason about* OpenStack — the architecture, the component flow, the CLI — genuinely
fast. It does **not** ramp you to production competence, because OpenStack's real skill
is operating a control plane under load, and that's earned, not prompted. The truthful
claim ([`README.md`](README.md)): a sound architectural grasp plus a verifiable ramp,
with the hypervisor underneath (KVM) as real ✋ ground and the OpenStack control plane
as the honest 🧗 — exactly the distinction this repo exists to keep.
