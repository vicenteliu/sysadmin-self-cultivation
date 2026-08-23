# Lab — "The records are published" is not the same claim as "the domain is protected"

**Goal:** make the gap between those two sentences measurable. SPF, DKIM and
DMARC are published, every checker returns green, and the domain is still fully
spoofable — not through an exotic failure, but through the ordinary one that
almost every domain is sitting in right now.

**You'll practise:** what
[build-out step 06](../../../build-out/06-tenant-and-mail.md) insists on —
enumerating everything that sends as you, and moving off `p=none` on a date that
is written down.

A hundred-person office publishes all three records. The aggregate reports arrive.
Nobody is lying and nothing is misconfigured in the way a checker can see. Over one
reporting window, **640 forged messages are delivered with the domain in the
`From:` line**, and two departments are one policy change away from an outage
nobody has warned them about.

## Why this lab is pure-local

Mail authentication is a *protocol* problem, not a vendor one. SPF authenticates
the envelope domain, DKIM authenticates the signing domain, and DMARC asks a third
question neither of them answers: does the authenticated domain match the `From:`
header a human actually reads? That relationship — **alignment** — is fully
expressible as a model: senders with an envelope domain, a signing domain, a
published-or-not SPF path, and a message volume.

No tenant, no DNS, no registrar, no credentials, no `pip install`. Python stdlib,
and CI can run it.

## Run it

```bash
python3 cross-cutting/labs/mail-authentication-alignment/dmarc_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Three green ticks, and `p=none`.** The checker verified that the records
   *exist*. It never read the policy. That is a real check answering a smaller
   question than it appears to, and it is where the work stops.
2. **Two sources of truth disagreeing in both directions.** The sender inventory
   lists **4**; the aggregate report shows **6**. Two real senders were never
   listed — one of them finance's, which is the outcome step 06 names in advance —
   and one listed sender no longer sends at all. Neither list is the truth. The
   report is only the more honest of the two.
3. **"Pass" and "aligned" are different words.** The ticketing system passes SPF
   **and** passes DKIM **and fails DMARC**: both authentications are real, and both
   are for the vendor's domain rather than yours. Two green ticks, no alignment,
   no pass.
4. **The spoofer passes SPF too.** On their own envelope domain, with their own
   published record. "SPF passed" is a statement about *a* domain and not
   necessarily about yours — alignment is the only thing that catches them.
5. **`p=none` delivers all of it identically.** The aligned, the misaligned and
   the forged: same disposition. The policy does not act on the verdict it spent
   a quarter computing.
6. **Enforcement's risk is measurable before you take it.** Moving to
   `p=quarantine` today breaks **3** legitimate senders — and it is *exactly* the
   ones the inventory got wrong. Fix the enumeration first and `p=reject` breaks
   **0** while bouncing all 640 forged messages.

## Verify (don't take the script's word for it)

```bash
python3 .../dmarc_drill.py --break-it   # exit 1
```

`--break-it` evaluates on the authentication results alone and never compares them
to the `From:` domain — **which is how mail health checkers report, and how these
reports are actually read.** The misaligned ticketing system turns green, and so
does the spoofer. The sharpest line in the output is the last table: under
`--break-it`, `p=reject` still delivers the forged mail. The strictest policy
available, read the standard way, stops nothing.

The drill exits `1` naming the four assertions that broke.

To go further, set the ticketing system's `in_spf_record` to `True` — *add the
vendor to your SPF record*, which is the fix almost everyone reaches for first.
Nothing moves: it was already passing SPF on the vendor's own domain, and adding a
path to your record does not make their domain yours. The drill still exits `0`
with that sender still failing. Alignment is not an SPF problem, so it does not
have an SPF fix.

## The point

**`p=none` is a monitoring configuration that is widely mistaken for a security
control.** It produces reports, dashboards go green, and anyone in the world can
still send as your domain — which is why "we have DMARC" needs a follow-up
question about the policy value.

Three things to carry out:

- **There are two authentications and one alignment.** Perfect SPF and perfect
  DKIM, both unaligned, is a failing message and a passing screenshot.
- **The inventory is a claim; the report is evidence.** They will disagree in both
  directions, and reconciling them is a person's job — the reports can be grouped
  and explained by a machine, but which senders are *authorised* is a decision.
- **The reason enforcement gets deferred is real and finite.** It breaks the
  senders you failed to enumerate — a knowable list, this week's work, not an
  open-ended danger.

## Teardown

None. The drill holds everything in memory and writes nothing.
