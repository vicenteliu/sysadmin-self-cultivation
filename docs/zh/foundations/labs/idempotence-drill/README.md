---
kind: lab
axis: foundations
themes: [linux-scripting]
platforms: []
derived: true
mirrors: foundations/labs/idempotence-drill/README.md
summary: "一个幂等的脚本是基础设施，一个脆弱的脚本是负债；strict mode 就是一件工具和一把自伤枪之间的那条线。建出来、跑两遍、在 bash 里感觉到。"
---
# Lab —— 幂等与 `set -euo pipefail`（脆弱对上安全，在 bash 里感觉到）

> 🌐 **语言：** [English（默认）](../../../../../foundations/labs/idempotence-drill/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`foundations/labs/idempotence-drill/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把 [foundations](../../README.md) 那个中心教训变得摸得着 —— **一个幂等的脚本（能安全
跑两遍）是基础设施；一个脆弱的脚本是负债，而 `set -euo pipefail` 就是一件工具和一把自伤枪之间的
那条线。** 你会跑一个演练：它造一个脆弱脚本和一个安全脚本，各自反复跑，然后检查那个差别。

**你会练到：** 认出那些非幂等的操作（那次无条件的追加、那个光秃秃的 `mkdir`）、为什么漏掉
`set -e` 会把失败掩盖掉，以及那个安全模式 —— strict mode、一道必填参数的守卫、`mkdir -p`，
以及先检查再追加。

## 这个 lab 为什么是纯本地的

除了 `bash` + coreutils 之外没有任何依赖，不用云，不用 root。它在一个用完即弃的 `mktemp` 目录里
工作，并且自己清理干净。重点是那份肌肉记忆：做完这个之后，一行非幂等的代码在你眼里*看起来*就是
错的。

## 跑它

```bash
bash idempotence_drill.sh
```

exit code `0` 表示每一条断言都成立 —— 它兼作一个 CI 检查。加上 `--keep` 可以把那个工作区留下来
查看。你会看到：

```
=== 1. The FRAGILE script — no safety, not idempotent ===
  ✓ the fragile script DOUBLED its config line on the 2nd run (LESSON 1)
  ✓ it reported SUCCESS (exit 0) despite mkdir failing — no set -e (LESSON 2)
=== 2. The SAFE script — set -euo pipefail + idempotent ===
  ✓ IDEMPOTENT — the line is present exactly once after 3 runs (LESSON 3)
  ✓ with no argument it FAILS FAST (the ${1:?} guard) (LESSON 4)
```

## 验证（别光信这个脚本说的）

把工作区留下，自己去读那两个配置文件：

```bash
bash idempotence_drill.sh --keep                 # 最后一行是 "(workspace kept at /…/tmp.XXXX)"
W=/…/tmp.XXXX                                    # 它打印出来的那个路径
cat $W/fragile-run/app/app.conf                  # server=prod —— 两次
cat $W/safe-run/app/app.conf                     # server=prod —— 一次
WORKDIR_INNER=$W/fragile-run bash $W/fragile.sh; echo "exit $?"   # 第三次跑
cat $W/fragile-run/app/app.conf                  # 现在是三次，而它说 exit 0
```

要看的是第三次：`mkdir` 失败了，那一行照样追加，退出码说成功。每一句"脚本跑得好好的"背后留下一台
半配置的机器，就是这个形状。用同样的方式把 `safe.sh` 跑第四次，文件不变 —— 收敛是一件你可以 `cat`
出来的事。

## 重点

- **非幂等的操作在重跑时会翻倍。** `echo x >> file` 每次都追加；`mkdir`（没有 `-p`）第二次就崩。
  那个脆弱脚本重跑之后留下了一行重复的配置 —— "跑它两遍"把它弄坏了。
- **没有 `set -e`，一个脚本会把自己的失败掩盖掉** —— 那个脆弱脚本的 `mkdir` 在第二次跑时失败了，
  可它报告 exit `0` 并且继续往下走，带着一个半成品状态继续造成破坏。一个"成功的"脚本就是这样留下
  一台坏掉的机器的。
- **那个安全模式会收敛。** `set -euo pipefail`、用 `${1:?...}` 拒绝一个空参数、`mkdir -p`，
  以及用 `grep -qxF ... || echo >>` 做"只在不存在时才追加" —— 跑一遍还是跑一百遍，状态都一样。
- **每一个 IaC 工具都建在这上面。** Ansible 的"这个包应该在"和 Terraform 的 plan/apply 就是幂等
  被产品化了。你刚刚在 bash 里感觉到了那个原始版本 —— 这也是为什么
  [iac 那一章](../../../cross-cutting/iac-and-config.md)说：如果你在这里内化了幂等，那你已经懂了
  那边每一个工具的内核。

## 拆除

这个演练会自动清理它那个 `mktemp` 工作区。如果你带 `--keep` 跑了，把它打印出来的那个路径删掉
（`rm -rf /var/folders/.../tmp.XXXX`）。
