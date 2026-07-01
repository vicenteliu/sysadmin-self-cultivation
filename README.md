# The Sysadmin's Self-Cultivation

### 《系统管理员的自我修养》

*A field guide to mastering the clouds — with AI riding shotgun.*

> 🌐 **Languages:** English (default) · [中文 (Chinese)](docs/zh/README.md)

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

- Start with **[the operating model](00-the-operating-model.md)** — the transferable skeleton.
- Then pick a platform under **[`platforms/`](platforms/)**. **AWS is the worked example** — read it end to end to see the shape; the others follow the same template.
- **[`cross-cutting/`](cross-cutting/)** covers the layers that transfer across every cloud (identity, networking, IaC, Kubernetes, observability, security, cost).
- **[`ai-workflow/`](ai-workflow/)** is the meta-layer: how AI is used here to learn and to operate — and, just as important, how it's kept honest.

## Status

| Platform | What it is | Skill map | AI-assisted ramp | Labs |
| --- | --- | --- | --- | --- |
| **AWS** | ✅ | ✅ | ✅ | ✅ 2 labs (boto3 + Terraform) |
| **Azure** | ✅ | ✅ | ✅ | 🚧 planned |
| GCP / GKE | 🚧 | 🚧 | 🚧 | — |
| Cross-cutting | 🚧 | | | |

This is a living project — built one platform at a time, out in the open.

## Who wrote this

An infrastructure and systems engineer with 15 years across Linux, networking,
virtualization, identity, and automation at scale — writing down the method for
ramping onto any platform fast, in the AI era. Corrections and pull requests
welcome.

## License

[MIT](LICENSE).
