# Lab — the estate that passed the permission lab is the one that fails this one

**Goal:** show a governance failure that contains no mistake. Nothing is
misconfigured, no policy is broken, no review would flag anything, and three years
later a private conversation is readable by three times as many people — including
someone it was about, who was not in the room.

**You'll practise:** the half of
[build-out step 12](../../../build-out/12-meeting-rooms-av-and-uc.md) that *can* be
made runnable — where recordings and transcripts land, who can read them, and for
how long. Step 12 is the one step in the series where the answer to "how much of
this is AI" is *substantially*, and this is what that changes.

## Where this sits, and why it is not lab 07 again

[`permission-sprawl`](../permission-sprawl/) asks **who can see this**. That is a
question about an instant, and it answers it well. Its recommendation — share to
groups, never to individuals, no open links — is followed exactly here.

This lab asks the two questions an instant cannot hold:

- who can see it over the artefact's **lifetime**, as a correct group grows
- is what they are reading still **checkable** against anything

**Doing it the way lab 07 recommends is what makes this happen.** Group sharing is
correct, and a correct group grows. There is no version of this failure that a
better ACL prevents.

## Why this lab is pure-local

Two clocks and a set. Group membership advances, retention expires, and the
readership is the union of everyone who was ever in the group — none of which needs
a suite, a tenant, credentials or `pip install`. Python stdlib, and CI can run it.

## Run it

```bash
python3 cross-cutting/labs/transcript-retention/retention_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Day 0 is correct.** Transcript shared to `group:project-atlas`, zero individual
   grants, zero open links. There is no misconfiguration anywhere in this fixture.
2. **The readership grows and nobody grants anything.** Six people were in the room;
   **21** have been able to read what was said in it, across **0** grants. The group
   today has **18** members — fewer than the 21 who have held access, because
   leavers do not un-read. A membership list is a snapshot of a set that only ever
   accumulated.
3. **The review passes. Every time. Truthfully.** Four access reviews across three
   years, four clean results, none of them wrong. A control that is correct at every
   instant it is evaluated can still be wrong about the interval between them, and
   an access review has no syntax for an interval.
4. **The source expires before the thing derived from it.** The recording carries a
   30-day platform default; the transcript and summary carry none. The transcript
   can be *read* on 1096 of the days modelled and *checked* on 31 of them — **3%**.
   The expensive artefact expires on a default and the cheap one does not, so the
   record that could settle an attribution is the one that goes first.
5. **The summary is wrong, quietly.** One line said by `mei` is attributed to
   `sofia` — an ordinary diarisation error. It was checkable for thirty days. It is
   now the account of what was said.
6. **Who is reading it now.** 15 people who were not in the room, one of whom is
   `priya` — named in it, discussed in the third person, who joined the project on
   day **700** through ordinary onboarding. She can read a conversation about
   herself, including one line attributed to the wrong colleague. The consent that
   covered the recording covered six people in a room three years earlier.

## Verify (don't take the script's word for it)

```bash
python3 .../retention_drill.py --break-it   # exit 1
```

`--break-it` governs by point-in-time access review — the control every
organisation actually runs. **It is not wrong.** It reads a correct state
correctly and returns the right answer every time it is asked.

Four assertions break, and the failure messages are the point: the regime cannot
see the drift, cannot notice that the source expired, and cannot name `priya`. Not
because it answers those questions incorrectly — because **it has no question whose
answer is any of them.**

To go further, give the transcript a retention of 365 days by setting
`TRANSCRIPT_RETENTION = 365`. Cumulative readership falls 21 → **11**, the
`no_expiry` and `unverifiable` findings disappear, and `priya` never gains access
at all — she joins on day 700 and the document stopped existing on day 365.

The drill exits `1` with **six** broken assertions, which is correct and worth
sitting with: most of what it asserts is an assertion *about* unbounded retention,
so setting a retention does not shrink the failure, it deletes the thing being
measured. One number, set once, at the point the recording button is pressed.

## The point

**The missing control is an expiry, not a permission.** If the only question you
ask about a transcript is who can see it, you will keep getting a correct answer
while the exposure grows.

Three things to carry out:

- **Every recording is a decision about the next three years**, taken by whoever
  clicked the button, usually without knowing that is what it was. The place to
  set retention is the platform default, before the first meeting, not the incident.
- **Ask for cumulative readership, not current membership.** "Who can see this" has
  a smaller and more comforting answer than "who has been able to see this", and
  the second one is the one a person in the transcript would ask.
- **Check the retention of a derived artefact against its source.** Summaries,
  transcripts and notes routinely outlive the recording they came from, which means
  the authoritative version is the one nobody can verify.

## Teardown

None. The drill holds everything in memory and writes nothing.
