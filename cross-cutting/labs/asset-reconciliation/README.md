---
kind: lab
axis: cross-cutting
themes: [itsm-saas]
platforms: []
summary: "A hundred-person office runs procurement (authoritative for who paid for it and who it belongs to) and an endpoint management tool (authoritative for what state it is in)."
---
# Lab — both systems report 97 devices, 97 devices exist, and three records are wrong

**Goal:** kill the idea that a matching total is reassurance. Two live, automatic,
well-maintained systems can agree on the count and still disagree about which
laptops those are — and the only way to see it is to reconcile row by row.

**You'll practise:** the discipline
[build-out step 11](../../../build-out/11-assets-and-tickets.md) insists on —
deciding which system is authoritative for what, choosing a key that survives the
life of a device, and treating **the diff as the work product rather than the
inventory**.

A hundred-person office runs procurement (authoritative for *who paid for it and
who it belongs to*) and an endpoint management tool (authoritative for *what state
it is in*). Neither owns both. A re-image wave, one warranty swap, one disposal
and one loaner net out to the same number on both sides.

## Why this lab is pure-local

Reconciliation is an *arithmetic* problem about identity, not a vendor one. Every
CMDB has the same shape underneath — two record sets, a key you join them on, and a
residue neither set explains. That is fully expressible as a model: devices with a
purchased serial and a current serial, a deployed hostname and a current hostname,
an owner on paper and a holder in fact.

No CMDB, no agent, no credentials, no `pip install`. Python stdlib, and CI can
run it.

## Run it

```bash
python3 cross-cutting/labs/asset-reconciliation/reconcile_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **97, 97, 97.** Procurement rows, endpoint rows and actual laptops. The count
   reconciles perfectly and tells you nothing: **3** devices are genuinely
   mis-recorded and **7** more carry a field that has drifted since deployment.
   Neither shows up in a total. This is the 2026 failure mode — not a stale sheet,
   a live sheet that is still wrong, which is harder to notice because staleness
   has a smell and this does not.
2. **The key decides how much of your fleet is fiction.** Same two sources, three
   join keys:

   | key | reports | discrepancies | of those, phantom |
   |---|---|---|---|
   | hostname | **104** | 15 | 12 |
   | serial | 99 | 5 | 2 |
   | asset tag | 98 | 3 | **0** |

   Keyed on hostname the reconciliation reports **104 devices against 97 that
   exist** — every re-imaged machine became a new device and its old record never
   retired.
3. **Most of what a bad key reports is phantoms.** Twelve of hostname's fifteen
   discrepancies are not device problems at all; the device is fine and the join
   failed. Asset tag invents none. *A check earns its place by what it eliminates,
   not by what it reports.*
4. **Serial is better and not clean either.** The warranty swap changed the serial
   and left the sticker alone, so serial-keying splits one laptop into two records.
   Every key has a blind spot. The decision is which one you can live with, and it
   is a five-minute decision before there is data.
5. **"Which source wins" has no global answer.** Procurement says the owner is
   someone who left in June; the endpoint tool says the person who actually has the
   laptop. Rule *procurement always wins* and offboarding chases a laptop she does
   not have. Rule *the endpoint tool always wins* and the cost centre changes every
   time someone borrows a machine for a week. The rule is per-field, not
   per-source.
6. **The residue is the job.** Three rows survive a good key, and each one has
   **three** candidate causes the data cannot separate — a disposal with no filed
   evidence looks exactly like a theft nobody reported. That is where a model is
   genuinely useful (propose the why) and exactly where it has to stop.

## Verify (don't take the script's word for it)

```bash
python3 .../reconcile_drill.py --break-it   # exit 1
```

`--break-it` reconciles on **hostname** instead of asset tag — the intuitive key,
the one both systems display, and the one that changes on every re-image. It is
what almost every first reconciliation is built on, because hostname is the only
human-readable field both sides already have.

Three assertions break, and the third is the one worth sitting with: **12 of the
15 rows sent to the advisory layer are phantoms, and it produces confident causes
for every one of them.** A bad key does not just cost somebody a week — it feeds
fiction to the thing you asked to explain the discrepancies.

To go further, add a second warranty swap to `build_fleet()`. The serial row gets
worse — discrepancies 5 → 7, phantoms 2 → 4 — while hostname's discrepancy and
phantom counts do not move at all (its reported total goes 104 → 105 only because
the fleet grew by one). The keys fail on different events, which is why "just use
serial" is a preference and not an answer.

## The point

**Collecting was the 2015 job. Reconciling is this one, and the diff — not the
inventory — is what you are paid for.**

Three things to carry out:

- **A matching total is not agreement.** If you report fleet size as evidence the
  CMDB is healthy, you are reporting the one number that survives every error in
  it.
- **Pick the key before there is data.** It costs one column on one form at device
  #1. Reconstructed at device #100 it costs a person a month and is still wrong.
- **Authority is per-field.** "Which system is the source of truth" is the wrong
  question; the right one is "source of truth *for which field*", and it has an
  answer you can write down in five minutes today.

## Teardown

None. The drill holds everything in memory and writes nothing.
