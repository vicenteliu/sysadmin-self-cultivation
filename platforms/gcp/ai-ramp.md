# GCP — The AI-assisted ramp

> 🚧 **Opening written; body in progress.** The method is fixed (it's the repo's
> standard ramp, GCP-flavored); the worked examples are being filled in.

The premise of [`WHY.md`](../../WHY.md): an experienced admin plus AI can be
operating a never-touched platform in days. GCP is the cleanest place to prove it,
because so much of it is a renaming of surfaces already mapped on AWS and Azure —
and the ramp is mostly about finding the few places that *aren't*.

## The method (GCP-flavored)

- **Translate, don't tutorial:** *"I know AWS VPCs and Azure VNets. Map GCP
  networking onto them — and be explicit about what the global VPC changes about
  multi-region design."* The diff is the lesson.
- **Hunt the structural outliers first:** global VPC, project/org hierarchy, custom
  machine types, service-account-centric IAM. These are where "GCP is just AWS"
  gets you burned — surface them deliberately.
- **Generate least-privilege, then tighten:** *"the tightest IAM binding that does
  exactly this."* AI drafts permissive; you cut.

## Where AI burns you (verify hardest)

- It **invents IAM roles and API names** that don't exist (GCP's role catalog is
  huge and AI guesses within it) — check against the current role reference.
- It **quotes machine-type specs, quotas, and prices from its training years** —
  all drift; verify current.
- It **forgets the global VPC** and gives you regional-model (AWS-shaped) advice.
- It **blurs project vs. folder vs. org** in the resource hierarchy.

Anything that grants access or costs money gets checked against current docs and,
ideally, tested with a denied-request probe — the same discipline as every other
module here.

> The worked examples (real prompts + the corrections they needed) fill in as the
> GCP module matures; the method above is the repo standard, already proven on the
> [AWS](../aws/ai-ramp.md) and [Azure](../azure/ai-ramp.md) modules.
