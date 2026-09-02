---
kind: companion
axis: endpoint
themes: [endpoint]
platforms: []
marker: "🔨"
summary: "The README names the imaging pipeline in four bullets; this note is the design underneath — what one platform across Windows, macOS and Linux genuinely shares, which of the two provisioning eras you are actually in, and why hardware diversity is the thing that breaks it."
---
# Provisioning across three operating systems

> 🌐 **Languages:** English (default) · [中文](../docs/zh/endpoint/provisioning.md)

> The [README](README.md) says *what the endpoint discipline is*. This note is the
> design question it names and does not answer: **what does a provisioning platform
> decide, when it has to cover Windows, macOS and Linux at the same time?**
> Written from designing and running one that was adopted org-wide and cumulatively
> provisioned six figures of devices — which is also why the honest parts of this note
> are about what did *not* transfer.

## The question underneath the question

*How do I provision three operating systems* almost always turns out to be two
questions wearing one coat.

**One is a delivery question**: how does a machine get from a box to a person's desk in
a state they can work in. **The other is a state question**: how does that machine stay
in a state you can describe, after the person has had it for eighteen months.

They are answered by different systems, on different cadences, and confusing them is the
most common structural mistake at this layer. This note is about the first one.
[`management.md`](management.md) is about the second.

## The two eras, and knowing which one you are in

There are exactly two provisioning models in service today, and the question is not
which is better — it is **which one your estate is actually in**, because most estates
are in both and have not noticed.

| | You build the machine | The vendor builds the machine |
|---|---|---|
| **How it starts** | Network boot, an image you made, applied by you | A serial number registered to your organisation before it ships |
| **What you maintain** | A golden image per hardware generation, plus drivers | An enrolment profile and a policy set |
| **Where the OS comes from** | Your image | The OS vendor's, mostly |
| **What breaks it** | A laptop model whose network driver is not in the image | A device that was never registered, or registered to the wrong tenant |
| **Where you touch the machine** | A bench, a technician, thirty to sixty minutes | Nowhere — a courier and the user's own hands |

**The criteria that decide which one you are in**, and none of them is a preference:

- **Can the vendor register the hardware to you at purchase?** If you buy through a
  channel that supports it, the second column is available. If you buy refurbished, or
  in a region without that channel, or the machines are already in a cupboard, it is
  not — and no amount of policy design changes that.
- **Does the OS have a first-boot enrolment path at all?** Two of the three do, cleanly.
  The third is the interesting one and it gets its own section below.
- **Do you control the network the machine first touches?** Network boot needs a
  network you own, in a room, with the machine plugged into it. Vendor enrolment needs
  any internet connection and no room at all — which is the entire reason the model won
  once offices stopped being where people are.
- **How many hardware models are in the estate?** This is the one that actually decides
  it, and it is the subject of the section after next.

**The reference office is in the second column and says so.**
[`build-out/04`](../build-out/04-devices-and-images.md) puts the image with the OS vendor
and the technician at zero minutes. That is the right answer for a hundred people buying
current hardware through a normal channel. It is not the answer everywhere, and a note
that only described it would be describing the easy case.

## What the three operating systems actually share

Less than an org chart assumes, and the honest accounting matters because it decides how
many people you need.

**They share the shape**: a device acquires an identity, receives a description of its
intended state, and converges toward it. That is real and it is why one team can run all
three. It is also the whole of what they share.

**They do not share the mechanism**, and each one is opinionated in a different
direction:

- **macOS** has the strictest and cleanest enrolment story of the three, because the OS
  vendor also runs the device-registration channel and the management protocol. The cost
  of that cleanliness is that **you cannot do anything the protocol does not offer**. The
  work is knowing the boundary, not working around it.
- **Windows** carries both eras at once, which is why Windows estates are the ones with
  two provisioning systems running in parallel and nobody able to decommission either.
  Its imaging heritage is deep, well-tooled, and the reason the first column above still
  exists in most large estates.
- **Linux** has no consumer-grade first-boot enrolment story to speak of, so it stays in
  the first column by default — and, because it is scriptable all the way down, tends to
  be provisioned by the same configuration-management tooling that runs the servers.
  That is a sensible answer and it has a consequence people miss: **the Linux endpoints
  end up managed by a different team than the other two.**

**That last point is the real finding.** Ask an organisation how many endpoint
management platforms it runs and it will say two. Count them and it is three, because
the Linux laptops are being handled by whoever runs Ansible. The estate is not wrong —
it is unaccounted for, which is a different problem and a worse one.

## Hardware diversity is the thing that breaks it

The README calls this *the leak point the cloud never shows you*, and at scale it is not
a leak, it is the design constraint.

**One image, twelve laptop models, and one of them will not take the wifi driver.** That
sentence is the entire difference between provisioning servers and provisioning
endpoints. A server fleet is bought in lots and is homogeneous by procurement policy. An
endpoint fleet accumulates: three generations of one model line, a batch bought during a
supply shortage, the design team's machines, the machines somebody inherited in an
acquisition.

