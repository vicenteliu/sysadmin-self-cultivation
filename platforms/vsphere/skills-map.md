# vSphere — Admin Skill Map

A checkable competency list. Tiers:

- **Core** — you cannot administer vSphere without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it and *explain* the failure modes — not when you've
read about it. Mirrors [`aws/skills-map.md`](../aws/skills-map.md) surface-for-surface
so the two read side by side.

## Identity & access — vCenter permissions
- [ ] **Core** — Explain roles, permissions, and objects; grant access via **AD
  groups**, not per-user.
- [ ] **Core** — Integrate vCenter SSO with Active Directory / LDAP.
- [ ] **Working** — Design a least-privilege role for a specific task (e.g. a backup
  service account) instead of handing out Administrator.
- [ ] **Depth** — Lockdown mode, ESXi host hardening, and reading a permission-denied
  in the vCenter events.

## Compute — hosts, clusters, VMs
- [ ] **Core** — Add ESXi hosts to vCenter; build a cluster; create/manage VMs.
- [ ] **Core** — Enable **DRS** (load balancing) and **HA** (restart on host
  failure); explain what each does and doesn't cover.
- [ ] **Working** — Resource pools, reservations/limits/shares; anti-affinity rules
  for replica placement.
- [ ] **Depth** — vMotion prerequisites and *why a migration fails*; Fault Tolerance;
  right-sizing from performance data.

## Networking — vSwitch and beyond
- [ ] **Core** — Standard vSwitch, port groups, VLAN tagging; connect a VM to the
  right network.
- [ ] **Working** — **Distributed vSwitch** (DVS) across hosts; uplinks, teaming,
  failover.
- [ ] **Depth** — NSX segments + distributed firewall; troubleshoot east-west
  connectivity (the [debug ladder](../../the-stack/02-network.md) on an overlay).

## Storage — datastores
- [ ] **Core** — VMFS and NFS datastores; provision a VMDK; monitor free space (a
  **full datastore** is a mass outage — [`the-stack/04`](../../the-stack/04-storage.md)).
- [ ] **Working** — **vSAN** (hyperconverged local disks as a datastore); storage
  vMotion.
- [ ] **Depth** — Multipathing, SAN/iSCSI presentation, VM/vSAN encryption + key
  custody.

## Provisioning & config — build from images
- [ ] **Core** — Golden VM → **template** → clone with a customization spec.
- [ ] **Working** — Content libraries across sites; cloud-init for Linux first boot.
- [ ] **Working** — **PowerCLI** automation for repeatable operations.
- [ ] **Depth** — Terraform against vSphere; lifecycle-managed host images.

## Lifecycle & observability
- [ ] **Core** — Host **maintenance mode** + evacuate; vCenter/ESXi upgrade path.
- [ ] **Core** — vCenter alarms that actually notify; read performance charts for
  contention (CPU ready, memory ballooning, datastore latency).
- [ ] **Depth** — vROps / Aria Operations for capacity and health; rolling the fleet
  with no downtime.

## The "can you actually operate it" test

If you can do the **Core** boxes — a DRS/HA cluster, vMotion, datastores you monitor,
template-based provisioning, and a clean upgrade — you can run a production vSphere
estate at a working level. **Working** and **Depth** are what keep a large cluster
healthy under load and what an interviewer probes for. This map is the one in the
repo backed by having *done* most of it in production.
