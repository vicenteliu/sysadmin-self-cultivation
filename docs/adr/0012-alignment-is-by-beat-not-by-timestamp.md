---
kind: adr
axis: meta
themes: []
platforms: []
summary: "The floor has to move in step with the narration, and the obvious way to do that is timestamps. Timestamps cannot work here, because there is no single recording to time against."
---
# Alignment is by beat, not by timestamp

The [floor](0011-the-floor-renders-the-reference-office-and-may-not-compute-it.md) advances
as the narration advances: the camera walks with the protagonist, the zoom changes
register, a prop lights up as it is named. Something has to say *when*.

Every video and podcast tool answers this with timestamps, and timestamps cannot work
here. [ADR-0009](0009-the-walkthrough-ships-its-script-not-its-audio.md) put no audio in
the tree, which means there is no single recording to time against — there are as many
timelines as there are readers. A listener generating speech with their own credentials
gets their engine's voice, their speaking rate and their language; the author's published
episode is a third timeline again. A timestamp is correct for exactly one of them.

## Decision

**A walkthrough is physically divided into beats, and the floor is cued by beat.**

One beat is **one paragraph, one TTS call, one audio segment, one floor state.** A player
advances the floor when a segment ends. No duration is recorded anywhere, so no duration
can be wrong.

Beats are delimited in the Markdown by an HTML comment carrying a **stable id**:

```markdown
<!-- beat: coverage-not-capacity -->
```

GitHub does not render it, the viewer does not render it, and a speech engine never
receives it — so the visible file stays nothing but the words that get spoken, as ADR-0009
requires. The floor state and prop bindings for each beat live in the sibling
`walkthrough/<episode>.floor.json`, keyed by that id.

**The id is a name, never an ordinal.** `coverage-not-capacity`, not `beat-17`. Inserting
a paragraph into a hundred-and-forty-beat script must not silently shift every cue after
it by one — and it would be silent, because a floor pointing at the wrong beat looks
exactly like a floor pointing at the right one.

## Considered options

- **Timestamps against the author's published episode, with a scroll-driven fallback for
  everyone else.** Rejected because it makes the author's recording the privileged
  artifact and every self-generated one second-class — in a repo that just decided not to
  ship the recording at all. It also puts the timing data in the tree while the audio it
  describes is not, which is the wrong half to keep.

- **Speech-boundary events from the browser's speech API.** Attractive: word-level
  synchronisation for free. Rejected because it binds the floor to one specific synthesis
  path. A reader generating audio files from a hosted TTS API — the case the walkthrough is
  written for — emits no boundary events at all.

- **Ordinal beat numbers.** Simpler to author and simpler to read. Rejected on the failure
  mode above: the drift is caused by an ordinary edit, produces no error, and is invisible
  until someone watches the whole episode and notices the floor is one beat behind.

- **No floor cues; let the reader drive.** Rejected because it turns the narration into a
  menu. The walkthrough's shape is a line you do not skip, which is what separates a story
  from a reference.

## Consequences

- **Any engine, any voice, any language works, and none of them needs configuring.** This
  is the whole point: the alignment unit is *which beat*, and every reader agrees on that
  regardless of how long their audio takes to say it.
- **One beat is the smallest thing the floor can react to.** Word-level effects — a prop
  lighting on the exact syllable that names it — are out of reach, and they stay out of
  reach. That is a real loss, accepted for the portability above.
- **Beat ids are an interface, and renaming one is a breaking change.** The `.floor.json`
  refers to them, and after publication so does a recording nobody can edit. Renames belong
  with errata, not with tidying.
- **The publish freeze has a natural unit.** Because segments are per-beat, the author's
  published episode is the same segments concatenated — so a correction in one beat is one
  segment to regenerate, not a whole recording. It does not make a published episode
  editable, but it makes the next one cheap.
