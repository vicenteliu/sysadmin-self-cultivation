# Lab — GKE has two auth planes (prove it in your own hands)

**Goal:** make the #1 GKE lesson of the [GCP support note](../../support.md) tangible —
**GKE authenticates you with Cloud IAM and authorizes you with Kubernetes RBAC; they
are separate planes, so `Unauthorized` (authn) and `Forbidden` (authz) are different
failures with different fixes — and being IAM "Cluster Admin" does NOT make `kubectl
get secrets` work.** You'll run a faithful model of GKE's authorization pipeline and
watch requests fail for the exact reasons behind most GKE access tickets.

**You'll practice:** reading a GKE access failure as *"which plane said no?"* — no
`container.clusters.get` (can't authenticate) vs. authenticated-but-no-RBAC (Forbidden)
— and the reflex the note insists on: **fix in-cluster access with an RBAC binding, not
by escalating IAM.**

## Why this lab is pure-local

No cluster, no credentials, no cost, no external packages — just Python 3.8+. IAM roles
and RBAC roles are small dicts; the evaluator is a faithful implementation of GKE's real
order:

1. **Authenticate (Cloud IAM):** the caller needs `container.clusters.get` to reach the
   API server at all. No IAM cluster role → **`Unauthorized`**.
2. **Authorize (RBAC first, IAM fallback second):** GKE checks for an RBAC binding; if
   none, it falls back to the caller's in-cluster IAM permissions. Neither grants the
   verb → **`Forbidden`**.

(The permission strings are illustrative; the *behaviour* — authn separate from authz,
RBAC-first-then-IAM-fallback, `clusterAdmin` ≠ in-cluster — is real.)

## Run it

```bash
python3 gke_authz_drill.py
```

That's it — no install. Exit code `0` means every assertion held, so it doubles as a
CI check.

## What you'll see

Seven narrated steps, each ending in a checked lesson:

```
=== 2. Authenticated ≠ authorized: reaching the cluster grants nothing inside ===
  kubectl get pods  as viewer (clusterViewer, no RBAC) → Forbidden
  ✓ viewer authenticates but is Forbidden — the two planes are separate (LESSON 2)
=== 3. The trap: IAM 'Cluster Admin' is NOT the RBAC cluster-admin ===
  kubectl get secrets  as infra-admin (clusterAdmin IAM) → Forbidden
  ✓ container.clusterAdmin changes cluster INFRA but grants nothing inside (LESSON 3)
=== 4. The fix is an RBAC binding — not escalating IAM ===
  support-eng (clusterViewer + RBAC 'view'):  get pods → OK,  delete pods → Forbidden
```

## Verify (don't take the script's word for it)

Drive the model yourself in a Python shell:

```python
from gke_authz_drill import Principal, kubectl
infra = Principal("infra-admin", ["roles/container.clusterAdmin"])
print(kubectl(infra, "get", "secrets"))   # ('Forbidden', ...) — IAM admin ≠ in-cluster
infra.rbac_roles = ["view"]                # add an RBAC binding
print(kubectl(infra, "get", "pods"))       # ('OK', 'authorized via RBAC')
```

Then break it deliberately — make `authorize()` skip the RBAC-first rule — and re-run:
the drill must exit **non-zero**. A self-verifier that can't fail is worthless.

## The point

- **Two planes, two questions.** *Can you reach the cluster?* (Cloud IAM authn) is
  separate from *can you do this action inside it?* (Kubernetes RBAC authz). A single
  Google identity can pass one and fail the other.
- **`Unauthorized` ≠ `Forbidden`.** Unauthorized is an authentication problem (bad/
  expired credential, missing `gke-gcloud-auth-plugin`, no `container.clusters.get`);
  Forbidden is an authorization problem (no RBAC binding). Fixing one as the other is
  the classic time-sink.
- **IAM "Cluster Admin" is not RBAC `cluster-admin`.** The IAM role changes cluster
  *infrastructure*; it grants nothing *inside*. "I'm Owner, why is kubectl Forbidden?"
  is this, exactly.
- **Fix in-cluster access with RBAC, scoped.** A `view` binding grants `get pods` and
  *not* `delete pods` — that's the point of RBAC over a broad IAM role. You just watched
  the scoped fix work and the over-broad IAM path work-but-over-privilege.

## Teardown

Nothing persistent is created — the drill writes no files. Nothing to clean up.
