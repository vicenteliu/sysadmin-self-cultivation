# OCI — Labs

Runnable, tear-down-able exercises — same shape as the [AWS labs](../../aws/labs/).
OCI's **Always Free tier** makes these genuinely no-cost.

> **Ground rules:** use a dedicated **compartment**, set a **budget** first, and
> terminate resources when done. Reach instances via a bastion or a private subnet —
> never open SSH to the internet.

## Why the command line

Every lab is **CLI-first** (`oci`). The console is for *looking*; the CLI is for
*doing* — **faster**, **exact**, **repeatable**, **reviewable**, and the same surface
your automation uses. Anything you can click, you can command.

## The three-lab arc

### Lab 01 — Scoped identity + inventory

A **compartment** (OCI's blast-radius unit) and a least-privilege **policy**, then
inventory. OCI's policy language reads like sentences — nicer than JSON:

```bash
oci setup config                                     # one-time: creates ~/.oci/config
oci iam region list --output table                   # confirm connectivity

# create a compartment (the isolation/blast-radius unit)
oci iam compartment create --name lab --description "lab compartment" \
  --compartment-id "$OCI_TENANCY"

# a human-readable least-privilege policy
oci iam policy create --name lab-read --compartment-id "$OCI_TENANCY" \
  --statements '["Allow group Readers to read all-resources in compartment lab"]' \
  --description "read-only in lab"

# inventory the compartment
oci compute instance list --compartment-id "$LAB_COMPARTMENT" \
  --query 'data[].{name:"display-name", shape:shape, state:"lifecycle-state"}' --output table
```

**Verify:** change the policy verb from `read` to `inspect` and watch which calls a
Readers member can still make — the policy language made concrete.

### Lab 02 — Minimal VCN + instance

A **VCN** (regional), a subnet, and an instance. Note the OCI filtering choice — **pick
security lists OR NSGs and standardize** (this lab uses the VCN's default security
list, then you'd switch to NSGs deliberately):

```bash
# the fast path: VCN + subnet + gateways in one wizard-equivalent command
oci network vcn create --compartment-id "$LAB" --cidr-blocks '["10.0.0.0/16"]' \
  --display-name lab-vcn
oci network subnet create --compartment-id "$LAB" --vcn-id "$VCN_ID" \
  --cidr-block 10.0.1.0/24 --display-name lab-subnet

# a flexible-shape instance — remember: an OCPU is a FULL CORE, not a hyperthread
oci compute instance launch --compartment-id "$LAB" \
  --availability-domain "$AD" --subnet-id "$SUBNET_ID" \
  --shape VM.Standard.E4.Flex --shape-config '{"ocpus":1,"memoryInGBs":8}' \
  --image-id "$UBUNTU_IMAGE" --assign-public-ip false \
  --metadata '{"ssh_authorized_keys":"'"$(cat ~/.ssh/id_rsa.pub)"'"}'
```

**Verify:** `oci compute instance list --compartment-id "$LAB" --query 'data[].shape'`
shows the flex shape; the instance has no public IP. **Teardown:** terminate the
instance, then delete the subnet and VCN.

### Lab 03 — Object storage + a budget

Object Storage (OCI's cheap-egress advantage makes it a good backup target) and a budget:

```bash
# a private bucket
oci os bucket create --compartment-id "$LAB" --name lab-bucket$RANDOM \
  --public-access-type NoPublicAccess

# put and list an object
echo "canary" > canary.txt
oci os object put --bucket-name "$BUCKET" --file canary.txt
oci os object list --bucket-name "$BUCKET" --query 'data[].name' --output table

# a budget on the compartment (set FIRST in real life)
oci budget budget create --compartment-id "$OCI_TENANCY" \
  --amount 20 --reset-period MONTHLY --target-type COMPARTMENT \
  --targets '["'"$LAB"'"]' --display-name lab-budget
```

**Verify:** `oci os bucket get --bucket-name "$BUCKET" --query 'data."public-access-type"'`
returns `NoPublicAccess`. **Teardown:** delete the object, then the bucket.

---

Each lab lands with the code (Terraform / Resource Manager is the persistent form), a
`README`, and explicit teardown. Honest note: OCI is a 🧗 ramp — the Always-Free tier
makes it a runnable one.
