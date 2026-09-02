---
kind: lab
axis: platforms
themes: [identity, cloud]
platforms: [aws]
derived: true
mirrors: platforms/aws/labs/01-scoped-identity-inventory/README.md
summary: "inventory-policy.json 只授予这个脚本会发起的那些只读调用 —— 别的都没有……"
---
# Lab 01 —— 受限身份 + 账号盘点

> 🌐 **语言：** [English（默认）](../../../../../../platforms/aws/labs/01-scoped-identity-inventory/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/aws/labs/01-scoped-identity-inventory/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 创建一个*最小权限、只读*的身份，然后用它从一个脚本去盘点这个账号 —— 也就是那个经典的
"把所有东西列出来"管理员脚本的云上版本。这是[运营模型](../../../../00-the-operating-model.md)
第 1 招和第 2 招（注册一个受限身份 → 用 API 驱动）被变具体。

**你会练到：** 写一条收紧的 IAM 策略、从代码里用一份受限凭据、正确地分页，以及遍历 region
（一个常见的坑 —— EC2/VPC 是*区域性*的，S3/IAM 是*全局*的）。

## 前置条件

- 一个 **沙箱/开发 AWS 账号**，并且 AWS CLI 已配置好（`aws sts get-caller-identity` 跑得通）。
- Python 3.9+。
- 这个账号上有一条 **Budget 告警**（每个账号做一次 —— 见 lab 04）。

## 步骤 1 —— 那条最小权限策略

[`inventory-policy.json`](../../../../../../platforms/aws/labs/01-scoped-identity-inventory/inventory-policy.json) *只*授予这个脚本会发起的那些只读调用 ——
别的都没有：

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

> **关于 `"Resource": "*"` 的一句诚实说明：** 这些 `Describe*` / `List*` action 在 IAM 里不支持
> 资源级别的范围限定 —— AWS 在设计上就是账号级去求值它们的。所以你转而把那些 **action** 收得
> 很紧，而不是收资源。知道*哪些* action 是只能 `*` 的，恰恰是
> [AI-ramp](../../ai-ramp.md) 说要对着文档去验证、而不要去信的那类平台特有细节。

创建一个附上这条策略的 role 或者 user（role + assume-role 优于一把长寿命的用户密钥）：

```bash
aws iam create-policy --policy-name inventory-readonly \
  --policy-document file://inventory-policy.json
# 然后按你的方式把它挂到一个你要扮演的 role 上，或者一个专用的 user 上
```

## 步骤 2 —— 跑那次盘点

```bash
pip install -r requirements.txt
export AWS_PROFILE=your-sandbox-profile     # 步骤 1 里那个受限身份
python inventory.py --out ./out
```

## 步骤 3 —— 验证

- 这个脚本会打印它正在以之运行的账号 ID 和 ARN —— 确认那是那个**受限**身份，不是你的 admin。
- `./out/` 里有 `ec2_instances.csv`、`vpcs.csv`、`s3_buckets.csv`、`iam_users.csv`。
- 挑一个 CSV 对着控制台核一下。然后**从那条策略里去掉一个 action**、重跑，看着恰好那次调用带着
  `AccessDenied` 失败 —— 这既是那条策略确实在做范围限定的证据，也是一次读被拒绝请求的练习。

## 拆除

```bash
# 做完之后把那条策略解绑并删掉（以及那个 role/user）
aws iam delete-policy --policy-arn arn:aws:iam::<acct>:policy/inventory-readonly
rm -rf ./out
```

这里没有任何东西会产生计费资源 —— 但把那个身份删掉能让账号保持干净，也是好卫生。