**The decisions this forces, in order of how much they cost to get wrong:**

1. **How many hardware models are supported, and what the exception process is.** This
   is a *policy* question that looks like a procurement one.
   [`build-out/04`](../build-out/04-devices-and-images.md) asks for exactly this and it
   is the highest-leverage sentence in the step. Every model is a driver set, a test
   matrix column, and a recurring cost — and the cost is paid by the imaging platform
   whether or not anybody wrote it down.
2. **Whether the image is generic or per-generation.** A generic image plus driver
   injection scales further and fails more obscurely. A per-generation image is simple
   and multiplies.
3. **Who owns the test matrix, and when it runs.** The failure mode is not that a model
   breaks. It is that a model breaks *in the image you already deployed to everyone*.
4. **What happens to the model that will not comply.** There is always one. The honest
   answer is a documented exception with an owner and a review date, not a workaround
   nobody wrote down — which is the same discipline
   [`build-out/08`](../build-out/08-endpoint-security-and-patching.md) asks for on
   patching, for the same reason.

**Vendor enrolment does not remove this problem, it relocates it.** You stop maintaining
drivers and start maintaining the assumption that every machine was registered
correctly. That assumption fails silently, at the loading dock, and you find out on
somebody's first morning.

## What scale changes, and what it does not

Running this at six figures of devices and running it at a hundred are different jobs,
and the difference is not the one people expect.

**What changes:**

- **Everything becomes a queue.** At a hundred devices, provisioning is an event. At a
  hundred thousand it is a rate, with a backlog, a throughput and a bottleneck that
  moves. The bottleneck is almost never the imaging.
- **The exception rate stops being noise.** Two percent of a hundred is two machines a
  technician handles. Two percent of a hundred thousand is a team.
- **Regional reality arrives.** Different channels, different hardware availability,
  different network conditions, different holidays. A platform that assumed one site
  discovers it encoded that assumption in a dozen places.
- **Rollback becomes the feature you actually need.** At small scale you fix forward. At
  large scale a bad image reaches thousands of machines before anyone reports it.

**What does not change** — and this is the transferable half:

- **The blast radius question.** Before any policy or image goes out: *how many devices
  does this reach, and what is the worst thing it does to them?* That question is
  identical at a hundred and at a hundred thousand. Only the consequence of skipping it
  scales.
- **Staging is not optional and is always the thing that gets cut.** A ring of your own
  machines, then a friendly team, then a region, then everyone. Every estate that
  skipped it has one story about why it now does not.
- **The person on the other end.** The output of this pipeline is a machine a
  non-technical human uses on their first day. That is the acceptance test and it does
  not get easier with volume.

## The reference office, specifically

A hundred people, [about twenty-three joiners a year and thirty-eight refresh
replacements](../the-reference-office.md#parameters) — so **about sixty-two machines
change hands a year, and fewer than four in ten of those are because somebody joined.**

That ratio is the design input most provisioning platforms are never given. A pipeline
built around onboarding handles the minority case well and the majority case by hand.
The refresh path — a person who already has a working machine, already has an account,
and needs their new one to be indistinguishable — is where the actual volume is, and it
has a requirement onboarding does not: **the old machine has to come back, get wiped,
and leave the register honestly**, which is
[`asset-reconciliation`](../cross-cutting/labs/asset-reconciliation/)'s entire subject.

## Honest boundaries

🔨 **Hands-on, and this is the deep end of it.** Designing and running a multi-OS
PXE and image-based provisioning platform adopted org-wide, cumulatively provisioning
six figures of devices; application packaging and targeted distribution; the warehouse
reality of imaging at volume, re-imaging returns and enrolling full-disk encryption at
scale. The hardware-diversity material above is not read, it is scar tissue.

🧭 **Where the ramp is, and it is specific.** **Autopilot and ConfigMgr** in particular
— the second column done the Microsoft way is a console this author has mapped rather
than run, and the [README](README.md) has always said so. The *shape* of vendor
enrolment is 🔨 through Apple's channel; the Windows dialect of it is the ramp.

**Not claimed at all:** procurement channel negotiation, and anything about the supply
side of hardware beyond the fact that it constrains the image.

## Read deeper

- [`endpoint/management.md`](management.md) — the state question, which is what happens
  after this pipeline finishes
- [`endpoint/encryption-and-keys.md`](encryption-and-keys.md) — the part of provisioning
  that is really an access-control decision
- [`build-out/04`](../build-out/04-devices-and-images.md) — the step this serves, and
  the hardware-standard question it asks
- [`the-stack/03`](../the-stack/03-compute-and-images.md) — *boot, image, personalise*
  at the layer above, where the targets are servers and homogeneous
- [`the reference office`](../the-reference-office.md#parameters) — the sixty-two
  handovers a year, and why most of them are not joiners
