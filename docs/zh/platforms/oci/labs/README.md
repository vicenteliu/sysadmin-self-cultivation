---
kind: lab
axis: platforms
themes: [cloud]
platforms: [oci]
marker: "🧭"
derived: true
mirrors: platforms/oci/labs/README.md
summary: "可跑、可拆的练习 —— 和 AWS 那些 lab 同一个形状。"
---
# OCI —— Lab

> 🌐 **语言：** [English（默认）](../../../../../platforms/oci/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/oci/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

可跑、可拆的练习 —— 和 [AWS 那些 lab](../../aws/labs/) 同一个形状。OCI 的 **Always Free 层**让
这些真的零成本。

> **地面规则：** 用一个专用的 **compartment**，先设一条**预算**，做完就把资源终结掉。经一台
> bastion 或者一个私有子网够到那些实例 —— 绝不要把 SSH 开到互联网上。

## 为什么是命令行

每一个 lab 都是**命令行优先**的（`oci`）。控制台是用来*看*的；命令行是用来*做*的 —— **更快**、
**更精确**、**可复现**、**可评审**，而且就是你的自动化所用的那片界面。凡是你点得了的，你都
命令得了。

## 那条三节 lab 弧

### Lab 01 —— 受限身份 + 盘点

一个 **compartment**（OCI 的爆炸半径单位）和一条最小权限**策略**，然后盘点。OCI 的策略语言读起来
像句子 —— 比 JSON 好看：

```bash
oci setup config                                     # 一次性：生成 ~/.oci/config
oci iam region list --output table                   # 确认连通性

# 创建一个 compartment（那个隔离/爆炸半径单位）
oci iam compartment create --name lab --description "lab compartment" \
  --compartment-id "$OCI_TENANCY"

# 一条人读得懂的最小权限策略
oci iam policy create --name lab-read --compartment-id "$OCI_TENANCY" \
  --statements '["Allow group Readers to read all-resources in compartment lab"]' \
  --description "read-only in lab"

# 盘点这个 compartment
oci compute instance list --compartment-id "$LAB_COMPARTMENT" \
  --query 'data[].{name:"display-name", shape:shape, state:"lifecycle-state"}' --output table
```

**验证：** 把那条策略的动词从 `read` 改成 `inspect`，然后看看一个 Readers 成员还调得动哪些 ——
那个策略语言被变具体了。

### Lab 02 —— 最小 VCN + 实例

一个 **VCN**（分 region 的）、一个子网，和一台实例。注意 OCI 那个过滤选择 —— **在 security list
和 NSG 之间挑一个，然后统一下来**（这个 lab 用 VCN 的默认 security list，之后你会刻意切到 NSG）：

```bash
# 那条快路径：一条相当于向导的命令搞定 VCN + 子网 + 网关
oci network vcn create --compartment-id "$LAB" --cidr-blocks '["10.0.0.0/16"]' \
  --display-name lab-vcn
oci network subnet create --compartment-id "$LAB" --vcn-id "$VCN_ID" \
  --cidr-block 10.0.1.0/24 --display-name lab-subnet

# 一台 flexible shape 的实例 —— 记住：一个 OCPU 是一个「完整核心」，不是一个超线程
oci compute instance launch --compartment-id "$LAB" \
  --availability-domain "$AD" --subnet-id "$SUBNET_ID" \
  --shape VM.Standard.E4.Flex --shape-config '{"ocpus":1,"memoryInGBs":8}' \
  --image-id "$UBUNTU_IMAGE" --assign-public-ip false \
  --metadata '{"ssh_authorized_keys":"'"$(cat ~/.ssh/id_rsa.pub)"'"}'
```

**验证：** `oci compute instance list --compartment-id "$LAB" --query 'data[].shape'`
显示那个 flex shape；那台实例没有公网 IP。**拆除：** 终结那台实例，然后删掉子网和 VCN。

### Lab 03 —— 对象存储 + 一条预算

Object Storage（OCI 出网便宜这个优势，让它成为一个不错的备份目标），以及一条预算：

```bash
# 一个私有 bucket
oci os bucket create --compartment-id "$LAB" --name lab-bucket$RANDOM \
  --public-access-type NoPublicAccess

# 放一个对象进去，然后列出来
echo "canary" > canary.txt
oci os object put --bucket-name "$BUCKET" --file canary.txt
oci os object list --bucket-name "$BUCKET" --query 'data[].name' --output table

# 一条挂在这个 compartment 上的预算（现实里这是「第一件」要做的事）
oci budget budget create --compartment-id "$OCI_TENANCY" \
  --amount 20 --reset-period MONTHLY --target-type COMPARTMENT \
  --targets '["'"$LAB"'"]' --display-name lab-budget
```

**验证：** `oci os bucket get --bucket-name "$BUCKET" --query 'data."public-access-type"'`
返回 `NoPublicAccess`。**拆除：** 先删那个对象，再删那个 bucket。

## 弧之外 —— 一个纯本地的 support 演练

上面那条三节弧需要一个（Always-Free 的）tenancy。另外还有一个**零成本、零凭据**的演练，用大约
200 行标准库 Python 给 OCI 那些标志性的访问教训建了模 —— 到哪儿都跑得起来，在 CI 里也是：

- [`a-compartment-is-not-an-account/`](a-compartment-is-not-an-account/) —— 为什么**没有策略 →
  `NotAuthorizedOrNotFound`（一个 404，不是一个 403）**、那些动词怎么嵌套成
  **`inspect ⊂ read ⊂ use ⊂ manage`**，以及一条策略怎么**沿 compartment 树往下继承、却停在一个
  兄弟节点前面**。`python3 verb_and_compartment_drill.py` → 教训成立则 exit `0`；
  `--sabotage verbs` 或者 `--sabotage scope` 会故意把那个模型弄坏，然后那些断言失败。与
  [OCI support 笔记](../support.md)配对。

---

每个 lab 落地时都带着代码（Terraform / Resource Manager 是那个持久形态）、一份 `README`，以及明确
的拆除步骤。一句诚实的说明：OCI 是一条 🧭 ramp —— Always-Free 层让它成为一条跑得起来的 ramp。
