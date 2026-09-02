---
kind: lab
axis: cross-cutting
themes: [iac-config]
platforms: []
derived: true
mirrors: cross-cutting/labs/terraform-state-and-drift/README.md
summary: "Terraform 并不是每次运行都对着真实世界收敛。它是对着一个状态文件做 plan 的，而配置、状态和现实这三者之间的缺口，正是每一次 Terraform 惊喜住的地方。"
---
# Lab —— 状态才是事实来源（而漂移是敌人）

> 🌐 **语言：** [English（默认）](../../../../../cross-cutting/labs/terraform-state-and-drift/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`cross-cutting/labs/terraform-state-and-drift/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 感觉到那件**一个 Ansible/配置管理系统管理员在 Terraform 上会搞错**的事 ——
它*并不是*每次运行都对着真实世界收敛。它是对着一个**状态文件**做 plan 的，而三个世界之间的缺口，
正是每一次 Terraform 惊喜住的地方：

```
config   your .tf — the desired state
state    terraform.tfstate — what Terraform BELIEVES exists
real     the actual infrastructure
```

`plan` = 先从 real 刷新 state，然后 diff **config 对 state** → 得出那些动作。
`apply` = 让 real 匹配 config，并把 state 更新成一致。

它演练什么 —— 从那一个模型里掉出来的六条教训：
1. **空状态 → CREATE。** 没有状态，所以 Terraform 计划去创建。
2. **apply → 收敛。** config == state == real；重新 plan 是一次干净的空操作。
3. **漂移 → 被改回去。** 一次对 real 的手改（那次控制台热修）会在刷新时被读进 state、被检测出来，
   并在下一次 apply 时**被改回 config** —— *Terraform 会跟你对着干。*
4. **不可变 → REPLACE。** 改一个 `ForceNew` 属性会强制**销毁+重建**，不是一次原地编辑。你只能靠
   在 plan 里读到 `forces replacement` 来抓住它。
5. **状态丢了 → 重复/覆盖。** 没有状态时，Terraform 想去*重新创建*一个已经存在的资源；
   `terraform import` 把状态和现实对上。
6. **`count` 对 `for_each`。** 从一个 `count` 列表中间删掉一项会让下标平移、把资源翻搅一遍；
   `for_each` 的 key 是稳定的，只有被删掉的那个 key 会被碰到。

## 为什么在本地

不用云账号、不用凭据、不用对着真实基础设施 `terraform apply`、不产生账单、没有爆炸半径。这个演练
是一份大约 200 行的 Terraform plan 引擎模型 —— 那个 配置/状态/现实 三角、刷新、替换对更新的决策，
以及下标寻址对 key 寻址 —— 好让你检视的是那份*逻辑*，不是满屏的 HCL。它在任何跑得了 Python 的地方
都跑得起来，在 CI 里也是。

## 跑

```bash
python3 state_drift_drill.py
```

## 你会看到什么

六个被叙述出来的步骤，每一个都带一个 `OK`/`XX`：一次空状态的 CREATE；apply 之后的收敛；一次控制台
热修被改回去；一次不可变变更强制 REPLACE；状态丢失时想去重新创建一个已存在的资源（然后被 `import`
修好）；以及 `count` 把一个平移了的资源翻搅一遍、而 `for_each` 放过了它的邻居。最后给出一个 PASS
判定，`exit 0`。

## 验证（要紧的那部分）

exit `0` = 每一条教训都成立；它兼作一个 CI 检查。现在**故意把这个模型弄坏** —— 有两条彼此独立的
破坏路径：

```bash
python3 state_drift_drill.py --break-it no-refresh    # plan 不再从 real 刷新 -> 漂移检测不到 -> 步骤 3 失败，exit 1
python3 state_drift_drill.py --break-it mutable-all   # 什么都不是 ForceNew -> 一次替换看起来像原地编辑 -> 步骤 4 失败，exit 1
```

如果无视真实世界的 plan 还能"通过"，那这次刷新本来就什么都没做；如果一次 ForceNew 变更看起来仍然
像一次原地编辑，那这条不可变规则本来就不承重。这些失败，正是这个模型确实要紧的证据。

## 重点

有两条配置管理的反射在这里同时被纠正。第一，**"再跑一遍就行了，它会收敛"** —— Terraform 的收敛是
经由一个*状态文件*中介的，而那个文件会漂、会被锁、会丢，而一次盲目的重跑可能会*销毁*东西。第二，
**"SSH 进去修一下"** —— 一次手动热修会变成漂移，并在下一次 apply 时被改回去。那门纪律是：改代码、
读 plan（尤其是留意 `forces replacement`）、把状态放远端 + 加锁，并且绝不绕过 Terraform 去编辑。
状态才是事实来源。完整的工单目录见 [Terraform support 笔记](../../terraform-support.md)，而发放在
哪儿结束、配置从哪儿开始见 [`iac-and-config.md`](../../iac-and-config.md)。

## 拆除

没有 —— 它就是一个自包含的脚本。把这个目录删掉就行。
