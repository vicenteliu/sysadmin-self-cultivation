---
kind: interview
axis: cross-cutting
themes: [identity]
platforms: [aws]
marker: "mixed"
summary: "Pairs with skills-maps/identity.md, section for section."
---
# Identity & Access — Interview Map

> 🌐 **Languages:** English (default) · [中文](../../docs/zh/cross-cutting/interview/identity.md)

> Pairs with [`skills-maps/identity.md`](../skills-maps/identity.md), section for
> section. Format, marker rules and the anonymisation discipline are in
> [`README.md`](README.md).

Identity is the densest cluster in the demand signal and the one where a wrong answer
is least visible — an over-broad grant looks exactly like a correct one until someone
uses it. Interviewers know this, so the questions here reward precision over fluency
more than anywhere else.

`⏳` marks an answer whose specific incident is not written down yet.

## Directory & the source of truth 🔨

### "What is the source of truth for identity in your environment, and how do you know?"
**Probes:** whether one system decides that a person exists, or whether several
believe they do.
**Answer:** One system decides existence and everything downstream follows it. The
test is not what the diagram says — it is what happens on an offboard: if disabling in
one place stops every path, that place is the source of truth; if anything survives,
you have two. The second directory is rarely declared, it accretes.

### "Walk me through a hybrid sync problem."
**Probes:** whether you know which attributes flow, which direction, and what a
conflict looks like from the inside.
**Answer:** ⏳ *Needs the specific.* The shape: an attribute edited on both sides, sync
picking a winner by rule rather than by intent, and the loser reappearing on the next
cycle so the fix looks like it worked and then un-worked. Diagnosis is direction first
— which side is authoritative for *this* attribute, which is often not the side
authoritative for the object.

## Authentication vs authorization 🔨

### "A user says they can't access something. Where do you start?"
**Probes:** the two questions, kept separate. Conflating them is the root of most
identity confusion and the fastest thing to check for in a candidate.
**Answer:** Establish first whether they signed in at all. A failed authentication and
a successful authentication followed by an authorization denial look identical to the
user and completely different in the log. Answer *who are you* before touching *what
may you do*, every time — the shortcut is what sends people editing permissions for a
password problem.

### "Rank MFA factors, and say why."
**Probes:** whether "we have MFA" is a checkbox to you or a spectrum.
**Answer:** Phishing-resistant first — FIDO2/WebAuthn, because the credential is bound
to the origin and cannot be replayed on a lookalike page. Then app-based push with
number matching. SMS last: it is a factor, and it is one that survives neither SIM swap
nor a convincing relay. Saying SMS is worthless is as wrong as treating it as
equivalent; it raises the floor and does not stop a targeted attempt.

## Federation & SSO (SAML / OIDC) 🔨

### "SSO is broken for one application. Walk me through it."
**Probes:** whether you have a short list of classic causes or you start reading XML.
**Answer:** Four candidates first: clock skew, wrong entity ID or audience, an expired
signing certificate, and an attribute or claim mismatch. Each is cheap to check and
each eliminates a class. Reading the assertion comes after, when the cheap four have
not landed — and the assertion is where you confirm, not where you start.

### "SAML or OIDC for a new application?"
**Probes:** whether you decide by preference or by what the application supports.
**Answer:** By what it supports, first — the choice is usually made for you. Where
both exist, OIDC for anything modern and mobile-adjacent, SAML where the enterprise
integration is the well-trodden path. A candidate who has a favourite here without
asking what the app speaks is answering a different question than the one asked.

## Running an IdP yourself 🧭

### "Would you self-host an identity provider?"
**Probes:** whether you can price the operational burden rather than the licence.
**Answer:** This is a ramp for me — I have operated *against* identity providers and
have not owned the availability of one. The reasoning I would bring: the moment it is
yours it becomes the highest-blast-radius system you run, because its downtime is not
its own — every other system's login stops. That reframes the comparison from licence
cost to on-call cost, signing-key lifecycle, and whether you can restore it, which is
an identity-continuity exercise rather than a database one. My honest position is that
the bar for self-hosting is higher than most build-vs-buy analyses assume, and I would
want someone who has carried that pager to check my sizing.

## SCIM & the joiner/mover/leaver lifecycle 🔨

### "Which of joiner, mover and leaver goes wrong most often, and why?"
**Probes:** whether you know the answer is *mover*, and can say why leaver gets the
attention instead.
**Answer:** Leaver gets the attention because it has an auditor attached. Mover is the
one that quietly breaks: the new access is granted because someone is waiting for it,
and the old access is not removed because nobody is. Repeat across a few role changes
and you have a person whose permissions are a career history. The fix is making mover a
revoke-and-grant rather than a grant.
**Prove it:** [`toolbox/user-lifecycle`](../../toolbox/user-lifecycle/)

### "What does SCIM do that SSO doesn't?"
**Probes:** whether the two are distinct in your head.
**Answer:** SSO answers *how do people sign in*. SCIM answers *how do accounts come
into existence and stop existing*. An estate with SSO and no SCIM has single sign-on to
accounts that were created by hand and will be deleted by memory.

## RBAC & least privilege 🔨

