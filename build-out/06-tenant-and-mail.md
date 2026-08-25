# 06 · Tenant and mail — domains, routing, SPF/DKIM/DMARC

> 🔨 hands-on — M365 tenant work and the break-fix craft around it
> **Before:** 03 identity. **After:** 07 files · 09 backup · 14 compliance evidence · 15 JML

The tenant is created in this step, but **the decision that shapes it was made in
03** — the directory and the productivity suite are the same purchase for most
offices, and pretending otherwise leads to the two being chosen by different
people for different reasons.

What is genuinely this step's own is **mail authentication**, and it deserves more
respect than it usually gets: SPF, DKIM and DMARC are the difference between your
invoices arriving and your domain being used to phish your customers.

## What this step produces

- The tenant, with its **regions and data residency** decided deliberately rather
  than accepted from a wizard.
- Domains verified, with a written record of where DNS is actually hosted and who
  can change it.
- **SPF, DKIM and DMARC published — and DMARC moved past `p=none` on a date that is
  written down.** Publishing `p=none` and stopping is the industry's most common
  half-done job.
- A mail-flow diagram that includes the things people forget: the ticketing system,
  the CI runner, the billing platform, the marketing tool.
- Retention and legal-hold settings chosen before there is anything to retain.

## Questions to ask first

- **Everything that sends as your domain — list it.** Not the mail server; every
  application. Each one is an SPF entry and a DKIM key, and the one that gets missed
  is always the one finance uses.
- **Who controls DNS, and how quickly can a record change?** Mail authentication is
  DNS. If the registrar login is with an agency that answers in three days, that is
  now your incident response time for a mail problem.
- **What is the plan to get DMARC to enforcement?** Not whether — when, and what
  evidence you need first. Without a date this stays at `p=none` forever, which
  provides reporting and protects nothing.
- **Where does the data live, and does the SOC 2 customer care?** Changing region
  later usually means a migration, not a setting.
- **What happens to a departed person's mailbox?** Convert, delegate, retain, delete —
  and for how long. Decide with 15, not in the moment.
- **Is there a break-glass path if conditional access misfires?** This is the same
  question as 03, asked from the other side, and it is the reason that lab exists.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Where mail runs | an Exchange server you patch, back up and fail over | a tenant; the server problem is gone entirely |
| The hard part | availability and storage | **authentication and routing** — proving mail is yours |
| SPF/DKIM/DMARC | optional, widely skipped | effectively mandatory; large receivers enforce it and deliverability collapses without it |
| Admin surface | one console | a tenant plus every app that sends on your behalf |
| Failure mode | the server is down | your domain is being spoofed and you find out from a customer |

**How much of that is AI: none for the build. One genuine use afterwards.**
Everything above is SaaS-ification — mail became someone else's server, and the
work moved to authentication and integration.

The real post-build use is **reading DMARC aggregate reports**: they arrive as XML,
in volume, and the question they answer ("is this legitimate sender ours?") is
pattern-matching over messy data with a human decision at the end. That is exactly
the advisory shape this series keeps landing on — let it group and explain the
senders, let a person decide which are authorised.

## Read deeper

- [`cross-cutting/m365-support.md`](../cross-cutting/m365-support.md) — the 🔨
  break-fix craft on this exact surface
- [`cross-cutting/saas-admin.md`](../cross-cutting/saas-admin.md) — the identity
  spine across Workspace and M365, and SCIM lifecycle
- [`cross-cutting/web-and-tls.md`](../cross-cutting/web-and-tls.md) — certificate and
  DNS record hygiene, the same discipline as mail records
- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md)

## Do it

- [`cross-cutting/labs/m365-conditional-access-lockout/`](../cross-cutting/labs/m365-conditional-access-lockout/)
  — the tenant-level mistake that is easiest to make and most expensive to undo.

- [`cross-cutting/labs/mail-authentication-alignment/`](../cross-cutting/labs/mail-authentication-alignment/)
  — three green records and a fully spoofable domain, which is the same screenshot.
  Why `p=none` is monitoring rather than protection, and what enforcement would
  break if you moved today.

## Getting it backwards

**Stopping at `p=none`.** The records exist, a dashboard shows reports arriving,
and everyone considers it done. It is monitoring, not protection — anyone can still
send as your domain and receivers will deliver it. The move to enforcement is the
work, and it is the part that gets deferred indefinitely because it carries a small
risk of breaking a legitimate sender you failed to enumerate.

**Discovering senders one bounce at a time.** The list is knowable up front with an
hour of asking around. Discovered reactively, each one is an outage for whichever
department owned that tool.

**Letting the tenant be created by whoever needed email first.** It happens during
the scramble, with a personal account as global admin and a `.onmicrosoft.com`
domain in the record. Untangling ownership later is possible and unpleasant.
