# vSphere — The AI-Assisted Ramp (inverted)

> Every other platform's AI-ramp note is about getting *to* competent fast. This one
> is different, and honest about it: **vSphere is a strength, not a gap.** So AI's job
> here isn't to teach the platform — it's to accelerate the narrow slices where even
> a strong admin benefits, and to run the operating model *in reverse* — from vSphere
> depth *out* to the clouds.

The repo's thesis ([`WHY.md`](../../WHY.md)) is that AI collapses the
unknown-unknowns for a platform you've never touched. On a platform you've operated in
production for years, there are few unknown-unknowns left — so using AI the same way
you'd use it on a first encounter would be a mistake, and a good way to get confidently
wrong answers on ground you actually know better than the model. The discipline
inverts: **you are the verifier by default; AI is the drafter for the three places it
genuinely helps.**

## Where AI earns its keep on vSphere

- **PowerCLI automation.** *"A PowerCLI script to report every VM with a snapshot
  older than 7 days across the cluster"* — AI drafts it in seconds, and because you
  know vSphere, you catch the wrong cmdlet or the missing `-Server` immediately. This
  is the best use: AI writes, your expertise reviews.
- **What's changed** — versions and licensing. vSphere moves, and the **post-Broadcom
  licensing changes** reshaped the economics. *"What changed in vSphere 8 vs. the 6.x
  I'm certified on, and what's the current licensing model?"* is a legitimate
  unknown-unknown even for an expert — and exactly the kind of moving detail AI
  mis-remembers, so verify it against current docs.
- **Cross-mapping to the clouds — the operating model in reverse.** *"I run DRS, HA,
  vMotion, datastores, and DVS. Map each onto its AWS and Azure equivalent, and tell
  me where the analogy breaks."* This turns a deep vSphere foundation into a fast ramp
  onto the public clouds — the single highest-value use of AI for someone with this
  background, and the reason the other platform modules in this repo ramp so quickly.

## Where AI burns you (verify hardest)

- It **mis-remembers version-specific behavior and licensing** — the fastest-moving,
  most-consequential vSphere details; never quote AI's numbers on cost or edition.
- It **invents PowerCLI cmdlets and parameters** — plausible, non-existent; the
  module is large and it guesses.
- It **over-generalizes cloud analogies** — "vMotion is just live migration like GCP"
  glosses real differences (shared-storage requirement, CPU compatibility). Use the
  analogy to orient, not to design.

## Why this note exists at all

Because honesty is the point of this repo. It would be easy to write vSphere the same
way as AWS — "here's how AI gets you competent fast" — and it would be false: this
platform didn't need AI to get competent on, and pretending otherwise would undercut
the ✋/🧗 discipline everywhere else. The truthful version is more useful anyway: **on
your strong platform, AI is a force multiplier for automation and translation, not a
teacher — and the judgment that makes it safe is exactly the judgment years on the
platform gave you.**
