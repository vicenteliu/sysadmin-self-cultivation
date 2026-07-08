# AWS — Labs

Runnable, tear-down-able exercises. Reading about a subnet and configuring one are
different skills; these make you do the second.

> **Ground rules:** use a **throwaway / sandbox account**, set a **hard Budget
> alarm** first, and `destroy` everything when you're done. Never run labs with
> long-lived root keys.

## Why the command line

Every lab here is **CLI-first**, and that's a teaching choice, not a preference. The
console is for *looking*; the command line is for *doing*. A single `aws` command is
**faster** than a click-path, **exact** (no mis-picked dropdown or wrong region left
selected), **repeatable** (paste it into a script, a runbook, a ticket), and
**reviewable** (a diff, not a screen recording) — and it's the *same* surface your
automation uses. Anything you can click, you can command; the command is the one you
can hand to the next person or the next machine. Learn the CLI and the GUI becomes
optional; learn only the GUI and you can't automate, can't reproduce, and can't move
fast at 3 a.m.

## The three-lab arc

The same shape on every platform in this repo — [the operating
model](../../../00-the-operating-model.md) made runnable, read-only first:

### Lab 01 — Scoped identity + inventory ✅ built

Register a least-privilege identity, then drive the API to inventory the account. See
**[`01-scoped-identity-inventory/`](01-scoped-identity-inventory/)** for the full
`boto3` script + policy. The CLI spine:

```bash
# who am I running as? (confirm it's the SCOPED identity, not admin)
aws sts get-caller-identity

# regional resources — you must iterate regions (EC2/VPCs are per-region)
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  aws ec2 describe-instances --region "$r" \
    --query 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name]' \
    --output text
done

# global services — one shot, no region loop
aws s3api list-buckets --query 'Buckets[].Name' --output text
aws iam list-users --query 'Users[].UserName' --output text
```

**Verify:** remove one action from the policy, re-run, and watch that exact call fail
with `AccessDenied` — proof the scoping is real, and practice reading a denied request.

### Lab 02 — Minimal network + compute from code ✅ built

A VPC (public + private subnet, IGW + NAT), one EC2 instance with an instance profile
(no baked keys), reachable over SSM (no open SSH), IMDSv2 + encrypted disk. Full
Terraform in **[`02-minimal-vpc-ec2-terraform/`](02-minimal-vpc-ec2-terraform/)**. The
CLI you drive it with — the whole point is `plan` before `apply`, `destroy` at the end:

```bash
terraform init
terraform plan          # READ this before trusting it — the skill is here
terraform apply
# reach the box with NO open SSH port — Session Manager over the instance role:
aws ssm start-session --target "$(terraform output -raw instance_id)"
terraform destroy       # tear down cleanly — no orphaned billing resources
```

### Lab 03 — Secure defaults + a budget guardrail 🚧 CLI walkthrough

The "right defaults" muscle and the cost guardrail, entirely from the CLI:

```bash
# an S3 bucket that is private + encrypted by default
aws s3api create-bucket --bucket my-unique-lab-bucket-$RANDOM --region us-east-1
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket "$BUCKET" \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'

# prove it: this SHOULD now be blocked
aws s3api get-public-access-block --bucket "$BUCKET"

# the budget alarm you set FIRST in every account (forgotten resource → page, not surprise)
aws budgets create-budget --account-id "$(aws sts get-caller-identity --query Account --output text)" \
  --budget '{"BudgetName":"lab-monthly","BudgetLimit":{"Amount":"20","Unit":"USD"},"TimeUnit":"MONTHLY","BudgetType":"COST"}'
```

**Verify:** `aws s3api get-bucket-encryption --bucket "$BUCKET"` returns the KMS rule;
public-access-block shows all four `true`. **Teardown:** `aws s3 rb s3://$BUCKET --force`.

## Beyond the arc — a pure-local support drill

The three-lab arc above needs a sandbox account. One more lab needs **nothing** — a
pure-local, stdlib-only, self-verifying drill tied to the [support note](../support.md),
in the spirit of the repo's other runnable drills:

### `iam-deny-by-default/` — IAM policy evaluation ✅ built (pure-local)

Implements AWS's real policy-evaluation order and proves the #1 support lesson —
**deny-by-default, explicit-`Deny`-wins, an SCP or permissions boundary caps even an
admin** — with zero credentials. See
**[`iam-deny-by-default/`](iam-deny-by-default/)**.

```bash
python3 iam-deny-by-default/iam_eval_drill.py   # exit 0 = the lessons held; runs in CI
```

Read it before the cloud arc if IAM "Access Denied" is what you're actually debugging.

---

Each built lab folder contains: the code, a `README` with the goal + what to verify,
and explicit teardown. Labs are added as the module matures.
