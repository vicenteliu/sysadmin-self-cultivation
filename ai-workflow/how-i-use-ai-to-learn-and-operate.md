# How I Use AI to Learn and Operate

> The meta-layer. Every platform module has its own AI-ramp; this is the shared
> philosophy behind them — and the part that keeps AI from quietly wrecking things.

The pitch of this whole project is that in 2026 a systems admin's advantage isn't
knowing every service — it's **judgment plus an AI-augmented ramp**. That only works
if the AI is used with discipline. Two rules do most of the work:

## Rule 1 — AI for speed, judgment for truth

AI is exceptional at the parts that are *tedious but not hard*: translating a concept
you already own into a new platform's vocabulary, drafting the IAM policy, writing the
first Terraform pass, explaining an error. It is unreliable at the parts that are
*load-bearing*: exact API parameters, current defaults, security-critical config,
cost. So the division of labor is fixed:

- **AI drafts.** You get to a working first version in minutes, not days.
- **You verify.** Every service name, parameter, and permission is checked against
  official docs, and every change is run in a throwaway sandbox with a hard budget
  alarm before it's trusted.

The failure mode to design against is **confident wrongness** — a plausible answer
that's subtly, expensively, or dangerously off. Assume the draft is ~90% right and
your job is hunting the 10%.

## Rule 2 — Anchor everything to what you already know

The fastest learning prompt isn't "teach me X." It's *"I already understand
\<Linux / networking / IAM / whatever I actually know\> — map X onto that; give me
the delta."* This skips the beginner tax entirely and plays to a experienced admin's
real strength: the concepts are already there; only the labels are new.

## The reusable prompt kit

- **Translator** — "explain X assuming I know \<foundation\>; just the delta."
- **80/20** — "what's the 20% of X an admin uses daily; what can I defer?"
- **Gotcha hunter** — "the 3 things that most commonly break with X, and how to avoid them."
- **Least-privilege generator** — "tightest policy/role that does exactly this, nothing more." (Then tighten by hand.)
- **Reviewer** — "review this IaC / policy / design for security, cost, reliability risks."
- **Rubber duck** — paste an error / CLI output / denied request; "what does this mean and how do I debug it?"

## What AI does *not* replace

It won't feel that a security group is one line from exposing a database. It won't
own the incident at 3 a.m. It can't be accountable. The craft — the least-privilege
instinct, "why can't this reach that," reading a failure, weighing cost against
reliability — is still yours. AI just removes the months of rote lookup between
*having* that judgment and *applying* it to a platform you've never touched.

That is the self-cultivation: keep sharpening the judgment; let the machine carry the
lookup.
