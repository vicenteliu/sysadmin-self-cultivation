# The Sysadmin's Self-Cultivation

*A field guide to mastering the clouds — with AI riding shotgun.*

> 🌐 **Languages:** English (default) · [Chinese](docs/zh/README.md)

---

## The thesis

A systems administrator's real craft was never memorizing every service on every
platform. It's a **transferable mental model** plus the **discipline to get
productive on anything, fast**. In 2026 that second half got a turbo: AI compresses
the learning curve from months to days — *if* you already have the judgment to
steer it and catch it when it's wrong.

This repo is that idea, proved out across the major clouds. For each platform it
answers three questions, in the same order every time:

1. **What is it?** — the platform's job and its core building blocks, on one page.
2. **What does an admin actually need to be able to do?** — a concrete, checkable
   competency map, not a marketing feature list.
3. **How do you get competent with AI as a co-pilot?** — the method: how to ramp
   fast *and* verify, so you're using AI, not trusting it blindly.

Then it makes you prove it with hands-on **labs** (scripts + infrastructure-as-code
you can actually run).

## Why "the same three moves"

Once you've administered one platform properly, the next one is mostly new syntax
over the same skeleton:

> **register a scoped identity → get a token / credential → drive the platform
> through its API and infrastructure-as-code.**

Jamf, Intune, Entra, and Configuration Manager work this way. So do AWS, Azure, and
GCP. This repo leans on that: master the pattern once (see
[`00-the-operating-model.md`](00-the-operating-model.md)), and every new platform
becomes a mapping exercise you can do with AI in a fraction of the time.

## How to read this

- **[Contents — the whole map](CONTENTS.md)** — every module, all four axes, what's written vs. scaffolded. Start here if you want the shape of the whole thing.
- **[Why this exists](WHY.md)** — the motivation, and an honest read on where the craft is heading in the AI era.
- Then **[the operating model](00-the-operating-model.md)** — the transferable skeleton.
- Then pick a platform under **[`platforms/`](platforms/)**. **AWS is the worked example** — read it end to end to see the shape; the others follow the same template.
- Or read the stack **layer by layer** in **[`the-stack/`](the-stack/)** — bottom-up (physical → network → application), with **seven platforms compared at every layer** (AWS, Azure, GCP, OCI, vSphere, OpenStack, self-host).
- **[`cross-cutting/`](cross-cutting/)** covers the layers that transfer across every cloud (identity, networking, IaC, Kubernetes, observability, security, cost).
- **[`ai-workflow/`](ai-workflow/)** is the meta-layer: how AI is used here to learn and to operate — and, just as important, how it's kept honest.
- **[Roadmap](ROADMAP.md)** — what's built and what's next, prioritized by real-world demand.

## Status

| Platform | What it is | Skill map | AI-assisted ramp | Labs |
| --- | --- | --- | --- | --- |
| **AWS** | ✅ | ✅ | ✅ | ✅ 2 labs (boto3 + Terraform) |
| **Azure** | ✅ | ✅ | ✅ | 🚧 planned |
| GCP / GKE | 🚧 opening | 🚧 opening | 🚧 opening | — |
| Cross-cutting | identity ✅ · saas-admin ✅ · iac-and-config ✅ · K8s/cost 🚧 openings · [CONTENTS](CONTENTS.md) | | | |
| Foundations · Endpoint | ✅ [foundations](foundations/) (Linux + scripting) · ✅ [endpoint](endpoint/) (MDM/imaging/EDR) | | | |
| **The Stack** (layer series) | ✅ **01→07** ([physical](the-stack/01-physical.md) · [network](the-stack/02-network.md) · [compute](the-stack/03-compute-and-images.md) · [storage](the-stack/04-storage.md) · [platform services](the-stack/05-platform-services.md) · [observability](the-stack/06-observability.md) · [security](the-stack/07-security.md)) | ✅ in-chapter | ✅ in-chapter | ✅ 1 runnable ([backup drill](the-stack/labs/04-backup-not-snapshot/)) · specs for rest |

This is a living project — built one platform at a time, out in the open.

## Who wrote this

An infrastructure and systems engineer with 15 years across Linux, networking,
virtualization, identity, and automation at scale — writing down the method for
ramping onto any platform fast, in the AI era. Corrections and pull requests
welcome.

## License

[MIT](LICENSE).
