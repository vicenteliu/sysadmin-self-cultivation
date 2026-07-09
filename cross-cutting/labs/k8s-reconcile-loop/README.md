# Lab — pods are cattle, and a controller reconciles forever

**Goal:** feel the one thing a **Linux/systemd/Docker sysadmin gets wrong about
Kubernetes** — that you don't manage processes, you declare desired state, and a
**controller** runs a reconciliation loop that continuously drives *actual → desired*.
It's the runtime twin of the [Terraform state lesson](../../terraform-support.md):
declarative config + a converging engine — one at provision time, one *forever* at run
time.

```
desired    the Deployment spec: replicas + pod template (you write this)
actual     the set of Pods that exist right now
reconcile  the controller closes the gap, every tick, forever
```

What it drills — six lessons that fall out of that one model:
1. **Delete a Pod → it comes back.** The controller recreates it (self-healing); you
   can't "just delete" a pod — change the desired state.
2. **Hand-fix a Pod → the fix vanishes.** `kubectl exec` in and patch a running pod, and
   the next reconcile replaces it from the template. Cattle, not pets — *fix the spec.*
3. **Scale desired → the count converges** (3 → 5 → 2). You edit the spec, not the pods.
4. **Bad image → CrashLoopBackOff.** The controller keeps restarting a crashing pod, but
   restarting a bad spec loops forever — *fix the template*, don't restart.
5. **Change the template → rolling replace.** Change the desired image and the controller
   rolls every pod; you change the spec, controllers roll.
6. **Readiness failing → pulled from endpoints.** A Running-but-not-Ready pod is removed
   from the Service's endpoints — *"the service is down but the pod is Running"* = check
   endpoints.

## Why local

No cluster, no `kubectl`, no cloud. The drill is a ~200-line model of a Deployment
controller's reconcile loop — desired replicas + template, the recreate/scale/roll
decisions, and the readiness→endpoints gate — so the *logic* is what you inspect, not a
screen of YAML. Runs anywhere Python does, and in CI.

## Run

```bash
python3 reconcile_drill.py
```

## What you'll see

Six narrated steps, each with an `OK`/`XX`: a deleted pod recreated; a hand-fix
vanishing on replacement; the count converging on scale; a broken image looping in
CrashLoopBackOff (then fixed by changing the template, not restarting); a template change
rolling every pod; and a not-Ready pod pulled from the Service endpoints. Ends with a PASS
verdict and `exit 0`.

## Verify (the important part)

Exit `0` = every lesson held; it doubles as a CI check. Now **break the model on
purpose** — two independent sabotage vectors:

```bash
python3 reconcile_drill.py --sabotage no-reconcile        # controller stops reconciling -> a deleted pod stays dead -> step 1 FAILS, exit 1
python3 reconcile_drill.py --sabotage ready-ignores-probe # endpoints ignore readiness -> a broken pod still gets traffic -> step 6 FAILS, exit 1
```

If the controller can be asleep and pods still self-heal, the reconcile loop wasn't doing
anything; if a not-Ready pod still receives traffic, the readiness gate wasn't
load-bearing. The failures are the proof the model matters.

## The point

Two sysadmin reflexes get corrected here at once. First, **"the process is the unit, and
I manage it"** — in Kubernetes the *Deployment/spec* is the unit and the pod is
disposable; deleting or editing a pod is futile because a controller reconciles it back.
Second, **"SSH in and fix it"** — a fix made inside a running pod dies when the pod is
replaced. The discipline: declare desired state, change the *spec* not the pod, and when
"the service is down" check the **endpoints** (readiness → selector). Pods are cattle. See
the [Kubernetes support note](../../kubernetes-support.md) for the full ticket catalog and
[`kubernetes.md`](../../kubernetes.md) for the object model.

## Teardown

None — it's a single self-contained script. Delete the folder to remove it.
