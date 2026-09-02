---
kind: guided-run
axis: platforms
themes: [cloud]
platforms: [azure]
derived: true
mirrors: platforms/azure/labs/README.md
summary: "对着一个沙箱订阅做的三次 guided run —— 和 AWS 那三次同一个形状，好让你感觉到这些概念在「迁移」，而不是从头再学一遍。"
---
# Azure —— Guided run

> 🌐 **语言：** [English（默认）](../../../../../platforms/azure/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/azure/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

对着一个沙箱订阅做的三次 guided run —— 和 [AWS 那三次](../../aws/labs/) 同一个形状，好让你
感觉到这些概念在*迁移*，而不是从头再学一遍。

**这些是 [guided run](../../../CONTEXT.md)，不是 lab。** 每一次都需要一个真实环境，所以这里没有
任何东西能断言你做过它，而 CI 也跑不了它。那就是全部的区分，而且它不是降级 —— 一次 guided run
够得到真实的延迟、真实的报错和真实的账单，而那是没有模型做得到的。

这个平台唯一的那个 lab —— 自验证、纯本地 —— 在弧的下面。

> **地面规则：** 用一个**免费/沙箱订阅**，先设一条 **Budget 告警**，把所有东西放进一个专用的
> **resource group**，做完就把那个 resource group 删掉（Azure 给你的最干净的拆除方式）。用
> **Bastion** 或者 `az ssh` 够到那些 VM —— 绝不要把 SSH/RDP 开到互联网上。

## 为什么是命令行

这里每一次 guided run 都是**命令行优先**的（`az`，PowerShell 的 `Az` 是同等的替代），而那是一个教学选择。
门户是用来*看*的；命令行是用来*做*的。一条 `az` 命令比一路翻 blade **更快**、**更精确**（不会挑错
下拉项）、**可复现**（粘进一份 runbook）、**可评审**（一份 diff，不是一段屏幕录像）—— 而且它就是
你的自动化所用的那片界面。凡是你点得了的，你都命令得了；而命令才是那个你能递给下一个人或者下一台
机器的东西。

## 那条三节 guided run 弧

### Run 01 —— 受限身份 + 盘点

一个最小权限的 **Reader**，然后盘点这个订阅 —— AWS lab 01 的 Azure 双胞胎。注意 **Azure Resource
Graph** 用一次查询就回答了组织范围的问题，不用循环（这是 Azure 的一项强项）：

```bash
az login
az account show --query '{sub:name, id:id}' -o table     # 确认是对的那个订阅

# 整个订阅，一次查询 —— Resource Graph（胜过逐资源循环）
az graph query -q "Resources | project name, type, location, resourceGroup | order by type asc" -o table

# 或者经典的逐服务列举
az vm list -d --query '[].{name:name, rg:resourceGroup, size:hardwareProfile.vmSize, power:powerState}' -o table
az storage account list --query '[].{name:name, rg:resourceGroup, kind:kind}' -o table
```

**验证：** 把那个 Reader 的范围收窄到一个 resource group，重跑，看着其余的从结果里消失 ——
那个范围限定被变得可见了。

### Run 02 —— 从代码起一套最小 VNet + VM

一个 VNet + 子网、一个**入站全无的 NSG**、一台带**托管身份**且**没有公网 IP** 的 VM，经 Bastion
可达。从命令行来（Terraform/Bicep 是那个持久形态；这里是那条命令式的序列）：

```bash
az group create -n lab-rg -l eastus
az network vnet create -g lab-rg -n lab-vnet --address-prefix 10.0.0.0/16 \
  --subnet-name app --subnet-prefix 10.0.1.0/24
az network nsg create -g lab-rg -n lab-nsg          # 默认 = 不放行任何入站。很好。
az vm create -g lab-rg -n lab-vm --image Ubuntu2204 \
  --vnet-name lab-vnet --subnet app --nsg lab-nsg \
  --public-ip-address "" --assign-identity \
  --admin-username azureuser --generate-ssh-keys
# 在「没有公网 IP」的情况下够到它 —— 走 Bastion 隧道：
az network bastion ssh -n lab-bastion -g lab-rg --target-resource-id "$(az vm show -g lab-rg -n lab-vm --query id -o tsv)" --auth-type ssh-key --username azureuser --ssh-key ~/.ssh/id_rsa
```

**验证：** `az vm show -d -g lab-rg -n lab-vm --query publicIps -o tsv` 返回空 —— 没有任何公网
暴露。**拆除：** `az group delete -n lab-rg --yes --no-wait`。

### Run 03 —— 安全的存储 + 一条策略护栏

安全默认值，加上一条*预防性*护栏（Azure Policy 让那件错的事变得不可能，而不只是告警）：

```bash
# 一个拒绝公开 blob 访问、并且强制 HTTPS 的存储账号
az storage account create -g lab-rg -n labstor$RANDOM -l eastus --sku Standard_LRS \
  --allow-blob-public-access false --https-only true --min-tls-version TLS1_2

# 一条 Budget 告警（现实里这是你「第一件」要做的事）
az consumption budget create --budget-name lab-budget --amount 20 --time-grain Monthly \
  --category Cost --start-date 2026-07-01 --end-date 2027-07-01

# 一条预防性护栏：DENY 掉任何允许公开 blob 访问的存储账号
az policy assignment create --name deny-public-blob \
  --policy "$(az policy definition list --query "[?displayName=='Storage accounts should prevent shared key access'].name | [0]" -o tsv)" \
  --resource-group lab-rg
```

**验证：** 试着把 `--allow-blob-public-access true` 翻过来，看着那条策略把它拒掉。
**拆除：** 已经折进 `az group delete -n lab-rg` 里了。

## 弧之外 —— 一个纯本地的 support 演练

上面那条三节弧需要一个沙箱订阅。还有一个 lab **什么都不需要** —— 一个纯本地、只用标准库、能自我
验证的演练，接着那篇 [support 笔记](../support.md)：

### `global-admin-is-not-owner/` —— Azure 的两个身份平面 ✅ 已建（纯本地）

把两个平面都建了模，并且在零凭据的情况下证明 Azure 那条标志性的访问教训 ——
**一个 Global Administrator（Entra）对 Azure 资源没有任何访问权；一个 Owner（RBAC）管不了用户；
那个提权开关授予的是在 `/` 上的 User Access Administrator（是「分配」，不是「使用」）**。见
**[`global-admin-is-not-owner/`](global-admin-is-not-owner/)**。

```bash
python3 global-admin-is-not-owner/two_planes_drill.py   # exit 0 = 那些教训成立；在 CI 里跑
```

在"我是 Global Admin，可我看不见那台 VM"落到你桌上的那一刻就去读它。

---

每次 guided run 落地时都带着代码（Terraform/Bicep + 任何脚本）、一份 `README`，以及明确的拆除步骤。
**Entra/身份**那一块（lab 01 那个受限角色，以及那个 support 演练）是从亲手做过的地面写出来的；
其余是那条诚实的 ramp。
