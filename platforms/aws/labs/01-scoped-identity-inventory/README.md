# Lab 01 — Scoped identity + account inventory

**Goal:** create a *least-privilege, read-only* identity, then use it to inventory
the account from a script — the cloud version of the classic "list everything" admin
script. This is move #1 and #2 of the [operating model](../../../../00-the-operating-model.md)
(register a scoped identity → drive by API) made concrete.

**You'll practice:** writing a tight IAM policy, using a scoped credential from code,
paginating properly, and iterating regions (a common gotcha — EC2/VPCs are *regional*,
S3/IAM are *global*).

## Prerequisites

- A **sandbox / dev AWS account** and the AWS CLI configured (`aws sts get-caller-identity` works).
- Python 3.9+.
- A **Budget alarm** on the account (do this once, in every account — see lab 04).

## Step 1 — the least-privilege policy

[`inventory-policy.json`](inventory-policy.json) grants *only* the read-only calls
this script makes — nothing else:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "InventoryReadOnly",
    "Effect": "Allow",
    "Action": [
      "sts:GetCallerIdentity",
      "ec2:DescribeRegions",
      "ec2:DescribeInstances",
      "ec2:DescribeVpcs",
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation",
      "iam:ListUsers"
    ],
    "Resource": "*"
  }]
}
```

> **Honest note on `"Resource": "*"`:** these `Describe*` / `List*` actions don't
> support resource-level scoping in IAM — AWS evaluates them account-wide by design.
> So you tighten the **actions** hard instead of the resources. Knowing *which*
> actions are `*`-only is exactly the kind of platform-specific detail the
> [AI-ramp](../../ai-ramp.md) says to verify against the docs rather than trust.

Create a role or user with this policy attached (role + assume-role is preferred over
a long-lived user key):

```bash
aws iam create-policy --policy-name inventory-readonly \
  --policy-document file://inventory-policy.json
# then attach it to a role you assume, or a dedicated user, per your setup
```

## Step 2 — run the inventory

```bash
pip install -r requirements.txt
export AWS_PROFILE=your-sandbox-profile     # the scoped identity from step 1
python inventory.py --out ./out
```

## Step 3 — verify

- The script prints the account ID and the ARN it's running as — confirm it's the
  **scoped** identity, not your admin.
- `./out/` has `ec2_instances.csv`, `vpcs.csv`, `s3_buckets.csv`, `iam_users.csv`.
- Spot-check one CSV against the console. Then **remove one action** from the policy,
  re-run, and watch the exact call fail with `AccessDenied` — proof the policy is
  actually doing the scoping (and practice reading a denied request).

## Teardown

```bash
# detach + delete the policy (and the role/user) when done
aws iam delete-policy --policy-arn arn:aws:iam::<acct>:policy/inventory-readonly
rm -rf ./out
```

Nothing here creates billable resources — but deleting the identity keeps the account
clean and is good hygiene.
