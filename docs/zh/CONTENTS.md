---
kind: index
axis: start-here
themes: []
platforms: [aws, azure, gcp, oci]
derived: true
mirrors: CONTENTS.md
summary: "详细索引：每个模块是什么、住在哪。"
---
# 目录 —— 整张地图

> 🌐 **语言：** [English（默认）](../../CONTENTS.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`CONTENTS.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 详细索引：每个模块是什么、住在哪。
> [`README.md`](README.md) 是正门和形状；[`ROADMAP.md`](ROADMAP.md) 说**下一步建什么、
> 为什么**；这一页是目录。

这个项目沿**六条轴**横穿同一批材料 —— 你从哪条进来，取决于你的问题是什么，而不是从头
读到尾。roadmap 规划的都已经**写完**（✅）；剩下的是更多可跑 lab、中文镜像，以及深化。

这六条的地图在[正门](README.md)上；这一页是它底下的细节。

| # | 轴 | 什么时候读它 |
| --- | --- | --- |
| **I** | **Start here** | 想搞懂哲学和方法 |
| **II** | **Foundations** | 想把 Linux + 脚本的底子补牢 |
| **III** | **The Stack** | 想一层一层地对比全部七个平台 |
| **IV** | **Platforms** | 想端到端地运维某一个平台 |
| **V** | **Cross-cutting** | 想学一项可迁移的技能 |
| **VI** | **Toolbox** | 想带走能跑、能被 agent 调用的工具 |

---

## I. Start here —— 论点与方法

| 模块 | 是什么 | 状态 |
| --- | --- | --- |
| [`WHY.md`](WHY.md) | 这个项目为什么存在；AI 时代这门手艺往哪走 | ✅ |
| [`00-the-operating-model.md`](00-the-operating-model.md) | 可迁移的骨架 —— 三个动作、七个面 | ✅ |
| [`ai-workflow/`](ai-workflow/) | 怎么用 AI 学习和运维 —— 以及怎么约束它诚实 | ✅ |

## II. Foundations —— 一切默认你有的底子

| 模块 | 是什么 | 状态 |
| --- | --- | --- |
| [`foundations/`](foundations/) | Linux + 脚本（Python/Bash/PowerShell）—— 每个岗位脚下的地板 | ✅ |

## III. The Stack —— 按层读，自底向上（✅ 完成，01→07）

七个平台在每一层被对比，从机房往上写。这个项目最有特色的一条轴。见
[`the-stack/`](the-stack/)。

| 章 | 覆盖 | 状态 |
| --- | --- | --- |
| [`01-physical`](the-stack/01-physical.md) | 数据中心、硬件、hypervisor、故障域 | ✅ |
| [`02-network`](the-stack/02-network.md) | underlay/overlay、VPC 模型、出网计费表、调试阶梯 | ✅ |
| [`03-compute-and-images`](the-stack/03-compute-and-images.md) | 计算形态、镜像流水线、bake vs fry、cloud-init | ✅ |
| [`04-storage`](the-stack/04-storage.md) | block/file/object、备份的恐惧 · **+ 可跑 [lab](../../the-stack/labs/04-backup-not-snapshot/)** | ✅ |
| [`05-platform-services`](the-stack/05-platform-services.md) | 容器、serverless、托管数据库、自建 vs 租用 | ✅ |
| [`06-observability`](the-stack/06-observability.md) | metric/log/trace、SLI/SLO、OpenTelemetry | ✅ |
| [`07-security`](the-stack/07-security.md) | 责任共担、纵深防御、CSPM/EDR/SIEM | ✅ |

## IV. Platforms —— 按平台读（全部七个）

每个模块都有 `README`（是什么 + 技能图 + AI-ramp 摘要）· `skills-map` · `ai-ramp` ·
`labs/` 里一条**三段式 CLI arc**；公有云另加更深的 **architecture · operations ·
automation** 三件套。The Stack 里对比的七个平台都有模块。见
[`platforms/`](platforms/)。

**公有云** —— 一个你用 API 驱动的租来的数据中心：

| 平台 | 有什么 · 诚实标注 |
| --- | --- |
| [`aws/`](platforms/aws/) | ✅ 范例 + [architecture](../../platforms/aws/architecture.md)/[operations](../../platforms/aws/operations.md)/[automation](../../platforms/aws/automation.md)/[support](platforms/aws/support.md) + labs（**2 个可跑** + 三段式 CLI arc）。先读它。· 🧭 |
| [`azure/`](platforms/azure/) | ✅ + [architecture](../../platforms/azure/architecture.md)/[operations](../../platforms/azure/operations.md)/[automation](../../platforms/azure/automation.md)/[support](platforms/azure/support.md) + 三段式 CLI arc。· 🧭，**Entra/身份 🔨** |
| [`gcp/`](platforms/gcp/) | ✅ + [architecture](../../platforms/gcp/architecture.md)/[operations](../../platforms/gcp/operations.md)/[automation](../../platforms/gcp/automation.md)/[support](platforms/gcp/support.md) + 三段式 CLI arc。global-VPC 是那个异类。· 🧭 |
| [`oci/`](platforms/oci/) | ✅ + [architecture](../../platforms/oci/architecture.md)/[operations](../../platforms/oci/operations.md)/[automation](../../platforms/oci/automation.md)/[support](platforms/oci/support.md) + 三段式 CLI arc + [compartment/verb lab](../../platforms/oci/labs/a-compartment-is-not-an-account/)。最年轻的超大规模云 —— compartment、OCPU、裸金属优先、便宜出网。· 🧭 |

**私有云 / 本地** —— 跑在**你自己**硬件上的平台：

| 平台 | 有什么 · 诚实标注 |
| --- | --- |
| [`vsphere/`](../../platforms/vsphere/) | ✅ + [architecture](../../platforms/vsphere/architecture.md)/[operations](../../platforms/vsphere/operations.md)/[automation](../../platforms/vsphere/automation.md) + 三段式 CLI arc（PowerCLI）。区域 vCenter 管理员，VCP6-DCV/NV。· **🔨 亲手做过的深度 —— 这是强项，不是 ramp** |
| [`openstack/`](../../platforms/openstack/) | ✅ + [architecture](../../platforms/openstack/architecture.md)/[operations](../../platforms/openstack/operations.md)/[automation](../../platforms/openstack/automation.md) + 三段式 CLI arc（DevStack）。"云是你自己搭的"；控制面即产品。· 🧭（与 KVM 邻接的 🔨） |
| [`self-host/`](../../platforms/self-host/) | ✅ + [architecture](../../platforms/self-host/architecture.md)/[operations](../../platforms/self-host/operations.md)/[automation](../../platforms/self-host/automation.md) + 三段式 CLI arc。PXE/镜像机队 10 万+、BMC/IPMI、DNS/RAID。· **🔨 亲手做过的深度 —— 最深的那条根** |

## V. Cross-cutting —— 按主题读（可迁移的那些面）

跨每个平台迁移的那几层。有些是**专门笔记**；有些按层读更自然，于是放在 The Stack 里，
这里**交叉链接而不重复**。见 [`cross-cutting/`](cross-cutting/)。

| 主题 | 归处 | 状态 |
| --- | --- | --- |
| [`identity-iam`](cross-cutting/identity-iam.md) | 专门笔记 | ✅ |
| [`iac-and-config`](../../cross-cutting/iac-and-config.md) | 专门笔记（Terraform/Ansible/Puppet） | ✅ |
| [`terraform-support`](cross-cutting/terraform-support.md) | 专门笔记（Terraform 修/救手艺 + Ansible sysadmin 的 ramp；state/漂移/替换）—— **🧭** | ✅ |
| [`ci-cd`](../../cross-cutting/ci-cd.md) | 专门笔记（CI/CD 流水线、GitOps、回滚） | ✅ |
| [`databases`](../../cross-cutting/databases.md) | 专门笔记（备份/PITR、复制、自建 vs 托管）—— **🔨** | ✅ |
| [`itsm-and-assets`](cross-cutting/itsm-and-assets.md) | 专门笔记（ITSM、CMDB、资产对账、访问治理）—— **🔨** | ✅ |
| [`endpoint/`](endpoint/) | 专门轨道（Jamf/Intune/PXE/打补丁）+ 三篇 companion —— [provisioning](../../endpoint/provisioning.md) · [management](../../endpoint/management.md) · [encryption and keys](../../endpoint/encryption-and-keys.md) | ✅ |
| [`saas-admin`](cross-cutting/saas-admin.md) | 专门笔记（Google Workspace / M365） | ✅ |
| [`m365-support`](cross-cutting/m365-support.md) | 专门笔记（M365 修/救手艺 + 跨方向转轨）—— **🔨** | ✅ |
| [`kubernetes`](../../cross-cutting/kubernetes.md) | 专门笔记（比 the-stack/05 更深） | ✅ |
| [`kubernetes-support`](cross-cutting/kubernetes-support.md) | 专门笔记（K8s 修/救手艺 + Linux sysadmin 的 ramp；调谐环 / cattle-not-pets / endpoints）—— **🧭** | ✅ |
| [`multi-cloud-support`](cross-cutting/multi-cloud-support.md) | 专门笔记（多云修/救手艺 —— 那些接缝：CIDR/身份/出网/态势；综合四篇平台笔记）—— **🧭** | ✅ |
| [`service-mesh`](../../cross-cutting/service-mesh.md) | 专门笔记（服务发现 + mesh；以及什么时候不要） | ✅ |
| [`web-and-tls`](../../cross-cutting/web-and-tls.md) | 专门笔记（反向代理、TLS/证书生命周期）—— **🔨** 基本功 | ✅ |
| [`incident-response`](../../cross-cutting/incident-response.md) | 专门笔记（事件生命周期、on-call、无指责复盘） | ✅ |
| [`working-with-security`](../../cross-cutting/working-with-security.md) | 专门笔记（与 InfoSec/SOC 协作 + 运维者的 ATT&CK 意识）—— **🔨** 运维安全 | ✅ |
| [`debug-ladder`](../../cross-cutting/debug-ladder.md) | 专门笔记（每一级一条命令，按它排除了什么来评判；refused vs timed out；为什么 *ping* 没有自己的一级）—— **🔨**。从命令手册收窄而来 | ✅ |
| [`vpn-and-remote-access`](../../cross-cutting/vpn-and-remote-access.md) | 专门笔记（从连接到够到之间的五个决策；网段、路由、解析器、会话寿命）—— **🔨**。收窄到决策，绝不写机制 | ✅ |
| [`network-evolution`](../../cross-cutting/network-evolution.md) | 专门笔记（十五年里变了什么、没变什么；防火墙的轴、F5 类设备、无线的代际、往上和往旁边搬走的速度）—— 有线 **🔨**、无线 **🧭**。关掉六个问题 | ✅ |
| [`site-network-design`](../../cross-cutting/site-network-design.md) | 专门笔记（一个物理站点：分段、编址、有线/无线、DNS-DHCP、802.1X、访客）—— **🔨**，无线部分 **🧭** | ✅ |
| [`cost`](cross-cutting/cost.md) | 专门笔记（把成本当作一种控制） | ✅ |
| 网络 | → [`the-stack/02`](the-stack/02-network.md) | ✅ 在 The Stack 里 |
| 存储 | → [`the-stack/04`](the-stack/04-storage.md) | ✅ 在 The Stack 里 |
| 虚拟化 | → [`the-stack/01`](the-stack/01-physical.md) | ✅ 在 The Stack 里 |
| 可观测 | → [`the-stack/06`](the-stack/06-observability.md) | ✅ 在 The Stack 里 |
| 安全与合规 | → [`the-stack/07`](the-stack/07-security.md) | ✅ 在 The Stack 里 |

**技能图** —— 同一批材料做成可勾选的能力清单，从平台图转置而来：一个主题横跨全部七个
平台，按每项技能能走多远分层。marker 落在这里的小节上，不落在文件上。

| 图 | 是什么 | 状态 |
| --- | --- | --- |
| [`skills-maps/networking.md`](../../cross-cutting/skills-maps/networking.md) | 11 节 / 63 格；4 格指向可跑的东西 | ✅ |
| [`skills-maps/identity.md`](../../cross-cutting/skills-maps/identity.md) | 10 节 / 58 格；5 格指向可跑的东西 | ✅ |

**面试图** —— 同样的小节，从面试官那一侧看。每个问题都带着它在测什么，以及一个形状由
该小节 marker 决定的答案（[ADR-0004](../adr/0004-interview-answers-are-evidence-for-a-marker.md)）。

| 图 | 是什么 | 状态 |
| --- | --- | --- |
| [`interview/networking.md`](../../cross-cutting/interview/networking.md) | 21 问 / 11 节；4 个答案仍是 ⏳ | ✅ |
| [`interview/identity.md`](../../cross-cutting/interview/identity.md) | 19 问 / 10 节；2 个答案仍是 ⏳ | ✅ |

---

## VI. Toolbox —— 跑起来

| 模块 | 是什么 | 状态 |
| --- | --- | --- |
| [`toolbox/README.md`](toolbox/README.md) | 章程：约定（安全默认、`Tested on:` 的诚实、agent 可读）+ 第一波计划 | ✅ |
| [`toolbox/linux-triage`](toolbox/linux-triage/) | 一次性事件分诊报告（只读） | ✅ |
| [`toolbox/user-lifecycle`](toolbox/user-lifecycle/) | CSV 批量建/停用用户（默认 dry-run） | ✅ |
| [`toolbox/patch-report`](toolbox/patch-report/) | 待更新 + 重启盘点（apt/dnf） | ✅ |
| [`toolbox/baseline-check`](toolbox/baseline-check/) | 小型加固基线审计（只读） | ✅ |
| [`toolbox/backup-restore-drill`](toolbox/backup-restore-drill/) | 用还原来证明一份备份 | ✅ |
| [`toolbox/cidr-check`](toolbox/cidr-check/) | 检测重叠的 CIDR 段 | ✅ |
| [`toolbox/ansible`](toolbox/ansible/) | 修复 role：baseline_hardening、patch、user_lifecycle（幂等） | ✅ |
| [`toolbox/vsphere-inventory`](toolbox/vsphere-inventory/) | 只读 vSphere 盘点，纯标准库 SOAP（无 SDK） | ✅ |
| [`toolbox/vm-migration-assess`](toolbox/vm-migration-assess/) | VMware→Proxmox 逐 VM 判决（EASY/MODERATE/HARD + 依据） | ✅ |
| [`toolbox/pve-inventory`](toolbox/pve-inventory/) | 同一套 schema 的 Proxmox 盘点（在线或从抓取文件） | ✅ |
| [`toolbox/snapshot-audit`](toolbox/snapshot-audit/) | 跨两种 hypervisor 标记陈旧/过深/过密的快照 | ✅ |
| [`toolbox/generate`](toolbox/generate/) | 按环境打包的生成器：关注点/平台标签 → 独立子集 + 它能诚实携带的那些 skill | ✅ |

## VII. Build-out —— 一条横穿六条轴的路线

不是第七批材料。一个场景端到端走一遍 —— 一间百人办公室，从第一天到开门营业 —— 每一步
承载**顺序与依赖**，实质内容指回上面那些轴。
决定：[`docs/adr/0001`](../adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)

| 条目 | 说明 | 状态 |
|---|---|---|
| [`build-out/`](build-out/) | **16 步全部写完。** 依赖图已验证无环且完全对称；16 步里有 15 步指向一个可跑 lab 或工具（94%） | ✅ |
| [`build-out/03-identity.md`](build-out/03-identity.md) | `Before` 为空的那一步 —— 身份没有物理前置条件，而有八步挂在它上面 | ✅ 🔨 |
| [`build-out/11-assets-and-tickets.md`](build-out/11-assets-and-tickets.md) | 编号第十一，却必须从第 1 台设备就开始 —— 对依赖诚实，对时间撒谎 | ✅ 🔨 |
| [`build-out/13-the-help-desk.md`](build-out/13-the-help-desk.md) | 一百个人需要几个 IT —— 在估算面被枚举清楚之前无法回答 | ✅ 🔨 |
| [`docs/questions.md`](../questions.md) | 有人问过这个仓库、而它还答不上的问题 —— **七个域三十问**，全部已答。索引，加上划在边界外的理由；各域是 [`docs/questions/`](../questions/) 下的文件，其中 4 个是先被收窄才答的，理由都留着 | ✅ |
| [`build-out/GAPS.md`](build-out/GAPS.md) | 场景浮出来的六个真缺口，其中四个是同一个形状 —— **六个现在全部关闭**，靠 [`remote-access-four-causes`](../../cross-cutting/labs/remote-access-four-causes/)、[`permission-sprawl`](../../cross-cutting/labs/permission-sprawl/)、[`mail-authentication-alignment`](../../cross-cutting/labs/mail-authentication-alignment/)、[`asset-reconciliation`](../../cross-cutting/labs/asset-reconciliation/)、[`help-desk-queue`](../../cross-cutting/labs/help-desk-queue/) 和 [`transcript-retention`](../../cross-cutting/labs/transcript-retention/) | ✅ 活的 |

## VIII. 走读 —— 第二条路线，是听的不是读的

同样不是一批材料。同一间参考办公室，慢慢走一遍、讲出来，稿子是写来**被 TTS 引擎念**的
—— 没有表格、没有行内链接，只有会被念出口的那些字。它的顺序是它自己的：第一篇横跨两条
轴上的三份文档外加根目录，所以它不是"`build-out/` 配个声音"。
决定：[`docs/adr/0009`](../adr/0009-the-walkthrough-ships-its-script-not-its-audio.md)

| 条目 | 说明 | 状态 |
|---|---|---|
| [`walkthrough/`](walkthrough/README.md) | 这条路线、它的格式和它的五条决定 | ✅ |
| **01 · 网络** | [中文](../../walkthrough/01-the-network.zh.md) · [English](../../walkthrough/01-the-network.en.md) —— 106 拍，念出来约二十分钟。取材于两条轴上的三份文档外加根目录 | ✅ |
| **02 · 第一个星期一** | [中文](../../walkthrough/02-the-first-monday.zh.md) · [English](../../walkthrough/02-the-first-monday.en.md) —— 93 拍。一个入职者，以及那两样没有任何东西会触发的事。与 01 同一张 plate；不同的是那些面板 | ✅ |
| **03 · 它坏掉的那一天** | [中文](../../walkthrough/03-the-day-it-breaks.zh.md) · [English](../../walkthrough/03-the-day-it-breaks.en.md) —— 102 拍。一次故障的头十分钟：哪些决定是你的、哪些检查什么都排除不掉，以及为什么修好它不是交付物 | ✅ |
| 每篇走读两份稿 | 并排放着，而且**互不是译本** —— 语流经不起翻译（[ADR-0010](../adr/0010-a-spoken-script-has-no-translation.md)） | ✅ |
| 音频 | **永不进这棵树。** 你用自己的 TTS 生成，或者去听已发布的那一集 | — |
| 拍 | 一段话、一次 TTS 调用、一个音频片段、一个楼面状态 —— 按稳定 id 对齐，绝不按时间戳（[ADR-0012](../adr/0012-alignment-is-by-beat-not-by-timestamp.md)） | ✅ |
| 楼面 | viewer 里一间可交互的二维办公室 —— 平移、三档语义缩放、20 个可点物体。那群人**就是**无线负载。它渲染 Markdown 已陈述的内容，自己不计算（[ADR-0011](../adr/0011-the-floor-renders-the-reference-office-and-may-not-compute-it.md)） | ✅ |
| 它的守卫 | [`build-walkthrough.py`](../../walkthrough/build-walkthrough.py) —— 拍、锚点、可念性、发布冻结 · [`tools/floor/`](../../tools/floor/README.md) —— 手绘的贴图集 | ✅ |

## Agent Skills —— 方法，可被调用

这个仓库带十个 [`.claude/skills/`](../../.claude/skills/)。七个打包它的**方法论**：
[`platform-ramp`](../../.claude/skills/platform-ramp/SKILL.md)（诚实地转轨到任何平台）、
[`honesty-audit`](../../.claude/skills/honesty-audit/SKILL.md)（把断言分类成 🔨/🧭/过度声称）、
[`author-module`](../../.claude/skills/author-module/SKILL.md)（用仓库的声音写一篇新笔记
—— 包括 **support 笔记** —— 有研究依据）、
[`runnable-lab`](../../.claude/skills/runnable-lab/SKILL.md)（把一个概念变成自验证的
drill）、[`diagram-module`](../../.claude/skills/diagram-module/SKILL.md)（判断一篇文档
需不需要图、选媒介、让派生产物保持同步）、
[`mirror-zh`](../../.claude/skills/mirror-zh/SKILL.md)（把一篇文档镜像进 `docs/zh/`），
以及 [`interview-drill`](../../.claude/skills/interview-drill/SKILL.md)（像面试官那样把
它问回来）。

三个是**用户侧**的 —— 它们包装 [toolbox](toolbox/)，好让 AI agent 替你跑：
[`linux-triage`](../../.claude/skills/linux-triage/SKILL.md)（分诊一台主机并把每个红旗
路由到它的修法）、[`harden-baseline`](../../.claude/skills/harden-baseline/SKILL.md)
（审计→修复的加固闭环，防锁死）、
[`toolbox-picker`](../../.claude/skills/toolbox-picker/SKILL.md)（说出任务，拿到对的工具
+ 确切的命令）。这就是 roadmap 指向的那套"AI 辅助工具集" —— 在一台新机器上装一个 skill，
一句话驱动整个工具箱。

## 在浏览器里读

二十万词已经超过"翻文件夹还管用"的体量。[`site/`](site/README.md) 是同一批材料，带导航、
全文搜索、语言切换和渲染好的图 —— 除此之外什么都没有。它有两种启动方式，两种都不用装
东西：

```bash
python3 site/serve.py                           # http://127.0.0.1:8000
docker compose -f site/docker-compose.yml up    # http://127.0.0.1:8099
```

它是一个**视图**，不是第七条轴：它显示的每一个字都是 GitHub 也能渲染的文件，删掉
`site/` 这个仓库不会少一条事实
（[ADR-0005](../adr/0005-the-site-is-a-view-not-a-seventh-axis.md)）。

## 诚实层（处处适用）

每个模块都按 [`WHY.md`](WHY.md) 标注 **🔨 亲手做过的深度** 与 **🧭 经过验证的 ramp**
—— 而这个标注是承重的，不是装饰。七个平台里有两个是 **🔨**：
[vSphere](../../platforms/vsphere/)（一套生产 vCenter 估算面，VCP6-DCV/NV）和
[self-host](../../platforms/self-host/)（10 万+ 设备的机队），以及那些横切的强项 ——
Linux、[endpoint](endpoint/)、[身份](cross-cutting/identity-iam.md)、
[SaaS 管理](cross-cutting/saas-admin.md)，和那份自动化纪律。公有云、OpenStack 的
控制面，以及深度 Kubernetes 是诚实的 **🧭** ramp —— 测绘过、验证过、可跑，从不吹。
这个区分就是全部的意义（[`WHY.md`](WHY.md) 解释了为什么它在 AI 时代更要紧，而不是更不
要紧）。
