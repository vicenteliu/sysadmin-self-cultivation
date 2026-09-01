---
kind: companion
axis: platforms
themes: [virtualization]
platforms: [vsphere, self-host]
marker: "mixed"
summary: "The difference between vCenter and Proxmox is almost never asked in the abstract — it is asked while standing in a migration. Answered that way: where each control plane lives and what you lose when it fails, what actually fights the move, and why the VMs are the easy part."
---
# vCenter and Proxmox — what actually differs

> [`architecture.md`](architecture.md) maps vSphere onto the seven surfaces. This note
> answers a narrower question that gets asked constantly and almost never in the
> abstract: **what is the real difference, and what breaks if I move?** It is written
> the way the question arrives — from inside a migration — because that is the only
> context in which the answer is worth anything.
>
> The repo already ships the runnable half: [`vsphere-inventory`](../../toolbox/vsphere-inventory/)
> and [`pve-inventory`](../../toolbox/pve-inventory/) produce **the same schema** from
> both sides, [`vm-migration-assess`](../../toolbox/vm-migration-assess/) turns one into
> a per-VM verdict, and [`snapshot-audit`](../../toolbox/snapshot-audit/) reads either.

## Where the control plane lives, and what you lose when it dies

This is the difference that generates most of the others, and feature tables never
mention it.

**vCenter is a thing.** It is a separate appliance that *is* the management plane, and
it is almost always running as a virtual machine on the estate it manages. Lose it and
the hosts keep running, the VMs keep serving, and you lose orchestration: no vMotion, no
DRS decisions, no central authentication, no API for everything you have wired to it.
You recover it before you can do anything else.

**Proxmox's control plane is the cluster.** Every node runs the management stack and
they agree through a quorum protocol borrowed from the Linux HA world. There is no
appliance to lose. What you can lose instead is **quorum** — and a cluster below quorum
will refuse to make changes, which is the behaviour you want and the behaviour that
surprises everybody the first time a two-node cluster loses a node.

**So the two failure modes are opposite shapes.** One is a single component whose loss
removes your ability to act. The other is a distributed agreement whose loss removes
your ability to act. The first is recoverable by restoring one thing and is a
**circular dependency** — the management plane is a guest of the estate it manages,
which is the same shape as
[a recovery key stored behind the identity it exists to bypass](../../endpoint/encryption-and-keys.md).
The second needs no restore and needs you to have thought about node counts before you
built it.

**The practical consequence, stated once:** whichever you run, write down how you manage
the estate on the day the management plane is unavailable, and test it. That sentence is
the transferable part of this whole note.

## The four surfaces where they genuinely diverge

Not a comparison table — the decisions each one forces on you.

**Storage.** vSphere gives you a purpose-built cluster filesystem and an integrated
hyper-converged option, and the decisions are about datastore layout and policy.
Proxmox hands you the Linux storage ecosystem — ZFS on a node, Ceph across the cluster,
LVM, plain directories — and the decision is *which one*, which is a genuinely larger
question than it looks. **The Proxmox side asks you to know storage; the vSphere side
asks you to know its storage.** Neither is easier; the skills transfer differently.

**Networking.** Distributed switching and, with the network-virtualisation product, an
overlay with policy. On the Proxmox side it is Linux bridges or OVS, configured the way
you would configure any Linux host, plus whatever you build on top. Again the same
shape: one is a product you learn, the other is a substrate you already know if you know
Linux — which is why this migration is easier for a team with Linux depth than its
reputation suggests.

**Clustering and mobility.** Live migration exists on both. Automated placement and
load-balancing is a first-class product feature on one side and something you assemble
on the other. **If nobody is actually using automated placement — and in a great many
estates nobody is — this difference costs nothing.** Find out before pricing it.

**Licensing and support posture.** 🧭 **This is the ramp and it is labelled.** The
post-Broadcom landscape is the single most common reason this question is being asked at
all, and it moves faster than a written document can track. What this note will say is
the durable half: a subscription-versus-perpetual change is a *procurement* event that
becomes an *architecture* event only because it forces a re-evaluation nobody had
scheduled. Read the current terms yourself; do not read them here.

## What actually fights the migration

