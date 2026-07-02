# OCI — Admin Skill Map

A checkable competency list. Tiers:

- **Core** — you cannot administer OCI without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it from code and *explain* the failure modes. Mirrors
[`aws/skills-map.md`](../aws/skills-map.md) surface-for-surface; the **OCI-specific
deltas are called out inline**. Honest note: these are the **ramp target** — see the
module's [honest boundaries](README.md).

## Identity & access — IAM + compartments
- [ ] **Core** — Design a **compartment** hierarchy (the blast-radius/isolation unit)
  and write **policy statements** (`Allow group X to manage Y in compartment Z`).
- [ ] **Core** — Use **instance principals** so a VM authenticates with no key.
- [ ] **Working** — Dynamic groups; scoped least-privilege policies.
- [ ] **Depth** — Federation with an external IdP; reading a denied request in the
  audit logs.

## Networking — VCN
- [ ] **Core** — Design a **VCN** (regional), subnets, an Internet/NAT gateway; trace
  *why an instance can't reach the internet*.
- [ ] **Core** — **Pick security lists OR NSGs and standardize** — don't tangle both
  (the OCI-specific filtering gotcha).
- [ ] **Working** — Route tables, service gateway (keep traffic off the internet).
- [ ] **Depth** — FastConnect / hybrid; multi-VCN peering.

## Compute — shapes
- [ ] **Core** — Launch an instance; use **flexible shapes** (dial OCPU + memory) and
  remember an **OCPU is a full core**, not a hyperthread.
- [ ] **Core** — Attach a service account / instance principal; cloud-init bootstrap.
- [ ] **Working** — Instance pools + autoscaling; custom images.
- [ ] **Depth** — **Bare-metal shapes** (OCI's first-class metal) for per-core
  licensing or performance; preemptible for cost.

## Storage & data
- [ ] **Core** — Block Volume attach; Object Storage with the right access controls.
- [ ] **Working** — File Storage (NFS); the **Archive tier** as a cheap-retrieval
  backup target (OCI's egress advantage).
- [ ] **Depth** — Cross-region replication and its (low) egress cost; Autonomous
  Database basics.

## Provisioning & config
- [ ] **Core** — Stand up a stack from **Terraform** (or **Resource Manager**, OCI's
  managed Terraform); destroy it cleanly.
- [ ] **Working** — The `oci` CLI / SDK; remote state.
- [ ] **Depth** — CI/CD for infra; Security Zones as policy-as-code guardrails.

## Observability & security
- [ ] **Core** — A Monitoring alarm that notifies; query Logging; a **budget alert**
  first.
- [ ] **Working** — **Cloud Guard** (posture + threat); Vault for secrets.
- [ ] **Depth** — **Security Zones** (preventive guardrails); APM tracing; cost
  anomaly detection.

## The "can you actually operate it" test

If you can do the **Core** boxes from code — a compartment + policy, a VCN, an
instance with an instance principal, storage, and a budget alert — you can administer
OCI at a working level. Because the surfaces map so cleanly onto AWS, an admin solid
on another cloud reaches that bar fast; the attention goes to the four deliberate
differences (compartments, OCPU vs vCPU, security-lists-vs-NSGs, the policy language).
