# Identity & Access (IAM)

> The densest, most-transferable surface there is. Get identity right and everything
> else has a front door with a lock on it; get it wrong and nothing else matters.
> This is the concept layer — the *same* discipline whether it's Active Directory,
> AWS IAM, Azure RBAC, GCP IAM, or Okta.

Identity is the surface job postings ask for more than any other, and for good
reason: it's the control plane. Every request to every system is, underneath,
*"who are you, and are you allowed to do this?"* Master that question once and each
platform's IAM is a renaming exercise.

## The two questions (never conflate them)

- **Authentication (authN)** — *who are you?* Proving identity: a password + MFA, a
  token, a certificate, a federated assertion.
- **Authorization (authZ)** — *what are you allowed to do?* Roles, policies,
  permissions, scopes.

Most identity bugs and breaches live in the gap between these two: a correctly
authenticated principal with far more authorization than it needed. Which leads to
the one rule that runs through everything:

## Least privilege — the whole game

Grant the *minimum* permission that still does the job, at the *narrowest* scope, for
the *shortest* time. Every platform gives you the tools; the discipline is yours:

- **Minimum permission** — read-only if it only reads; one action, not a wildcard.
- **Narrowest scope** — one bucket / one resource group / one project, not the whole account.
- **Shortest time** — short-lived credentials and just-in-time elevation over standing access.

If you internalize one thing from this file, it's this. Everything below is machinery
for applying it.

## Principals: humans vs. workloads

Two kinds of identity, and mixing them up is a classic mistake:

- **Human identities** — people, in a directory (AD, Entra, Okta, Google). Managed by
  lifecycle (below), protected by MFA, granted access through **groups**.
- **Workload identities** — apps, scripts, servers, pipelines. The correct pattern is
  a platform-managed identity with **no long-lived secret on the box** — AWS IAM
  roles / instance profiles, Azure Managed Identities, GCP service accounts. A secret
  key baked into a VM or a repo is the thing you're trying to never do.

## The lifecycle: Joiner / Mover / Leaver (JML)

Human access has a life cycle, and automating it is where identity stops being
ticket-work and becomes engineering:

- **Joiner** — new hire → account created, added to the right groups, productive on
  day one.
- **Mover** — role change → permissions added *and removed* to match the new role
  (the "removed" half is the one everyone forgets, and it's how permission creep
  happens).
- **Leaver** — departure → access cleanly revoked, everywhere, promptly.

Done by hand this doesn't scale and it fails audits. Done as code — driven through the
directory's API, or through **SCIM** to downstream SaaS — headcount can grow without
ticket volume growing with it. That's the difference between *scaling people* and
*scaling tickets*.

## The same concepts, renamed per platform

Once the concepts above are solid, each platform is a lookup:

| Concept | On-prem AD | Microsoft Entra | AWS | GCP | Okta |
| --- | --- | --- | --- | --- | --- |
| **Directory / IdP** | Active Directory | Entra ID | IAM Identity Center | Cloud Identity | Universal Directory |
| **Human authZ** | AD groups + GPO | **Azure RBAC** roles | IAM roles + policies | IAM roles + bindings | groups + app assignments |
| **Workload identity** | service accounts / gMSA | **Managed Identities** | IAM roles (instance profiles) | service accounts | — (human IdP) |
| **Federation / SSO** | AD FS | Entra SSO | Identity Center / SAML-OIDC | Workforce Identity Federation | **Okta itself** (the hub) |
| **Provisioning** | AD/LDAP | Entra provisioning / SCIM | SCIM to Identity Center | — | Okta Lifecycle / SCIM |
| **Privileged access** | tiered admin / PAW | **PIM** (just-in-time) | permission sets + STS | — | Okta PAM |

> **The Azure gotcha worth memorizing:** Azure has *two* permission systems — **Entra
> ID roles** (directory-level: who manages users/apps/groups) and **Azure RBAC**
> (resource-level: who touches this VM/storage). AWS has one IAM. Confusing the two is
> the #1 Azure identity mistake.

## Federation & SSO — the protocol layer

"Sign in once, reach many apps." Three acronyms you must be able to keep straight,
because interviewers and incidents both test it:

- **SAML 2.0** — the older, XML-based enterprise standard. An Identity Provider (IdP)
  sends a signed **assertion** to a Service Provider (SP). Still everywhere in
  enterprise SaaS.
- **OAuth 2.0** — an *authorization* framework, not authentication. It issues
  **access tokens** with **scopes** for delegated access ("let this app read my
  calendar"). People misuse it as login; it isn't login by itself.
- **OpenID Connect (OIDC)** — an *authentication* layer built **on top of** OAuth 2.0.
  It adds an **ID token** (a signed JWT saying "this user authenticated"). This is
  modern web/app SSO.

One-liner to hold: **SAML and OIDC are for signing in; OAuth is for granting an app
scoped access; OIDC is OAuth with an identity layer bolted on.**

## SCIM — provisioning as an API

**SCIM** (System for Cross-domain Identity Management) is the standard REST API for
**pushing** user/group create-update-delete from your IdP into downstream SaaS. It's
what turns JML from a person clicking around N admin consoles into one automated flow:
hire in the directory → SCIM provisions the SaaS accounts → offboard in the directory
→ SCIM deprovisions them everywhere. If SSO answers "how do people log in," SCIM
answers "how do accounts get created and destroyed."

## The admin discipline (what to be able to do)

- Create a **scoped role/policy** for a specific task and explain why it's minimal.
- Design **group-based** access for humans (never per-user grants at scale).
- Give a workload a **managed identity** — no secret on the box.
- Automate **joiner/mover/leaver** through the directory API and/or **SCIM**.
- Stand up **SSO** for an app and know whether it's SAML or OIDC, and why.
- Run an **access review**: find stale accounts and over-broad grants, and prove it.
- Read a **denied request** (CloudTrail / Azure Activity Log / audit log) and explain the deny.

## The AI-assisted ramp (identity flavor)

Identity is a place where AI is a huge accelerant *and* a real hazard, because the
artifacts are security-critical and the vocabulary collides across platforms.

- **Translate, don't tutorial:** *"I know AD groups, LDAP, and SSO concepts — map that
  onto Azure RBAC vs. Entra roles, and flag where they genuinely differ."*
- **Generate least-privilege, then tighten by hand:** *"the tightest IAM policy / RBAC
  role that does exactly this and nothing more."* AI drafts permissive; you cut.
- **Untangle the two Azure planes:** *"does this task need an Entra role or an Azure
  RBAC role, and at what scope?"* Ask every time until it's reflex.
- **Where AI burns you (verify hardest):** it invents IAM **action strings** and RBAC
  role names that don't exist; it blurs OAuth vs. OIDC; it mixes Entra roles with
  Azure RBAC; it forgets the *Leaver* half of lifecycle. Every generated policy gets
  checked against the docs and tested with a denied-request probe.

## Honest boundaries

This is a **hands-on strength** surface, and the notes say so plainly: real experience
building and running directory/identity infrastructure — Active Directory lifecycle,
an in-house **OpenLDAP-backed SSO**, an initial **Entra ID / Azure AD** setup, and
**joiner/mover/leaver automation via Graph** at scale, with SCIM as a working concept.
Where it's *evaluation-level* rather than production, it's labeled that way — e.g.
**Okta** was chosen against (in favor of in-house OpenLDAP) rather than operated for
years. The claim is a deep, transferable identity foundation plus a fast, verifiable
ramp onto any specific IdP — not "ten years of Okta."
