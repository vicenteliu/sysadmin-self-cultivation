---
kind: companion
axis: endpoint
themes: [endpoint, security]
platforms: []
marker: "🔨"
summary: "Three places in this repo call recovery-key escrow the actual work and none of them shows it. This is it — why escrow moves the risk rather than removing it, the circular dependency at the centre of every design, and the keys that outlive the machines they unlocked."
---
# Full-disk encryption at scale, and the keys

> 🌐 **Languages:** English (default) · [中文](../docs/zh/endpoint/encryption-and-keys.md)

> Turning encryption on is a setting. **Everything difficult about it happens
> afterwards**, and this repo has said so three times without ever showing the work:
> [`build-out/08`](../build-out/08-endpoint-security-and-patching.md) calls the recovery
> key escrow *the actual work*, and the [README](README.md) calls encryption at fleet
> volume *key escrow, recovery-key custody, and a process*. This note is the process.

## The reframe that decides everything else

Before escrow, an encrypted laptop's data is protected by **one person's credential**.
The company cannot read it. Neither can the company when that person forgets the
password, leaves abruptly, or is hit by a bus — which is why no organisation ships
encryption without escrow.

After escrow, the data is protected by **whoever can retrieve the key**.

**That is not a smaller risk. It is a different one, and it is concentrated.** A hundred
laptops each protected by a hundred separate passwords became a hundred laptops
protected by one access-control decision. The threat model moved from *someone steals a
laptop* to *someone reaches the escrow*, and the second is the kind of thing that gets
you the whole fleet at once rather than one machine.

Say it plainly, because it is the sentence that should govern the design: **encryption
with escrow makes disk encryption an access-control problem wearing a cryptography
costume.** Every subsequent question in this note follows from that.

## The mechanism is the least interesting part

Each of the three platforms has a full-volume encryption facility that is on by default
or one policy away, integrates with the platform's management protocol, and can hand a
recovery secret to that protocol at enablement time. As **signatures**, you will meet
one per platform and they are not interchangeable in tooling — but the design questions
below are identical across all three, which is why this note spends no further time on
them.

What *is* worth knowing per platform is where the recovery secret can legally live,
because that differs and it constrains the answer to the next section.

## The five questions, in the order they bite

**1. Where does the key go, and is that the same system that manages the device?**

The convenient answer is the MDM, because it is already there and enablement can escrow
in one step. The consequence of the convenient answer is that **MDM administration
becomes equivalent to physical access to every machine in the estate.** That may be an
acceptable trade — it often is — but it has to be a decision somebody made, and the
people holding MDM admin have to be told that is what they are holding.

The alternative is a separate secret store, which costs an integration and a second
system to keep alive, and buys a genuine separation: the person who can push a policy
is not automatically the person who can read a disk.

**2. Who can retrieve one, and what has to be true before they can?**

Not *who has the permission* — **what has to happen**. A named requester, a verified
identity for the machine's holder, a reason, and a record. The failure mode here is not
malice; it is a help-desk agent retrieving a key over chat for someone who sounded
right, forty times a year, with nothing written down.

[`build-out/08`](../build-out/08-endpoint-security-and-patching.md) states the test and
it is a good one: **a key can actually be retrieved by someone who is not you.** A
process only you can execute is a single point of failure with a person in it. A process
anybody can execute is not a control.

**3. Is retrieval logged, and does anyone read the log?**

Retrieval is the highest-signal event this whole system produces and it is almost never
alerted on. In the reference office it should happen a handful of times a year. **A
month with nine of them is either an incident or a broken password-reset path**, and
both are worth knowing on the day rather than at audit.

**4. What happens to the key after it has been used?**

It has now been read by a human, possibly transcribed, possibly pasted into a chat.
**A recovery key that has been disclosed and not rotated is a permanent credential held
by whoever last saw it.** Rotation after use is the single most commonly skipped step in
this entire design, and it is skipped because nothing breaks when you skip it.

**5. What happens to the key when the machine is retired?**

This one is the finding, and it gets its own section.

## The keys outlive the machines

