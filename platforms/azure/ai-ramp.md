# Azure — The AI-Assisted Ramp

> Getting to *competent* on Azure fast. Same discipline as everywhere else
> (**AI for speed, judgment for truth** — see [`ai-workflow/`](../../ai-workflow/) and
> the [AWS ai-ramp](../aws/ai-ramp.md)); this note is the Azure-specific delta.

## Azure is the easiest cloud to ramp *if you already have anchors*

By the time you reach Azure you usually have two:

1. **On-prem fundamentals** — and Azure rewards them, because it grew out of Active
   Directory and Windows Server. Entra ID, group policy-style thinking, RBAC — a lot
   of it is familiar.
2. **The AWS mental model** (if you did that module) — and ~80% maps one-to-one.

So the highest-leverage first prompt is a **translation table**, not a tutorial:

> *"I know AWS (IAM, VPC, EC2, S3, CloudFormation) and on-prem Active Directory. Build
> me a mapping table to the Azure equivalents, and in a second column flag where
> Azure genuinely differs, not just renames."*

You'll get productive in an afternoon, and the "genuinely differs" column is your
study list.

## The Azure-specific things that map badly (verify these hardest)

These are exactly where the AWS model misleads you and where AI is confidently wrong:

- **Two permission systems.** **Entra ID roles** (directory: who can manage users,
  apps, groups) are *not* **Azure RBAC** (resources: who can touch this VM/storage).
  AWS has one IAM; Azure has two planes. AI blends them constantly.
- **Resource Groups.** There's no real AWS equivalent — a mandatory lifecycle
  container. Scope, cost, and RBAC all key off it. Design around it deliberately.
- **RBAC scope inheritance.** A role assigned at the subscription flows down to every
  RG and resource. Assigning `Owner` too high is the Azure blast-radius mistake.
- **Managed Identities**, not instance profiles — same idea ("no secrets on the box"),
  different name and two flavors (system- vs. user-assigned).
- **Bicep vs. ARM vs. Terraform** — AI mixes ARM JSON and Bicep syntax, and
  hallucinates resource-provider property names. Verify every property against the
  Bicep/Terraform resource reference.
- **`az` vs. `Az` PowerShell** — two different CLIs with different verbs; AI mixes them.

## Prompt kit (Azure flavor)

- **Translator** — "map \<AWS thing / AD thing\> to Azure; flag real differences."
- **The permission untangler** — "does this task need an Entra role or an Azure RBAC
  role, and at what scope?" (Ask this every time you're unsure — you will be, early.)
- **Least-privilege** — "the built-in RBAC role closest to *exactly* this, or a
  custom role that does only this, at the RG scope."
- **Reviewer** — "review this Bicep/Terraform for security (public exposure,
  encryption), cost, and least-privilege issues."
- **Rubber duck** — paste the `az` error / a denied action from the Activity Log.

## The honest part

Because identity is where the real hands-on experience is (Entra/Azure AD setup +
lifecycle), the ramp here is *asymmetric*: the identity surface is depth, the
resource surfaces are breadth-in-progress. The method is the same — AI compresses the
lookup, verification and the labs make it real — but this module doesn't pretend the
whole thing is equally deep. That honesty is the brand.
