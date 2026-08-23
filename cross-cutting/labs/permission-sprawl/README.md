# Lab — "Who can see this?" is not answered by reading the permissions

**Goal:** make the auditor's real question tangible. Not *is it locked down* —
**who can see this, and how do you know?** The second half is the one that fails,
and it fails quietly, in an estate that looks fine from the sharing dialog.

**You'll practise:** the discipline
[build-out step 07](../../../build-out/07-files-and-collaboration.md) insists on —
permissions expressed in groups, links on a leash, and a review that examines the
thing it claims to examine.

Two estates, built the same week, same documents, same hundred people. One granted
access only through groups. The other said *just this once* four times and left
link sharing open. The visible difference is four extra names. The actual
difference is ninety-three people.

## Why this lab is pure-local

Permission sprawl is a *structural* failure, not a vendor one. It happens the same
way in every suite because every suite has the same two grant paths — an
access-control list and a sharing link — and only the first one is what people mean
by "permissions". That is fully expressible as a model: principals, nested groups,
grants with or without a recorded reason, and links with a scope and an expiry.

No tenant, no suite, no credentials, no `pip install`. Python stdlib, and CI can
run it.

## Run it

```bash
python3 cross-cutting/labs/permission-sprawl/sprawl_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **One visible difference.** Four individual grants. It reads as minor
   untidiness, which is exactly why nobody escalates it.
2. **The ACL undercounts — in both.** The clean estate has one reader its ACL does
   not name (a scoped auditor link, deliberate). The sprawled one has **93**,
   because "anyone with the link, no expiry" means the whole company.
3. **The access review returns clean.** Walking group membership examines three
   people. It steps straight past the four individual grants — they are not group
   members — and it cannot see link readers at all. It is not a wrong answer. It is
   a correct answer to a different question.
4. **"Why does this person have access?"** In the group-only estate every grant
   answers with a role, so the reason outlives whoever granted it. In the sprawled
   estate four grants have no recorded reason and none can be reconstructed.
5. **Revocation is the test.** Remove one person from the group. The clean estate
   revokes everywhere. The sprawled estate revokes nothing — the open link still
   admits them, and nobody reading the group would know.

## Verify (don't take the script's word for it)

```bash
python3 .../sprawl_drill.py --break-it   # exit 1
```

`--break-it` makes the audit ignore sharing links — **the way access reviews are
actually performed.** Every hidden reader disappears from the result, the two
estates start to look comparable, and the drill exits `1` naming the assertions
that broke.

That is the sharpest form of the lesson: the sabotage is not an exotic failure, it
is the industry-standard procedure.

To go further, set the open link's `expired` to `True` and watch 93 readers vanish
— one field, on one link, worth more than any amount of group hygiene.

## The point

**A permission model is only a model if revocation works.** If removing someone
from a group does not remove their access, what you have is not a model — it is a
history of decisions, and reading it backwards is archaeology.

Three things to carry out:

- **There are two grant paths.** Perfect discipline on the one you can see buys
  nothing if the other is open.
- **A review that walks groups is clean about the wrong set.** Ask what a review
  *examined*, not what it *concluded*.
- **Individual grants lose their reason.** The click is one second; the
  unanswerable question it creates lasts as long as the document does.

## Teardown

None. The drill holds everything in memory and writes nothing.
