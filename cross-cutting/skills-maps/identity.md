---
kind: skill-map
axis: cross-cutting
themes: [identity]
platforms: [aws]
marker: "mixed"
summary: "One theme, cut across every platform. The substance lives in cross-cutting/identity-iam.md — this is the checkable version of it."
---
# Identity & Access — Theme Skill Map

> One theme, cut across every platform. The substance lives in
> [`cross-cutting/identity-iam.md`](../identity-iam.md) — this is the checkable
> version of it. Conventions, tier anchors and the marker rule are in
> [`README.md`](README.md).

Tiers anchor on **how far the skill travels**: **Core** is true on all seven
platforms, **Working** is true on most and you must know which one you're on,
**Depth** is where the platforms genuinely disagree. Check a box when you can
*do* it and *explain the failure modes*.

Identity is the densest cluster in the demand signal and the one where a wrong
answer is least visible: an over-broad grant looks exactly like a correct one
until someone uses it.

## Directory & the source of truth 🔨

- [ ] **Core** — Name the **one** system that decides a person exists, and what happens downstream when it says they stopped.
- [ ] **Core** — Users, groups, OUs, attributes — and why group-based access is the only thing that survives scale.
- [ ] **Core** — Say what breaks when the directory is unreachable, per dependent system, before it happens.
- [ ] **Working** — Hybrid: an on-prem directory synchronised to a cloud one, which attributes flow, which direction, and what a sync conflict looks like.
- [ ] **Working** — Two directories that both believe they are authoritative — recognise the shape before it is a project.
- [ ] **Depth** — Migrate the source of truth without an outage: coexistence, cutover, and the rollback nobody plans.

## Authentication vs authorization 🔨

- [ ] **Core** — Keep the two questions separate — *who are you* and *what may you do* — in every conversation. Conflating them is the root of most identity confusion.
- [ ] **Core** — MFA factors and their real strength ranking; why SMS is a factor and still a weak one.
- [ ] **Core** — Session lifetime, token expiry, and the refresh that quietly keeps a revoked user signed in.
- [ ] **Working** — Passwordless and FIDO2/WebAuthn: what is actually resistant to phishing and why.
- [ ] **Working** — Read an authentication log and separate a failed sign-in from a successful sign-in that was then denied authorization.
- [ ] **Depth** — Token replay and consent phishing — attacks that never touch the password.

## Federation & SSO (SAML / OIDC) 🔨

- [ ] **Core** — Draw the flow: SP/RP, IdP, assertion or token, and who trusts whom.
- [ ] **Core** — Decide SAML vs OIDC for a given application and say why — not by preference, by what the application supports.
- [ ] **Core** — Debug the four classic federation failures: clock skew, wrong entity ID / audience, certificate expiry, attribute or claim mismatch.
- [ ] **Working** — Claims/attribute mapping into the roles the target actually evaluates.
- [ ] **Working** — Trust in both directions across an interconnect: OIDC issuer, subject mapping, JWKS reachability.
- [ ] **Depth** — Signing-certificate rotation on a live federation, without dropping the sessions mid-rotation.

## Running an IdP yourself 🧭

- [ ] **Core** — Say what you are taking on when the IdP becomes yours: it is now the highest-blast-radius system you operate.
- [ ] **Core** — Design its availability first — every other system's login depends on it, so its downtime is not its own.
- [ ] **Working** — Signing-key lifecycle, storage and rotation.
- [ ] **Working** — Back it up and **restore it**: an IdP restore is an identity-continuity exercise, not a database exercise.
- [ ] **Depth** — Upgrade a live IdP; and know the honest cost comparison against a hosted one before choosing to run it.

## SCIM & the joiner/mover/leaver lifecycle 🔨

- [ ] **Core** — Automate all three of J, M and L. **Leaver is the one that gets skipped**, and the only one with an auditor attached.
- [ ] **Core** — Say what SCIM does that SSO does not: SSO answers how people sign in, SCIM answers how accounts come into existence and stop.
- [ ] **Core** — Trace a *mover* end to end — the case that quietly accumulates permissions, because the new access is granted and the old is not removed.
- [ ] **Working** — Deprovision across systems SCIM does not reach, and enumerate them before you need the list.
- [ ] **Working** — Reconcile the directory against each downstream system and explain every difference.
- [ ] **Depth** — Contractors, service accounts and shared mailboxes — the principals the lifecycle was not designed for and still owns.

**Prove it:** [`toolbox/user-lifecycle`](../../toolbox/user-lifecycle/)

## RBAC & least privilege 🔨