[The reference office](../the-reference-office.md#parameters) buys about **two hundred
and twenty machines across one lease to hold about a hundred and fifteen at a time**,
retiring roughly thirty-eight a year.

Each machine's escrow record is created at enablement. **Almost nothing deletes it.**
Retirement is a procurement and asset event; the escrow is a security system; the two
are rarely wired together, and no failure occurs when they are not. So the escrow
accumulates: after five years it holds keys for a hundred-odd machines that no longer
exist, alongside the hundred-odd that do, with nothing in the record distinguishing
them.

That is [`asset-reconciliation`](../cross-cutting/labs/asset-reconciliation/)'s problem
applied to secrets — two systems that should agree, drifting, with no event forcing a
comparison. And it is the same shape as
[the reference office's non-human identities](../the-reference-office.md#why-these-numbers):
**a credential with no last day.** There are about forty of those before you count
recovery keys. Counting them, there are a hundred and forty.

The remediation is unglamorous and it is a wiring job: **retirement in the asset
register must delete the escrow record**, and the count of escrow records should be
reconcilable against the count of live machines. If those two numbers cannot be compared
in one query, that is the finding.

## The circular dependency

The recovery key exists for the case where **the user cannot authenticate**.

It is stored in a system you reach **by authenticating**.

Most of the time those are different authentications and the circle does not close. But
the failure modes where you most need a recovery key are disproportionately the ones
where identity itself is the problem: a directory outage, a conditional-access policy
that locked everyone out, an account disabled in error, a tenant-wide incident. That is
not hypothetical — it is
[`m365-conditional-access-lockout`](../cross-cutting/labs/m365-conditional-access-lockout/),
one layer down.

**The design answer is the same as identity's:** the two break-glass accounts
[`build-out/03`](../build-out/03-identity.md) asks for, excluded from conditional access,
**with credentials physically retrievable by someone who is not you.** If escrow lives
behind the corporate identity, break-glass has to reach it, and that path has to be
tested on a date, by a person, with the result written down — the same standard
[`build-out/09`](../build-out/09-backup-and-the-restore-drill.md) holds a restore to,
and for exactly the same reason: an untested recovery path is a belief.

## What this looks like in the reference office

A hundred to a hundred and thirty machines, [about sixty-two handovers a
year](../the-reference-office.md#parameters), a help desk with a fifty-hour window and
no dedicated security function.

- **Escrow in the MDM is the right call at this size**, because the alternative costs an
  integration and a second system that one part-time administrator would own. The price
  of that call is that MDM admin equals fleet-wide data access, and the correct response
  is to keep that list to about three people and say out loud why it is short.
- **Retrieval belongs to a named process, not to a role.** At forty joiner-and-leaver
  events a year plus refresh, the help desk will meet this often enough for a habit to
  form, and the habit is what you are designing.
- **The escrow-to-register reconciliation is a quarterly query, not a project.** Two
  counts and a difference.

## Honest boundaries

🔨 **Hands-on.** Full-disk encryption enrolled at scale as part of a multi-OS
provisioning platform — enablement, escrow, recovery-key custody and the process around
retrieval, across a fleet where retirement volume was continuous rather than
occasional. The keys-outlive-the-machines finding is operational, not theoretical.

🧭 **The cryptography itself is out of altitude here and deliberately unwritten** — how a
volume key is wrapped, what the recovery secret actually is per platform, and the
security proofs underneath. This repo's stated altitude is *decisions somebody has to
make and own*, and every decision in this note survives being wrong about the internals.

**Not claimed:** key-management systems and HSM operations as a discipline, or
regulatory positions on key custody in any jurisdiction.

## Read deeper

- [`build-out/08`](../build-out/08-endpoint-security-and-patching.md) — the step that
  asks for escrow and for the retrieval test
- [`build-out/03`](../build-out/03-identity.md) — break-glass, which the circular
  dependency above depends on
- [`endpoint/management.md`](management.md) — the MDM that is probably holding these keys
- [`cross-cutting/labs/m365-conditional-access-lockout/`](../cross-cutting/labs/m365-conditional-access-lockout/)
  — the identity failure this design has to survive
- [`the reference office`](../the-reference-office.md#parameters) — 220 machines across a
  lease, and the credentials with no last day
