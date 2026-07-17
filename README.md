# The Sysadmin's Self-Cultivation

*A field guide to mastering the clouds — with AI riding shotgun.*

> 🌐 **Languages:** English (default) · [中文](docs/zh/README.md)

---

## What this is

A sysadmin's real craft was never memorizing every service on every platform — it's a
**transferable mental model** plus the **discipline to get productive on anything,
fast**. AI now compresses that ramp from months to days — *if* you already have the
judgment to steer it and catch it when it's wrong.

This repo writes that judgment down: across **seven platforms**, down **every layer of
the stack**, behind one strict rule — **✋ hands-on depth** is claimed only where it's
real; everything else is a **🧗 verified ramp**, mapped and checked, never bluffed.

## The one idea: three moves

Administer one platform properly and the next is mostly new syntax over the same three
moves:

```mermaid
flowchart LR
  id["① Register a scoped identity<br/>least privilege, narrowest scope"] --> cred["② Get a credential<br/>short-lived token — no key on the box"] --> drive["③ Drive by API and codify it<br/>CLI / SDK / infrastructure-as-code"]
  drive -.->|"new platform = same three moves, new names"| id
```

Jamf, Intune, Entra, AWS, Azure, GCP — all the same skeleton. Master it once (see
[`00-the-operating-model.md`](00-the-operating-model.md)) and every new platform
becomes a mapping exercise you can do with AI in a fraction of the time.

## The shape

Six axes over the same material — enter from whichever matches your question:

```mermaid
mindmap
  root((Self-cultivation))
    Start here
      WHY - the motivation
      the operating model - the skeleton
      ai-workflow - the method
      agent skills - the method made invokable
    Foundations
      Linux and scripting - the floor
    The Stack - by layer, bottom-up
      01 physical
      02 network
      03 compute and images
      04 storage
      05 platform services
      06 observability
      07 security
    Platforms - all seven
      AWS - the worked example
      Azure
      GCP
      OCI
      vSphere - hands-on depth
      OpenStack
      self-host - hands-on depth
    Cross-cutting - transferable skills
      identity and IAM
      IaC and config
      CI-CD and GitOps
      databases
      ITSM and assets
      web and TLS
      service mesh
      incident response
      working with security
      SaaS admin
      kubernetes
      cost
      endpoint
    Toolbox - run it
      scripts - find
      Ansible roles - fix
      user-side skills - drive
      generator - your own subset
```

The distinctive one is **The Stack**: it reads the stack *bottom-up*, comparing all
seven platforms at **every layer** — written from the machine room up, not the console
down.

## How to read this

