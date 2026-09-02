---
kind: lab
axis: platforms
themes: [cloud]
platforms: [oci]
derived: true
mirrors: platforms/oci/labs/a-compartment-is-not-an-account/README.md
summary: "OCI 那两条标志性的访问教训，徒手做、不用云账号：NotAuthorizedOrNotFound 是一个 404 而不是一个 403，所以一个资源是「不可见」而不是「明确被禁」；而 inspect/read/use/manage 是一个层级，不是一组角色。"
---
# Lab —— 一个 compartment 不是一个账号（一个动词也不是一个角色）

> 🌐 **语言：** [English（默认）](../../../../../../platforms/oci/labs/a-compartment-is-not-an-account/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/oci/labs/a-compartment-is-not-an-account/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 按你在一张工单里真正会撞上的样子，去感觉 OCI 那两条标志性的访问教训 ——
*徒手做，不用云账号* —— 好让 `NotAuthorizedOrNotFound` 和 `inspect/read/use/manage` 这个动词层级
不再是冷知识，而变成反射。

它演练什么：
1. **没有策略 → `NotAuthorizedOrNotFound`（一个 404，不是一个 403）。** 对"它不存在"和"你不许看
   它"，OCI 返回*同一个*报错 —— 那个资源是**不可见**的，不是明确被禁的。碰到这个报错，先怀疑一个
   策略/compartment/region 的问题，再怀疑一个资源不存在。
2. **动词是累加的：`inspect ⊂ read ⊂ use ⊂ manage`。** `read` 授予 get/list 但**不**授予 delete；
   `use` 能启停一个已有实例，但**创建不了**一个；`manage` 什么都能干，并且吞掉下面那些动词。
3. **compartment 就是那个范围。** 一条挂在**父** compartment 上的策略会**往下继承**到它的子级；
   一条范围限定在某一个 compartment 上的策略，在一个**兄弟**里**什么都不做**。范围就是那个边界
   —— 而不是一个新的账号/订阅/project。

## 为什么在本地

不用 tenancy、不用凭据、不用 OCID，也不用等 home region 传播。这个 lab 是一份大约 200 行的 OCI
策略求值模型 —— 动词层级、资源类型族、compartment 树继承，以及那个刻意为之的 404 歧义 —— 好让你
检视的是那份*逻辑*，不是满屏的控制台。它在任何跑得了 Python 的地方都跑得起来，在 CI 里也是。

## 跑

```bash
python3 verb_and_compartment_drill.py
```

## 你会看到什么

六个被叙述出来的步骤，每一个都带一个 ✓/✗：carol（没有策略）撞上那个 404；alice 那条范围在 Dev 上
的 `read` 够得到**子** compartment Dev:App（继承），但**删不掉**东西（动词的地板）；dave 的 `use`
启得动一个实例，但**创建不了**；bob 的 `manage` 什么都能干；而 bob 那条范围在 Dev 上的 `manage`
**碰不到兄弟** compartment Prod（隔离）。最后给出一个 PASS 判定，`exit 0`。

## 验证（要紧的那部分）

exit `0` = 每一条教训都成立；它兼作一个 CI 检查。现在**故意把这个模型弄坏**，看着那些保证塌掉 ——
有两条彼此独立的破坏路径：

```bash
python3 verb_and_compartment_drill.py --break-it verbs   # 每个动词都授予一切 -> 步骤 3 和 4 失败，exit 1
python3 verb_and_compartment_drill.py --break-it scope   # 策略变成整个 tenancy 范围 -> 步骤 6 失败，exit 1
```

如果把那个动词层级压平之后它还"通过"，那这个层级本来就什么都没做；如果范围变成整个 tenancy 之后
它还"通过"，那 compartment 本来就不是一个边界。这些失败，正是这个模型确实承重的证据。

## 重点

有两条 AWS/Azure/GCP 的反射在这里同时被纠正。第一，**"404 意味着它没了"** —— 在 OCI 上它同样经常
意味着*你没有策略*。第二，**"我对这个资源类型有访问权，所以我对它想干什么都行"** —— 在 OCI 上那个
**动词**给你能干什么封顶，那个 **compartment** 给你能在哪儿干封顶，而且两者都在一个 tenancy 内部
沿着一棵树往下继承。一个 compartment 不是一个账号；一个动词不是一个角色。完整的工单目录见
[OCI support 笔记](../../support.md)。

## 拆除

没有 —— 它就是一个自包含的脚本。把这个目录删掉就行。
