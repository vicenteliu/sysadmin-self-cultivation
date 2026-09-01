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
| 1 | How is a provisioning platform designed when it has to cover Windows, macOS **and** Linux? | ✅ | [`endpoint/provisioning.md`](../../endpoint/provisioning.md) — the two eras, what the three systems genuinely share, and hardware diversity as the constraint |
| 2 | What does an MDM actually manage, and how do the estates differ in practice? | ✅ | [`endpoint/management.md`](../../endpoint/management.md) — the rented management surface, and an Apple estate's shape read **as signatures, not a recommendation** |
| 3 | Where are full-disk encryption recovery keys stored, and who is allowed to retrieve one? | ✅ | [`endpoint/encryption-and-keys.md`](../../endpoint/encryption-and-keys.md) — escrow concentrates the risk it removes, and the keys outlive the machines |
| 4 | What is the blast radius of a policy before you run it on three thousand machines? | ⏳ | the endpoint lab — currently a 🚧 spec that cannot be built as written, because it needs a live MDM and every lab here is pure-local |
