---
kind: note
axis: cross-cutting
themes: [identity]
platforms: [aws, azure]
derived: true
mirrors: cross-cutting/identity-iam.md
summary: "存在的东西里，最密、最可迁移的那一片面。"
---
# 身份与访问（IAM）

> 🌐 **语言：** [English（默认）](../../../cross-cutting/identity-iam.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`cross-cutting/identity-iam.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 存在的东西里，最密、最可迁移的那一片面。身份做对了，别的一切都有一扇带锁的正门；身份做错了，
> 别的一切都不要紧。这里是概念层 —— **同一门**纪律，不管它是 Active Directory、AWS IAM、
> Azure RBAC、GCP IAM 还是 Okta。

身份是招聘启事里出现频率高过任何其他东西的那片面，而且理由充分：它是控制面。对每一个系统的
每一次请求，底下都是那一句 *"你是谁，以及你被允许做这件事吗？"* 把这个问题掌握一次，之后每个
平台的 IAM 都变成一次改名练习。

## 那两个问题（永远不要把它们混为一谈）

- **认证（authN）** —— *你是谁？* 证明身份：一个密码加 MFA、一个 token、一张证书、一份联合
  断言。
- **授权（authZ）** —— *你被允许做什么？* 角色、策略、权限、scope。

绝大多数身份 bug 和入侵，都住在这两者之间的那道缝里：一个被正确认证的主体，拿着远超它所需的
授权。这引出贯穿一切的那一条规则：

## 最小权限 —— 这就是全部的游戏

授予仍然能把活干完的**最小**权限，在**最窄**的范围上，持续**最短**的时间。每个平台都给你工具；
那份纪律是你的：

- **最小权限** —— 只读的东西就给只读；给一个 action，不给一个通配符。
- **最窄范围** —— 一个桶 / 一个资源组 / 一个项目，不是整个账号。
- **最短时间** —— 短寿命凭据和即时提权，而不是常驻访问权。

如果你只从这个文件里内化一样东西，就是这一条。下面的一切都是施行它的机械。

## 主体：人与工作负载

两种身份，而把它们搞混是一个经典错误：

- **人的身份** —— 人，在一个目录里（AD、Entra、Okta、Google）。由生命周期管理（见下），由
  MFA 保护，通过**组**被授予访问权。
- **工作负载身份** —— 应用、脚本、服务器、流水线。正确的模式是一个平台托管的身份，**机器上不放
  长寿命密钥** —— AWS IAM role / instance profile、Azure Managed Identity、GCP service
  account。一把被烤进 VM 或仓库里的密钥，就是你努力永远不去做的那件事。

## 那条生命周期：入职 / 转岗 / 离职（JML）

人的访问权有一条生命周期，而把它自动化，正是身份不再是工单活、开始成为工程的地方：

- **入职** —— 新人 → 账号被创建、被加进正确的组、第一天就能干活。
- **转岗** —— 角色变更 → 权限被加上，**也被拿下来**（"拿下来"那一半是所有人都会忘的那一半，
  而权限蔓延就是这么发生的）。
- **离职** —— 离开 → 访问权在各处被干净地、及时地回收。

手动做既不扩展也过不了审计。做成代码 —— 通过目录的 API 驱动，或者通过 **SCIM** 推向下游 SaaS
—— 人数就能增长而工单量不跟着增长。那就是**扩张人**和**扩张工单**之间的差别。

## 同样的概念，逐平台改名

上面那些概念一旦扎实，每个平台都只是一次查表：

| 概念 | 本地 AD | Microsoft Entra | AWS | GCP | Okta |
| --- | --- | --- | --- | --- | --- |
| **目录 / IdP** | Active Directory | Entra ID | IAM Identity Center | Cloud Identity | Universal Directory |
| **人的 authZ** | AD 组 + GPO | **Azure RBAC** 角色 | IAM role + policy | IAM role + binding | 组 + 应用分配 |
| **工作负载身份** | 服务账号 / gMSA | **Managed Identity** | IAM role（instance profile） | service account | ——（人的 IdP） |
| **联合 / SSO** | AD FS | Entra SSO | Identity Center / SAML-OIDC | Workforce Identity Federation | **Okta 本身**（那个枢纽） |
| **开通** | AD/LDAP | Entra provisioning / SCIM | 到 Identity Center 的 SCIM | —— | Okta Lifecycle / SCIM |
| **特权访问** | 分层管理 / PAW | **PIM**（即时） | permission set + STS | —— | Okta PAM |

> **那个值得背下来的 Azure 坑：** Azure 有**两套**权限系统 —— **Entra ID 角色**（目录级：谁来
> 管理用户/应用/组）和 **Azure RBAC**（资源级：谁能碰这台 VM / 这个存储）。AWS 只有一套 IAM。
> 把这两个搞混，是 Azure 身份上的第一大错误。

## 联合与 SSO —— 协议层

"登录一次，够得到很多应用。"三个缩写你必须分得清，因为面试官和故障都会考它：

- **SAML 2.0** —— 更老的、基于 XML 的企业标准。一个 Identity Provider（IdP）把一份签过名的
  **断言**发给一个 Service Provider（SP）。在企业 SaaS 里仍然到处都是。
- **OAuth 2.0** —— 一个**授权**框架，不是认证。它签发带 **scope** 的 **access token** 用于
  委托访问（"让这个应用读我的日历"）。人们把它误用成登录；它本身不是登录。
- **OpenID Connect（OIDC）** —— 一个建**在 OAuth 2.0 之上**的**认证**层。它加了一个
  **ID token**（一个签过名的 JWT，说"这个用户认证过了"）。这是现代 web/应用 SSO。

要记住的那句话：**SAML 和 OIDC 是用来登录的；OAuth 是用来给一个应用授予受限访问的；OIDC 是
OAuth 外挂了一层身份。**

## SCIM —— 把开通变成 API

**SCIM**（System for Cross-domain Identity Management）是那套标准 REST API，用来把用户/组的
增删改**推**出你的 IdP、送进下游 SaaS。它就是那个把 JML 从"一个人在 N 个管理控制台里点来点去"
变成一条自动化流程的东西：在目录里入职 → SCIM 开通那些 SaaS 账号 → 在目录里离职 → SCIM 在各处
把它们停用掉。如果说 SSO 回答的是"人怎么登录"，SCIM 回答的就是"账号怎么被创建和销毁"。

## 管理纪律（你应该做得到什么）

七件事，其余的是词汇：创建一条**受限**的 role 或 policy 并解释它为什么是最小的；为人设计
**基于组**的访问，在规模上绝不逐用户授予；给一个工作负载一个**托管身份**，让机器上不坐着一把
密钥；通过目录 API 或 **SCIM** 把**入职/转岗/离职**自动化，*离职*那一半也在内；把 **SSO** 立
起来，并且知道它是 SAML 还是 OIDC 以及为什么；跑一次产出**证据**而不是产出一句断言的访问复审；
以及把一次**被拒绝的请求**读到能点名是哪一条规则、在哪个范围上拒绝的。

这一切的可勾选版本 —— 十节 58 个框，按每项技能能走多远分层而不是按平台分 —— 在
[`skills-maps/identity.md`](../../../cross-cutting/skills-maps/identity.md)。

## AI 辅助的 ramp（身份口味）

身份是那种 AI 既是巨大加速器**又是**真实危险源的地方，因为这里的产物关乎安全，而那些词汇跨平台
互相碰撞。

- **翻译，不要教程：** *"我懂 AD 组、LDAP 和 SSO 概念 —— 把这些映射到 Azure RBAC 与 Entra 角色
  上，并标出它们真正不同的地方。"*
- **生成最小权限，然后手动收紧：** *"恰好只做这件事、不多做任何事的那条最紧的 IAM policy /
  RBAC role。"* AI 起草时偏宽松；你来剪。
- **把 Azure 那两个平面理清：** *"这个任务需要一个 Entra 角色还是一个 Azure RBAC 角色，在哪个
  范围上？"* 每一次都问，直到它变成反射。
- **AI 会烧到你的地方（验得最狠的地方）：** 它会发明不存在的 IAM **action 字符串**和 RBAC 角色
  名；它会把 OAuth 和 OIDC 搅在一起；它会把 Entra 角色和 Azure RBAC 混起来；它会忘掉生命周期
  里*离职*那一半。每一条生成出来的 policy 都要对着文档核过，并用一次拒绝请求的探测测过。

## 诚实边界

这是一片**亲手做过的强项**，而笔记就这么直说：真实地建过并运维过目录/身份基础设施 ——
Active Directory 生命周期、一套自建的 **OpenLDAP 支撑的 SSO**、一次初始的 **Entra ID /
Azure AD** 搭建，以及规模上**通过 Graph 做的入转离自动化**，SCIM 作为一个能用的概念。凡是属于
*评估级*而非生产级的，都被那样标着 —— 例如 **Okta** 是被**否掉**的选项（选择了自建 OpenLDAP），
不是被运维了多年。这里的声称是：一份很深、可迁移的身份地基，加上一条通向任何一个具体 IdP 的、
快速且可验证的 ramp —— 而不是"十年 Okta"。
