# GCP — The AI-Assisted Ramp

> How to get to *competent* on GCP in days — using AI as a co-pilot and keeping it
> honest. GCP is the cleanest place to prove the method, because so much of it is a
> renaming of surfaces already mapped on AWS and Azure. The ramp is mostly finding
> the few places that *aren't*.

The premise of [`WHY.md`](../../WHY.md): an experienced admin plus AI can be
operating a never-touched platform in days. On GCP that's almost literally true —
the seven surfaces are nearly identical to AWS's, so the job isn't learning a cloud
from scratch, it's **translating one you know and catching the four places Google
did something different.** AI is excellent at the translation and dangerous at the
details, so the method is the same two disciplines held together: **AI for speed,
judgment for truth.**

## The loop (GCP-flavored)

For any new area (say, networking):

1. **Anchor to what you already know.** Not "teach me GCP networking." Instead:
   *"I know AWS VPCs, subnets, security groups, and on-prem TCP/IP. Map GCP
   networking onto that — what's the same, what's renamed, and what's genuinely
   different?"* The answer surfaces the global-VPC outlier in minutes.
2. **Hunt the structural outliers first.** GCP has four places where the AWS reflex
   fails — spend your attention here, not on the 90% that's identical:
   - **Global VPC** — one network spans regions; subnets are regional; multi-region
     is "just routes," no peering ([`the-stack/02`](../../the-stack/02-network.md)).
   - **Project / org hierarchy** — projects are the account/blast-radius unit, not a
     tag; the org tree is the guardrail surface.
   - **Custom machine types** — dial exact vCPU/memory instead of picking a menu size.
   - **Service-account-centric IAM** — roles bind to members on the resource
     hierarchy; service accounts are the default workload identity.
3. **Get the 80/20.** *"Of GCP networking, what 20% does an admin use daily, and what
   can I defer?"* Now you can prioritize.
4. **Generate the artifact.** *"Terraform for a global VPC with two regional subnets
   and a firewall rule targeting a service account,"* or *"the tightest custom IAM
   role that lets this service account read one bucket."* First draft in seconds.
5. **Verify — the non-negotiable step.** Cross-check every role name, API, and
   argument against the **current GCP docs**. GCP's role catalog is huge and AI
   guesses within it confidently; assume the draft is 90% right and hunt the 10%.
6. **Run it in a sandbox with a budget alert.** Reality is the final reviewer — a
   plan that `terraform apply`s and a stack you can `destroy` cleanly beats any
   explanation.
7. **Have AI review it back.** *"Here's my Terraform / IAM binding — what's the
   security or cost risk I missed, and did I use the global-VPC model correctly?"*

## Prompt patterns that pull their weight

- **The translator:** *"Explain X assuming I know the AWS/Azure equivalent — just the
  GCP-specific delta."* (Skips the beginner tax entirely on GCP.)
- **The outlier hunter:** *"Where does GCP's model genuinely differ from AWS here,
  and where would my AWS instinct give me the wrong answer?"*
- **The 80/20:** *"Minimum I must understand about X to be dangerous, and what's safe
  to defer?"*
- **The least-privilege generator:** *"The tightest custom role / IAM binding that
  does exactly this."* (Then tighten by hand.)
- **The reviewer / rubber duck:** paste an error, a `gcloud` output, a denied
  request — *"what does this mean and how do I debug it?"*

## Where AI will burn you (so verify these hardest)

- **IAM roles and permissions** — GCP's catalog is enormous; AI invents role names
  and permission strings that don't exist. Check the role reference.
- **The global VPC** — AI trained on AWS-heavy text and will hand you
  **regional-model (AWS-shaped) networking advice** for GCP; catch it every time.
- **Resource hierarchy** — it blurs **project vs. folder vs. org**, and where a
  policy or quota actually applies.
- **Machine types, quotas, and prices** — all drift; verify current numbers, never
  quote AI's.
- **Anything security-critical** — bucket access (uniform vs. legacy ACLs), key
  policies, firewall exposure. Verify and test, never ship on trust.

## Why this is a *sysadmin's* skill, not a shortcut around one

AI can generate a global VPC in seconds. It cannot tell you that your instance can't
reach the internet because the firewall rule targets the wrong service account, or
that you put two replicas in the same zone under a regional resource. It cannot own
the 3 a.m. incident. The judgment — least-privilege instinct, "why can't this reach
that," reading the failure, weighing cost vs. reliability — is the craft, and it's
the same craft whether the console says AWS or GCP. AI just removes the rote lookup
between *having* that judgment and *applying* it to GCP's names.

That's the whole thesis, on the third cloud: **the mental model is the asset; the
AWS/Azure-to-GCP translation is where AI is most obviously an accelerant; verifying
the four outliers is the discipline that makes it safe.**
