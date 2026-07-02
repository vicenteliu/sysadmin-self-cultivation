# Self-Hosted / Bare Metal — Admin Skill Map

A checkable competency list. Tiers:

- **Core** — you cannot run bare metal without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it and *explain* the failure modes. Mirrors
[`aws/skills-map.md`](../aws/skills-map.md) surface-for-surface. Honest note: on this
platform, most of these boxes are *checked from production* — see the module's
[honest boundaries](README.md).

## Identity & access — you run the directory
- [ ] **Core** — Linux users/groups/sudo, SSH key management, PAM basics.
- [ ] **Core** — Run a directory (AD or **OpenLDAP**); centralize auth instead of
  per-box accounts.
- [ ] **Working** — SSO backed by the directory; least-privilege sudo policy.
- [ ] **Depth** — Certificate/PKI basics; bastion + jump-host access patterns.

## Compute — the physical box
- [ ] **Core** — Rack, cable, and boot a server; reach it via **BMC/IPMI/iLO/iDRAC**
  when there's no OS.
- [ ] **Core** — Run VMs with **KVM** or **Proxmox** on your hardware.
- [ ] **Working** — Firmware/BIOS management; hardware health monitoring.
- [ ] **Depth** — GPU passthrough; NUMA/CPU pinning; the hardware-diversity problem
  (one image, many models).

## Networking — both planes are yours
- [ ] **Core** — VLANs, switch config, a firewall; **DNS (BIND)** and **DHCP** you
  operate.
- [ ] **Core** — Trace *why a host can't reach the internet* — the
  [debug ladder](../../the-stack/02-network.md), on hardware you own.
- [ ] **Working** — NTP, routing between subnets, VPN/site-to-site.
- [ ] **Depth** — EVPN/VXLAN overlay; asymmetric-routing and MTU debugging.

## Storage — made of metal
- [ ] **Core** — RAID levels and the rebuild window; local disk + a NAS/NFS share.
- [ ] **Core** — Monitor free space; a full disk is an outage
  ([`the-stack/04`](../../the-stack/04-storage.md)).
- [ ] **Working** — SAN/iSCSI presentation, multipath; snapshots.
- [ ] **Depth** — Ceph/MinIO for object storage; **RAID is not backup** — a tested
  3-2-1 restore.

## Provisioning — the pipeline
- [ ] **Core** — **PXE boot** + a golden image + **cloud-init** first boot,
  hands-off.
- [ ] **Core** — FDE enrolled at scale with key escrow.
- [ ] **Working** — **Ansible** for configuration; image versioning per hardware gen.
- [ ] **Depth** — Terraform/MAAS-style bare-metal provisioning; re-image over
  patch-in-place.

## Observability & security
- [ ] **Core** — Prometheus/Grafana or equivalent; monitor from *outside* the thing.
- [ ] **Core** — Patch discipline; CIS/hardening baselines baked into the image.
- [ ] **Working** — Centralized logs (ELK/Loki); IPMI/hardware alerting.
- [ ] **Depth** — Physical access controls; air-gapped / controlled-environment
  operation.

## The "can you actually operate it" test

If you can PXE-and-image a fleet hands-off, reach a dead box out-of-band, run the
core services (DNS/DHCP/LDAP/NTP), design failure domains, and keep storage
surviving disk deaths — you can run bare metal at scale. This is the one skill map in
the repo where the honest answer to "have you done this?" is *yes, at fleet scale* —
and it's the foundation the cloud maps are read *against*.
