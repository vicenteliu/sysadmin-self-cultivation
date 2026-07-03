---
name: honesty-audit
description: Audit a resume, bio, skills list, LinkedIn blurb, or any technical claim and classify every claim as ✋ hands-on depth / 🧗 verified ramp / ❌ overclaim, using this repo's honesty discipline. Flags anything bluffed, suggests honest reframes, and (for ramps) the fast-verifiable-ramp wording. Use when the user says "audit this for overclaims", "is this honest", "check my resume claims", "am I bluffing", "✋ or 🧗", or shares a claims doc to vet.
created: 2026-07-02
owner: Vicente Liu
---

# Skill: honesty-audit

The honesty layer of [The Sysadmin's Self-Cultivation](../../WHY.md), turned into a
review pass you can run over any claim. It answers one question per claim: **can this
survive a probing follow-up in an interview — and if not, how do we make it true?**

## Why this matters (the repo's whole thesis)

In the AI era, tool knowledge is cheap; what separates people is judgment you can't
prompt into existence. A claim you can't defend under questioning is worse than
useless — it collapses in the interview that mattered. Honest labeling isn't modesty;
it's what makes the strong claims *land* and the ramps *credible*.

## The three tags

| Tag | Means | Verb test |
| --- | --- | --- |
| **✋ hands-on depth** | operated it for real; survives a deep follow-up | "led / built / ran / operated / administered" — defensible |
| **🧗 verified ramp** | concepts mapped and doc-checked, not run in production | "mapped / studied / can ramp onto" — honest about the gap |
| **❌ overclaim** | states depth the person doesn't have | any ✋ verb on 🧗 (or absent) experience |

Transferable *instincts* (least privilege, failure domains, idempotence, incident
method, scripting discipline) count as ✋ even on a platform the person hasn't run —
but the platform-*specific* surface is 🧗. Keep the two separate.

## The workflow

### 1 — Extract the claims

List every discrete technical claim in the input — each tool, platform, scope word
("at scale", "in production", "led"), and metric.

### 2 — Tag each claim

For each, ask: *"If an interviewer said 'walk me through a time you did this, in
detail,' would it hold?"*
- Holds with real specifics → **✋**.
- Holds only as "I understand the concept / could ramp fast" → **🧗**; rewrite the
  verb to match (studied/mapped/can operate, not led/owned).
- Doesn't hold → **❌ overclaim**; flag it loudly and propose the true version.

Cross-check against the person's known depth where available (for Vicente: the repo's
✋ platforms are self-host, vSphere; ✋ cross-cutting is Linux/foundations, endpoint,
identity, SaaS-admin, databases, ITSM/assets, web/TLS fundamentals; clouds and deep
K8s are 🧗).

### 3 — Reframe, don't just flag

For every 🧗 and ❌, give the honest rewrite that keeps the strength while dropping the
bluff — usually the repo's move: **"a transferable model/discipline plus a fast,
verifiable ramp."** A ramp stated honestly is a *selling point* (it shows judgment),
not a weakness.

### 4 — Output the ledger

A table: claim → tag → verdict → suggested wording. End with the two or three
strongest ✋ claims to lead with, and any ❌ that must be fixed before the doc ships.

## Guardrails

- Sensitive/gated facts (e.g. anything under a separation agreement or NDA) are a
  separate concern from honesty — if a claim is true but sensitive, flag it as
  **gated**, not as an overclaim, and defer to the user's decision on disclosure.
- Don't sand off real strength. The goal is *defensible*, not *modest* — a genuine ✋
  should be stated confidently.
- For public artifacts under the user's real name, never surface private context
  (job search, employer names) that the user hasn't chosen to make public.
