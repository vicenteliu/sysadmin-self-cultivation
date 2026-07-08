# GCP — Labs

Runnable, tear-down-able exercises — same shape as the [AWS labs](../../aws/labs/), so
the concepts *translate*.

> **Ground rules:** use a **sandbox project** (or the Always-Free tier), set a
> **budget alert** first, and delete the project or the resources when done. Reach VMs
> via **IAP** tunneling — never open SSH to the internet.

## Why the command line

Every lab is **CLI-first** (`gcloud`). The console is for *looking*; `gcloud` is for
*doing* — **faster** than a menu-hunt, **exact** (no wrong project left selected),
**repeatable** (paste into a runbook), and **reviewable** (a diff, not a screencap) —
the same surface your automation uses. Anything you can click, you can command.

## The three-lab arc

### Lab 01 — Scoped identity + inventory

A least-privilege **service account**, then inventory the project. Note **Cloud Asset
Inventory** answers org-wide questions in one call — and remember you often loop
*projects*, and resources are zonal/regional:

```bash
gcloud auth login
gcloud config set project my-sandbox-project
gcloud config list                                   # confirm the right project

# the whole project in one call — Cloud Asset Inventory (beats looping every API)
gcloud asset search-all-resources --scope=projects/my-sandbox-project \
  --format="table(name, assetType, location)"

# or the classic per-service list (compute is zonal — this lists across zones)
gcloud compute instances list --format="table(name, zone, machineType.basename(), status)"
gcloud storage buckets list --format="table(name, location, default_storage_class)"
```

**Verify:** grant the service account `roles/viewer` on one resource only, impersonate
it (`--impersonate-service-account`), and watch the rest disappear.

### Lab 02 — Minimal network + compute from code

Remember GCP's outlier: the **VPC is global**, subnets are regional. A network, a
firewall rule targeting a **tag** (not an IP range — the GCP model), and an instance
with **no external IP**:

```bash
gcloud compute networks create lab-vpc --subnet-mode=custom
gcloud compute networks subnets create lab-subnet \
  --network=lab-vpc --region=us-central1 --range=10.0.1.0/24
# firewall targets a TAG, not a CIDR — GCP's identity-aware model
gcloud compute firewall-rules create allow-iap-ssh \
  --network=lab-vpc --direction=INGRESS --action=ALLOW --rules=tcp:22 \
  --source-ranges=35.235.240.0/20 --target-tags=lab   # 35.235.240.0/20 = IAP
gcloud compute instances create lab-vm \
  --zone=us-central1-a --subnet=lab-subnet --no-address --tags=lab \
  --machine-type=e2-micro
# reach it with NO external IP — IAP tunnel:
gcloud compute ssh lab-vm --zone=us-central1-a --tunnel-through-iap
```

**Verify:** `gcloud compute instances describe lab-vm --zone=us-central1-a --format='value(networkInterfaces[0].accessConfigs)'`
returns empty — no external IP. **Teardown:** delete the instance, firewall, subnet,
then `gcloud compute networks delete lab-vpc`.

### Lab 03 — Secure storage + a budget

Secure-by-default storage (GCP defaults are strong; make them explicit) and the budget:

```bash
# a bucket with uniform bucket-level access (no legacy per-object ACLs) + a class
gcloud storage buckets create gs://my-unique-lab-bucket-$RANDOM \
  --location=us-central1 --uniform-bucket-level-access --default-storage-class=STANDARD

# prove no public access is possible via legacy ACLs (uniform access blocks them)
gcloud storage buckets describe gs://$BUCKET --format='value(uniform_bucket_level_access)'

# a budget (set FIRST in real projects) — via the billing API
gcloud billing budgets create --billing-account=$BILLING_ACCT \
  --display-name=lab-budget --budget-amount=20USD \
  --filter-projects=projects/my-sandbox-project
```

**Verify:** the uniform-access value is `True`; attempting a legacy public ACL is
rejected. **Teardown:** `gcloud storage rm --recursive gs://$BUCKET`.

## Beyond the arc — a pure-local support drill

The three-lab arc above needs a sandbox project. One more lab needs **nothing** — a
pure-local, stdlib-only, self-verifying drill tied to the [support note](../support.md):

### `gke-iam-vs-rbac/` — GKE's two auth planes ✅ built (pure-local)

Models GKE authorization and proves the #1 GKE support lesson — **Cloud IAM
authenticates, Kubernetes RBAC authorizes; `Unauthorized` ≠ `Forbidden`; IAM "Cluster
Admin" is not in-cluster admin** — with zero credentials. See
**[`gke-iam-vs-rbac/`](gke-iam-vs-rbac/)**.

```bash
python3 gke-iam-vs-rbac/gke_authz_drill.py   # exit 0 = the lessons held; runs in CI
```

Read it before the cloud arc if "I'm Owner but kubectl says Forbidden" is the ticket.

---

Each lab lands with the code (Terraform is the persistent form), a `README`, and
explicit teardown. Honest note: GCP is the 🧗 ramp — these are the ramp made runnable
at no cost on the free tier.
