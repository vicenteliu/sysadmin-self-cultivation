# AWS — Labs

Runnable, tear-down-able exercises. Reading about a subnet and configuring one are
different skills; these make you do the second.

> **Ground rules:** use a **throwaway / sandbox account**, set a **hard Budget
> alarm** first, and `destroy` everything when you're done. Never run labs with
> long-lived root keys.

## Planned labs (build order)

1. **`01-scoped-identity-inventory/`** — Create a least-privilege IAM role, then a
   `boto3` script that inventories the account (EC2, S3, VPCs, IAM users) to CSV.
   The cloud version of the classic "list everything" admin script — mirrors the
   read-only, paginated inventory pattern used for on-prem/MDM fleets.
   ✅ **built** — see [`01-scoped-identity-inventory/`](01-scoped-identity-inventory/).
2. **`02-minimal-vpc-ec2-terraform/`** — Terraform for a VPC (one public + one
   private subnet across two AZs, IGW + NAT), one EC2 instance with an instance
   profile (no baked-in keys), reachable over SSM (no open SSH). Apply, verify,
   destroy.
3. **`03-s3-secure-defaults/`** — An S3 bucket with encryption + block-public-access,
   a least-privilege bucket policy, and a lifecycle rule — proving the "right
   defaults" muscle.
4. **`04-budget-and-alarm/`** — A Budget + CloudWatch alarm, so a forgotten resource
   pages you instead of surprising you on the invoice.

Each lab folder will contain: the code, a `README` with the goal + what to verify,
and explicit teardown steps. Labs are added as the AWS module matures.
