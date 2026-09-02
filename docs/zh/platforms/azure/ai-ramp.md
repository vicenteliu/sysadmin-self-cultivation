---
kind: companion
axis: platforms
themes: [cloud]
platforms: [azure]
derived: true
mirrors: platforms/azure/ai-ramp.md
summary: "快速在 Azure 上走到胜任。和别处同一门纪律（AI 提供速度，判断提供真相 —— 见 ai-workflow/ 和 AWS 那条 ai-ramp）；这篇笔记讲的是 Azure 特有的那部分差量。"
---
# Azure —— 那条 AI 辅助 ramp

> 🌐 **语言：** [English（默认）](../../../../platforms/azure/ai-ramp.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/azure/ai-ramp.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 快速在 Azure 上走到*胜任*。和别处同一门纪律（**AI 提供速度，判断提供真相** —— 见
> [`ai-workflow/`](../../ai-workflow/how-i-use-ai-to-learn-and-operate.md) 和
> [AWS 那条 ai-ramp](../aws/ai-ramp.md)）；这篇笔记讲的是 Azure 特有的那部分差量。

## 如果你已经有锚，Azure 是最容易上手的那朵云

等你走到 Azure 的时候，你通常已经有两个锚：

1. **本地基本功** —— 而 Azure 奖励它们，因为它是从 Active Directory 和 Windows Server 长出来的。
   Entra ID、组策略式的思维、RBAC —— 其中很多是熟悉的。
2. **那套 AWS 心智模型**（如果你做过那个模块）—— 而其中约八成是一一对应的。

所以杠杆最高的第一个提示词是一张**映射表**，不是一份教程：

> *"我懂 AWS（IAM、VPC、EC2、S3、CloudFormation）和本地 Active Directory。给我建一张到 Azure
> 对应物的映射表，并在第二栏里标出 Azure 真正不同、而不只是改了名的地方。"*

一个下午你就能开始干活，而"真正不同"那一栏就是你的学习清单。

## 那些映射得很糟的 Azure 特有之物（这些验得最狠）

这些恰恰是 AWS 模型误导你、而 AI 自信地错着的地方：

- **两套权限系统。** **Entra ID 角色**（目录：谁能管理用户、应用、组）**不是** **Azure RBAC**
  （资源：谁能碰这台 VM/存储）。AWS 有一套 IAM；Azure 有两个平面。AI 一直把它们混在一起。
- **Resource Group。** AWS 没有真正的对应物 —— 一个强制的生命周期容器。范围、成本和 RBAC 全都以它
  为键。刻意地围着它设计。
- **RBAC 范围继承。** 一个在 subscription 上分配的角色会向下流到每一个 RG 和每一个资源。把
  `Owner` 分配得太高，就是那个 Azure 爆炸半径错误。
- **Managed Identity**，不是 instance profile —— 同一个想法（"机器上不放密钥"），不同的名字，
  而且有两种口味（system 分配对 user 分配）。
- **Bicep 对 ARM 对 Terraform** —— AI 会把 ARM JSON 和 Bicep 语法混起来，并对 resource provider
  的属性名产生幻觉。对着 Bicep/Terraform 的资源参考核实每一个属性。
- **`az` 对 `Az` PowerShell** —— 两套不同的 CLI，动词不同；AI 会把它们混起来。

## 提示词工具包（Azure 口味）

- **翻译者** —— "把〈某个 AWS 的东西 / AD 的东西〉映射到 Azure；标出真正的差别。"
- **权限解缠器** —— "这个任务需要一个 Entra 角色还是一个 Azure RBAC 角色，在哪个范围上？"
  （每一次你不确定的时候都问这个 —— 早期你会经常不确定。）
- **最小权限** —— "最接近*恰好*这件事的那个内置 RBAC 角色，或者一个只做这件事、在 RG 范围上的
  自定义角色。"
- **评审者** —— "从安全（公开暴露、加密）、成本和最小权限的角度评审这份 Bicep/Terraform。"
- **橡皮鸭** —— 把那条 `az` 报错 / Activity Log 里一次被拒绝的动作贴进去。

## 诚实的那部分

因为身份才是真正有亲手经验的地方（Entra/Azure AD 搭建加生命周期），这里的 ramp 是*不对称*的：
身份那片面是深度，资源那些面是进行中的广度。方法是一样的 —— AI 把查找压掉，而核实和那些 lab 让它
变真实 —— 但这个模块不假装整件事一样深。那份诚实就是这个招牌。
