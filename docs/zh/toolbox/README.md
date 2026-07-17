# Toolbox 工具箱 — 带得走的部分

> 这个仓库的其余部分解释事情**如何运作**；toolbox 是你可以**直接运行**的部分：
> 小而自洽的工具，系统管理员——或者与之协作的 AI agent——几分钟内就能上手使用。

## 为什么要有工具箱

读懂证明理解，跑通证明手艺。这条线把仓库从*用来读的东西*演进为*用来用的东西*——
并且从第一天起就按**可被 agent 调用**来设计：每个工具的文档精确到足以让 AI 助手
安全地替你操作它。这就是 [`ai-workflow/`](../../../ai-workflow/) 那一章的可执行版。

## 设计规则（约定——每个工具遵守全部六条）

1. **一目录一工具，自洽。** `toolbox/<tool-name>/` 内含脚本和一份 README，写明用途、
   用法、退出码。工具之间互不依赖。
2. **默认安全。** 凡是*可能*改变系统状态的工具，默认只读或 `--dry-run`；破坏性动作
   必须显式加参数。一个不敢随手跑的工具，就是一个你根本不会去跑的工具。
3. **诚实边界。** 每份 README 带一行 `Tested on:`（如 *Ubuntu 22.04、RHEL 9 lab*）。
   lab 验证过不等于生产级加固，README 会直说——仓库的 ✋/🧗 诚实层，应用到代码上。
4. **朴素依赖。** Bash 和 Python 标准库优先；编排确有必要时才用 Ansible。
   不引框架，不搞 curl 管道安装。
5. **Agent 可读。** 每份 README 开头一小块写明输入、输出、风险级别，让 AI agent
   无需猜测就能调用。包装这些工具的使用者侧 Agent Skills 在后续波次落地。
6. **成功安静，失败响亮。** 一切正常时退出码 0、输出克制；出问题时非零退出码 +
   可行动的报错信息——因为人和 agent 都要靠它分支。

## 目录结构

```
toolbox/
├── README.md            ← 你在这里：章程 + 约定
└── <tool-name>/
    ├── README.md        ← 用途 · 用法 · tested-on · 风险级别
    └── <tool>.sh|.py    ← 工具本体
```

## 第一波（✅ 已交付——按任务在真实 JD 中出现的频率排序）

| 工具 | 做什么 | 来源 |
| --- | --- | --- |
| `linux-triage` | 一键健康/分诊报告——CPU、内存、磁盘、网络、近期日志错误 | 新写；每次事故的第一步 |
| `user-lifecycle` | CSV 驱动的 Linux 批量用户创建/停用 | 新写；身份是 JD 里最密集的集群 |
| `patch-report` | 待更新清单（apt/dnf），带是否需重启标记 | 新写 |
| `baseline-check` | 只读审计一小组加固基线 | 新写；Ansible 修复在 Ansible 波次 |
| `backup-restore-drill` | 用恢复来证明备份——没恢复过的备份不算备份 | 从 [the-stack lab 04](../../../the-stack/labs/04-backup-not-snapshot/) 生长而来 |
| `cidr-check` | 检测网络规划中的 CIDR 网段重叠 | 从 multi-cloud lab 生长而来 |

## Ansible 线（✅ 已交付——修复的那一半）

上面的脚本负责*发现*；[`ansible/`](../../../toolbox/ansible/) roles 负责*修复*，且幂等：

| Role | 修复什么 | 与谁配对 |
| --- | --- | --- |
| `baseline_hardening` | SSH 姿态、umask、sysctl、journald | `baseline-check` |
| `patch` | 应用更新（apt/dnf）+ 重启编排 | `patch-report` |
| `user_lifecycle` | 声明式用户（present / disabled）| `user-lifecycle` |

## Agent Skills（✅ 已交付——一句话驱动工具箱）

三个使用者侧 [`.claude/skills/`](../../../.claude/skills/) 把这些工具包装成
AI agent 可以替你运行的形态：**linux-triage**（分诊一台主机，把每个红旗路由到
对应修复）、**harden-baseline**（audit→remediate 加固闭环，防锁死）、
**toolbox-picker**（说出任务，拿到对的工具 + 命令）。在新机器上装一个 skill，
一句话驱动整个工具箱——"AI-assisted toolset" 本体。

## 虚拟化波次（✅ 已交付——hypervisor 层）

前六个工具看的是 OS *内部*；这三个看它底下的平台——合在一起回答这一季的
问题："这套 VMware 环境搬得去 Proxmox 吗？"：

| 工具 | 做什么 | 与谁配对 |
| --- | --- | --- |
| [`vsphere-inventory`](vsphere-inventory/) | 用**纯标准库 SOAP** 只读清点 vSphere（无 SDK、无 govc）| 喂给 `vm-migration-assess` |
| [`vm-migration-assess`](vm-migration-assess/) | 每台 VM 一个裁决——EASY/MODERATE/HARD——附具体发现 | 读 `vsphere-inventory` |
| [`pve-inventory`](pve-inventory/) | **同一 schema** 的 Proxmox 清点，节点现场或读捕获 | 目的端的镜像 |

## 生成器（✅ 已交付——可定制工具箱）

[`generate`](generate/) 一条命令组装出某个环境真正需要的子集：匹配的脚本、
配对的 Ansible roles、以及引用完全满足的 Agent Skills（包里永远不会出现指向
包中不存在工具的 skill）：

```bash
./toolbox/generate/generate.py --profile security-baseline --out ~/kit
```

选择模型 = [`generate/catalog.json`](../../../toolbox/generate/catalog.json) 里的
关注点 + 平台标签；新工具加一条 JSON 记录即可加入。

## 这不是什么

不是产品，不是生产级加固，不是你配置管理系统的替代品。它是工作材料，
和这里的一切一样遵守同样的诚实规则——如果一个工具没在某个真实环境里演练过，
它的 README 会明确告诉你它*在哪里*验证过。
