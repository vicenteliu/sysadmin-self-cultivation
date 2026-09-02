---
kind: index
axis: platforms
themes: [cloud]
platforms: [gcp]
derived: true
mirrors: platforms/gcp/README.md
summary: "每一个平台模块所遵循的那份模板：它是什么 → 管理技能图 → AI 辅助 ramp → lab —— 外加四篇对应 AWS 那个做过的实例的更深姊妹笔记。"
---
# Google Cloud Platform（GCP）—— 第三朵云

> 🌐 **语言：** [English（默认）](../../../../platforms/gcp/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/gcp/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 每一个平台模块所遵循的那份模板：**它是什么 → 管理技能图 → AI 辅助 ramp → lab** ——
> 外加四篇对应 AWS 那个做过的实例的更深姊妹笔记：**[architecture](architecture.md)**（它怎么
> 组织）、**[operations](operations.md)**（day-2 地跑它、那份运维活拆解、运营循环里的 AI）、
> **[automation](automation.md)**（把 API 写成脚本去管理并运维它），以及 **[support](support.md)**
> （那门修/救手艺 —— GCP 加 GKE —— 以及一个 AWS 管理员要接手它必须忘掉什么）。和
> [`aws/`](../aws/README.md) 与 [`azure/`](../azure/README.md) 是同一个形状。GCP 是那套 ramp 方法
> 得到最干净检验的地方 —— 它大部分是改了名的 AWS/Azure，外加几处真正的结构性差别要抓住。

## 1. GCP 是什么

Google Cloud 是一座你用 API 驾驶的租来的数据中心 —— 和 AWS、Azure 是同一笔交易，只不过跑在
Google 为跑搜索和 YouTube 而建的那张织物上。对一个已经在一朵云上把那[七片面](../../00-the-operating-model.md)
映射过的管理员来说，GCP 基本是一次词汇练习 —— **除了**少数几个 Google 做了真正不同设计选择的地方，
而那些正是"GCP 不就是换了个 logo 的 AWS"会烧到你的地方。那个标题级差别：**VPC 是全局的**。

映射到那七片面上：

| 面 | GCP 对它的叫法 | 那一句话 |
| --- | --- | --- |
| **身份与访问** | **Cloud IAM**（role + binding）、service account、Cloud Identity | role 在资源上绑定到 member 上；service account 就是那个工作负载身份的故事。 |
| **计算** | **Compute Engine**（VM）、**Cloud Run**（serverless 容器）、**GKE**（Kubernetes）、Cloud Functions | 代码跑的地方。机型**外加一个自定义尺寸旋钮**；GKE 是那个参照级的 Kubernetes。 |
| **网络** | **VPC（全局！）**、区域级 subnet、防火墙规则、Cloud NAT、Cloud Load Balancing（全局 anycast） | 那个结构上的异类：一个 VPC 能横跨整个星球；subnet 是区域级的。 |
| **存储与数据** | **Cloud Storage**（对象）、**Persistent Disk / Hyperdisk**（块，zonal **或** regional）、Filestore、Cloud SQL / Spanner | 比 AWS 那一摊更少、更正交的产品。 |
| **发放与配置** | **gcloud**、**Terraform**、project 加组织层级 | project 是那个账号/爆炸半径单位；那个组织层级是护栏面。 |
| **可观测性** | **Cloud Operations** —— Monitoring、Logging、Trace —— 带**原生 SLO 工具** | Google 的 SRE 血统露了出来：SLO 是内建的，不是外挂的。 |
| **安全与合规** | Cloud IAM、**Security Command Center**、Org Policy、默认开启的加密、**Budgets** | 默认安全的姿态；Org Policy 是那道预防性护栏。 |

知道那些服务名以及每一个属于哪片面，你就能进行一场真正的 GCP 对话。那张图和 AWS 的几乎一模一样
—— 而那恰恰是重点。

## 2. 管理技能图

一份具体的、可勾选的清单，列出一个 GCP 管理员必须**做得到**什么。带熟练度分层的完整清单在
**[`skills-map.md`](skills-map.md)** 里。那些标题级能力，并把 GCP 特有的差量点出来：

- **IAM 做对** —— 在资源层级上的 role 加 binding；把 **service account** 当作工作负载身份
  （机器上不放密钥）；primitive 对 predefined 对 custom 角色那个区分。
- **一个你自己设计的网络 —— 记住它是全局的** —— 一个 VPC、**区域级 subnet**、瞄准 tag/service
  account 的防火墙规则；那个在这里"只是路由"、而在别处需要 peering 的多区域设计
  （[`the-stack/02`](../../the-stack/02-network.md)）。
- **你跑得起来也扩得动的计算** —— 从代码起 Compute Engine、**自定义机型**（把 vCPU/内存拨到准确
  数值）、instance template → Managed Instance Group、热迁移。
- **默认值正确的存储** —— Cloud Storage 的存储类别加访问控制；把 **regional Persistent Disk**
  当成一个比锁在 AZ 里的 block 更干净的 HA 原语。
- **一切从代码来** —— 对着 GCP 的 Terraform；把 **project 和那个组织层级**当作结构和爆炸半径模型。
- **你会看见它坏掉** —— Cloud Monitoring 告警、Cloud Logging 查询，以及那套**内建的 SLO 工具**
  （[`the-stack/06`](../../the-stack/06-observability.md)）。
- **安全并且在预算内** —— **先设一条预算告警**、默认开启的加密、**Org Policy** 护栏、
  Security Command Center（[`the-stack/07`](../../the-stack/07-security.md)）。
- **GKE** —— 那个参照级的托管 Kubernetes；见
  [`cross-cutting/kubernetes.md`](../../cross-cutting/kubernetes.md)。

## 3. 通往胜任的那条 AI 辅助路径

那套方法 —— 在几天里从"懂 AWS/Azure 加本地"走到"能运维 GCP" —— 在 **[`ai-ramp.md`](ai-ramp.md)**
里。用一段话说：

GCP 是这个仓库那个论点最纯粹的演示，因为它有那么大一部分是别处已经映射过的那些面的一次*改名*。
用 AI 去翻译 —— *"我懂 AWS 的 VPC 和 IAM；把 GCP 的网络和 IAM 映射到它们上面，并且只标出那些真正
的差别"* —— 而那条 ramp 基本就是去猎那四个结构性异类（全局 VPC、project/组织层级、自定义机型、
以 service account 为中心的 IAM）。然后对着当前文档核实每一个角色名和每一个 API，并在一个带预算
告警的沙箱里跑它。AI 写第一稿；你那份在 AWS/Azure 和本地挣来的判断，是那道评审闸门。

## 4. Lab

读一个全局 VPC 和建一个全局 VPC 是两种不同的技能。一条**三段式 CLI arc（guided run）**（受限身份加盘点 →
全局 VPC 网络加实例 → 安全存储加预算）在 **[`labs/`](labs)** 里，
配真实的 `gcloud` 命令 —— 第二个 lab 正是那个全局 VPC 模型明显改变命令、和 AWS 版本拉开差距的
地方。

## 5. 往深里走 —— architecture、operations、automation 与 support

四篇姊妹笔记把 GCP 带过"那些服务是什么"，对应 AWS 那一组：

- **[`architecture.md`](architecture.md)** —— GCP 是怎么**组织**的：把那个资源层级
  （Org → Folder → Project）当成爆炸半径单位、region 与 zone、那个**全局 VPC 异类**、
  以 service account 为中心的 IAM、共担责任，以及一份展示每一片面组合起来的参考三层架构。
- **[`operations.md`](operations.md)** —— day-2 地**跑** GCP：那份简报、那些运维笔记（什么会把你
  叫醒）、**按节奏拆解**的那些反复出现的活，以及 **AI 怎么协助那条运营循环** —— 包括 AI 在 GCP 上
  那个特有的陷阱：递给你 AWS 形状的（区域级 VPC 的）建议。
- **[`automation.md`](automation.md)** —— **把 API 写成脚本**：那个 `身份 → client → API 调用`
  的模型、`gcloud` 对客户端库对 Terraform 那架高度阶梯、ADC 和挂上去的 service account
  （脚本里绝不放一个密钥文件）、那些规则（遍历 project/region/zone、批量用 Cloud Asset Inventory、
  幂等、先只读），以及只读审计与修复这两种形状。
- **[`support.md`](support.md)** —— **那门修/救手艺（GCP 加 GKE）**：支持 GCP 让你为什么负责、
  那些反复出现的工单以及*你去哪儿看*（`403 PERMISSION_DENIED` 的层级走查、那个全局 VPC 防火墙，
  以及那次 GKE 深潜 —— 那个 auth 插件、**IAM 对 RBAC 那两个平面**、`IP_SPACE_EXHAUSTED`），
  以及一个管理员必须**忘掉**的那些承重的 AWS 直觉 —— 配一个可跑的 GKE auth lab 和一份验证过的
  GitHub 现场工具包。

## 诚实边界

🧭 **诚实的 ramp —— 而且被那样标着。** 不声称任何生产 GCP 运维：这个模块是那套可迁移的运营模型
（AWS/Azure 的那些面加上本地的深度）被映射到 GCP 的名字上、并对着当前文档验证过 —— 恰好就是
[`WHY.md`](../../WHY.md) 所论证的那套 ramp 方法。那些结构性差别（全局 VPC、project、自定义机型、
service account IAM）被点出来，恰恰因为它们正是"GCP 不就是 AWS"这个反射失效的地方。这里的声称不是
"多年 GCP"；而是"一套可迁移的模型，加上一条快速、可验证的 ramp" —— 和这个仓库里每一个 🧭 模块
同样诚实的立场。
