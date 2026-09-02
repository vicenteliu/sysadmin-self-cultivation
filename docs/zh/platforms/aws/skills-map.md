---
kind: skill-map
axis: platforms
themes: [cloud]
platforms: [aws]
derived: true
mirrors: platforms/aws/skills-map.md
summary: "当你能从代码把它做出来、并且解释得出它的故障模式时，才勾上一个框 —— 不是在你读过它的时候。"
---
# AWS —— 管理技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/aws/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/aws/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

一份可勾选的能力清单。分层：

- **Core** —— 没有这个你管理不了 AWS。
- **Working** —— 对一个扎实的中/高级管理员的预期。
- **Depth** —— 把一个强管理员区分出来的东西；常常是面试的分水岭。

**当你能从代码把它*做*出来、并且*解释*得出它的故障模式时**，才勾上一个框 —— 不是在你读过它的时候。

## 身份与访问（IAM）—— 那扇正门

- [ ] **Core** —— 解释 user 对 role 对 policy 对 group；各自什么时候用。
- [ ] **Core** —— 为一件具体任务写一条最小权限 JSON policy（例如只读一个 S3 桶）。
- [ ] **Core** —— 把 root 账号保护好：MFA、没有访问密钥、只做 break-glass。
- [ ] **Working** —— 用 assume-role / 短寿命凭据（STS）取代长寿命密钥。
- [ ] **Working** —— instance profile：给一台 EC2 机器一个 role，而不是把密钥烤进去。
- [ ] **Working** —— 用 IAM Identity Center（SSO）做人的访问；联合的基本功。
- [ ] **Depth** —— permission boundary、SCP（Organizations），以及在 CloudTrail 里读一次被拒绝的请求。

## 网络（VPC）—— 装着一切的那个盒子

- [ ] **Core** —— 设计一个 VPC：CIDR、跨 AZ 的公有对私有 subnet。
- [ ] **Core** —— route table、Internet Gateway、NAT —— 并追查*一台主机为什么上不了网*。
- [ ] **Core** —— security group 对 NACL：有状态对无状态，以及该去够哪一个。
- [ ] **Working** —— 负载均衡（ALB/NLB）和 target group。
- [ ] **Working** —— 用 Route 53 做 DNS；公有对私有 hosted zone。
- [ ] **Depth** —— VPC peering / Transit Gateway；VPC endpoint（让流量不上互联网）；混合连通（VPN / Direct Connect）。

## 计算 —— 代码跑的地方

- [ ] **Core** —— 从 CLI 启动/停止/终止 EC2；合理地挑实例类型。
- [ ] **Core** —— 给一台实例挂一个 IAM role；用 user-data 做引导。
- [ ] **Working** —— Auto Scaling group 加一个负载均衡器加健康检查。
- [ ] **Working** —— 构建/维护一个 AMI（镜像构建的云上版本）。
- [ ] **Depth** —— ECS/EKS 上的容器；用 Lambda 做事件驱动/serverless；用 Spot 省成本。

## 存储与数据 —— 状态住的地方

- [ ] **Core** —— S3 带加密加 block-public-access；bucket policy 对 IAM。
- [ ] **Core** —— EBS 卷加快照；生命周期基本功。
- [ ] **Working** —— 私有子网里的 RDS/Aurora；备份、参数组、故障切换。
- [ ] **Working** —— S3 生命周期规则加存储类别（成本）。
- [ ] **Depth** —— DynamoDB 基本功；用 EFS 做共享文件存储；跨 region 复制。

## 发放与配置 —— 从代码建，不从点击建

- [ ] **Core** —— 用版本控制里的 **Terraform** 或 **CloudFormation** 把一套栈立起来。
- [ ] **Core** —— 干净地销毁它（不留孤儿的、还在计费的资源）。
- [ ] **Working** —— 远端 state 加锁；module / 可复用的栈。
- [ ] **Working** —— 用 Systems Manager（SSM）做打补丁、run-command、Parameter Store。
- [ ] **Depth** —— 给基础设施做 CI/CD；漂移检测；策略即代码护栏。

## 可观测性 —— 它健康吗，以及谁做了什么

- [ ] **Core** —— CloudWatch 指标加一条真的会把人叫醒的告警。
- [ ] **Core** —— 把日志送进 CloudWatch Logs 并搜索它们。
- [ ] **Core** —— CloudTrail：回答"谁创建/删除了这个？"
- [ ] **Working** —— 仪表盘；log-metric filter；基本的 SLO 思维。
- [ ] **Depth** —— 分布式 tracing（X-Ray）；跨账号的集中日志。

## 安全与合规 —— 安全、可证明、负担得起

- [ ] **Core** —— KMS 静态加密；Secrets Manager / Parameter Store（代码里不放密钥）。
- [ ] **Core** —— 一条 **Budget 告警**，好让一个被遗忘的资源不会让你意外。
- [ ] **Working** —— GuardDuty（威胁检测）、AWS Config（合规规则）。
- [ ] **Working** —— 用 Organizations 做多账号；把生产和开发的爆炸半径分开。
- [ ] **Depth** —— landing zone / 护栏设计；一把泄露密钥的事故响应；成本异常检测。

## 那个"你到底能不能运维它"的测试

如果你能在全部七片面上、从代码把那些 **Core** 框做出来，并且调得动那些常见故障，你就能诚实地说
你能在一个可用的水平上管理 AWS。**Working** 框让你在第一天就真的有用。**Depth** 框是一个强候选人
在面试里会去够的东西，也是让一个生产账号不出事的东西。
