---
kind: questions
axis: meta
themes: [endpoint]
platforms: []
summary: "Questions asked of this repo about the endpoint estate — provisioning across three operating systems, what MDM actually manages, and where a disk recovery key is kept."
---
# Questions · Endpoint

> The index, the status legend and the out-of-scope reasoning live one level up in
> [`docs/questions.md`](../questions.md).

| # | Question | Status | Where |
|---|---|---|---|
| 1 | How is a provisioning platform designed when it has to cover Windows, macOS **and** Linux? | ⏳ | [`endpoint/provisioning.md`](../../endpoint/README.md) — 🔨, the deepest claim in the repo and the one with least written behind it |
| 2 | What does an MDM actually manage, and how do the estates differ in practice? | ⏳ | `endpoint/management.md` — **as signatures, not a recommendation**: Jamf and Workspace ONE are 🔨, Intune/Autopilot/ConfigMgr are 🧭 and [`endpoint/`](../../endpoint/README.md) already says so |
| 3 | Where are full-disk encryption recovery keys stored, and who is allowed to retrieve one? | ⏳ | `endpoint/encryption-and-keys.md` — [step 08](../../build-out/08-endpoint-security-and-patching.md) calls escrow *the actual work* and [`endpoint/`](../../endpoint/README.md) calls it *key escrow, recovery-key custody, and a process*. **Named three times, shown zero** |
| 4 | What is the blast radius of a policy before you run it on three thousand machines? | ⏳ | the endpoint lab — currently a 🚧 spec that cannot be built as written, because it needs a live MDM and every lab here is pure-local |
