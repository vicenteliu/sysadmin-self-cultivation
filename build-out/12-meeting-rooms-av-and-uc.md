# 12 · Meeting rooms, AV and UC — the orphan nobody owns

> 🧗 **verified ramp.** Room AV integration is not this author's hands-on ground;
> the network, identity and support surfaces underneath it are.
> **Before:** 02 the building · 05 network. **After:** 13 the help desk

Every step so far has had an owner by convention. This one does not. AV is bought
by facilities or by whoever ran the office fit-out, it is installed by an
integrator, and then it breaks — and the person who gets called is IT, who was not
consulted, has no admin access, and has never seen the equipment before.

**Deciding who owns it is the deliverable.** The technology is secondary.

## What this step produces

- A named owner for room AV, in writing, before the first room is commissioned.
- Admin credentials to the room systems, held by whoever will be called.
- Rooms on their own network segment with the reasoning from step 05 applied — these
  are appliances that update on the vendor's schedule, not yours.
- A resource calendar per room that people actually book, and one meeting platform
  chosen rather than three tolerated.
- A support path that assumes the person reporting the problem is standing in front
  of eleven colleagues and a client.

## Questions to ask first

- **Who owns this?** If the answer is unclear, IT owns it in practice and should
  either accept that with the budget attached, or force the decision now.
- **Does IT get admin on the room systems?** An integrator who keeps the credentials
  is a support contract, not a handover. Find out before the invoice is paid.
- **What is the one meeting platform?** Rooms that must join anything are meaningfully
  more expensive and more fragile. Standardising is a business decision with a real
  cost either way.
- **How do these devices authenticate to the network?** They are usually poor
  candidates for the same method as laptops, which is exactly why step 05 asked.
- **What is the failure people will actually hit?** It is not the codec. It is a cable,
  a source that will not switch, or a room account whose password expired.
- **Who is called when a board meeting cannot start?** That is a response-time
  commitment, and it should be agreed rather than discovered.

## 2015 → today

| | 2015 | today |
|---|---|---|
| The room | a projector, a phone in the middle of the table, an HDMI cable | a video bar, a touch controller, a room account in your directory |
| Who owned it | facilities, mostly | contested — which is the whole problem |
| The meeting | people in the room, one caller dialling in | **hybrid by default**; the remote participants are the majority |
| Failure impact | inconvenient | the meeting does not happen |
| Notes | someone volunteered | generated automatically, and read by people who were not there |

**How much of that is AI: substantially, and this is the one step in the series
where that is true.** Live transcription, speaker attribution, automatic summaries
and action-item extraction are genuinely model-driven, genuinely new in the last few
years, and genuinely in daily use. Nothing about them is SaaS-ification with a new
label.

It is worth saying plainly precisely because every other step in this series has
answered "almost none". A series that always gives the same answer is not measuring
anything. Here the answer is different, and it changes what IT has to think about:

- **Consent and recording.** Who is told, what is retained, for how long, and which
  jurisdictions apply. This becomes a compliance question in step 14, not an AV one.
- **Where the transcript lives.** It is a document containing everything said in a
  private meeting, and step 07's permission model applies to it — usually without
  anyone having thought about it.
- **Accuracy.** Attribution errors in a summary read as authoritative. The failure is
  quiet and the artefact is durable.

## Read deeper

- [`the-stack/02-network.md`](../the-stack/02-network.md) — segmentation for devices
  you do not control
- [`cross-cutting/saas-admin.md`](../cross-cutting/saas-admin.md) — room accounts and
  resource calendars are directory objects
- [`cross-cutting/itsm-and-assets.md`](../cross-cutting/itsm-and-assets.md) — room
  systems are assets, and they are the ones most often missing from the inventory

## Do it

🔴 **Gap, and partly a boundary.** Nothing here is runnable and little of it could
be — commissioning a room is physical work with a vendor. What *could* exist is the
governance side: where recordings and transcripts land, and who can read them.
Recorded in [`GAPS.md`](./GAPS.md).

## Getting it backwards

**Letting the integrator keep the credentials.** The rooms work at handover. The
first change request goes to a company with a ticket queue and a rate card, and it
is discovered during a week when a meeting has to happen.

**Rooms on the staff network.** They are appliances with vendor firmware, updated on
the vendor's schedule, and they sit in a room anyone can walk into. Step 05 gave you
the pattern; this is the device it was for.

**Buying rooms before choosing a platform.** Every room becomes a compatibility
project, and the cost lands as recurring support rather than as a line item anyone
reviews.

**Assuming the transcript is nobody's problem.** It is a written record of a private
conversation, stored in the collaboration suite, inheriting whatever sharing default
step 07 set. Nobody decides this; everyone assumes someone did.
