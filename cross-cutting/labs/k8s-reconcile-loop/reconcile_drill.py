#!/usr/bin/env python3
"""
Kubernetes drill — pods are cattle, and a controller reconciles forever.

Pure-local, stdlib-only. Models the one thing a Linux/systemd/Docker sysadmin gets
wrong about Kubernetes: you don't manage processes, you declare desired state, and a
CONTROLLER runs a reconciliation loop that continuously drives actual -> desired.
It's the runtime twin of Terraform's state lesson — declarative + a converging engine,
one at provision time, one forever at run time.

    desired   the Deployment spec: replicas + pod template (you write this)
    actual    the set of Pods that exist right now
    reconcile the controller closes the gap, every tick, forever

Six lessons fall out of that one model:
  1. delete a Pod       -> the controller RECREATES it (self-healing; you can't just delete it)
  2. hand-fix a Pod     -> the fix VANISHES on replacement (cattle, not pets — fix the spec)
  3. scale desired      -> the controller converges the count (3 -> 5 -> 2)
  4. bad image          -> CrashLoopBackOff; restarting a bad spec loops forever (fix the template)
  5. change the template-> the controller ROLLS pods to the new template (you change desired, not pods)
  6. readiness failing  -> a Running-but-not-Ready pod is pulled from the Service ENDPOINTS
                           ("the service is down but the pod is Running")

Run clean and every lesson holds -> exit 0 (doubles as a CI check).
Run with --sabotage to break the model and watch the guarantees fall -> exit 1:
  --sabotage no-reconcile      : the controller stops reconciling -> a deleted pod stays dead (step 1)
  --sabotage ready-ignores-probe : endpoints ignore readiness -> a broken pod still gets traffic (step 6)
"""

import argparse
import sys

GOOD_IMAGES = {"app:v1", "app:v2"}          # images that actually run; anything else crashes
_next_id = [0]


def log(msg=""):
    print(msg)


def step(n, title):
    log(f"\n[{n}] {title}")


def healthy(pod):
    """A pod is healthy iff its image is one that runs. A 'broken' image crashes."""
    return pod["template"]["image"] in GOOD_IMAGES


def new_pod(template, ready=True):
    _next_id[0] += 1
    return {"id": _next_id[0], "template": dict(template), "ready": ready}


def endpoints(pods, honor_readiness=True):
    """A Service's endpoints = the Pods it can send traffic to. A Pod must be BOTH
    healthy AND ready. --sabotage ready-ignores-probe drops the readiness gate."""
    if honor_readiness:
        return [p for p in pods if healthy(p) and p["ready"]]
    return [p for p in pods if healthy(p)]   # the sabotage: traffic to not-ready pods


