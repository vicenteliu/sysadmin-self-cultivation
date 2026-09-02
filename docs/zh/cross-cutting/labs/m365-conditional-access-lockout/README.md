---
kind: lab
axis: cross-cutting
themes: [identity, itsm-saas]
platforms: []
derived: true
mirrors: cross-cutting/labs/m365-conditional-access-lockout/README.md
summary: "不用租户、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。"
---
# Lab —— Conditional Access 把自己锁在外面（亲手把它证明出来）

> 🌐 **语言：** [English（默认）](../../../../../cross-cutting/labs/m365-conditional-access-lockout/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`cross-cutting/labs/m365-conditional-access-lockout/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把 [M365 support 笔记](../../m365-support.md)里最危险的那条教训变得摸得着 ——
**一条范围指向"All users"的 Conditional Access 策略，在你启用它的那一瞬间就是租户级生效的；它会
挡住每一个不满足那条授予条件的人，包括写它的那个管理员，以及那个没被排除的 break-glass 账号 ——
而 `report-only` 就是你在故障*之前*、而不是在故障当中学到这件事的方式。** 你会发布一条朴素的策略、
看着自己被锁在外面、加上那道消防出口，然后看见 report-only 什么都不强制执行。

**你会练到：** 那篇笔记坚持的那个反射 —— **排除两个 break-glass 账号，并且先跑 report-only** ——
方法是亲身感觉一下不这么做会发生什么。

## 这个 lab 为什么是纯本地的

不用租户、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。四个 `User` 和一条 `CAPolicy` 给那个
租户建了模；`evaluate_sign_in()` 施加的是和真实服务一样的顺序：**状态 → 范围 → 排除 → 授予控制**。
那个 break-glass 账号是按那篇笔记规定的样子建模的 —— 仅云、用一把 FIDO2 密钥、*不是*一台 Intune
合规设备 —— 而这恰恰就是一条"要求合规设备"的授予条件会逮住它的原因。

## 跑它

```bash
python3 ca_lockout_drill.py
```

就这样 —— 不用装任何东西。exit code `0` 表示每一条断言都成立，所以它兼作一个 CI 检查。

## 你会看到什么

五个被叙述出来的步骤，每一个都以一条被检查过的教训收尾：

```
=== 1. Ship a naive policy: All users, require compliant device, ENABLED ===
  admin        LOCKED OUT  — BLOCKED: policy requires a compliant device, user has none
  alice        sign-in OK  — grant satisfied
  ✓ the ADMIN who wrote it is locked out — 'it won't apply to me' is false (LESSON 1)
=== 2. The break-glass account is NOT excluded — so it's locked out too ===
  ✓ break-glass is ALSO locked out — you now have NO way back in (LESSON 2)
=== 4. The safe way to have shipped it: the SAME policy in REPORT-ONLY ===
  ✓ report-only enforces NOTHING — nobody is blocked, impact is only logged (LESSON 4)
```

## 验证（别光信这个脚本说的）

在一个 Python shell 里自己去驱动这个模型：

```python
from ca_lockout_drill import User, CAPolicy, evaluate_sign_in
admin = User("admin", compliant_device=False)
enabled = CAPolicy("Require compliant device", state="enabled",
                   all_users=True, require_compliant_device=True)
print(evaluate_sign_in(admin, enabled))   # (False, 'BLOCKED: ... no compliant device')
enabled.excluded = {"admin"}
print(evaluate_sign_in(admin, enabled))   # (True, 'excluded from the policy (the fire exit)')
```

然后刻意把它弄坏 —— 让 report-only 像 enabled 一样去强制执行 —— 再跑一次：这个演练必须**非零**
退出。一个不会失败的自我验证器毫无价值。

## 重点

- **"我是管理员，它不会作用到我头上"是假的。** 一条 all-users 的策略对它的作者没有任何特殊照顾；
  它被启用的那一刻，它同样在求值*你*。
- **break-glass 只有在你把它排除掉的时候才活得下来。** 两个仅云的应急账号，被排除在每一条 CA 策略
  之外，就是"两分钟恢复"和"在故障期间开一个 Microsoft support case"之间的差别。
- **`report-only` 是那个安全阀。** 它求值并记录影响，但不强制执行 —— 每一条新的租户级策略都先这样
  发布，去读那些登录日志，*然后*再启用。这个演练展示了同一条策略如何仅凭翻转一个字段，就从"把所有
  人锁在外面"变成"什么都不强制执行"。
- **这就是那个租户级的爆炸半径，被感觉到。** 一条策略、一次保存、所有人同时中招 —— 恰恰就是那篇
  笔记说"绝不要在没有试点组和 report-only 的情况下编辑一条租户级策略"的原因。

## 拆除

没有创建任何持久化的东西 —— 这个演练不写任何文件。没有要清理的。
