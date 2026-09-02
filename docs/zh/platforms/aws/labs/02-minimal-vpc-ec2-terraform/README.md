---
kind: lab
axis: platforms
themes: [iac-config, cloud]
platforms: [aws]
derived: true
mirrors: platforms/aws/labs/02-minimal-vpc-ec2-terraform/README.md
summary: "一个 VPC、一个公有子网和一个私有子网，以及一台不用打开任何一个入站端口就够得到的 EC2 —— 完全从 Terraform 立起来，再干净地拆掉。运营模型的第 3 招，按「从代码建，不是点出来」那条线来。"
---
# Lab 02 —— 从 Terraform 起一套最小 VPC + EC2

> 🌐 **语言：** [English（默认）](../../../../../../platforms/aws/labs/02-minimal-vpc-ec2-terraform/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/aws/labs/02-minimal-vpc-ec2-terraform/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 完全从代码立起一套小而*默认安全*的栈 —— 一个 VPC、一个公有子网和一个私有子网，以及
一台你**不用打开任何一个入站端口**就够得到的 EC2 —— 然后干净地把它拆掉。这是
[运营模型](../../../../00-the-operating-model.md)的第 3 招（用 API 驱动 + 把它写成代码），
也是[技能图](../../skills-map.md)里那条"从代码建，不是点出来"的线。

## 它建出什么

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

那些被刻意烤进去的教训：

- **没有 SSH，没有开放端口。** 你用 **SSM Session Manager** 够到那台机器，所以那个 security group
  有*零*条入站规则。这是相对于常见的"把 22 端口开给 0.0.0.0/0"的那个最大的现实收益。
- **没有烤进去的凭据。** 那台实例经由一个 instance profile 拿到一个 **IAM role** —— 绝不把访问
  密钥放在机器上。
- **默认私有。** 那台实例住在私有子网里，没有公网 IP；出网走 NAT。
- **实例上的安全默认值。** 要求 IMDSv2 + 加密的根卷。
- **不硬编码 AMI。** 最新的 AL2023 镜像是在 plan 阶段从一个 SSM 公共参数里解析出来的。

## 前置条件

- **Terraform** ≥ 1.5，以及一个**沙箱账号**的 AWS 凭据（`aws sts get-caller-identity` 跑得通）。
- AWS CLI 的 **SSM Session Manager 插件**（验证那一步要连进去用）。
- 这个账号上有一条 **Budget 告警**（见 lab 04）—— 每个地方做一次。

> ⚠️ **成本。** 这里几乎所有东西都对免费层友好，**除了那个 NAT gateway**（约 \$0.045/小时 +
> 流量）以及那个在分配期间的 Elastic IP。短短一个 lab 也就是几分钱，但**做完就
> `terraform destroy`** —— 一个被遗忘的 NAT 正是那个经典的"我账单怎么 \$35 了？"惊喜。

## 跑它

```bash
terraform init
terraform fmt -check      # 风格
terraform validate        # 配置在内部是自洽的
terraform plan            # 读一读它「将要」创建什么 —— 那个习惯才是重点
terraform apply           # 输入 yes
```

## 验证

```bash
# 那台实例「没有公网 IP、也没有开放端口」—— 而这条命令仍然给你一个 shell：
aws ssm start-session --target "$(terraform output -raw instance_id)" \
  --region "$(terraform output -raw region 2>/dev/null || echo us-west-2)"
```

- 你落在一台只有私有 IP、并且入站 security group 是空的主机的 shell 里。这就是全部的重点。
- 在控制台里确认：那台实例没有公网 IP、那个 SG 没有入站规则，并且这台实例在 Systems Manager →
  Fleet Manager 里显示为"已纳管"。

## 拆掉它

```bash
terraform destroy        # 输入 yes —— 把所有东西移除，包括那个 NAT
```

第二天在 Cost Explorer 里确认什么都没残留。干净的拆除是一项技能；每一次都练它。

## AI 在哪儿帮上了忙，你又该验证什么（见 [ai-ramp](../../ai-ramp.md)）

AI 起草这类 Terraform 很快。要**亲手验证**的那些部分：那套 NAT/路由表的确切接线（一条接错的路由
是头号"为什么上不了网"）、那个 SG 是不是真的没有入站、IMDSv2 的 `http_tokens = "required"`，
以及 `terraform destroy` 之后有没有留下任何会计费的东西。AI 写那份草稿；而 plan 的输出和一次干净
的 destroy 才是证据。
