#!/usr/bin/env python3
"""
AWS account inventory — a read-only "list everything" admin script.

Runs under a least-privilege identity (see inventory-policy.json), paginates
properly, and iterates regions (EC2/VPCs are regional; S3/IAM are global). Writes
one CSV per resource type. Read-only: it never mutates anything.

    pip install -r requirements.txt
    export AWS_PROFILE=your-sandbox-profile   # or AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
    python inventory.py --out ./out
"""

import argparse
import csv
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


def _iso(value):
    return value.isoformat() if value else ""


def _tag(tags, key):
    return next((t["Value"] for t in (tags or []) if t["Key"] == key), "")


def account_context(session):
    ident = session.client("sts").get_caller_identity()
    return ident["Account"], ident["Arn"]


def all_regions(session):
    resp = session.client("ec2").describe_regions(AllRegions=False)
    return sorted(r["RegionName"] for r in resp["Regions"])


def ec2_instances(session, regions):
    rows = []
    for region in regions:
        ec2 = session.client("ec2", region_name=region)
        try:
            for page in ec2.get_paginator("describe_instances").paginate():
                for reservation in page["Reservations"]:
                    for inst in reservation["Instances"]:
                        rows.append({
                            "region": region,
                            "instance_id": inst["InstanceId"],
                            "name": _tag(inst.get("Tags"), "Name"),
                            "type": inst["InstanceType"],
                            "state": inst["State"]["Name"],
                            "private_ip": inst.get("PrivateIpAddress", ""),
                            "public_ip": inst.get("PublicIpAddress", ""),
                            "vpc_id": inst.get("VpcId", ""),
                            "launch_time": _iso(inst.get("LaunchTime")),
                        })
        except ClientError as e:
            print(f"  ! describe_instances failed in {region}: "
                  f"{e.response['Error']['Code']}", file=sys.stderr)
    return rows


def vpcs(session, regions):
    rows = []
    for region in regions:
        ec2 = session.client("ec2", region_name=region)
        try:
            for vpc in ec2.describe_vpcs()["Vpcs"]:
                rows.append({
                    "region": region,
                    "vpc_id": vpc["VpcId"],
                    "name": _tag(vpc.get("Tags"), "Name"),
                    "cidr": vpc.get("CidrBlock", ""),
                    "is_default": vpc.get("IsDefault", False),
                    "state": vpc.get("State", ""),
                })
        except ClientError as e:
            print(f"  ! describe_vpcs failed in {region}: "
                  f"{e.response['Error']['Code']}", file=sys.stderr)
    return rows


def s3_buckets(session):
    s3 = session.client("s3")
    rows = []
    for bucket in s3.list_buckets().get("Buckets", []):
        try:
            loc = s3.get_bucket_location(Bucket=bucket["Name"])["LocationConstraint"]
            region = loc or "us-east-1"  # null == us-east-1, an AWS quirk
        except ClientError:
            region = "?"
        rows.append({
            "bucket": bucket["Name"],
            "region": region,
            "created": _iso(bucket.get("CreationDate")),
        })
    return rows


def iam_users(session):
    rows = []
    for page in session.client("iam").get_paginator("list_users").paginate():
        for user in page["Users"]:
            rows.append({
                "user": user["UserName"],
                "arn": user["Arn"],
                "created": _iso(user.get("CreateDate")),
                "password_last_used": _iso(user.get("PasswordLastUsed")),
            })
    return rows


def write_csv(out_dir, name, rows):
    path = out_dir / f"{name}.csv"
    if not rows:
        path.write_text("")  # create it anyway so an empty result is obvious
        print(f"  {name:<14} {0:>4} rows -> {path}")
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {name:<14} {len(rows):>4} rows -> {path}")


def main():
    ap = argparse.ArgumentParser(description="Read-only AWS account inventory.")
    ap.add_argument("--out", default="./out", help="output directory for CSVs")
    args = ap.parse_args()

    session = boto3.Session()
    try:
        account, arn = account_context(session)
    except ClientError as e:
        print(f"Could not authenticate: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Account {account}  |  running as {arn}")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    regions = all_regions(session)
    print(f"Scanning {len(regions)} regions for regional resources...")

    write_csv(out_dir, "ec2_instances", ec2_instances(session, regions))
    write_csv(out_dir, "vpcs", vpcs(session, regions))
    write_csv(out_dir, "s3_buckets", s3_buckets(session))
    write_csv(out_dir, "iam_users", iam_users(session))
    print("Done.")


if __name__ == "__main__":
    main()
