#!/usr/bin/env python3
"""
gke_authz_drill.py — prove, in your own hands, the #1 GKE support lesson from the
GCP support note: GKE has TWO auth planes. Cloud IAM AUTHENTICATES you to the cluster
(you need the IAM permission container.clusters.get just to reach the API server);
Kubernetes RBAC AUTHORIZES what you do INSIDE it. GKE checks RBAC first, then falls
back to IAM. So 'Unauthorized' (authn) and 'Forbidden' (authz) are different failures
with different fixes — and being IAM "Cluster Admin" does NOT make `kubectl get
secrets` work: the fix for in-cluster access is an RBAC binding, not more IAM.

No cloud, no cluster, no credentials, no external dependencies. Pure Python stdlib.

We model GKE's authorization pipeline and run kubectl requests through it. This is a
faithful (simplified) model — the permission strings are illustrative; the behaviour
(authn separate from authz, RBAC-first-then-IAM-fallback, clusterAdmin != in-cluster)
is real.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass, field


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


def matches(rule, verb, resource):
    """(verb, resource) rule match with '*' wildcards, k8s-RBAC style."""
    rv, rr = rule
    return (rv in ("*", verb)) and (rr in ("*", resource))


# --- IAM roles: GCP permissions + which in-cluster (verb,resource) they grant -------
# clusterViewer/clusterAdmin authenticate you and (for admin) let you change cluster
# INFRA, but grant NOTHING inside the cluster. container.admin is the broad role whose
# IAM permissions DO map to in-cluster access via GKE's IAM fallback (over-privileged).
IAM_ROLES = {
    "roles/container.clusterViewer": {
        "perms": {"container.clusters.get"},          # can reach the API server
        "incluster": set(),                           # authorizes nothing inside
    },
    "roles/container.clusterAdmin": {
        "perms": {"container.clusters.get", "container.clusters.update"},  # infra
        "incluster": set(),                           # NOT the RBAC cluster-admin
    },
    "roles/container.admin": {
        "perms": {"container.clusters.get", "container.clusters.update"},
        "incluster": {("*", "*")},                    # broad in-cluster via IAM fallback
    },
}

# --- RBAC roles: (verb, resource) rules granted INSIDE the cluster ------------------
RBAC_ROLES = {
    "view": {("get", "pods"), ("list", "pods"), ("get", "services")},   # read-only
    "cluster-admin": {("*", "*")},                                      # the real one
}


@dataclass
class Principal:
    name: str
    iam_roles: list = field(default_factory=list)   # e.g. ["roles/container.clusterViewer"]
    rbac_roles: list = field(default_factory=list)  # e.g. ["view"]

    def iam_perms(self):
        p = set()
        for r in self.iam_roles:
            p |= IAM_ROLES[r]["perms"]
        return p

    def iam_incluster(self):
        rules = set()
        for r in self.iam_roles:
            rules |= IAM_ROLES[r]["incluster"]
        return rules

    def rbac_rules(self):
        rules = set()
        for r in self.rbac_roles:
            rules |= RBAC_ROLES[r]
        return rules


def authenticate(p: Principal) -> bool:
    """Plane 1 — Cloud IAM: can this principal even reach the API server?"""
    return "container.clusters.get" in p.iam_perms()


def authorize(p: Principal, verb, resource):
    """Plane 2 — GKE checks RBAC first, then falls back to IAM. Returns (ok, how)."""
    if any(matches(rule, verb, resource) for rule in p.rbac_rules()):
        return True, "RBAC"
    if any(matches(rule, verb, resource) for rule in p.iam_incluster()):
        return True, "IAM fallback"
    return False, None


def kubectl(p: Principal, verb, resource):
    """The full request pipeline. Returns (result, reason)."""
    if not authenticate(p):
        return "Unauthorized", "authn failed — no container.clusters.get (can't reach the API server)"
    ok, how = authorize(p, verb, resource)
    if ok:
        return "OK", f"authorized via {how}"
    return "Forbidden", "authn OK, but no RBAC binding and no in-cluster IAM grants this"


def run() -> int:
    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"  ✓ {ok_msg}")
        else:
            log(f"  ✗ {fail_msg}")
            failures.append(fail_msg)

    nobody = Principal("nobody")                                    # no IAM at all
    viewer = Principal("viewer", ["roles/container.clusterViewer"])  # authn only
    infra_admin = Principal("infra-admin", ["roles/container.clusterAdmin"])  # infra, no inside
    support = Principal("support-eng", ["roles/container.clusterViewer"], ["view"])  # RBAC fix
    broad = Principal("broad-iam", ["roles/container.admin"])       # in-cluster via IAM

    step(1, "Plane 1 (authn): no IAM cluster role → can't even reach the API server")
    res, why = kubectl(nobody, "get", "pods")
    log(f"  kubectl get pods  as nobody → {res}  ({why})")
    check(res == "Unauthorized",
          "Unauthorized = authentication plane — container.clusters.get is the ticket in (LESSON 1)",
          "expected Unauthorized for a principal with no IAM")

    step(2, "Authenticated ≠ authorized: reaching the cluster grants nothing inside")
    res, why = kubectl(viewer, "get", "pods")
    log(f"  kubectl get pods  as viewer (clusterViewer, no RBAC) → {res}  ({why})")
    check(authenticate(viewer) and res == "Forbidden",
          "viewer authenticates but is Forbidden — the two planes are separate (LESSON 2)",
          "clusterViewer should authenticate yet be Forbidden with no RBAC")

    step(3, "The trap: IAM 'Cluster Admin' is NOT the RBAC cluster-admin")
    res, why = kubectl(infra_admin, "get", "secrets")
    log(f"  kubectl get secrets  as infra-admin (clusterAdmin IAM) → {res}  ({why})")
    check(res == "Forbidden",
          "container.clusterAdmin changes cluster INFRA but grants nothing inside (LESSON 3)",
          "IAM clusterAdmin unexpectedly authorized an in-cluster resource")

    step(4, "The fix is an RBAC binding — not escalating IAM")
    res_get, _ = kubectl(support, "get", "pods")
    res_del, _ = kubectl(support, "delete", "pods")
    log(f"  support-eng (clusterViewer + RBAC 'view'):  get pods → {res_get},  delete pods → {res_del}")
    check(res_get == "OK",
          "an RBAC 'view' binding authorizes get pods — the correct, scoped fix (LESSON 4)",
          "the RBAC view binding failed to authorize get pods")
    check(res_del == "Forbidden",
          "…and 'view' does NOT grant delete — RBAC is scoped, not all-or-nothing",
          "RBAC 'view' wrongly allowed delete pods")

    step(5, "The IAM fallback is real — but it's the over-privileged path")
    res, why = kubectl(broad, "get", "secrets")
    log(f"  kubectl get secrets  as broad-iam (container.admin) → {res}  ({why})")
    check(res == "OK" and why.endswith("IAM fallback"),
          "a broad IAM role authorizes inside via the fallback — which is why scoped principals get RBAC, not broad IAM",
          "the IAM fallback did not authorize a broad IAM role")

    step(6, "Two words, two failures, two fixes")
    r_nobody, _ = kubectl(nobody, "get", "pods")
    r_viewer, _ = kubectl(viewer, "get", "pods")
    log(f"  nobody → {r_nobody}  (fix: credentials / auth plugin / container.clusters.get)")
    log(f"  viewer → {r_viewer}    (fix: an RBAC binding)")
    check(r_nobody == "Unauthorized" and r_viewer == "Forbidden",
          "Unauthorized (authn) and Forbidden (authz) are distinct — don't fix one as the other (LESSON 5)",
          "the Unauthorized/Forbidden distinction did not hold")

    step(7, "Your instinct vs. reality — 'I'm cluster admin, kubectl just works'")
    instinct = "OK"                                     # the imported assumption
    reality, _ = kubectl(infra_admin, "get", "secrets")  # IAM clusterAdmin
    log(f"  instinct: IAM Cluster Admin ⇒ kubectl works = {instinct}")
    log(f"  reality:  get secrets as infra-admin = {reality}")
    check(instinct != reality,
          "the 'IAM admin ⇒ full kubectl' instinct is WRONG — RBAC governs inside",
          "instinct and reality agreed — the drill proved nothing")

    log("\n" + "=" * 70)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the lessons held:")
    log("  1. Cloud IAM authenticates (container.clusters.get); no IAM → Unauthorized.")
    log("  2. Authenticating grants nothing inside — RBAC/IAM must authorize the action.")
    log("  3. The IAM 'Cluster Admin' role is not the RBAC cluster-admin (infra, not inside).")
    log("  4. You fix in-cluster access with a scoped RBAC binding, not more IAM.")
    log("  5. Unauthorized (authn) and Forbidden (authz) are different failures + fixes.")
    log("")
    log("The instinct this drill retired:")
    log("  'I have admin, so kubectl works' — on GKE, IAM gets you to the door;")
    log("  RBAC decides what you can touch once you're inside.")
    return 0


def main():
    argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    sys.exit(run())


if __name__ == "__main__":
    main()
