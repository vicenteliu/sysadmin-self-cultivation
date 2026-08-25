---
name: interview-drill
description: Run an interview drill against this repo's interview maps — ask a question, listen to the answer, and follow up the way an interviewer does, then judge whether the answer stayed on evidence or drifted into the fluent version. Marks 🔨 answers that arrived without a specific, and 🧭 answers that quietly claimed depth. Use when the user says "quiz me", "interview me", "practise interview questions", "drill me on networking/identity", "面试模拟", or asks whether an answer would hold up.
created: 2026-08-25
owner: Vicente Liu
---

# Skill: interview-drill

Written answers are material. Recalling one under a follow-up is a different skill,
and it is the one that decides interviews. This drill is the loop for the second.

**The premise:** a memorised answer fails on the second question. So the drill never
scores the first answer — it scores what survives the follow-up.

## Where the material lives

- [`cross-cutting/interview/networking.md`](../../../cross-cutting/interview/networking.md) — 21 questions, 11 sections
- [`cross-cutting/interview/identity.md`](../../../cross-cutting/interview/identity.md) — 19 questions, 10 sections
- The paired [`skills-maps/`](../../../cross-cutting/skills-maps/README.md) — every
  section maps one-to-one, so a weak answer points at the exact capability behind it.
- [`docs/index.json`](../../../docs/index.json) — search by `themes`, `platforms` or
  `marker` when the user asks for a topic rather than a file.

**Read the section's marker before asking.** It decides what a good answer looks like,
and judging a 🧭 answer by 🔨 standards teaches exactly the bluff this repo exists to
prevent.

## The loop

### 1 — Pick, and say why

Draw from the section the user named, or — if they did not name one — from a section
whose answers carry `⏳`, since those are the questions with no written answer behind
them. Ask **one** question, exactly as written. Do not preview what it probes.

### 2 — Listen, then follow up once at minimum

The follow-up is the skill. Pick it from what the answer did:

- **Named a mechanism** → ask for the time they hit it. *"When did that happen to you?"*
- **Named an incident** → ask for the number, the sequence, or the alternative.
  *"How did you know it was that and not the other three?"*
- **Was fluent and general** → narrow hard. *"On which platform? What was the command?"*
- **Said "it depends"** → make it choose. *"Depends on what, and what did you pick?"*

Fluency without specificity is the thing to probe, every time. It is also what a
model-generated answer sounds like, which is worth saying out loud when it happens.

### 3 — Judge against the marker, not against the answer

| Section | A good answer | The failure to name |
| --- | --- | --- |
| **🔨** | A real, anonymised specific — a decision, a sequence, a number | Mechanism recited with no incident behind it. The marker is unsupported. |
| **🧭** | The boundary stated plainly: what is mapped, what transfers, where it stops | Drift into depth. A 🧭 that starts sounding 🔨 under pressure is the overclaim. |

Both failures are the same failure at different markers: **the answer claimed more
than the marker does.** Say so directly, with the sentence that overreached quoted
back.

For a 🧭, remember the framing the repo argues for and
[`honesty-audit`](../honesty-audit/SKILL.md) states: a ramp declared plainly reads as
judgement. *"I have not run this in production; here is what I verified and here is
what transfers"* is a strong answer, not a concession. Say so when the user
apologises for a 🧭.

### 4 — Check the anonymisation, out loud

Every work example is subject to
[ADR-0004](../../../docs/adr/0004-interview-answers-are-evidence-for-a-marker.md).
If an answer named a company, a region, or a date that aligns with a tenure, flag it
in the moment — the drill is where the habit gets built, and the compositional test
applies: not *"is this detail sensitive"* but *"does it narrow the field, given the
rest."*

### 5 — Write the gap down

When an answer arrives that is better than what is on the page — and it usually does,
because saying it is easier than writing it — **offer to write it into the file**,
replacing the `⏳`. That is the whole point of the loop: the drill is how the
placeholders get filled.

When an answer does not arrive at all, leave the `⏳` and say which capability it sits
under in the skill map. An unanswerable question is a study target, not a failure.

## Modes

- **Default — one question, drilled.** Ask, follow up, judge, offer to write.
- **`sweep`** — walk a whole section, one question at a time, and finish with which
  answers held and which were fluent.
- **`gaps`** — ask only questions whose answers carry `⏳`. The highest-yield mode,
  and the one to suggest when the user has no preference.
- **`cold`** — do not reveal the section, so the marker is not a hint. Closest to a
  real interview, and the right mode once a section has been swept before.

## What this skill does not do

**It does not soften.** An interviewer will not, and a drill that grades kindly
teaches a confidence the interview then removes.

**It does not invent examples.** If the user has no incident for a 🔨, the answer is
`⏳` and a study target — never a plausible story offered to fill the gap. Composing
one here would put a fabrication into the file that the markers exist to keep out,
which is the one failure this repo cannot tolerate from its own tooling.
