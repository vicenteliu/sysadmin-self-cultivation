---
kind: route-step
axis: build-out
themes: [identity, networking]
platforms: []
marker: "🔨"
summary: "🔨 hands-on — VPN operations, certificate and TLS fundamentals, the auth failure paths Before: 01 uplink · 03 identity · 05 network."
---
# 10 · Remote access — VPN, or the thing that replaced it

> 🌐 **Languages:** English (default) · [中文](../docs/zh/build-out/10-remote-access.md)

> 🔨 hands-on — VPN operations, certificate and TLS fundamentals, the auth failure paths
> **Before:** 01 uplink · 03 identity · 05 network. **After:** 13 the help desk

The scenario has one office and one small branch, and **nobody is in either of them
five days a week**. That makes this step load-bearing in a way it was not a decade
ago: for most staff, most days, the "network" is whatever they are sitting on, and
this step decides what that gets them.

The question is no longer whether to have a VPN. It is **what still requires one**,
and the honest answer for a SaaS-first office is: a short list, mostly the things
that could not leave the building in step 05.

## What this step produces

- A written list of what actually requires network-level access — and it should be
  short. Everything reachable by SSO does not belong on it.
- Access to that short list, tied to the directory, with device posture as a
  condition rather than a hope.
- A path for the branch that is decided rather than improvised.
- A break-glass route for the people who fix things, that does not depend on the
  thing being fixed.
- A support runbook, because this is the single highest-volume failure the help desk
  will see (see 13).

## Questions to ask first

- **What genuinely needs it?** The lab gear, the door controller's management page,
  maybe a legacy appliance. If a full-tunnel VPN is being used to reach a SaaS app,
  something is misconfigured or someone is solving an access problem with a network
  tool.
- **Is access conditioned on the device, or only on the person?** A correct password
  from an unmanaged machine is the case this step exists to think about.
- **What happens when the identity provider is unreachable?** Every remote path now
  depends on 03. Does the failure lock out the people who would fix it?
- **Split tunnel or full tunnel — and can you defend the answer?** Full tunnel sends
  every video call through the office uplink you sized in 01. That is a capacity
  decision disguised as a security preference.
- **How does someone get help when they cannot connect?** The support channel must not
  require the thing that is broken.
- **What does the branch do when its link drops** — fail to a tunnel over consumer
  broadband, or stop? Both are answers.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Purpose | reach the corporate LAN, where the work was | reach the few things that never left it |
| Who used it | travellers and a few remote staff | most people, most days |
| Trust model | on the VPN means trusted | the tunnel is transport; identity and device posture decide access |
| Scale expectation | a fraction of headcount | everyone at once, on a snow day, and it must not fall over |
| Most common ticket | "VPN won't connect" | **"VPN won't connect"** — the one row that did not change |

**How much of that is AI: none for the design.** The shift from network-perimeter to
identity-and-device is architectural, and it was well underway before the current
wave of models.

Where AI earns a place is the last row. VPN and authentication failures are
high-volume, low-variance, and opaque to the person experiencing them — the symptom
is identical whether the cause is an expired certificate, a directory outage, a
policy change, or a hotel captive portal. Given the client log, proposing which of
those it is, is genuinely useful triage. It should propose; a person should act.

## Read deeper

- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — conditional
  access, and why "on the network" stopped being an authorisation
- [`the-stack/07-security.md`](../the-stack/07-security.md) — where remote access
  sits in defence-in-depth
- [`cross-cutting/web-and-tls.md`](../cross-cutting/web-and-tls.md) — certificate
  lifecycle, which is the cause of a large share of the failures above
- [`the-stack/02-network.md`](../the-stack/02-network.md) — routing, and why the
  tunnel changes which route is more specific

## Do it

- ✅ [`cross-cutting/labs/remote-access-four-causes/`](../cross-cutting/labs/remote-access-four-causes/)
  — **runnable, pure-local.** All four failure paths above, producing one identical
  user report. Watch the reflex checks eliminate nothing, watch a captive portal
  masquerade as an identity outage, and watch an elimination order resolve 4/4 with
  a bounded worst case where habit resolves 2/4.

  ```bash
  python3 cross-cutting/labs/remote-access-four-causes/four_causes_drill.py
  ```

- [`cross-cutting/labs/m365-conditional-access-lockout/`](../cross-cutting/labs/m365-conditional-access-lockout/)
  — the policy that locks out remote users is the same policy that locks out you

## Getting it backwards

**Full tunnel by default.** Every video call from every home now traverses the
office uplink. It is discovered as "the internet is slow" complaints that nobody
connects back to this decision, and the fix is a capacity purchase that was never
needed.

**Access conditioned on the person only.** The credential is correct; the machine is
personal, unpatched, and outside every control from step 08. This is the gap
conditional access exists to close, and it costs nothing to close on day one.

**A break-glass path that depends on the identity provider.** When the directory has
a bad hour, the people who could fix it cannot get in. Test this specific failure
before you need it.

**No runbook for the top ticket.** This will be the most common request the help desk
receives, forever. Not writing it down means solving it from scratch, at volume, by
whoever is nearest.
