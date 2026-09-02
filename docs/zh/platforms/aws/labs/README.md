---
kind: lab
axis: platforms
themes: [cloud]
platforms: [aws]
derived: true
mirrors: platforms/aws/labs/README.md
summary: "可跑、可拆的练习。读一个子网和配一个子网是两项不同的技能；这些逼你做第二件。"
---
# AWS —— Lab

> 🌐 **语言：** [English（默认）](../../../../../platforms/aws/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/aws/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

可跑、可拆的练习。读一个子网和配一个子网是两项不同的技能；这些逼你做第二件。

> **地面规则：** 用一个**用完即弃/沙箱账号**，先设一条**硬性的 Budget 告警**，做完之后把所有东西
> `destroy` 掉。绝不要拿长寿命的 root 密钥跑 lab。

## 为什么是命令行

这里每一个 lab 都是**命令行优先**的，而那是一个教学选择，不是偏好。控制台是用来*看*的；命令行是
用来*做*的。一条 `aws` 命令比一串点击路径**更快**、**更精确**（不会挑错下拉项，也不会留着一个选错
的 region）、**可复现**（粘进一个脚本、一份 runbook、一张工单里）、**可评审**（一份 diff，不是一段
屏幕录像）—— 而且它就是你的自动化所用的*同一片*界面。凡是你点得了的，你都命令得了；而命令才是那个
你能递给下一个人或者下一台机器的东西。学会命令行，GUI 就变成可选的；只学 GUI，你自动化不了、复现
不了，凌晨三点也快不起来。

## 那条三节 lab 弧

这个仓库里每个平台都是同一个形状 —— [那个运营模型](../../../00-the-operating-model.md)被做成可跑
的，而且先只读：

### Lab 01 —— 受限身份 + 盘点 ✅ 已建

注册一个最小权限身份，然后驱动 API 去盘点这个账号。完整的 `boto3` 脚本 + 策略见
**[`01-scoped-identity-inventory/`](01-scoped-identity-inventory/)**。那条命令行主干：

```bash
# 我是以谁的身份在跑？（确认是那个受限身份，不是 admin）
aws sts get-caller-identity

# 区域性资源 —— 你必须遍历 region（EC2/VPC 是逐 region 的）
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  aws ec2 describe-instances --region "$r" \
    --query 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name]' \
    --output text
done

# 全局服务 —— 一次搞定，不用 region 循环
aws s3api list-buckets --query 'Buckets[].Name' --output text
aws iam list-users --query 'Users[].UserName' --output text
```

**验证：** 从那条策略里去掉一个 action，重跑，看着恰好那次调用带着 `AccessDenied` 失败 —— 这既是
那个受限确实生效的证据，也是一次读被拒绝请求的练习。

### Lab 02 —— 从代码起一套最小网络 + 计算 ✅ 已建

一个 VPC（公有 + 私有子网，IGW + NAT）、一台带 instance profile 的 EC2（不烤任何密钥）、经 SSM
可达（不开 SSH）、IMDSv2 + 加密磁盘。完整 Terraform 在
**[`02-minimal-vpc-ec2-terraform/`](02-minimal-vpc-ec2-terraform/)**。你用来驱动它的那些命令 ——
重点全在 `apply` 之前先 `plan`、最后 `destroy`：

```bash
terraform init
terraform plan          # 在信它之前先「读」它 —— 那项技能就在这儿
terraform apply
# 在没有任何开放 SSH 端口的情况下够到那台机器 —— 走实例角色的 Session Manager：
aws ssm start-session --target "$(terraform output -raw instance_id)"
terraform destroy       # 干净地拆掉 —— 别留下孤儿计费资源
```

### Lab 03 —— 安全默认值 + 一条预算护栏 🚧 引导式命令行走查

那份"对的默认值"的肌肉记忆，和那条成本护栏，全部从命令行来：

```bash
# 一个默认私有 + 默认加密的 S3 bucket
aws s3api create-bucket --bucket my-unique-lab-bucket-$RANDOM --region us-east-1
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket "$BUCKET" \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'

# 证明它：这件事现在「应该」被挡掉
aws s3api get-public-access-block --bucket "$BUCKET"

# 那条你在每个账号里「第一件事」就设的预算告警（被遗忘的资源 → 呼你，而不是吓你）
aws budgets create-budget --account-id "$(aws sts get-caller-identity --query Account --output text)" \
  --budget '{"BudgetName":"lab-monthly","BudgetLimit":{"Amount":"20","Unit":"USD"},"TimeUnit":"MONTHLY","BudgetType":"COST"}'
```

**验证：** `aws s3api get-bucket-encryption --bucket "$BUCKET"` 返回那条 KMS 规则；
public-access-block 四项全是 `true`。**拆除：** `aws s3 rb s3://$BUCKET --force`。

## 弧之外 —— 一个纯本地的 support 演练

上面那条三节弧需要一个沙箱账号。还有一个 lab **什么都不需要** —— 一个纯本地、只用标准库、能自我
验证的演练，接着那篇 [support 笔记](../support.md)，和这个仓库里别的那些可跑演练一个精神：

### `iam-deny-by-default/` —— IAM 策略求值 ✅ 已建（纯本地）

实现了 AWS 真实的策略求值顺序，并且在零凭据的情况下证明那条头号 support 教训 ——
**默认拒绝、显式 `Deny` 胜出、一条 SCP 或者一个 permissions boundary 连一个 admin 都能封顶**。见
**[`iam-deny-by-default/`](iam-deny-by-default/)**。

```bash
python3 iam-deny-by-default/iam_eval_drill.py   # exit 0 = 那些教训成立；在 CI 里跑
```

如果你真正在调的就是 IAM 的"Access Denied"，那就在那条云上弧之前先读它。

---

每个已建成的 lab 目录里都有：代码、一份带目标 + 该验证什么的 `README`，以及明确的拆除步骤。lab 会
随着这个模块成熟而增加。
