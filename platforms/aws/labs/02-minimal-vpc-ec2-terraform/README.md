# Lab 02 — Minimal VPC + EC2, from Terraform

**Goal:** stand up a small, *secure-by-default* stack entirely from code — a VPC, a
public and a private subnet, and one EC2 instance you can reach **without opening a
single inbound port** — then tear it down cleanly. This is move #3 of the
[operating model](../../../../00-the-operating-model.md) (drive by API + codify it)
and the "build from code, not clicks" bar from the [skill map](../../skills-map.md).

## What it builds

```
VPC 10.20.0.0/16
├── public subnet  10.20.1.0/24  ── IGW (inbound/outbound) ── NAT gateway
└── private subnet 10.20.11.0/24 ── NAT (outbound only)
        └── EC2 (Amazon Linux 2023, no public IP)
              ├── IAM instance role → SSM (no SSH keys)
              ├── security group: NO inbound, egress only
              ├── IMDSv2 required
              └── encrypted root volume
```

The lessons baked in, on purpose:

- **No SSH, no open ports.** You reach the box with **SSM Session Manager**, so the
  security group has *zero* inbound rules. This is the single biggest real-world win
  over the usual "open port 22 to 0.0.0.0/0."
- **No baked-in credentials.** The instance gets an **IAM role** via an instance
  profile — never access keys on the box.
- **Private by default.** The instance lives in the private subnet with no public IP;
  outbound goes through the NAT.
- **Secure defaults on the instance.** IMDSv2 required + encrypted root volume.
- **No hardcoded AMI.** The latest AL2023 image is resolved from an SSM public
  parameter at plan time.

## Prerequisites

- **Terraform** ≥ 1.5 and AWS credentials for a **sandbox account** (`aws sts get-caller-identity` works).
- The **SSM Session Manager plugin** for the AWS CLI (to connect in the verify step).
- A **Budget alarm** on the account (see lab 04) — do this once, everywhere.

> ⚠️ **Cost.** Almost everything here is Free-Tier-friendly, **except the NAT
> gateway** (~\$0.045/hr + data) and the Elastic IP while allocated. It's cents for a
> short lab, but **`terraform destroy` when you're done** — a forgotten NAT is the
> classic "why is my bill \$35?" surprise.

## Run it

```bash
terraform init
terraform fmt -check      # style
terraform validate        # config is internally valid
terraform plan            # read what it will create — this is the habit
terraform apply           # type yes
```

## Verify

```bash
# The instance has NO public IP and NO open ports — yet this gives you a shell:
aws ssm start-session --target "$(terraform output -raw instance_id)" \
  --region "$(terraform output -raw region 2>/dev/null || echo us-west-2)"
```

- You land in a shell on a host with only a private IP and an empty inbound
  security group. That's the whole point.
- In the console, confirm: instance has no public IP, the SG has no inbound rules,
  and the instance shows as "managed" in Systems Manager → Fleet Manager.

## Tear down

```bash
terraform destroy        # type yes — removes everything, including the NAT
```

Confirm in Cost Explorer the next day that nothing lingers. Clean teardown is a
skill; practice it every time.

## Where AI helped, and where you verify (see [ai-ramp](../../ai-ramp.md))

AI drafts this kind of Terraform fast. The parts to **verify by hand**: the exact
NAT/route-table wiring (a mis-wired route is the #1 "why no internet"), that the SG
truly has no inbound, `http_tokens = "required"` for IMDSv2, and that
`terraform destroy` leaves nothing billable behind. AI writes the draft; the plan
output and a clean destroy are the proof.