### "Write me a least-privilege policy for this task."
**Probes:** whether you start narrow and widen, or start broad and intend to tighten.
**Answer:** Start from the specific action on the specific resource and widen only when
something breaks, with the failure telling you what to add. The direction matters
because the other one never finishes — a permissive draft that "we'll tighten later"
is in production three years later. Where AI drafts it, it drafts permissive; the
cutting is the human half.
**Prove it:** [`aws/iam-deny-by-default`](../../platforms/aws/labs/iam-deny-by-default/)

### "A request was denied and the user says they have the role. What now?"
**Probes:** whether you can read an evaluation rather than guess at it.
**Answer:** Name which rule denied it, at which scope, in which order — explicit deny
beats allow, and an organisation-level boundary overrides a local grant that looks
correct in isolation. The other frequent cause is two planes: a directory role and a
resource role, or cloud IAM and cluster RBAC, where a grant in one says nothing about
the other.
**Prove it:** [`azure/global-admin-is-not-owner`](../../platforms/azure/labs/global-admin-is-not-owner/) ·
[`gcp/gke-iam-vs-rbac`](../../platforms/gcp/labs/gke-iam-vs-rbac/)

## Conditional access & device trust 🔨

### "How do you roll out a conditional access policy safely?"
**Probes:** whether you have ever locked yourself out, or understood why others do.
**Answer:** Report-only first, and actually read the report — the value is in seeing
who *would* have been blocked, which is always a larger and stranger set than
expected. Exclude a break-glass account before saving, every time, without exception.
Then enforce narrowly and widen. The failure is not writing a bad policy; it is
writing a correct policy that also applies to the person who would have to undo it.
**Prove it:** [`labs/m365-conditional-access-lockout`](../labs/m365-conditional-access-lockout/)

### "What bypasses a conditional access policy?"
**Probes:** whether you have looked for the paths that predate it.
**Answer:** ⏳ *Needs the specific.* The shape is legacy authentication — protocols
that never learned to present the signals the policy evaluates, so the policy has
nothing to apply and the sign-in succeeds. They are found by looking at sign-in logs
for protocol rather than for user, and they are usually kept alive by one appliance
nobody wants to touch.

## Privileged access & break-glass 🔨

### "Describe your break-glass design."
**Probes:** whether it exists, whether it is tested, and whether it depends on the
thing it is meant to survive.
**Answer:** An account that bypasses the conditional-access policies, with the
credential held out of band, alerting on any use. The two questions that decide whether
it is real: does it authenticate against the directory that might be the thing that is
down, and when was it last exercised. An untested break-glass path is a belief, not a
control — and it is believed hardest by the people who designed it.

### "How do you handle standing admin access?"
**Probes:** just-in-time versus permanent, and whether you can name the trade.
**Answer:** Elevation with approval and expiry rather than standing privilege, so the
window is bounded and the request is a record. The trade is friction during an
incident, which is exactly when you least want it — so the design has to include a
path that is fast enough to use at 3am, which is usually the break-glass account and
brings you back to the previous question.

## Access review & permission sprawl 🔨

### "How do you answer 'who can see this document?'"
**Probes:** whether you know that reading the permissions does not answer it.
**Answer:** Enumerate every grant path, not the ACL: direct, group, nested group,
sharing link, inherited, and API token. The link is the one that breaks reviews,
because it is a second grant path that no access review walks — the ACL can differ by
four names while the real audience differs by ninety.
**Prove it:** [`labs/permission-sprawl`](../labs/permission-sprawl/)

### "A quarterly access review passed every time and you still had a problem. How?"
**Probes:** whether you can see a control answering a smaller question than the one
being asked.
**Answer:** Because a point-in-time review asks *who has access now* and answers it
truthfully, every time, while the thing that went wrong was duration. Content shared
to a group stays readable by everyone who later joins the group — no grant is ever
made, so no review has anything to flag. The missing control was never an access
control; it was an expiry.
**Prove it:** [`labs/transcript-retention`](../labs/transcript-retention/)

## Workload identity 🧭

### "How do you give a workload in one cloud access to another?"
**Probes:** whether you reach for a key, and whether you can debug federation when it
fails.
**Answer:** A ramp — I have built and verified this pattern and have not run it in
production at scale. OIDC federation with no stored key: the target trusts the source's
issuer, and the trust conditions pin the subject so the trust is narrow. When it breaks
it is almost always one of four things — issuer misconfigured, subject claim not
matching the condition, token expiry, or JWKS unreachable — and the debugging is
reading both sides' view of the same token rather than either side alone.
**Prove it:** [`aws/01-scoped-identity-inventory`](../../platforms/aws/labs/01-scoped-identity-inventory/)

### "Why is a rotated secret still a secret?"
**Probes:** whether "we rotate them" reads to you as a solution or a mitigation.
**Answer:** Because it still exists somewhere that is not the identity system — on a
box, in a pipeline variable, in someone's notes — and rotation shortens the window
without closing it. Rotation is what you do while you are moving to workload identity,
not instead of it.

## Using this file

Every `⏳` is a question you can answer and have not written down. That gap is the
point of the format: an unwritten example is indistinguishable from an absent one at
the moment it is asked for.
