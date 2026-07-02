# SaaS & Collaboration Administration

> 🚧 **Opening written; body in progress.** The framework below is complete —
> what this module will cover is fixed; the prose is being filled in.

> The clouds run your infrastructure; SaaS runs your company. Google Workspace,
> Microsoft 365, and the identity fabric under them are where most employees
> actually live — and administering them well is a distinct, high-demand craft the
> platform folders don't touch. This one is **✋ hands-on depth**.

Every layer below this one asked how machines run; this asks how *people* work —
mail, docs, collaboration, and the account lifecycle that grants and revokes it all.
It's the operate-and-automate lane pointed at the productivity suite, and it leans
directly on the identity discipline of [`cross-cutting/identity-iam.md`](identity-iam.md):
a user's SaaS access *is* their joiner/mover/leaver lifecycle, made concrete.

## Planned coverage

- **Google Workspace administration** — the admin console, org units, document
  ownership and permission transfers, account and email lifecycle, and running the
  suite through an email-platform migration (Workspace → self-hosted) without
  breaking anyone's day.
- **Microsoft 365 administration** — Exchange (mailboxes, shared mailboxes,
  distribution groups, transport rules), SharePoint (sites and permissions), Teams;
  the admin-center operations distinct from end-user support.
- **The identity spine** — Entra ID / Azure AD, SSO, MFA, Conditional Access, and
  PIM as the control plane over the SaaS estate (initial-setup depth; ties to
  [`the-stack/07`](../the-stack/07-security.md) and the identity note).
- **Provisioning at scale** — SCIM and directory-driven lifecycle so onboarding and
  offboarding scale with headcount instead of ticket volume.
- **Email as infrastructure** — domain and DNS records (SPF and friends), mail
  flow, and where email security lives — honestly scoped to what's been operated.
- **The AI-assisted ramp** — AI is strong at admin-console PowerShell/Graph scripts;
  it invents cmdlets and over-scopes permissions, so generated automation gets
  checked and least-privileged by hand.

## Honest boundaries

✋ **hands-on depth.** Google Workspace administered for a global workforce through
a live email-platform migration; Microsoft 365 admin operations (Exchange/SharePoint/
Teams) and Entra ID initial setup (tenant-wide MFA, a Conditional Access policy,
PIM) done for real. Scoped honestly: deep Exchange Online tenant engineering,
Proofpoint, and DMARC/DKIM operations are 🧗 ramps, not claims — the same
distinction this repo draws everywhere.
