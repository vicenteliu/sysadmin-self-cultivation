# The Operating Model

> The transferable skeleton under every platform. Learn this once; everything else
> is syntax.

Most "learn AWS / Azure / GCP" material throws a hundred services at you and hopes
some stick. That's backwards. Underneath the branding, an administrator is always
doing the same handful of things. Name them, and a new platform stops being a wall
of jargon and becomes a fill-in-the-blanks exercise.

## The three moves

Everything an admin does to *drive* a platform reduces to:

1. **Register a scoped identity.** A principal (user, service account, role, app
   registration) with the *least* privilege that still does the job.
2. **Get a credential and authenticate.** An access key, a token, a short-lived
   session, a certificate. This is what your scripts and tools carry.
3. **Drive the platform through its API — and codify it.** The console is for
   looking; the API/CLI/SDK is for doing; infrastructure-as-code is for making it
   repeatable, reviewable, and disposable.

If you can do those three cleanly, you can operate anything. The rest is knowing
*which* resources exist and *what* the failure modes are.

## The seven surfaces every platform has

Give any cloud/platform this once-over and you've mapped ~90% of the admin's job:

| Surface | The question it answers | Transfers as |
| --- | --- | --- |
| **Identity & access** | Who can do what, and how do they prove it? | IAM / RBAC, roles, policies, least-privilege, lifecycle |
| **Compute** | Where does code run? | VMs, containers, serverless, autoscaling |
| **Networking** | How do things reach each other, safely? | Virtual networks, subnets, routing, firewalls, DNS, load balancing |
| **Storage & data** | Where does state live? | Object / block / file storage, managed databases, backup |
| **Provisioning & config** | How is all of this created and kept consistent? | Infrastructure-as-code, config management, images |
| **Observability** | Is it healthy, and how do I know? | Metrics, logs, traces, alerts, dashboards |
| **Security & compliance** | Is it safe, and can I prove it? | Encryption, secrets, hardening, audit, guardrails, cost as a control |

Every platform module in this repo is organized around these surfaces. Once you've
internalized them, learning platform #2 is *"okay, what's their word for a VNet,
and what's the gotcha?"* — a question AI answers in seconds.

## What actually transfers (and what doesn't)

**Transfers cleanly** — the concepts above. Least-privilege is least-privilege
whether it's an AWS IAM policy or an Azure role assignment. A subnet is a subnet.
Idempotent, reviewable infrastructure is the goal on every platform.

**Doesn't transfer** — the *names*, the *defaults*, the *quirks*, and the *failure
modes*. This is exactly the layer where mistakes and outages come from, and exactly
where "I read the marketing page" gets you burned. It's also the layer AI is best
at compressing — *if* you verify (see [`ai-workflow/`](ai-workflow/)).

## The discipline that makes it real

A mental model without hands is just trivia. For each platform the bar is:

- I can create a **scoped identity** and authenticate a script with it.
- I can stand up a small, realistic stack from **code** (not clicks).
- I can **tear it down** as cleanly as I built it.
- I can explain the **security and cost** implications of what I built.
- I know the **three or four things that most commonly break**, and how I'd debug them.

That's "competent." The labs in each platform folder exist to make you actually do
it, because reading about a subnet and configuring one are different skills — and
only one of them shows up in an interview or an incident.
