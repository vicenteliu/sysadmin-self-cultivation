# OpenStack — Admin Skill Map

A checkable competency list. Tiers:

- **Core** — you cannot administer OpenStack without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it and *explain* the failure modes. Mirrors
[`aws/skills-map.md`](../aws/skills-map.md) surface-for-surface. Honest note: on this
platform the boxes are the **ramp target**, not a claim of production depth — see the
module's [honest boundaries](README.md).

## Identity & access — Keystone
- [ ] **Core** — Explain projects (tenants), users, roles, and tokens; the auth flow
  every other service depends on.
- [ ] **Working** — Role assignments scoped to a project; service accounts for
  automation.
- [ ] **Depth** — Federation / external identity; reading a denied request in the
  Keystone logs.

## Compute — Nova
- [ ] **Core** — Launch/manage an instance; understand **flavors** (the size menu)
  and images from Glance.
- [ ] **Core** — Know Nova runs on **KVM** underneath — the hypervisor you may already
  operate.
- [ ] **Working** — Quotas per project; host aggregates and availability zones for
  placement.
- [ ] **Depth** — Live migration; the scheduler; **Ironic** for bare-metal instances.

## Networking — Neutron
- [ ] **Core** — Tenant networks (VXLAN overlay), a router, and a floating IP to reach
  an instance.
- [ ] **Core** — Security groups (stateful) — and trace *why an instance can't reach
  the internet*.
- [ ] **Working** — Provider networks; multiple tenant networks and inter-network
  routing.
- [ ] **Depth** — Debug Neutron (the component operators most often name as what
  breaks); the [debug ladder](../../the-stack/02-network.md) on an overlay.

## Storage — Cinder / Swift / Glance (often Ceph)
- [ ] **Core** — Attach a **Cinder** block volume; store and boot from a **Glance**
  image.
- [ ] **Working** — **Swift** object storage; snapshots; understand Ceph sits under
  all three in many deployments.
- [ ] **Depth** — Operate **Ceph** (health, rebalancing, placement groups) — its own
  platform; the backup discipline of [`the-stack/04`](../../the-stack/04-storage.md).

## Provisioning & the control plane
- [ ] **Core** — Drive it from the **`openstack` CLI**; cloud-init for first boot.
- [ ] **Working** — **Heat** stacks (or Terraform) for declarative provisioning.
- [ ] **Depth** — **The control-plane failure mode**: a wedged queue/DB stops the API
  while running VMs survive — know it before it teaches you.

## Observability & security
- [ ] **Core** — Telemetry (Ceilometer/Gnocchi) or the Prometheus stack everyone adds;
  an alarm that notifies.
- [ ] **Working** — Barbican for secrets; security-group hygiene.
- [ ] **Depth** — Monitor the control plane itself (its outage is your outage);
  capacity planning across projects.

## The "can you actually operate it" test

The honest bar here is different from the public clouds: if you can stand up
**DevStack**, create a project/flavor/network, launch a cloud-init instance, and
*explain the control-plane failure modes*, you can reason about operating OpenStack —
the ramp target. Production competence (debugging Neutron and Ceph under load, at 3
a.m.) is the part that only comes from running it, and this map says so.
