---
kind: index
axis: platforms
themes: [cloud]
platforms: [aws]
derived: true
mirrors: platforms/aws/README.md
summary: "每一个平台模块所遵循的那份模板：它是什么 → 管理技能图 → AI 辅助 ramp → lab —— 外加 AWS 作为那个做过的实例所拿到的四篇更深的姊妹笔记。"
---
# AWS —— 那个做过的实例

> 🌐 **语言：** [English（默认）](../../../../platforms/aws/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/aws/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 每一个平台模块所遵循的那份模板：**它是什么 → 管理技能图 → AI 辅助 ramp → lab** ——
> 外加 AWS 作为那个做过的实例所拿到的四篇更深的姊妹笔记：**[architecture](architecture.md)**
> （它是怎么组织的）、**[operations](operations.md)**（day-2 地跑它、那份运维活的拆解，以及运营
> 循环里的 AI）、**[automation](automation.md)**（把 API 写成脚本去管理并运维它），以及
> **[support](support.md)**（那门修/救手艺，以及一个来自另一条车道的强系统管理员要接手它必须
> **忘掉**什么）。AWS 是最先做、也做得最彻底的；从头到尾读一遍，去看那个形状。

## 1. AWS 是什么

Amazon Web Services 是一座你用 API 驾驶的租来的数据中心。你不买服务器、机柜、交换机或存储阵列 ——
你**请求**它们，按小时/秒/GB 付费，用完还回去。管理员的工作从**拧螺丝**转向**声明意图**，并让结果
保持安全、可靠、负担得起。

映射到那[七片面](../../00-the-operating-model.md)上：

| 面 | AWS 对它的叫法 | 那一句话 |
| --- | --- | --- |
| **身份与访问** | **IAM**（user、role、policy）、IAM Identity Center | 通往一切的正门。role 加最小权限 policy 就是全部的游戏。 |
| **计算** | **EC2**（VM）、**Lambda**（serverless）、**ECS/EKS**（容器）、Auto Scaling | 你的代码跑的地方。从 EC2 起步；再毕业到容器/serverless。 |
| **网络** | **VPC**、subnet、route table、security group、NACL、**ELB**、**Route 53**（DNS） | 你在云上的私有网络。一个 VPC 是装着一切的那个盒子。 |
| **存储与数据** | **S3**（对象）、**EBS**（块）、**EFS**（文件）、**RDS**/Aurora、DynamoDB | 状态住的地方。S3 是"我该把这个放哪儿？"的默认答案。 |
| **发放与配置** | **CloudFormation**、**Terraform**（第三方）、CDK、AMI、Systems Manager | 你怎么从代码而不是从点击把它建起来。 |
| **可观测性** | **CloudWatch**（指标/日志/告警）、CloudTrail（审计）、X-Ray（trace） | 它健康吗，以及谁做了什么？ |
| **安全与合规** | IAM、KMS（加密）、Secrets Manager、GuardDuty、Config、Organizations、**Cost Explorer / Budgets** | 它安全吗、证明得了吗、财务上没着火吧？ |

如果你知道那大约 25 个服务名，以及每一个属于哪片面，你就能就 AWS 进行一场真正的对话。那就是那张
地图。现在说技能。

## 2. 管理技能图

一份具体的、可勾选的清单，列出一个 AWS 管理员必须**做得到**什么 —— 不是"听说过"。带熟练度分层的
完整清单在 **[`skills-map.md`](skills-map.md)** 里。那些标题级能力：

- **IAM 做对** —— 创建受限的 role 和最小权限 policy；理解 user、role 和 policy 之间的差别；
  assume-role 和短寿命凭据优于长寿命密钥；MFA 和 root 账号卫生。
- **一个你自己设计的 VPC** —— subnet（公有/私有）、route table、一个 internet gateway 和一个
  NAT、security group 对 NACL，以及*一个东西为什么上不了网*（第一大支持问题）。
- **你跑得起来也扩得动的计算** —— 从代码启动 EC2、挂上正确的 IAM role（绝不把密钥烤进一台实例）、
  基本的 Auto Scaling 加一个负载均衡器。
- **默认值正确的存储** —— S3 默认开着加密加 block-public-access；EBS 快照；一个私有子网里的托管
  RDS 数据库。
- **一切从代码来** —— 同一套栈用 Terraform 或 CloudFormation 写出来，在版本控制里、可评审、
  可销毁。
- **你会看见它坏掉** —— CloudWatch 告警、CloudTrail 用来查"谁干的"，以及调试一次连通性或权限失败
  的那份肌肉记忆。
- **安全并且在预算内** —— 用 KMS/Secrets Manager 而不是把密钥放代码里；一个 Budget 告警，好让一台
  被遗忘的 GPU 实例不会花掉四千美元。

## 3. 通往胜任的那条 AI 辅助路径

那套方法 —— 怎么用 AI 当副驾**并且让它保持诚实**，在几天而不是几个月里从"懂 Linux/网络"走到
"能运维 AWS" —— 在 **[`ai-ramp.md`](ai-ramp.md)** 里。用一段话说：

用 AI 去把那些*未知的未知*压掉 —— "既然我已经懂 Linux、网络和 IAM 概念，AWS 里覆盖一个管理员八成
工作的那两成是什么？" —— 然后让它生成那条最小权限 policy、那份 Terraform、那条 CLI 命令。
**然后对着文档核实每一句声称，并在一个用完就扔的账号里跑它。** AI 写第一稿；你的判断是那道评审闸门。
2026 年一个系统管理员的价值不在于知道每一个参数 —— 而在于知道机器什么时候在自信地错着。

## 4. Lab

读一个 subnet 和配一个 subnet 是两种不同的技能。那三次 guided run 住在 **[`labs/`](labs)**
里 —— 从一个最小权限 IAM role 加一个盘点你账号的 `boto3` 脚本开始（那个经典"列出一切"管理脚本的
云上版本），然后是一个用 Terraform 写的最小 VPC 加 EC2。

## 5. 往深里走 —— architecture、operations、automation 与 support

四篇姊妹笔记把 AWS 带过"那些服务是什么"：

- **[`architecture.md`](architecture.md)** —— AWS 是怎么**组织**的：作为爆炸半径单位的
  账号/组织模型、region 与 AZ、全局与区域的分野、那条共担责任线、把 Well-Architected 当作一面评审
  镜子，以及一份把每一片面组合进一套系统的参考三层架构。
- **[`operations.md`](operations.md)** —— **跑** AWS 是什么样：那份 day-2 简报、那些运维笔记
  （什么会把你叫醒）、**按节奏拆解**的那些反复出现的运维活（持续/每日/每周/每月/每季/有故障时），
  以及 **AI 怎么协助那条运营循环** —— 与那条学习 ramp 不同，并带着那条护栏：AI 碰信号和初稿，
  而你碰生产。
- **[`automation.md`](automation.md)** —— **把 API 写成脚本**去管理并运维 AWS：那个
  `身份 → client → API 调用` 的模型、CLI 对 boto3 对 Terraform 那架高度阶梯、那条凭据链
  （脚本里绝不放密钥）、把一个能用的脚本和一把自伤枪分开的那些规则（分页、遍历 region、处理错误、
  保持幂等），以及只读审计与修复这两种形状 —— 全都扎在那个可跑的
  [盘点 lab](labs/01-scoped-identity-inventory) 上。
- **[`support.md`](support.md)** —— **那门修/救手艺**：支持 AWS 让你为什么负责、那些反复出现的
  工单以及*你去哪儿看*（`AccessDenied` 的语法、超时对拒绝、S3 403 的那几层、ALB 5xx、那些成本
  意外），以及一个强系统管理员要接手它必须**忘掉**的那些承重的本地/云直觉 —— 那条 ramp 被落到
  实处，配一份验证过的 GitHub 现场工具包。

## 诚实边界

按整个项目的精神写的：这记录的是一套**方法和一张能力图**，而那些 lab 是真的。凡是在某个具体
AWS 服务上深度生产经验还在前方的地方，这些笔记会这么说，而不是虚张 —— 那份诚实就是重点。这里的
声称不是"十五年 AWS"；而是"一套可迁移的运营模型，加上一条能快速走到胜任、并且能在这个仓库里被
验证的 AI 增强 ramp"。
