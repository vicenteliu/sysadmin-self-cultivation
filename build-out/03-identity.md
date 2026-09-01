---
kind: route-step
axis: build-out
themes: [identity]
platforms: []
marker: "🔨"
summary: "🔨 hands-on (Entra/Azure AD, M365 tenant work, JML at scale) Before: nothing."
---
# 03 · Identity — directory, groups, SSO

> 🔨 hands-on (Entra/Azure AD, M365 tenant work, JML at scale)
> **Before:** nothing. **After:** 04 devices · 05 network (802.1X) · 06 tenant and mail ·
> 07 files · 08 endpoint security · 10 remote access · 11 assets · 14 compliance evidence · 15 JML

**This step has no physical prerequisite, and that is the whole argument for
where it sits.** Identity is the only part of a build-out that can begin before
there is a building — and almost everything that comes later attaches to it. Put
it after the hardware and you are not sequencing badly, you are committing to
re-doing work you have already paid for.

## What this step produces

- A directory chosen, with the reason written down — and the reason is rarely the
  directory's features. It is which SaaS estate and which device platforms have to
  attach to it later.
- A **group model** with one rule enforced: a group means *a job function* or *an
  access bundle*, never both. (See "Getting it backwards".)
- A naming convention that survives a legal name change, a contractor converting to
  staff, and a rehire. **All three are routine at this size**: across one lease the
  reference office issues accounts to
  [about two hundred and sixteen different people](../the-reference-office.md#parameters)
  for a floor that seats a hundred and thirty, so a convention that only works for a
  first-time hire breaks inside the first year.
- **Two break-glass accounts**, excluded from conditional access, credentials
  physically retrievable by someone who is not you.
- A count of the **identities that are not people**. In the reference office the network
  alone requires
  [about twenty-six device credentials](../the-reference-office.md#parameters) before a
  single integration is bought, and none of them has a leaver event.
- A named answer to: *what system decides whether a person is still an employee?*

## Questions to ask first

- **Who is the source of truth for employment?** HR system or directory? Until this
  has one answer, Leaver never works reliably — someone leaves, HR knows, the
  directory does not, and access persists for months. This is the single most
  common finding in a first audit.
- **What will a group mean?** Job function (`engineering`) or access bundle
  (`can-read-finance-share`)? Both is the answer that feels efficient on day one and
  is unrecoverable by year two.
- **Who is the second admin?** If the answer is "nobody yet", the build is one
  person away from an outage nobody else can end.
- **What is excluded from conditional access, and who can physically reach it?**
- **What happens to a person's data at Leaver** — mailbox, files, licence? Decide
  before the first departure, not during it.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Directory | on-prem AD, domain controllers you rack and patch | cloud directory as primary; on-prem is the exception needing justification |
| App integration | per-app accounts; ADFS if you were ambitious | SSO via SAML/OIDC as the default; an app without it is a procurement red flag |
| Provisioning | scripts against LDAP, or a person and a ticket | SCIM to downstream SaaS |
| "Is this request safe?" | *are you on the LAN* | conditional access — device state, location, risk signal |
| Cost of getting it wrong | contained; you controlled the perimeter | unbounded; the identity *is* the perimeter |

**How much of that is AI: almost none.** This shift is SaaS-ification — the
directory became somebody else's service, and the integration protocol became
standard. Nothing here waited on a model.

Where AI does show up is **after** the build, in the review work: access reviews,
orphaned-account detection, explaining why two systems disagree about a person.
That is advisory, and the industry treats it that way — in a 2026 survey of
1,000+ sysadmins, the tasks where AI adoption actually landed were the advisory
ones, while anything holding authority over a production change stayed in the
teens. Identity is the clearest case of that split: let it *find* the orphaned
account; do not let it *disable* one.

## Read deeper

- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — the two
  questions, least privilege, principals, JML, SCIM, federation
- [`cross-cutting/saas-admin.md`](../cross-cutting/saas-admin.md) — the identity
  spine across Workspace / M365
- [`cross-cutting/m365-support.md`](../cross-cutting/m365-support.md) — the
  break-fix craft on the tenant you are about to create
- [`the-stack/07-security.md`](../the-stack/07-security.md) — where identity sits
  in defence-in-depth
- [the reference office](../the-reference-office.md#parameters) — the joiner, mover and
  leaver volumes this directory has to absorb, and why the population turns over faster
  than an annual access review

## Do it

- [`cross-cutting/labs/m365-conditional-access-lockout/`](../cross-cutting/labs/m365-conditional-access-lockout/)
  — ship a naive policy, lock yourself out, add the fire exit. Do this **before**
  the tenant has users in it, not after.
- [`toolbox/user-lifecycle/`](../toolbox/user-lifecycle/) — joiner/mover/leaver as
  a CSV rather than fifty hand-typed commands. Dry-run by default.

## Getting it backwards

**Buying and enrolling the fleet first.** You order 100 machines, image them, and
enrol them — and then discover the directory that actually fits your SaaS estate
uses a different join model. Re-enrolment is not a settings change; it is a
re-imaging project across 100 desks, and it happens during the weeks people are
trying to start working.

**Groups that mean two things.** `engineering` starts as a job function, then
someone grants it access to a finance share because the engineers needed one
report. Two years on, nobody can answer "who should be able to see this?" —
because the group no longer describes anything. Access reviews at that point are
not reviews, they are archaeology, and at the first SOC 2 audit you cannot produce
the evidence because the evidence was supposed to have been accumulating all along.

**No second admin, no break-glass.** The failure is not that it is likely. It is
that its cost is unbounded and its fix costs nothing on day one.
