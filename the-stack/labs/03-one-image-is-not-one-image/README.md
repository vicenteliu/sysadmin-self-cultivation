---
kind: lab
axis: the-stack
themes: [virtualization]
platforms: []
summary: "Two machines built from the same image reference six weeks apart are two different machines, the inventory records them as identical, and nothing in it is lying."
---
# Lab 03 — one image is not one image

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/the-stack/labs/03-one-image-is-not-one-image/README.md)

> **Inputs:** none · **Outputs:** what each reference resolved to, and where the two
> machines actually differ · **Risk:** none — no cloud, no hypervisor, no credentials ·
> **Root:** not needed

**Goal:** make tangible the seam [chapter 03](../../03-compute-and-images.md) is built
on — **baked** (in the image) versus **fried** (applied by cloud-init at first boot) —
and the one word that quietly voids the whole reproducibility guarantee: `latest`.

**You'll practise:** treating an image reference as a *query answered at build time*
rather than a name, and deciding which side of the seam a value belongs on before the
day you have to change it.

## Why this lab is pure-local

The guided run in the chapter builds one Packer image for KVM and a cloud and boots
both with the same user-data. Do that — it reaches real boot failures and a real serial
console, which no model does. But the finding underneath it is arithmetic about a
catalogue and a date, and you cannot watch six weeks pass on a trial account.

No cloud, no hypervisor, no credentials, no `pip install`. Python stdlib, and CI can
run it.

## Run it

```bash
python3 the-stack/labs/03-one-image-is-not-one-image/image_pinning_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Two machines, one written procedure, six weeks apart.** Both say `latest`. One
   resolved to `linux-lts-2401`, the other to `linux-lts-2403`. **The inventory row has
   no column for what the reference resolved to**, so it records them as identical and
   is not lying.

2. **Where they differ, and which half of the pipeline it is in.** Three differences,
   *all of them baked*. The fried half is byte-identical because cloud-init ran the
   same user-data on both — which is the useful half of the finding: the
   personalisation you wrote is doing exactly what you asked, and the drift is
   underneath it.

3. **The bug that only reproduces on the newer machine.** *"It crashes on app-02 and
   works on app-01."* Same role, same reference, same user-data, different agent
   version — **a change nobody made, on a day nobody picked, with no change record.**
   And rebuilding app-01 to reproduce it resolves `latest` again and turns app-01 into
   app-02: the evidence destroys itself on contact.

4. **Pin the reference and the fleet becomes reproducible.** Two machines, forty-one
   days apart, byte-identical. Reproducibility is a property of the **reference**, not
   of the pipeline. Pinning does not stop you upgrading; it makes the upgrade a commit.

5. **What the seam costs, in the unit that decides where a value lives.** The same edit
   costs *one reboot* or *a rebuild plus forty redeploys*, decided entirely by which
   side of the seam the value was put on.

## Verify (don't take the script's word for it)

```bash
python3 image_pinning_drill.py --break-it latest-is-stable  # exit 1
python3 image_pinning_drill.py --break-it baked-is-free     # exit 1
```

`latest-is-stable` implements the model in the operator's head — a moving reference
treated as a name — and three assertions break at once, because that single belief is
what all three findings rest on. `baked-is-free` prices a baked change like a fried
one, and the seam stops being load-bearing; if it still passed, the seam was decoration.

To go further, add a fourth catalogue entry published on day 60 and rebuild app-01 to
"reproduce the bug". It becomes a third machine, distinct from both. There is no number
of rebuilds that converges, which is the argument for pinning stated as a limit.

## The point

**`latest` is a query, and it is answered at build time.**

Three things to carry out:

- **Record what the reference resolved to, not what it said.** The inventory was never
  wrong; it has no column for the question. One column, written at build time, and the
  ticket in step 3 is a two-minute lookup instead of a week.
- **Bake what is slow and shared; fry what is per-machine or likely to change.** A value
  on the wrong side is not a bug until the day you need to change it, and then it is a
  project.
- **A drift with no change record is still a change.** The absence of a deploy is not
  evidence that nothing moved — it is evidence that whatever moved was not deployed by
  you.

## Teardown

None. The drill holds everything in memory and writes nothing.
