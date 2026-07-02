# GCP — Admin Skill Map

A checkable competency list. Tiers:

- **Core** — you cannot administer GCP without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it from code and *explain* the failure modes — not
when you've read about it. This mirrors [`aws/skills-map.md`](../aws/skills-map.md)
surface-for-surface, so the two read side by side; the **GCP-specific deltas are
called out inline**.

## Identity & access (Cloud IAM) — the front door

- [ ] **Core** — Explain the resource hierarchy (org → folder → project → resource)
  and how IAM **roles bind to members** at each level (inheritance flows down).
- [ ] **Core** — Grant a **predefined role** at the narrowest scope that works; know
  primitive (owner/editor/viewer) roles are too broad for real use.
- [ ] **Core** — Create a **service account** and use it as workload identity — no
  key file on the box (the "no secret on the box" rule).
- [ ] **Working** — Write a **custom role** with exactly the permissions a task
  needs; read a denied request in the audit logs.
- [ ] **Depth** — Workload Identity Federation (no service-account keys at all);
  Org Policy constraints as preventive guardrails.

## Networking (the **global** VPC) — the structural outlier

- [ ] **Core** — Design a VPC and internalize that it's **global**; create
  **regional subnets** under it.
- [ ] **Core** — **Firewall rules** targeting network tags or service accounts (not
  just IP ranges) — the GCP-specific model.
- [ ] **Core** — Cloud NAT for private egress; trace *why an instance can't reach the
  internet*.
- [ ] **Working** — Cloud Load Balancing (global anycast) and its backend model;
  Cloud DNS public vs. private zones.
- [ ] **Depth** — Multi-region on one global VPC ("just routes" vs. AWS peering);
  Private Google Access / Private Service Connect; hybrid via Cloud Interconnect.

## Compute — where code runs

- [ ] **Core** — Create/stop/delete a Compute Engine instance from `gcloud`; pick a
  machine type sanely — **or dial a custom machine type** (GCP's exact-size option).
- [ ] **Core** — Attach a **service account** to an instance; startup-script bootstrap.
- [ ] **Working** — Instance templates → **Managed Instance Groups** with
  autoscaling + a load balancer + health checks.
- [ ] **Working** — Build/maintain a custom **image** (the cloud image pipeline,
  [`the-stack/03`](../../the-stack/03-compute-and-images.md)).
- [ ] **Depth** — GKE for containers; **Cloud Run** for serverless containers;
  preemptible/Spot for cost; understanding live migration.

## Storage & data — where state lives

- [ ] **Core** — Cloud Storage bucket with the right access controls (uniform
  bucket-level access, not public); storage classes.
- [ ] **Core** — Persistent Disk: **zonal vs. regional** (regional PD synchronously
  replicates across two zones — a cleaner HA primitive than AZ-locked block).
- [ ] **Working** — Cloud SQL in a private network; backups, HA config, failover.
- [ ] **Working** — Cloud Storage lifecycle rules + class transitions (cost).
- [ ] **Depth** — Filestore for shared file; Spanner basics; cross-region replication
  and its egress cost.

## Provisioning & config — build from code, not clicks

- [ ] **Core** — Stand up a stack from **Terraform** in version control; destroy it
  cleanly (no orphaned billing resources).
- [ ] **Core** — Structure work with **projects** (the account/blast-radius unit);
  understand the org hierarchy.
- [ ] **Working** — Remote state + locking; reusable modules.
- [ ] **Working** — `gcloud` scripting; instance startup scripts / OS Config.
- [ ] **Depth** — CI/CD for infrastructure; Org Policy as policy-as-code guardrails;
  drift detection.

## Observability — is it healthy, and who did what

- [ ] **Core** — A Cloud Monitoring alerting policy that actually pages someone.
- [ ] **Core** — Query logs in Cloud Logging; answer "who created/deleted this?" from
  the audit logs.
- [ ] **Working** — Dashboards; log-based metrics; **the built-in SLO tooling**
  (a GCP advantage — SLOs are native).
- [ ] **Depth** — Distributed tracing (Cloud Trace); centralized multi-project logging.

## Security & compliance — safe, provable, affordable

- [ ] **Core** — A **budget alert** first, before real resources; default-on
  encryption; uniform bucket-level access.
- [ ] **Core** — Secret Manager (no secrets in code); Cloud KMS for keys.
- [ ] **Working** — Security Command Center basics; Org Policy constraints;
  separate projects for prod/dev blast radius.
- [ ] **Depth** — Landing-zone / org-hierarchy guardrail design; incident response for
  a leaked service-account key; cost anomaly detection.

## The "can you actually operate it" test

If you can do the **Core** boxes across all seven surfaces from code, and debug the
common failures, you can honestly say you can administer GCP at a working level.
Because the surfaces map so cleanly onto AWS, an admin solid on one cloud should
reach that bar on GCP fast — the ramp is real, and the four structural outliers
(global VPC, projects, custom machine types, service-account IAM) are where the
attention goes.
