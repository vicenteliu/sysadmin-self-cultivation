# Agent Skills

This repo ships with five [Claude Code / Agent Skills](https://docs.claude.com) —
`SKILL.md` workflows that package the repo's methodology so an AI agent can *apply*
it, not just read it. They're the repo's ideas turned into invokable tools.

| Skill | What it does | Invoke when |
| --- | --- | --- |
| [`platform-ramp`](platform-ramp/SKILL.md) | Ramp onto any platform fast + honestly: seven-surface map → skill map → AI-ramp method → ✋/🧗 ledger | "help me ramp onto X", "map X onto what I know", "I've never touched X" |
| [`honesty-audit`](honesty-audit/SKILL.md) | Classify every technical claim ✋ hands-on / 🧗 verified ramp / ❌ overclaim, with honest reframes | "is this honest", "audit my resume for overclaims", "am I bluffing" |
| [`author-module`](author-module/SKILL.md) | Write a new module (platform / cross-cutting / companion / **support note** / lab) matching the repo's voice, structure, ✋/🧗 markers, research grounding, and validated mermaid | "add a note on X", "write a support note for X", "keep it consistent with the repo" |
| [`runnable-lab`](runnable-lab/SKILL.md) | Turn a concept into a pure-local, self-verifying lab (exit 0 = lessons held), like the repo's drills | "make this a runnable lab", "prove X in code" |
| [`mirror-zh`](mirror-zh/SKILL.md) | Mirror an English doc into a Chinese translation under `docs/zh/` — path-mirrored, terms kept in English, bidirectional 🌐 switcher, links back to canonical | "做个中文镜像", "mirror this to Chinese", "put it in docs/zh" |

Each skill is grounded in the repo's canonical files — the
[operating model](../../00-the-operating-model.md), [`WHY.md`](../../WHY.md)'s honesty
discipline, and the [AWS worked example](../../platforms/aws/) — so what they produce
lands consistent with everything else here.

> The through-line: the repo teaches a **transferable model + a fast, honest ramp**.
> `platform-ramp` *is* that ramp; `honesty-audit` enforces the honesty; `author-module`,
> `runnable-lab`, and `mirror-zh` keep the repo growing in the same voice — with runnable
> evidence and a Chinese mirror.
