---
kind: lab
axis: platforms
themes: [cloud]
platforms: [azure]
derived: true
mirrors: platforms/azure/labs/global-admin-is-not-owner/README.md
summary: "不用租户、不用订阅、不用凭据、不装外部包 —— 只要 Python 3.8+。"
---
# Lab —— Global Admin 不是 Owner（亲手把它证明出来）

> 🌐 **语言：** [English（默认）](../../../../../../platforms/azure/labs/global-admin-is-not-owner/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/azure/labs/global-admin-is-not-owner/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把 [Azure support 笔记](../../support.md)里那条 Azure 标志性的访问教训变得摸得着 ——
**Azure 有两个彼此独立的身份平面：Microsoft Entra ID 的目录角色管租户，Azure RBAC 管资源，而它们
「互不跨越」。一个 Global Administrator 对 Azure 资源没有任何访问权；一个 Owner 管不了用户。唯一
那座桥是那个提权开关 → 在根 `/` 上的 User Access Administrator（是「分配」，不是「使用」），
而资源访问真正的解法是一次带范围的 RBAC 分配。** 你会跑一个忠实的双平面模型，看着每一次跨平面的
请求被拒。

**你会练到：** 那篇笔记坚持的那个反射 —— *在授予任何东西之前，先判定你在哪个平面上* —— 以及把
`AuthorizationFailed` 读成"平面错了 / 范围错了"，而不是"把他设成 Global Admin"。

## 这个 lab 为什么是纯本地的

不用租户、不用订阅、不用凭据、不装外部包 —— 只要 Python 3.8+。Entra 的目录角色和 Azure RBAC 角色
是几个小字典；资源平面用真实的 ARM 风格路径给
**management group → subscription → resource group → resource** 这个范围层级建了模，所以继承
（一个订阅上的 `Owner` 够得到它下面的一台 VM）和隔离（在另一个订阅里什么都不是）都是精确的。

（那些角色/action 名是示意性的；那个*行为* —— 两个互不跨越的平面、可叠加的范围继承、提权 = 在
`/` 上的 User Access Administrator、解法是一次带范围的 RBAC 分配 —— 是真实的。）

## 跑它

```bash
python3 two_planes_drill.py
```

就这样 —— 不用装任何东西。exit code `0` 表示每一条断言都成立，所以它兼作一个 CI 检查。

## 你会看到什么

六个被叙述出来的步骤，每一个都以一条被检查过的教训收尾：

```
=== 1. A Global Administrator tries to read a VM (an Azure resource) ===
  global-admin (Entra Global Administrator) → read vm1 → AuthorizationFailed
  ✓ Global Administrator has NO Azure RBAC → denied on the resource (LESSON 1)
=== 4. The one bridge: the elevation toggle → User Access Administrator at '/' ===
  global-admin can now assign access on the VM = True, can write it = False
  ✓ elevation grants User Access Administrator at '/' — ASSIGN roles, not USE resources
=== 6. Scope is everything: an Owner on S1 does nothing in S2 ===
  res-owner (Owner on /subscriptions/S1):  write S1 VM → OK,  write S2 VM → AuthorizationFailed
```

## 验证（别光信这个脚本说的）

在一个 Python shell 里自己去驱动这个模型：

```python
from two_planes_drill import Principal, elevate, VM
ga = Principal("ga", entra_roles=["Global Administrator"])
print(ga.can_resource("read", VM))   # False —— Global Admin 没有 RBAC
elevate(ga)                          # 把「Azure 资源的访问管理」那个开关翻过来
print(ga.can_resource("manage-access", VM))  # True —— 现在可以「分配」角色了
print(ga.can_resource("write", VM))          # False —— 仍然「用」不了这个资源
```

然后刻意把它弄坏 —— 让那两个平面互相跨越（一个 Entra 角色授予资源访问）—— 再跑一次：这个演练必须
**非零**退出。一个不会失败的自我验证器毫无价值。

## 重点

- **两扇门，一把钥匙永远开不了另一扇。** *Entra = 你是谁*（那个目录）；*Azure RBAC = 你碰得了
  什么*（那些资源）。Global Admin 是其中一个平面的顶，也是另一个平面的底。
- **那个提权开关是 break-glass，不是日常座驾。** 它授予的是**在 `/` 上的 User Access
  Administrator** —— 也就是在整个租户范围内*分配*角色的权力，好让你能引导或者恢复访问。它不让你
  *使用*资源，而且用完你要把它关回去。
- **用一次带范围的 RBAC 分配去修资源访问。** 不是靠发 Global Administrator。resource group 上的
  一个 `Reader` 授予（经由继承的）读，而且*只有*读 —— 这就是带范围的 RBAC 胜过一个宽泛目录角色
  的意义。
- **范围就是爆炸半径。** 一次分配沿着它的范围往下继承，然后停住；订阅 S1 上的一个 `Owner` 在 S2
  里什么都不是。这就是每一次 `AuthorizationFailed` 背后的那个心智模型。

## 拆除

没有创建任何持久化的东西 —— 这个演练不写任何文件。没有要清理的。
