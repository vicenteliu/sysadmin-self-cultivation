---
kind: index
axis: platforms
themes: [cloud]
platforms: [azure]
derived: true
mirrors: platforms/azure/README.md
summary: "和 AWS 同样的四段式模板：它是什么 → 管理技能图 → AI 辅助 ramp → lab —— 外加四篇对应 AWS 那个做过的实例的更深姊妹笔记。"
---
# Azure

> 🌐 **语言：** [English（默认）](../../../../platforms/azure/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/azure/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 和 [AWS](../aws/README.md) 同样的四段式模板：**它是什么 → 管理技能图 → AI 辅助 ramp → lab**
> —— 外加四篇对应 AWS 那个做过的实例的更深姊妹笔记：**[architecture](architecture.md)**（它怎么
> 组织）、**[operations](operations.md)**（day-2 地跑它、那份运维活拆解、运营循环里的 AI）、
> **[automation](automation.md)**（把 API 写成脚本），以及 **[support](support.md)**
> （那门修/救手艺 —— Azure 加 Entra —— 而身份那一半是亲手做过的）。如果你读过 AWS 那个模块，
> 这里大部分就是*"那些概念里哪一个被改名成了什么，以及 Azure 的怪癖是什么？"* ——
> 而那恰恰是[运营模型](../../00-the-operating-model.md)的意义。

## 1. Azure 是什么

微软的云。和 AWS 是同一个想法 —— 一座你用 API 驾驶的租来的数据中心 —— 带着一股鲜明的微软味道：
身份被放在最前面（它是从 Active Directory 长出来的），而资源住在一个显式的层级里。

**那个组织层级是第一件要内化的东西**（它在 AWS 里没有干净的对应物）：

```
Microsoft Entra ID 租户            身份边界 —— 那个目录
└── Management Group              策略 / 组织分组
    └── Subscription              计费 + 隔离边界 ≈ 一个 AWS 账号
        └── Resource Group        生命周期容器 —— AWS 没有对应物
            └── Resources         VM、VNet、存储……
```

你创建的一切都住在一个 **subscription** 里的一个 **resource group** 里。搞懂这个，其余的就映射到
那[七片面](../../00-the-operating-model.md)上：

| 面 | Azure 的叫法 | 那一句话 |
| --- | --- | --- |
| **身份与访问** | **Microsoft Entra ID**（目录身份）+ **Azure RBAC**（资源访问）+ **Managed Identity** | 两套系统，不是一套 —— Entra = *你是谁*，RBAC = *你能碰什么*。把它们搞混是那个经典错误。 |
| **计算** | **Virtual Machines**、VM Scale Set、**Azure Functions**、**AKS**、App Service | 代码跑的地方。从一台 VM 起步；再毕业到 AKS/Functions。 |
| **网络** | **VNet**、subnet、**NSG**、route table（UDR）、**Load Balancer / App Gateway**、**Azure DNS**、Private Endpoint | 一个 VNet 是那个盒子；NSG 是那些防火墙规则。 |
| **存储与数据** | **Storage Account**（Blob/File/Queue/Table）、Managed Disk、**Azure SQL**、Cosmos DB | Blob 存储是默认的"我该把这个放哪儿？" |
| **发放与配置** | **Bicep** / ARM 模板、**Terraform**、**Azure CLI / PowerShell（Az）**、**Azure Policy** | Bicep 是 Azure 原生的 IaC；Terraform 是那个跨云的选择。 |
| **可观测性** | **Azure Monitor**（指标）、**Log Analytics** + KQL（日志）、App Insights（trace）、**Activity Log**（审计） | KQL 是你真正会用来回答"发生了什么？"的那门语言。 |
| **安全与合规** | **Defender for Cloud**、**Key Vault**、**Azure Policy**、Entra Conditional Access / **PIM**、**Cost Management + Budgets** | 用 Key Vault 放密钥；用 Policy 做护栏；用一个 Budget 让你不被意外。 |

## 2. 管理技能图

完整清单在 **[`skills-map.md`](skills-map.md)** 里。那些标题级能力：

- **身份做对（两层）** —— Entra ID 的 user/group/service principal，加上在正确范围
  （management group / subscription / resource group / resource）上的 Azure **RBAC** 角色分配；
  用 **Managed Identity** 好让没有任何东西携带一个密钥。
- **一个你自己设计的 VNet** —— subnet、**NSG**（以及 NSG 对上那个老的"全放行"默认值）、
  route table，以及*一台 VM 为什么出不去* —— 那第一号支持问题的 Azure 版本。
- **你跑得起来的计算** —— 从代码起一台带 managed identity 的 VM，**没有公网 IP、没有开着的 SSH**
  （通过 **Azure Bastion** 或者经 Entra 的 `az ssh` 够到它）。
- **默认值安全的存储** —— 一个关掉了公开访问、开着加密、并通过 RBAC 或者一个你真的理解的 SAS 做
  最小权限访问的 Storage Account。
- **一切从代码来** —— 同一套栈用 **Bicep** 或 **Terraform** 写出来，在版本控制里、`what-if`/`plan`
  过、并且删得掉（删掉那个 resource group → 它就没了）。
- **你会看见它坏掉** —— Azure Monitor 告警、Log Analytics 里的 **KQL**，以及用 Activity Log 查
  "谁改了这个？"
- **安全并且在预算内** —— 用 **Key Vault** 而不是把密钥放代码里；**Azure Policy** 护栏；
  一条 **Budget** 告警。

## 3. 通往胜任的那条 AI 辅助路径

方法在 **[`ai-ramp.md`](ai-ramp.md)** 里。专门针对 Azure 的短版本：你现在有两个锚 —— 本地基本功，
**以及**在你做完 AWS 那个模块之后，一整套云的心智模型。所以最快的提示词不是"教我 Azure"，而是
*"我懂 AWS 的 IAM/VPC/EC2/S3 和本地 AD —— 把每一个映射到它的 Azure 对应物上，并标出 Azure 真正
不同的地方（RBAC 对 Entra 角色、resource group、managed identity）。"* 然后生成那份 Bicep/Terraform
并**对着文档核实** —— Azure 那个双权限系统的分野和它的 resource provider 怪癖，恰恰是 AI 自信地
错着的地方。

## 4. Lab

可跑的练习在 **[`labs/`](../../../../platforms/azure/labs/)** 里 —— 和 AWS 同一个形状：一个受限身份
加一次 subscription 盘点（Azure Resource Graph / CLI），然后一个用 Terraform 写的、不用开端口就够
得到的最小 VNet 加 VM，然后 Key Vault 加 managed identity，然后一个 Budget。

## 5. 往深里走 —— architecture、operations、automation 与 support

四篇姊妹笔记把 Azure 带过"那些服务是什么"，对应 AWS 那一组：

- **[`architecture.md`](architecture.md)** —— Azure 是怎么**组织**的：把 management group →
  subscription → resource group 那个层级当成爆炸半径模型、region / zone / **配对 region**、
  被给足分量的那个**双权限平面**陷阱（Entra ID 角色对 Azure RBAC）、共担责任，以及一份参考三层
  架构。
- **[`operations.md`](operations.md)** —— day-2 地**跑** Azure：那份简报、那些运维笔记
  （公开的 blob、NSG 挂在子网还是网卡上、那次 Entra 对 RBAC 的拒绝）、**按节奏拆解**的那些反复
  出现的活，以及 **AI 怎么协助那条运营循环** —— 重点落在给 Log Analytics / Sentinel 写 KQL 上。
- **[`automation.md`](automation.md)** —— **把 ARM API 写成脚本**：那个
  `身份 → client → API 调用` 的模型、Azure 那架 **CLI 加一等 PowerShell** 的双高度阶梯、
  **managed identity** / `DefaultAzureCredential`（脚本里绝不放密钥）、那些规则
  （`ItemPaged` 分页、用 **Resource Graph** 做批量），以及只读审计与修复这两种形状。
- **[`support.md`](support.md)** —— **那门修/救手艺（Azure 加 Entra）**：支持 Azure 让你为什么
  负责、那些反复出现的工单以及*你去哪儿看*（`AuthorizationFailed` 的角色与范围检查、
  `MissingSubscriptionRegistration` 那个 provider 陷阱、用 Network Watcher 而不是 `tcpdump`），
  以及那些要**忘掉**的、承重的 AWS / 本地 AD 直觉 —— 其中**身份那一半是 🔨 亲手做过的**，
  配一个可跑的"Global Admin ≠ Owner" lab，以及一份验证过的 GitHub 现场工具包。

## 诚实边界

这里正是这个项目的诚实政策挣到饭钱的地方。**身份是我真正亲手做过的地方** —— 我做过初始的
Microsoft Entra ID / Azure AD 搭建，并在规模上跑过身份生命周期，所以 Entra/RBAC 这片面对我不是
理论。**生产规模上的资源管理那一侧**（大型 VNet 设计、生产里的 AKS、多 subscription 的 landing
zone）才是我在 ramp 的地方 —— 而这个模块诚实地记录那条 ramp，而不是把它打扮起来。这里的声称是
"一份很强的身份地基，加上一条通向其余部分的、快速且可验证的 ramp"，不是"十年 Azure"。
