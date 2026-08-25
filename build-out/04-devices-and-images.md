# 04 · Devices and images — purchase, build, enroll

> 🔨 hands-on — PXE and image pipelines at fleet scale, BMC/IPMI, hardware lifecycle
> **Before:** 02 the building · 03 identity. **After:** 05 network · 08 endpoint security · 11 assets · 13 the help desk

Its dependency on 03 is the one that costs money if you get it wrong: **a device is
enrolled into a directory**, and which directory decides the join model, which
decides the image, which decides whether the machine on the desk needs to be wiped
to change its mind. Order the hardware whenever you like; do not *enrol* it before
identity is settled.

## What this step produces

- A build that is **reproducible from nothing** — an artefact plus a procedure, not a
  golden machine somebody cloned once and cannot rebuild.
- Enrolment that happens at first boot, in the user's hands, without a technician
  touching the device.
- A hardware standard: how many models, and what the exception process is.
- A **spare pool** with a number attached, and the reasoning for the number.
- A record written at receipt, not at deployment — see step 11.

## Questions to ask first

- **How many models will you support?** Every additional model is a driver set, an
  image variant, and a spare inventory. Two is comfortable, four is a tax, and the
  request for a fifth always sounds reasonable in isolation.
- **Who opens the box?** If devices ship to the office, are unboxed, imaged and
  hand-delivered, you have signed up for a logistics operation. Drop-shipping to the
  user with zero-touch enrolment removes it — but only if 03 is done.
- **What is the state of a device the day it is handed over** — patched, encrypted,
  compliant, in inventory? Each of those is a checkbox that has to be *proved*
  later, at the audit, and the cheapest time to make it true is now.
- **What is the spare policy?** Zero spares means a failed laptop is a lost week.
  The number is a business decision; making sure a number exists is IT's.
- **What happens at end of life** — resale, recycling, destruction? The answer has to
  produce evidence. Decide now while it is a paragraph.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Build method | PXE, a task-sequence server, a technician per machine | **zero-touch**: vendor registers the device, first boot pulls policy |
| Where the image lives | on-site, on your infrastructure | a config profile and an app list; the "image" is mostly the OS vendor's |
| Domain join | on the LAN, always | over the internet, at first boot, anywhere |
| Technician time per device | 30–60 minutes | approaching zero, if 03 is right — and a re-imaging project if it is not |
| Where the difficulty moved | building the image | **deciding the policy**, and proving compliance afterwards |

**How much of that is AI: essentially none, and this one is worth being blunt
about.** Zero-touch provisioning is vendor programmes plus device management —
it was built and shipped before the current wave of models and does not use one.

Where AI does earn its place is the boring end: reading a failed enrolment log and
proposing what went wrong. That is triage assistance, and it is genuinely useful
because enrolment failures are opaque and their error strings are unhelpful.

## Read deeper

- [`the-stack/03-compute-and-images.md`](../the-stack/03-compute-and-images.md) —
  compute and the image pipeline, the layer this step lives at
- [`endpoint/`](../endpoint/) — the MDM model, imaging pipeline, patch and EDR, BYOD
- [`platforms/self-host/operations.md`](../platforms/self-host/operations.md) — the 🔨
  fleet material this step's habits come from

## Do it

- [`toolbox/baseline-check/`](../toolbox/baseline-check/) — assert a built machine is
  actually in the state you claim. Run it against the first device off the line, not
  the hundredth.
- [`foundations/labs/idempotence-drill/`](../foundations/labs/idempotence-drill/) —
  the property a build procedure has to have; running it twice must be safe.

## Getting it backwards

**Enrolling before identity exists.** The machines work. They are joined to
something provisional, or to nothing. Then the directory decision lands and the
join model differs — and every device has to be reset. It is not a settings change,
it is a re-imaging project across every desk, during the weeks people are trying to
start work.

**One-off builds that nobody can reproduce.** The first ten machines get built by
hand because it is faster than automating. It is faster, right up until the
eleventh is different from the first and nobody can say how.

**Deferring the inventory record to deployment.** By then the box is open, the
serial is on a desk somewhere, and the person who received it has left for lunch.
See step 11; the record starts at receipt.