class Deployment:
    """A controller: desired = (replicas, template); reconcile() drives actual -> desired."""
    def __init__(self, replicas, template):
        self.replicas = replicas
        self.template = template

    def reconcile(self, pods, enabled=True):
        if not enabled:
            return pods                       # the controller is asleep (sabotage)
        # keep only pods that match the desired template AND are healthy; the rest get replaced
        pods = [p for p in pods if p["template"] == self.template and healthy(p)]
        while len(pods) > self.replicas:      # scale down
            pods.pop()
        while len(pods) < self.replicas:      # scale up, from the DESIRED template
            pods.append(new_pod(self.template))
        return pods


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage", choices=["no-reconcile", "ready-ignores-probe"],
                    help="break the model: 'no-reconcile' = controller stops reconciling; "
                         "'ready-ignores-probe' = endpoints ignore readiness")
    args = ap.parse_args()
    reconcile_on = args.sabotage != "no-reconcile"
    readiness_on = args.sabotage != "ready-ignores-probe"
    if args.sabotage:
        log(f"  !! SABOTAGE ENABLED: {args.sabotage} !!")

    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"    OK  {ok_msg}")
        else:
            log(f"    XX  {fail_msg}")
            failures.append(fail_msg)

    dep = Deployment(replicas=3, template={"image": "app:v1"})
    pods = [new_pod(dep.template) for _ in range(3)]   # steady state already exists
    ids = lambda ps: sorted(p["id"] for p in ps)
    log(f"Deployment: replicas=3, template=app:v1 -> pods {ids(pods)}")

    # 1. Delete a pod -> the controller recreates it.
    step(1, "kubectl delete pod  -> the controller reconciles")
    victim = pods[0]["id"]
    pods = [p for p in pods if p["id"] != victim]     # you delete one
    log(f"    deleted pod {victim}; pods now {ids(pods)}")
    pods = dep.reconcile(pods, reconcile_on)
    log(f"    after reconcile: {ids(pods)}")
    check(len(pods) == 3 and victim not in ids(pods),
          "the controller RECREATED it (self-healing) — you can't 'just delete' a pod; change desired state",
          "deleting a pod should trigger the controller to recreate it back to replicas=3")

    # 2. Hand-fix a running pod -> the fix vanishes on replacement.
    step(2, "kubectl exec + hand-fix a pod  -> next reconcile")
    pods[0]["template"]["image"] = "app:hotfix-by-hand"   # you SSH in and 'fix' it
    hotfix_id = pods[0]["id"]
    log(f"    hand-patched pod {hotfix_id} to app:hotfix-by-hand")
    pods = dep.reconcile(pods, reconcile_on)
    log(f"    after reconcile: {ids(pods)}")
    check(hotfix_id not in ids(pods) and all(p["template"] == dep.template for p in pods),
          "the hand-fix VANISHED — the pod was replaced from the template (cattle, not pets); fix the spec",
          "a pod hand-edited off-template should be replaced, discarding the manual fix")

    # 3. Scale desired -> the controller converges the count.
    step(3, "Scale the Deployment: 3 -> 5 -> 2")
    dep.replicas = 5; pods = dep.reconcile(pods, reconcile_on)
    up = len(pods)
    dep.replicas = 2; pods = dep.reconcile(pods, reconcile_on)
    down = len(pods)
    log(f"    replicas=5 -> {up} pods; replicas=2 -> {down} pods")
    check(up == 5 and down == 2,
          "changing DESIRED replicas drove the actual count — you edit the spec, not the pods",
          "scaling desired replicas should converge the actual pod count")

    # 4. Bad image -> CrashLoopBackOff; restarting a bad spec loops forever.
    step(4, "Ship a broken image  -> reconcile a few times")
    dep.replicas = 3; dep.template = {"image": "app:broken"}
    for _ in range(3):
        pods = dep.reconcile(pods, reconcile_on)
    live = sum(1 for p in pods if healthy(p))
    log(f"    after 3 reconciles with a broken image: {live} healthy of {len(pods)}")
    check(live == 0,
          "the controller keeps replacing crashed pods but they crash again — CrashLoopBackOff; restart != fix",
          "a broken image should never become healthy just by the controller restarting it")
    dep.template = {"image": "app:v2"}                 # fix the SPEC, not the pod
    pods = dep.reconcile(pods, reconcile_on)
    check(sum(1 for p in pods if healthy(p)) == 3,
          "fixing the template (app:v2) — not restarting — made the Deployment healthy again",
          "fixing the template image should make all pods healthy")

    # 5. Change the template -> rolling replace.
    step(5, "Change the pod template (app:v2 -> app:v1)  -> reconcile")
    before = ids(pods)
    dep.template = {"image": "app:v1"}
    pods = dep.reconcile(pods, reconcile_on)
    log(f"    pods {before} -> {ids(pods)}")
    check(all(p["template"]["image"] == "app:v1" for p in pods) and not set(before) & set(ids(pods)),
          "changing the DESIRED template rolled every pod to the new image — you change the spec, controllers roll",
          "changing the template should replace pods with ones matching the new template")

    # 6. Readiness failing -> pulled from Service endpoints (Running but no traffic).
    step(6, "A pod fails its readiness probe (still Running)  -> Service endpoints")
    pods[0]["ready"] = False                            # readiness probe fails; pod still exists/Running
    eps = endpoints(pods, readiness_on)
    log(f"    pods {ids(pods)} (all Running); Service endpoints {ids(eps)}")
    check(len(pods) == 3 and pods[0]["id"] not in ids(eps),
          "the not-Ready pod is still Running but PULLED from endpoints — 'service down but pod Running' = check endpoints",
          "a Running-but-not-Ready pod must be removed from the Service endpoints")

    # verdict
    log("\n" + "=" * 72)
    if failures:
        log(f"XX FAIL — {len(failures)} lesson(s) broke:")
        for f in failures:
            log(f"    - {f}")
        if args.sabotage:
            log("\n(expected: --sabotage breaks the model, so the guarantees fall.)")
        log("=" * 72)
        return 1
    log("OK PASS — all six Kubernetes lessons held:")
    log("    you declare desired state; a controller reconciles actual -> desired, forever.")
    log("    Delete a pod, it comes back; hand-fix a pod, the fix dies with it;")
    log("    a bad image loops (restart != fix); change the template, controllers roll;")
    log("    readiness gates the Service endpoints. Pods are cattle — manage the spec.")
    log("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
