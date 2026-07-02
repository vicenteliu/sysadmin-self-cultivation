# GCP — Admin Skill Map

> 🚧 **Opening written; body in progress.** The tier structure and surface
> headings are fixed (mirroring [`aws/skills-map.md`](../aws/skills-map.md)); the
> checkable items are being filled in.

A checkable competency list. Tiers:

- **Core** — you cannot administer GCP without this.
- **Working** — expected of a solid mid/senior admin.
- **Depth** — separates a strong admin; often the interview differentiator.

Check a box when you can *do* it from code and *explain* the failure modes — not
when you've read about it.

## Identity & access (IAM)
- [ ] **Core** — Roles + bindings; service accounts as workload identity; the
  primitive-vs-predefined-vs-custom role distinction. *(to be expanded)*

## Networking (the global VPC)
- [ ] **Core** — Design a VPC and remember it's **global**; regional subnets;
  VPC-level firewall rules targeting tags/service accounts. *(to be expanded)*

## Compute
- [ ] **Core** — Compute Engine instances; machine types **and custom machine
  types**; instance templates → Managed Instance Groups. *(to be expanded)*

## Storage & data
- [ ] **Core** — Cloud Storage with the right access controls; Persistent Disk
  zonal vs. **regional**. *(to be expanded)*

## Provisioning & config
- [ ] **Core** — Stand up a stack from **Terraform** in version control; destroy it
  cleanly; understand project/org structure. *(to be expanded)*

## Observability
- [ ] **Core** — Cloud Monitoring alert; Cloud Logging query; the built-in SLO
  tooling. *(to be expanded)*

## Security & compliance
- [ ] **Core** — A **budget alert** first; default-on encryption; Org Policy
  guardrails; Security Command Center basics. *(to be expanded)*

> The item bodies fill in as the GCP module matures; the surfaces and tiers are
> fixed so the map's shape matches AWS and Azure for side-by-side reading.
