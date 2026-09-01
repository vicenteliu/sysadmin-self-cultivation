---
kind: roadmap
axis: start-here
themes: []
platforms: [aws, azure, gcp, oci]
derived: true
mirrors: ROADMAP.md
summary: "这个项目按需求优先构建。下面的顺序由每项技能在真实的基础设施 / 平台 / IT 工程岗位描述里出现的频率决定 —— 让仓库朝着市场真正要的东西生长。"
---
# Roadmap

> 🌐 **语言：** [English（默认）](../../ROADMAP.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`ROADMAP.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 这个项目按**需求优先**构建。下面的顺序由每项技能在真实的**基础设施 / 平台 / IT 工程
> 岗位描述**里出现的频率决定 —— 让仓库朝着市场真正要的东西生长，而不是朝着一份随意的
> 教学大纲。

## 需求信号

在大约 40 份近期美国 infra / platform / IT-engineering 岗位描述的样本里，被要求最多的
技术技能大致聚成这样（按频率粗排）：

| 集群 | 以什么形式出现 | 大约多频繁 |
| --- | --- | --- |
| **Linux + 脚本** | Linux（RHEL/Ubuntu）、Python、Bash | 接近全覆盖 |
| **Identity & access** | AD、Entra/Azure AD、Okta、SSO/SAML/OIDC、SCIM、IAM/RBAC、least-privilege、joiner/mover/leaver | 非常高（最密的单一集群） |
| **Endpoint & MDM** | macOS、Windows、Jamf、Intune、PXE/imaging、打补丁 | 非常高 |
| **网络** | TCP/IP、DNS、DHCP、路由/交换、防火墙（Palo Alto/Fortinet）、VPN | 高 |
| **IaC 与配置管理** | Ansible、Terraform、Git/CI-CD、Puppet | 高 |
| **安全与合规** | 加固/基线、EDR/XDR、SIEM、zero-trust、SOC 2 / SOX / GDPR / FedRAMP | 高 |
| **虚拟化** | VMware/vSphere/ESXi、KVM、Proxmox | 高 |
| **云** | AWS、Azure、GCP、OpenStack、OCI | 中—高 |
| **容器** | Kubernetes（EKS/AKS/GKE）、Docker | 中 |
| **可观测 / SRE** | 监控、SLI/SLO、事件响应 | 中 |
| **协作 / SaaS** | Google Workspace、M365、ITSM、企业 AI 工具 | 中 |

塑造这个仓库的结论是：这些岗位的重心在**运维与自动化那条 lane** —— Linux + 脚本 +
endpoint + **身份** + 配置管理 —— 而云只是其中若干个重要面之一。所以 roadmap 以能跨每
个平台迁移的**横切**技能开路，并把每一朵云当作**验证**这套模型的地方，而不是全部目的。

## 状态

| 领域 | 模块 | 状态 |
| --- | --- | --- |
| 论点 | [`00-the-operating-model.md`](00-the-operating-model.md) | ✅ |
| 论点 | [`WHY.md`](WHY.md) | ✅ |
| 方法 | [`ai-workflow/`](ai-workflow/) | ✅ |
| 平台 | [`platforms/aws/`](platforms/aws/) | ✅ + 2 个可跑 lab |
| 平台 | [`platforms/azure/`](platforms/azure/) | ✅（lab 已规划） |
| 横切 | [`cross-cutting/identity-iam.md`](cross-cutting/identity-iam.md) | ✅ |
| 分层系列 | [`the-stack/01-physical.md`](the-stack/01-physical.md) —— 物理层，七个平台对比 | ✅ |
| 分层系列 | [`the-stack/02-network.md`](the-stack/02-network.md) —— 网络层（覆盖 Tier-1 第 2 项） | ✅ |
| 分层系列 | [`the-stack/03-compute-and-images.md`](the-stack/03-compute-and-images.md) —— 计算与镜像流水线 | ✅ |
| 分层系列 | [`the-stack/04-storage.md`](the-stack/04-storage.md) —— 存储层（block/file/object、备份） | ✅ |
| 分层系列 | [`the-stack/05-platform-services.md`](the-stack/05-platform-services.md) —— 平台服务（自建 vs 租用） | ✅ |
| 分层系列 | [`the-stack/06-observability.md`](the-stack/06-observability.md) —— 可观测（三支柱、SLI/SLO、OTel；覆盖 Tier-3 第 9 项） | ✅ |
| 分层系列 | [`the-stack/07-security.md`](the-stack/07-security.md) —— 安全（责任共担、纵深防御、CSPM/EDR/SIEM；覆盖 Tier-2 第 6 项） | ✅ |
| 分层系列 | **the-stack 01→07 完成** —— 五层自底向上 + 可观测 + 安全（两顶横切的帽子） | ✅ |
| 分层 lab | [`the-stack/labs/04-backup-not-snapshot/`](../../the-stack/labs/04-backup-not-snapshot/) —— 可跑的纯 Python "复制不是备份" drill | ✅ |
| 可跑 lab | 另外 3 个纯本地、自验证的 lab（退出 0 = 教训成立）：[failure-domains](../../the-stack/labs/01-failure-domains/)（Python）、[idempotence-drill](../../foundations/labs/idempotence-drill/)（bash）、[ci-cd-pipeline](../../cross-cutting/labs/ci-cd-pipeline/)（带测试的应用 + 真实 GitHub Actions workflow） | ✅ |
| Agent Skills | 7 个 [`.claude/skills/`](../../.claude/skills/) 把仓库的方法打包：platform-ramp · honesty-audit · author-module · runnable-lab · diagram-module · mirror-zh · interview-drill —— 加上下面三个驱动工具箱的，共十个 | ✅ |
| 路线 | [`build-out/`](build-out/) —— 一间百人办公室端到端，**16 步全部完成**；它承载顺序与依赖，实质内容指回各条轴。依赖图已验证无环且对称；94% 的步骤挂着一个可跑 lab 或工具；[`GAPS.md`](build-out/GAPS.md) 记录这个场景发现缺了什么（[ADR-0001](../../docs/adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)） | ✅ |
| 浏览器 | [`site/`](site/README.md) —— 同一批材料，带导航、二十万词的全文搜索、🌐 切换和渲染好的图。两种启动方式，两种都不用装东西。它是一个**视图**，不是第七条轴（[ADR-0005](../../docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)）；依赖是提交进来的而不是生成的（[ADR-0006](../../docs/adr/0006-the-viewer-vendors-its-dependencies.md)） | ✅ |
| 图 | 4 张品牌门面图（轴图 · the stack · ramp · 路线），手写一次，由 [`site/build-diagrams.py`](../../site/build-diagrams.py) 派生成 12 个产物，外加文档内的 109 张 mermaid（算上中文镜像是 119 张）。媒介由 [ADR-0007](../../docs/adr/0007-a-figures-medium-is-decided-by-what-renders-it.md) 决定 | ✅ |
| 框架 | [`CONTENTS.md`](CONTENTS.md) + 每个规划模块的开篇（foundations/endpoint/iac/saas/k8s/cost/gcp） | ✅ |
| Foundations | [`foundations/`](foundations/) —— Linux 心智模型、调试反射、脚本、诚实的范围界定（Tier-3 第 10 项） | ✅ 已写 |
| Endpoint | [`endpoint/`](endpoint/) —— MDM 模型、装机流水线、补丁/EDR、BYOD、Intune 作为 ramp（Tier-2 第 5 项），外加三篇承载底下设计的 companion：跨三个操作系统的 [provisioning](../../endpoint/provisioning.md)、[management](../../endpoint/management.md)、以及 [encryption and keys](../../endpoint/encryption-and-keys.md) —— 那件这个仓库点名过三次却从没展示的密钥托管的活 | ✅ |
| SaaS 管理 | [`cross-cutting/saas-admin.md`](cross-cutting/saas-admin.md) —— Google Workspace / M365、身份主干、SCIM 生命周期（Tier-3 第 11 项） | ✅ 已写 |
| IaC 与配置 | [`cross-cutting/iac-and-config.md`](cross-cutting/iac-and-config.md) —— 供给 vs 配置、Terraform state、Ansible、漂移（Tier-1 第 3 项） | ✅ 已写 |
| 成本 | [`cross-cutting/cost.md`](cross-cutting/cost.md) —— 把成本当成运维信号、形状、意外、right-sizing、异常告警 | ✅ 已写 |
| Kubernetes | [`cross-cutting/kubernetes.md`](cross-cutting/kubernetes.md) —— 对象模型、控制面、CNI/CSI 的渗漏、Pending vs CrashLoop（Tier-2 第 8 项） | ✅ 已写 |
| **横切** | **所有专门笔记均已写完**（identity · saas-admin · iac · cost · kubernetes）；网络/存储/虚拟化/可观测/安全在 the-stack 里覆盖 | ✅ |
| 补缺 | [`cross-cutting/ci-cd.md`](cross-cutting/ci-cd.md) —— CI/CD 与 GitOps（相对 roadmap.sh/devops 最大的缺口）；🔨 自动化底子上的 🧭 ramp | ✅ 已写 |
| 补缺 | [`cross-cutting/databases.md`](cross-cutting/databases.md) —— 运维数据库（备份/PITR、复制、自建 vs 托管）—— **🔨**（生产 PostgreSQL） | ✅ 已写 |
| 补缺 | [`cross-cutting/itsm-and-assets.md`](cross-cutting/itsm-and-assets.md) —— ITSM、CMDB、资产对账、访问治理 —— **🔨**（ServiceNow 五年、审计自动化） | ✅ 已写 |
| 补缺（第二批） | [`service-mesh`](cross-cutting/service-mesh.md)（发现 + mesh，🧭）· [`web-and-tls`](cross-cutting/web-and-tls.md)（反向代理 + 证书生命周期，🔨 基本功）· [`incident-response`](cross-cutting/incident-response.md)（生命周期、on-call、复盘） | ✅ 已写 |
| 原创 | [`working-with-security`](cross-cutting/working-with-security.md) —— 运维者视角的安全：与 InfoSec/SOC 协作 + MITRE ATT&CK 意识；🔨 运维安全 vs 🧭 专家。选择自己写而不是引入（这是与外部安全体系建立关系的诚实方式） | ✅ 已写 |
| 平台 | [`platforms/gcp/`](platforms/gcp/) —— README + skills-map + ai-ramp（global-VPC 的异类；Tier-1 第 4 项）；lab 已出规格 | ✅ 已写 |
| 平台深度 | [`platforms/aws/architecture.md`](../../platforms/aws/architecture.md) + [`operations.md`](../../platforms/aws/operations.md) + [`automation.md`](../../platforms/aws/automation.md) —— 账号模型、day-2 运维工作拆解、AI 在环、给 API 写脚本 | ✅ 已写 |
| 平台深度 | Azure + GCP 的 architecture/operations/automation 三件套（对齐 AWS） | ✅ 已写 |
| 私有云 | [`platforms/vsphere/`](../../platforms/vsphere/) —— 🔨 亲手做过（VCP6-DCV/NV、区域 vCenter 管理员）+ [`platforms/openstack/`](../../platforms/openstack/) —— 🧭 ramp，与 KVM 邻接 | ✅ 已写 |
| 平台补齐 | [`platforms/oci/`](platforms/oci/) —— 🧭 第四朵云 + [`platforms/self-host/`](../../platforms/self-host/) —— 🔨 最深的根。**the-stack 的七个平台现在都有模块** | ✅ 已写 |
| Labs | **每个平台一条三段式 CLI arc**（7×3 = 21 个 lab）—— 受限身份盘点 → 从代码起网络与计算 → 安全默认/signature drill，每个都带真实命令行示例（CLI 优先于 GUI） | ✅ 已写；AWS 01/02 可跑 |
| 平台深度 | **vSphere + self-host** 的 architecture/operations/automation 三件套 —— 这两个 🔨 平台的深度现在与 AWS/Azure/GCP 齐平（从生产环境写出来的） | ✅ 已写 |
| 平台深度 | **OCI + OpenStack** 的 architecture/operations/automation 三件套（🧭 ramp）。**七个平台现在都带全套三件套** —— 平台深度对称 | ✅ 已写 |
| 技能图 | [`cross-cutting/skills-maps/`](cross-cutting/skills-maps/) —— 平台技能图的**转置**：一个主题横跨全部七个平台，按可迁移性而非按云分层。[networking](cross-cutting/skills-maps/networking.md)（63 格）+ [identity](cross-cutting/skills-maps/identity.md)（58 格）；两个最密的需求集群优先 | ✅ |
| 面试 | [`cross-cutting/interview/`](cross-cutting/interview/) —— 技能图的再一次转置，这回从面试官那一侧：[networking](cross-cutting/interview/networking.md)（21 问）+ [identity](cross-cutting/interview/identity.md)（19 问）。答案的形状由小节的 marker 决定（[ADR-0004](../../docs/adr/0004-interview-answers-are-evidence-for-a-marker.md)）；六个 🔨 答案仍带 ⏳ | ✅ |
| AI 方法 | [`ai-workflow/ai-in-the-day-job.md`](../../ai-workflow/ai-in-the-day-job.md) —— 稳态而非 ramp：分诊 → 变更 → 事件 → 复盘 → 扫尾，每一段都点名交出去什么、在哪里收回来 | ✅ |
| 检索 | 156 个文件上的 front-matter 作为唯一来源 + [`docs/build-index.py`](../build-index.py) → [`docs/index.json`](../index.json)（191 条记录，镜像标 derived）。面向 agent；幂等，`--check` 报告过期 | ✅ |
| 站点设计 | [`cross-cutting/site-network-design.md`](cross-cutting/site-network-design.md) —— 从参考办公室的参数到一份设计之间的那一步，海拔与分层章节相同。与 [`the-reference-office.md`](the-reference-office.md) 配对，后者现在在空间参数之外承载**六个参数域** —— 人员流动、终端与备机、身份形状、SaaS 清册、支持负载、数据与恢复 —— 每一个都是因为某个 lab 或某一步已经被迫编造过它才写的，且都记在那个文件自己的需求账本里。`Reference build` 保持 ⏳，因为没有哪一步需要型号；`Where things run` **两半都已写完** —— 四样东西留在这层楼或某朵云上，六样被考虑过并被拒绝，而后者是更短也更有用的那份清单 | ✅ |
| 走读 | [`walkthrough/`](walkthrough/README.md) —— 第二条路线，是念的不是读的：格式、五条决策（[ADR-0009](../../docs/adr/0009-the-walkthrough-ships-its-script-not-its-audio.md)–[0013](../../docs/adr/0013-godot-is-a-design-tool-and-the-floor-keeps-one-palette.md)）以及 viewer 的注册都已写完，而且**目前共三篇走读已建成** —— 01 · 网络（106 拍）、02 · 第一个星期一（93 拍）与 03 · 它坏掉的那一天（102 拍），各两种语言，播放在同一张可交互的二维楼面上。稿子进仓库，音频永远不进。像 `toolbox/` 那样一次长一篇，没有目标篇数 | ✅ |
| **Roadmap** | **所有分层条目均已落地** —— 每个规划模块都有已写的内容；剩下的工作是 lab + `docs/zh/` 镜像 + 深化 | ✅ |

## 构建顺序（需求驱动）

> **注（2026-07）：** 分层优先的系列 [`the-stack/`](the-stack/) 现在是下面若干条目
> 的载体 —— 网络（#2）落在 `the-stack/02-network.md`，虚拟化（#7）从
> `the-stack/01-physical.md` 起一路承载，OpenStack/OCI（#11）在每一章里被对比，而不是
> 后期各拿一个独立目录。

### Tier 1 —— 投入产出最高（需求最高、最可迁移）

1. **`cross-cutting/identity-iam.md`** —— ✅ *已完成。* 最密的需求集群
   （AD / Entra / Okta / SSO / SCIM / RBAC / 生命周期），也是跨每个平台最可迁移的那个面。
2. **`cross-cutting/networking.md`** —— 每个岗位都默认你有的云/本地网络基本功
   （TCP/IP、DNS、DHCP、路由、防火墙、负载均衡）。
3. **`cross-cutting/iac-and-config.md`** —— 把 Terraform + Ansible + Puppet 当作一个
   通用控制面。（Ansible 是被点名最多的单一工具之一。）
4. **`platforms/gcp/`** —— 补齐三朵云的叙事；结构对齐 AWS/Azure。

### Tier 2 —— 高需求、有真深度

5. **`endpoint/`** —— 给 endpoint/MDM 那条 lane 一条一等公民的轨道（Jamf、Intune、
   PXE/imaging、打补丁、macOS/Windows 机队）—— 一个需求非常高、而平台目录覆盖不到的领域。
6. **`cross-cutting/security-compliance.md`** —— 加固/基线、EDR/XDR、SIEM、zero-trust，
   以及点名的合规（SOC 2 / SOX / GDPR / FedRAMP / ISO 27001）。
7. **`cross-cutting/virtualization.md`** —— VMware/vSphere、KVM、Proxmox。
8. **`cross-cutting/kubernetes.md`** —— 容器 + 编排，横跨 EKS/AKS/GKE。

### Tier 3 —— 补全

9. **`cross-cutting/observability.md`** —— metric/log/trace、SLI/SLO、事件响应。
10. **`foundations/`** —— Linux + 脚本（Python/Bash/PowerShell）作为默认底子，明确写出来。
11. **`cross-cutting/storage.md`**、SaaS 管理（Google Workspace / M365），以及按需增加
    的平台（OpenStack、OCI）。

## 工具箱这条线（2026-07 开启）

上面所有内容都在**解释**；[`toolbox/`](toolbox/) 让它**能跑** —— 小而自足、可被 agent
调用的工具，遵循同一套需求优先的排序（分诊、身份生命周期、打补丁、加固，正是 JD 真正
要求运维者去做的事）。章程和约定在 [`toolbox/README.md`](toolbox/README.md)。已交付：
第一波脚本、[Ansible roles](toolbox/ansible/)（修复的那一半）、三个包装这些工具好让 AI
agent 能驱动它们的用户侧 [Agent Skill](../../.claude/skills/)（linux-triage /
harden-baseline / toolbox-picker），以及把上述所有东西按环境打包的
[生成器](toolbox/generate/)。这条线现在按需求一件工具一件工具地生长 —— 最新的是
**虚拟化那一波**（用标准库 SOAP 做 vSphere 盘点、VMware→Proxmox 的逐 VM 评估、
Proxmox 侧的镜像、以及跨 hypervisor 的快照卫生；生成器里的
`--profile escape-vmware`）。

## 这件事怎么保持诚实

每个模块都标注哪些是**亲手做过的深度**、哪些是**诚实的 ramp** —— roadmap 的权重偏向
把强项写好，**同时**把常见缺口可见地补上，而不是假装水平均匀。为什么这个区分就是全部
的意义，见 [`WHY.md`](WHY.md)。
