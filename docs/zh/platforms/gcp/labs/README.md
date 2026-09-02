---
kind: lab
axis: platforms
themes: [cloud]
platforms: [gcp]
marker: "🧭"
derived: true
mirrors: platforms/gcp/labs/README.md
summary: "可跑、可拆的练习 —— 和 AWS 那些 lab 同一个形状，好让这些概念「迁移」过来。"
---
# GCP —— Lab

> 🌐 **语言：** [English（默认）](../../../../../platforms/gcp/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/gcp/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

可跑、可拆的练习 —— 和 [AWS 那些 lab](../../aws/labs/) 同一个形状，好让这些概念*迁移*过来。

> **地面规则：** 用一个**沙箱 project**（或者 Always-Free 层），先设一条**预算告警**，做完就把那个
> project 或者那些资源删掉。用 **IAP** 隧道够到那些 VM —— 绝不要把 SSH 开到互联网上。

## 为什么是命令行

每一个 lab 都是**命令行优先**的（`gcloud`）。控制台是用来*看*的；`gcloud` 是用来*做*的 ——
比一路翻菜单**更快**、**更精确**（不会留着一个选错的 project）、**可复现**（粘进一份 runbook）、
**可评审**（一份 diff，不是一张截图）—— 而且它就是你的自动化所用的那片界面。凡是你点得了的，
你都命令得了。

## 那条三节 lab 弧

### Lab 01 —— 受限身份 + 盘点

一个最小权限的 **service account**，然后盘点这个 project。注意 **Cloud Asset Inventory** 一次调用
就回答了组织范围的问题 —— 而且记住你常常要遍历的是 *project*，并且资源是分 zone/region 的：

```bash
gcloud auth login
gcloud config set project my-sandbox-project
gcloud config list                                   # 确认是对的那个 project

# 整个 project 一次调用 —— Cloud Asset Inventory（胜过把每个 API 都循环一遍）
gcloud asset search-all-resources --scope=projects/my-sandbox-project \
  --format="table(name, assetType, location)"

# 或者经典的逐服务列举（compute 是分 zone 的 —— 这条会跨 zone 列出来）
gcloud compute instances list --format="table(name, zone, machineType.basename(), status)"
gcloud storage buckets list --format="table(name, location, default_storage_class)"
```

**验证：** 只在一个资源上给那个 service account 授予 `roles/viewer`，扮演它
（`--impersonate-service-account`），然后看着其余的消失。

### Lab 02 —— 从代码起一套最小网络 + 计算

记住 GCP 那个异类之处：**VPC 是全局的**，子网是分 region 的。一个网络、一条以**标签**（不是一个
IP 段 —— 这是 GCP 的模型）为目标的防火墙规则，以及一台**没有外部 IP** 的实例：

```bash
gcloud compute networks create lab-vpc --subnet-mode=custom
gcloud compute networks subnets create lab-subnet \
  --network=lab-vpc --region=us-central1 --range=10.0.1.0/24
# 防火墙的目标是一个「标签」，不是一个 CIDR —— GCP 那个身份感知的模型
gcloud compute firewall-rules create allow-iap-ssh \
  --network=lab-vpc --direction=INGRESS --action=ALLOW --rules=tcp:22 \
  --source-ranges=35.235.240.0/20 --target-tags=lab   # 35.235.240.0/20 = IAP
gcloud compute instances create lab-vm \
  --zone=us-central1-a --subnet=lab-subnet --no-address --tags=lab \
  --machine-type=e2-micro
# 在「没有外部 IP」的情况下够到它 —— 走 IAP 隧道：
gcloud compute ssh lab-vm --zone=us-central1-a --tunnel-through-iap
```

**验证：** `gcloud compute instances describe lab-vm --zone=us-central1-a --format='value(networkInterfaces[0].accessConfigs)'`
返回空 —— 没有外部 IP。**拆除：** 删掉那台实例、那条防火墙规则、那个子网，然后
`gcloud compute networks delete lab-vpc`。

### Lab 03 —— 安全的存储 + 一条预算

默认就安全的存储（GCP 的默认值本来就强；把它们显式写出来），以及那条预算：

```bash
# 一个开了 uniform bucket-level access 的 bucket（没有遗留的逐对象 ACL）+ 一个存储类
gcloud storage buckets create gs://my-unique-lab-bucket-$RANDOM \
  --location=us-central1 --uniform-bucket-level-access --default-storage-class=STANDARD

# 证明经由遗留 ACL 的公开访问是不可能的（uniform access 把它们挡掉了）
gcloud storage buckets describe gs://$BUCKET --format='value(uniform_bucket_level_access)'

# 一条预算（在真实的 project 里这是「第一件」要做的事）—— 走计费 API
gcloud billing budgets create --billing-account=$BILLING_ACCT \
  --display-name=lab-budget --budget-amount=20USD \
  --filter-projects=projects/my-sandbox-project
```

**验证：** uniform-access 的值是 `True`；尝试设一个遗留的公开 ACL 会被拒绝。
**拆除：** `gcloud storage rm --recursive gs://$BUCKET`。

## 弧之外 —— 一个纯本地的 support 演练

上面那条三节弧需要一个沙箱 project。还有一个 lab **什么都不需要** —— 一个纯本地、只用标准库、能
自我验证的演练，接着那篇 [support 笔记](../support.md)：

### `gke-iam-vs-rbac/` —— GKE 的两个鉴权平面 ✅ 已建（纯本地）

给 GKE 的授权建了模，并且在零凭据的情况下证明那条头号 GKE support 教训 ——
**Cloud IAM 负责认证，Kubernetes RBAC 负责授权；`Unauthorized` ≠ `Forbidden`；IAM 的
"Cluster Admin" 不是集群内的 admin**。见 **[`gke-iam-vs-rbac/`](gke-iam-vs-rbac/)**。

```bash
python3 gke-iam-vs-rbac/gke_authz_drill.py   # exit 0 = 那些教训成立；在 CI 里跑
```

如果那张工单是"我是 Owner，可 kubectl 说 Forbidden"，那就在那条云上弧之前先读它。

---

每个 lab 落地时都带着代码（Terraform 是那个持久形态）、一份 `README`，以及明确的拆除步骤。一句
诚实的说明：GCP 是那条 🧭 ramp —— 这些是那条 ramp 被做成可跑的，而且在免费层上零成本。
