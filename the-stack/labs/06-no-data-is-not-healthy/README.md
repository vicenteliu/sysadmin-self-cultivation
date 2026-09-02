---
kind: lab
axis: the-stack
themes: []
platforms: []
summary: "The outage that produces silence instead of a page. Green and silent are the same colour on every dashboard ever built, and only one kind of alert can tell them apart."
---
# Lab 06 — no data is not healthy

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/the-stack/labs/06-no-data-is-not-healthy/README.md)

> **Inputs:** none · **Outputs:** who was paged, when, and by what · **Risk:** none —
> no services, no exporters, no credentials · **Root:** not needed

**Goal:** make tangible the failure [chapter 06](../../06-observability.md) warns about
and that no dashboard is shaped to show — **the outage that produces silence instead of
a page.**

Every alert in a normal stack is a predicate over data that arrived. That is a sound
design with exactly one blind spot:

```
a threshold alert   fires when a number crosses a line
no data             is not a number, so it crosses nothing
a monitor inside    the failure domain it watches stops sending at the same
                    instant its target stops serving
```

**You'll practise:** applying [chapter 01](../../01-physical.md)'s placement rule to the
thing that tells you about chapter 01, and alerting on absence rather than on values.

## Why this lab is pure-local

The chapter's guided run stands up Prometheus, Grafana and an OTel trace, defines an
SLO and blows the error budget. Do that — it reaches real cardinality and a real bill,
which no model does. But the finding underneath it is a question about *which failure
domain the monitor is in*, and you cannot cut power to a rack in a trial account.

Three monitors, one hour, and a rack that loses power at minute 12. No services, no
exporters, no credentials, no `pip install`. Python stdlib, and CI can run it.

## Run it

```bash
python3 the-stack/labs/06-no-data-is-not-healthy/silence_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **Minute 12, and what each monitor reports at minute 20.** The in-rack monitor
   stopped sending at the instant its target died — it shared the failure domain it was
   watching. The off-rack one is reporting the errors users are actually getting.

2. **Who got paged.** The in-rack error alert **never fired**: it is a predicate over
   data, and no data arrived. The off-rack symptom alert paged at minute 14, which is
   the minute users noticed.

3. **The cause alert, which is the one most estates actually have.** CPU was 0.35 right
   up to the power cut and unreported after it. **There is no threshold value that
   would have caught this outage** — tuning it is not the fix and never was.

4. **The only control that catches an in-domain monitor.** A staleness alert — a
   dead-man's switch — pages at minute 15 on the *absence* of samples. Every other
   alert in the file asks a question about a number; this one asks whether there was a
   number, which is why it is the only one that survives its own subject dying.

5. **What the dashboard shows at minute 20, and why it is not lying.** Two green
   panels, each displaying the last thing it was told, nine minutes stale. The users
   have been getting errors for six minutes. **Green and silent are the same colour.**

## Verify (don't take the script's word for it)

```bash
python3 silence_drill.py --break-it no-data-is-green      # exit 1
python3 silence_drill.py --break-it cause-alerts-suffice  # exit 1
```

`no-data-is-green` treats silence as health — which is what a UI does — and the
staleness assertion is the one that breaks, because it is the only assertion that ever
depended on the distinction.

`cause-alerts-suffice` makes every monitor measure something that does not move when
users suffer, which is the estate that alerts on resources and calls it observability.
The off-rack alert stops paging, and nothing else in the run changes: the outage still
happens, the dashboards still look the same, and nobody is told.

To go further, move `errors-in-rack` to `rack-b` and re-run. It pages at minute 14 and
the staleness alert never fires — the placement change makes the dead-man's switch
redundant *for that monitor*, which is the right order to fix these in.

## The point

**The worst hour you will have is the one that produces no data at all.**

Two things to carry out:

- **Put the monitor in a different failure domain from the thing it watches.** This is
  chapter 01's anti-affinity rule, applied to the system whose job is to tell you about
  chapter 01, and it is skipped almost universally because a monitor feels like
  infrastructure rather than a workload.
- **Alert on the absence of data.** A staleness alert is unglamorous, fires rarely, and
  is the only predicate in the estate whose input is not a value. Every other alert you
  own has already agreed to be silent about this.

And the third, which is the one to say out loud in a review: *a green dashboard is a
claim about the last sample, not about now.* Ask any panel when it last heard anything.

## Teardown

None. The drill holds everything in memory and writes nothing.