The VMs are the easy part. Here is the rule set the shipped assessor applies, and it is
worth reading as a description of reality rather than as a tool's configuration:

| Severity | What it finds | Why it is that severity |
|---|---|---|
| **Hard** | A raw device mapping | There is no direct equivalent. That storage needs a redesign, not a conversion |
| **Hard** | An end-of-life Windows guest | The paravirtual drivers do not exist for it. You are choosing between legacy-device workarounds and rebuilding the guest |
| Moderate | Snapshots present | Chains do not convert. Consolidate first, which is a maintenance window nobody budgeted |
| Moderate | A modern Windows guest | Drivers must go in before or at cutover. Entirely doable, entirely a per-VM task |
| Minor | A non-virtio NIC on Linux | The model changes and the driver is already in the kernel |
| Minor | EFI firmware | Recreate with the matching firmware and check Secure Boot expectations |
| Minor | More than a couple of terabytes | A transfer window, not a technical problem |

**Notice what is not on that list.** The hypervisor. Nothing about the migration is hard
*because it is a different hypervisor* — the hard findings are storage abstractions with
no counterpart and guests too old to have drivers. That is the finding worth carrying:
**a hypervisor migration is a storage-and-guest-support project wearing a hypervisor
costume.**

## And the part the assessor cannot score

Every VM can be EASY and the migration can still fail, because the thing wired to
vCenter is not the VMs.

**It is everything holding its API.** Backup software with a vSphere integration.
Monitoring with a vCenter collector. The automation that provisions VMs. The CMDB that
believes it is authoritative. Scripts nobody has read since the person who wrote them
left. **Each of those is a separate migration, none of them appears in a VM inventory,
and together they are usually most of the work.**

The honest first step is therefore not an inventory of VMs. It is an inventory of
**things that authenticate to vCenter** — which is the same question as
[the non-human identities nobody counts](../../the-reference-office.md#why-these-numbers),
asked about one system, and it has the same answer: the list is longer than anyone
expects and nothing maintains it.

## What this means for the reference office

Nothing, and that is the useful answer. [The reference office runs no VM estate
beyond a staging ring](../../the-reference-office.md#on-premises--what-cannot-leave) —
with imaging at the vendor, files in a tenant and identity in a cloud, there is nothing
for a hypervisor cluster to hold. **A hundred-person office asking this question is
usually asking a question it inherited**, and the first move is to find out what is
actually running on the estate before comparing platforms to host it.

Where the question is real is one size band up, or in an estate with a reason to keep
compute local that this office does not have — which is exactly the
[three tests](../../the-reference-office.md#on-premises--what-cannot-leave) that
office applies, run against a bigger set of requirements.

## Honest boundaries

🔨 **Deep on the vSphere side.** Operated as a regional vCenter administrator,
maintaining and upgrading VM infrastructure and services; VCP6-DCV and VCP6-NV
certified. The control-plane failure behaviour above is operational, not read.

🔨 **Adjacent and real on the Proxmox and KVM side** — including physical-GPU
passthrough — in lab and internal environments rather than as a production estate of
this author's own. The distinction matters and is why this note's marker is `mixed`
rather than 🔨: **the vSphere half is production ground; the Proxmox half is real
hands, smaller stakes.**

🧭 **The post-Broadcom licensing and support landscape**, and the newest vSphere and
NSX features. Verified and labelled, never bluffed, and deliberately not quoted here
because it dates faster than this file can be maintained.

**Not claimed:** running a Proxmox estate at production scale, Ceph operations at scale,
or any statement about which platform an organisation should choose.

## Read deeper

- [`architecture.md`](architecture.md) — vSphere across the seven surfaces
- [`toolbox/vm-migration-assess/`](../../toolbox/vm-migration-assess/) — the rule table
  above, runnable, read-only, against a real inventory
- [`toolbox/snapshot-audit/`](../../toolbox/snapshot-audit/) — one audit, both
  hypervisors, and the thing the moderate row above is about
- [`platforms/self-host/operations.md`](../self-host/operations.md) — what running the
  hardware underneath either of them actually looks like
- [`the-stack/01`](../../the-stack/01-physical.md) — failure domains, which is the
  layer this note's control-plane argument sits on