- [ ] **Core** — Write a **scoped** policy for one task and defend why it is minimal.
- [ ] **Core** — Principal, role, policy, scope — map the four onto whichever platform is in front of you.
- [ ] **Core** — Read a **denied** request and explain the deny: which rule, at which scope, evaluated in which order.
- [ ] **Working** — Deny-by-default and explicit-deny precedence, and the org-level boundary that overrides a local allow.
- [ ] **Working** — Two authorization planes at once — a directory role and a resource role, or cloud IAM and cluster RBAC — where a grant in one plane says nothing about the other.
- [ ] **Depth** — Right-size an existing over-broad role from usage evidence rather than from a guess.

**Prove it:** [`aws/iam-deny-by-default`](../../platforms/aws/labs/iam-deny-by-default/) · [`azure/global-admin-is-not-owner`](../../platforms/azure/labs/global-admin-is-not-owner/) · [`gcp/gke-iam-vs-rbac`](../../platforms/gcp/labs/gke-iam-vs-rbac/) · [`oci/a-compartment-is-not-an-account`](../../platforms/oci/labs/a-compartment-is-not-an-account/)

## Conditional access & device trust 🔨

- [ ] **Core** — Express a policy as *signals → decision*: user, device, location, risk → allow, block, or require something more.
- [ ] **Core** — **Never write a policy that can lock you out.** Exclude a break-glass account before saving, every time.
- [ ] **Core** — Read a sign-in log and say which policy applied and why.
- [ ] **Working** — Device compliance as a signal, and the enrolment path that has to exist first.
- [ ] **Working** — Report-only mode as the default before enforcement — and actually reading the report.
- [ ] **Depth** — Legacy-authentication paths that bypass the policy entirely, and finding them before an attacker does.

**Prove it:** [`labs/m365-conditional-access-lockout`](../labs/m365-conditional-access-lockout/)

## Privileged access & break-glass 🔨

- [ ] **Core** — Separate the daily account from the privileged one, for yourself first.
- [ ] **Core** — Design a **break-glass** account: what it bypasses, where the credential lives, and who is alerted when it is used.
- [ ] **Core** — Root/global-admin hygiene: MFA, no keys, no daily use, monitored.
- [ ] **Working** — Just-in-time elevation with approval and expiry, instead of standing privilege.
- [ ] **Working** — Test the break-glass path on a schedule. An untested one is a belief, not a control.
- [ ] **Depth** — Highest-privilege actions that leave no useful audit trail — find them, then compensate.

## Access review & permission sprawl 🔨

- [ ] **Core** — Answer *"who can see this?"* — and know that reading the permissions does not answer it, because a sharing link is a grant path no review walks.
- [ ] **Core** — Run a review that finds stale accounts and over-broad grants, and produces evidence rather than an assertion.
- [ ] **Working** — Enumerate **every** grant path to a resource: direct, group, nested group, link, inherited, and API token.
- [ ] **Working** — Recognise the shape where a point-in-time review passes truthfully and the estate is still wrong — because the missing control was an **expiry**, not an access control.
- [ ] **Working** — Reconcile two systems that disagree and decide which is right; the join key you pick decides how much of the answer is fiction.
- [ ] **Depth** — Make review evidence auditable: reproducible, dated, and attributable to a decision-maker.

**Prove it:** [`labs/permission-sprawl`](../labs/permission-sprawl/) · [`labs/transcript-retention`](../labs/transcript-retention/)

## Workload identity 🧭

- [ ] **Core** — Give a machine an identity instead of a secret, and say why a rotated secret is still a secret.
- [ ] **Core** — Short-lived credentials over long-lived keys — and find the long-lived keys already in your estate.
- [ ] **Working** — Attach an identity to a compute resource per platform, and enumerate who else on that host can then reach it.
- [ ] **Working** — Federate a workload from one cloud into another with OIDC and no stored key; debug it at the trust conditions and the subject claim.
- [ ] **Depth** — Inventory every non-human principal and its blast radius. This list is usually longer than the human one and reviewed less often.

**Prove it:** [`aws/01-scoped-identity-inventory`](../../platforms/aws/labs/01-scoped-identity-inventory/)

## The "can you actually operate it" test

Every **Core** box checked means identity transfers: the vocabulary changes per
platform, the questions do not. **Working** boxes are where the platforms stop
agreeing — two authorization planes, hybrid sync, cross-cloud federation — and
where a single-platform instinct is most confidently wrong.

Five of the ten sections point at something runnable, which is the highest
density in the repo, and it is not an accident: identity is where this repo's
labs concentrated, because it is where a mistake is least visible from the
inside. The sections without a drill — directory, AuthN/AuthZ, federation,
running an IdP, privileged access — are the ones to be most suspicious of your
own confidence on.
