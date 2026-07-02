# OCI — The AI-Assisted Ramp

> How to get to *competent* on OCI in days — using AI as a co-pilot and keeping it
> honest. OCI is a clean case for the ramp method: an admin who knows another cloud
> has already mapped the seven surfaces, so the job is translating names and catching
> the handful of deliberate differences Oracle built in.

The premise of [`WHY.md`](../../WHY.md): an experienced admin plus AI can be operating
a never-touched platform in days. OCI rewards this more than most, because it was
designed *after* AWS/Azure/GCP and borrows their shape — so much of it is a rename,
and the ramp is mostly finding the four places it isn't. Same two disciplines held
together: **AI for speed, judgment for truth.**

## The loop (OCI-flavored)

1. **Anchor to what you already know.** *"I know AWS accounts/VPCs/IAM (or GCP
   projects). Map OCI compartments, VCN, shapes, and IAM policy onto that — same,
   renamed, or genuinely different?"* The four differences surface in minutes.
2. **Hunt the deliberate differences first** — spend attention here, not on the 90%
   that's identical:
   - **Compartments** — the blast-radius unit (nested; IAM policies scope to them),
     the analog of an AWS account / GCP project.
   - **OCPU vs vCPU** — an OCPU is a *full physical core*; the same "2 CPUs" means
     twice the compute of a hyperthreaded vCPU elsewhere. Miss this and your sizing
     and cost comparisons are off by 2×.
   - **Security lists vs NSGs** — two overlapping packet-filter mechanisms; pick one
     and standardize.
   - **The policy language** — human-readable statements (`Allow group … to … in
     compartment …`), not JSON. Nicer, and different enough to learn.
3. **Get the 80/20**, **generate the artifact** (Terraform / `oci` CLI), **verify
   against current docs**, and **run it in an Always-Free-tier tenancy** — OCI's free
   tier makes reality-as-reviewer genuinely free.

## Prompt patterns that pull their weight

- **The translator:** *"Explain X assuming I know the AWS/GCP equivalent — just the
  OCI-specific delta."*
- **The outlier hunter:** *"Where does OCI genuinely differ from AWS here, and where
  would my AWS instinct give the wrong answer?"*
- **The least-privilege generator:** *"The tightest OCI policy statement that does
  exactly this."* (Then tighten by hand.)

## Where AI will burn you (verify hardest)

- **IAM policy statements** — it invents verbs/resource-types and mis-scopes
  compartments; the human-readable syntax makes wrong policies *look* right.
- **OCPU/vCPU and pricing** — it conflates OCI's full-core OCPU with hyperthreaded
  vCPUs and quotes stale prices; every sizing/cost number gets verified.
- **Security lists vs NSGs** — it blurs the two filtering layers, the way it blurs
  NACL-vs-SG on AWS.
- **Service names and CLI flags** — OCI is younger and less represented in training
  data, so AI hallucinates here *more* than on AWS, not less. Verify harder.

## Why this is a *sysadmin's* skill, not a shortcut

AI can generate a VCN and a compartment policy in seconds. It cannot tell you the
instance can't reach the internet because the route table has no gateway, or that
your "2 OCPU" box is quietly twice the cost-basis you compared it against. It cannot
own the incident. The judgment — least-privilege instinct, "why can't this reach
that," reading the failure, the bare-metal and failure-domain sense from real
[self-host](../self-host/) and [vSphere](../vsphere/) work — is the craft, and it maps
onto OCI as well as any cloud. AI just removes the rote lookup between having that
judgment and applying it to Oracle's names.