| I want to… | Start at |
| --- | --- |
| **See the whole shape** | [`CONTENTS.md`](CONTENTS.md) — every module, all four axes, one page |
| **Understand the philosophy** | [`WHY.md`](WHY.md) → [`00-the-operating-model.md`](00-the-operating-model.md) |
| **Go deep on one platform** | [`platforms/`](platforms/) — **AWS is the worked example**, read it end to end |
| **Read the stack by layer** | [`the-stack/`](the-stack/) — physical → security, seven platforms compared |
| **Learn a transferable skill** | [`cross-cutting/`](cross-cutting/) — identity · IaC · CI/CD · databases · ITSM · web/TLS · incident response · and more |
| **Support a platform I inherited** | the break-fix **support notes** (see [What's built](#whats-built)) — recurring tickets, the cross-lane experience gap, a runnable lab each |
| **See how AI is kept honest** | [`ai-workflow/`](ai-workflow/) — the method and its guardrails |
| **Take runnable tools with me** | [`toolbox/`](toolbox/) — nine find/audit scripts (incl. a VMware→Proxmox assessment trio), three Ansible remediation roles, and a [generator](toolbox/generate/) that packs a per-shop subset |
| **Use the method as a tool** | [`.claude/skills/`](.claude/skills/) — eight Agent Skills: five for the method (ramp · audit · author · lab · mirror), three that drive the toolbox |

## What's built

Everything the [roadmap](ROADMAP.md) planned is written, with **twelve runnable,
self-verifying labs** (exit `0` = the lesson held), **eight break-fix support notes**,
**eight Agent Skills**, and a **runnable toolbox** (nine scripts, three Ansible
remediation roles, a per-shop pack [generator](toolbox/generate/)); what remains is
more runnable labs, a full Chinese mirror ([`docs/zh/`](docs/zh/README.md) is
started), and demand-first deepening.

- **Foundations & method** — [WHY](WHY.md) · [operating model](00-the-operating-model.md) · [ai-workflow](ai-workflow/) · [foundations](foundations/) (Linux + scripting) ✅
- **The Stack** — [seven layers, 01→07](the-stack/), all seven platforms compared at each, + runnable [failure-domains](the-stack/labs/01-failure-domains/) and [backup-drill](the-stack/labs/04-backup-not-snapshot/) labs ✅
- **Cross-cutting & endpoint** — [identity](cross-cutting/identity-iam.md) · [iac](cross-cutting/iac-and-config.md) · [ci-cd](cross-cutting/ci-cd.md) · [databases](cross-cutting/databases.md) · [itsm & assets](cross-cutting/itsm-and-assets.md) · [web & TLS](cross-cutting/web-and-tls.md) · [service mesh](cross-cutting/service-mesh.md) · [incident response](cross-cutting/incident-response.md) · [working with security](cross-cutting/working-with-security.md) · [saas-admin](cross-cutting/saas-admin.md) · [kubernetes](cross-cutting/kubernetes.md) · [cost](cross-cutting/cost.md) · [endpoint](endpoint/) ✅
- **Support notes (break-fix craft)** — for the surfaces you *inherit and support*, not just stand up: [M365](cross-cutting/m365-support.md) · [AWS](platforms/aws/support.md) · [Azure](platforms/azure/support.md) · [GCP](platforms/gcp/support.md) · [OCI](platforms/oci/support.md) · [Terraform](cross-cutting/terraform-support.md) · [Kubernetes](cross-cutting/kubernetes-support.md) · [Multi-cloud](cross-cutting/multi-cloud-support.md) — each with the recurring tickets, the cross-lane experience gap a strong sysadmin gets wrong, a runnable lab, and a Chinese mirror ✅
- **Toolbox (run it)** — [charter + conventions](toolbox/README.md) · nine scripts (triage · users · patching · baseline · backup-drill · cidr · a [vSphere→Proxmox assessment trio](toolbox/vm-migration-assess/)) · [Ansible remediation roles](toolbox/ansible/) pairing audit→fix · a [per-shop pack generator](toolbox/generate/) — safe-by-default, every tool carries its own `Tested on:` line ✅

**Platforms** — all seven compared in The Stack have a dedicated "operate it end to end"
module (what-it-is · skill map · AI-ramp · a **3-lab CLI arc**), and **all seven now
carry the deeper architecture · operations · automation trio**:

| Platform | Module | Arch · Ops · Auto | Labs | Honesty |
| --- | --- | --- | --- | --- |
| **[AWS](platforms/aws/)** (worked example) | ✅ · [support](platforms/aws/support.md) | ✅ ✅ ✅ | ✅ 3-lab arc — **2 runnable** (boto3 + Terraform) + iam-deny lab | 🧗 ramp |
| **[Azure](platforms/azure/)** | ✅ · [support](platforms/azure/support.md) | ✅ ✅ ✅ | ✅ 3-lab CLI arc (`az`) + two-planes lab | 🧗 + Entra/identity ✋ |
| **[GCP / GKE](platforms/gcp/)** | ✅ · [support](platforms/gcp/support.md) | ✅ ✅ ✅ | ✅ 3-lab CLI arc (`gcloud`) + gke-auth lab | 🧗 ramp |
| **[OCI](platforms/oci/)** | ✅ · [support](platforms/oci/support.md) | ✅ ✅ ✅ | ✅ 3-lab CLI arc (`oci`) + compartment/verb lab | 🧗 ramp |
| **[vSphere / vCenter](platforms/vsphere/)** | ✅ | ✅ ✅ ✅ | ✅ 3-lab CLI arc (PowerCLI) | **✋ hands-on depth** (VCP6-DCV/NV) |
| **[OpenStack](platforms/openstack/)** | ✅ | ✅ ✅ ✅ | ✅ 3-lab CLI arc (`openstack` / DevStack) | 🧗 ramp (KVM-adjacent ✋) |
| **[self-host / bare metal](platforms/self-host/)** | ✅ | ✅ ✅ ✅ | ✅ 3-lab CLI arc (virsh / ipmitool / ansible) | **✋ hands-on depth** (100k+ fleet) |

Two of the seven are labeled **✋ hands-on depth** (vSphere and self-host — production
ground, not a ramp); the rest are honest 🧗 ramps. The labs are **CLI-first** on
purpose: the command line is faster, exact, repeatable, and reviewable — and it's the
same surface your automation uses.

**Agent Skills** — the repo ships eight [`.claude/skills/`](.claude/skills/). Five
turn its methodology into invokable AI workflows: **platform-ramp** (ramp onto any
platform, honestly), **honesty-audit** (classify claims ✋/🧗/overclaim),
**author-module** (write a new note — including a **support note** — in the repo's
voice, research-grounded), **runnable-lab** (turn a concept into a self-verifying
drill), and **mirror-zh** (mirror a doc into `docs/zh/` Chinese). Three are
**user-side** — **linux-triage**, **harden-baseline**, and **toolbox-picker** wrap
the [toolbox](toolbox/) so an AI agent can drive it for you: install one on a new
box and run a triage, or the whole audit→remediate loop, in one sentence.

## Who wrote this

An infrastructure and systems engineer with 15 years across Linux, networking,
virtualization, identity, and automation at scale — writing down the method for ramping
onto any platform fast, in the AI era. A living project, built out in the open, one
layer at a time. Corrections and pull requests welcome.

## License

[MIT](LICENSE).
