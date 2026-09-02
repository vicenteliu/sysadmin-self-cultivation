---
kind: lab
axis: platforms
themes: [identity, cloud]
platforms: [aws]
derived: true
mirrors: platforms/aws/labs/iam-deny-by-default/README.md
summary: "不用云、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。"
---
# Lab —— IAM 是默认拒绝的（亲手把它证明出来）

> 🌐 **语言：** [English（默认）](../../../../../../platforms/aws/labs/iam-deny-by-default/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/aws/labs/iam-deny-by-default/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把 [AWS support 笔记](../../support.md)那个中心教训变得摸得着 ——
**IAM 是默认拒绝的，一条显式的 `Deny` 永远胜出，而一条 SCP 或者一个 permissions boundary 连一个
"admin"都能封顶 —— 所以"给他 `Allow *` 不就完了"并不是你那份本地直觉以为的那个解法。** 你会跑一个
忠实（但简化）的 AWS 真实策略求值逻辑模型，看着请求因为五种不同的原因被拒绝 —— 也就是多数
"Access Denied"工单背后的那些确切原因。

**你会练到：** 把一个判定读成*"是哪一层说了不？"* —— 隐式拒绝（没有 allow）、显式拒绝、SCP 交集、
permissions boundary 天花板 —— 并且精确地看见那份本地的*"admin 什么都能干"*模型错在哪儿。

## 这个 lab 为什么是纯本地的

不用云、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。那些"策略"是一串 `Statement` 对象，
而那个求值器是 AWS 真实运算顺序的一份小而诚实的实现：

1. **任何**一条适用策略里的显式 `Deny` 覆盖一切。
2. 否则这个请求必须被一条**身份策略显式允许** —— 没有匹配的 Allow 就是一次*隐式拒绝*。
3. 如果有 SCP 适用，这个 action 还必须**同时**被每一条 SCP 允许（**交集**）。
4. 一个 **permissions boundary** 只能**削减**（一个天花板）。
5. 一条 **session policy** 只能削减。

（基于资源的策略和条件键也是存在的；这里略去，好让"默认拒绝 + 显式拒绝 + 交集"这个行为无可辩驳，
而不是被埋起来。）

## 跑它

```bash
python3 iam_eval_drill.py
```

就这样 —— 不用装任何东西。exit code `0` 表示每一条断言都成立，所以它兼作一个 CI 检查。

## 你会看到什么

六个被叙述出来的步骤，每一个都以一条被检查过的教训收尾：

```
=== 3. Explicit Deny beats Allow — even 'Allow *' admin ===
  admin (Allow *) + an explicit Deny on s3:DeleteObject → Deny (explicit deny in identity policy)
  ✓ explicit Deny overrides the Allow * — an admin can be blocked (LESSON 2)
=== 4. An SCP caps even the admin — and lives where the account can't see it ===
  admin (Allow *) but org SCP allows only s3:* → ec2:RunInstances → Deny
  ✓ the SCP intersection denies it despite Allow * — 'grant them admin' fails (LESSON 3)
=== 6. Your on-prem instinct vs. AWS reality — where they disagree ===
  s3:DeleteObject    instinct=Allow ≠ reality=Deny    (capped by explicit Deny)
  ec2:RunInstances   instinct=Allow ≠ reality=Deny    (capped by an SCP)
  s3:PutObject       instinct=Allow ≠ reality=Deny    (capped by a boundary)
```

## 验证（别光信这个脚本说的）

在那个文件旁边开一个 Python shell，自己去驱动那个求值器：

```python
from iam_eval_drill import evaluate, Statement, ADMIN
# Allow * 的 admin，但组织的 SCP 只允许 S3 —— 试着拉起一台实例：
scp = [Statement("Allow", ["s3:*"])]
print(evaluate("ec2:RunInstances", "*", identity=ADMIN, scps=[scp]))
# → ('Deny', 'denied by SCP #1 (org guardrail does not allow the action)')
```

然后刻意把它弄坏 —— 不是去改 `evaluate()`，而是让它按 on-prem 直觉读策略的方式去评估：

```bash
python3 iam_eval_drill.py --break-it allow-wins      # exit 1
python3 iam_eval_drill.py --break-it no-guardrails   # exit 1
```

`allow-wins` 把一条 Allow 当成答案，从不去看 Deny；`no-guardrails` 在 identity policy 就停止评估，
好像 SCP 和 boundary 是别人的问题。每一种都必须带着失败的断言**非零**退出 —— 一个不会失败的自我
验证器毫无价值。`check.py` 每次 push 都把两种都跑一遍。

## 重点

- **默认拒绝就是那个打破你直觉的反转。** 在本地，admin 是上帝，而防火墙是一张允许清单。在 AWS 上，
  `Allow *` 是那次求值的*开始*，不是结束 —— 还有五层可以说不。
- **一条显式的 `Deny` 永远胜出。** 护栏之所以被写成 Deny，恰恰是因为它们必须打得过任何 Allow，
  包括一个 admin 的。
- **那个拦路者可能从这个账号里根本看不见。** 一条 SCP 住在 AWS Organizations 里；那个请求被拒的
  账号常常连读都读不到它 —— 这也是为什么"加一条 allow 不就行了"会失败，而真正的技能是*读出是哪
  一层拒的*。
- **这是头号 support 工单。** "这为什么被拒了？"就是靠走一遍这些层来回答的 —— 在控制台里用 IAM
  Policy Simulator、CloudTrail 的 `errorCode`，以及 IAM Access Analyzer。你刚刚把那些工具所求值
  的那个模型建出来了。

## 拆除

没有创建任何持久化的东西 —— 这个演练不写任何文件。没有要清理的。
