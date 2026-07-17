# generate

> **输入：** 一个选集——`--profile 名称` 或 `--pick 关注点,关注点`（可加 `--platform`）·
> **输出：** 写入 `--out 目录` 的独立工具箱包 · **风险：** 对仓库和你的系统只读——
> 只往 `--out` 里写，目标非空时拒绝执行（除非 `--force`）· **root：** 不需要

工具箱的"可定制"一半：一条命令组装出某个环境真正需要的子集——匹配的脚本、
配对的 Ansible 修复 roles 和 playbooks、以及引用完全满足的 Agent Skills——
生成一个可以直接交给同事或丢上跳板机的目录。

生成的包保持本仓库的目录结构（`toolbox/…`、`.claude/skills/…`），所以被复制文件里的
每个相对链接、每条文档中的命令都原样可用；包顶层会生成一份 `README.md`，说明包里
有什么、怎么跑、哪些约定随包生效。

## 用法

```bash
./generate.py --list                                    # 关注点、profile、目录清单
./generate.py --profile security-baseline --out ~/kit   # 具名场景
./generate.py --pick triage,backup --out ./pack         # 按关注点点菜
./generate.py --pick network --platform macos --out p   # 平台过滤
```

profile 只是具名的关注点集合——`linux-shop`（全部）、`security-baseline`
（加固 + 补丁）、`incident-response`（分诊 + 它路由到的修复）。它们和工具/role 的
关注点、平台标签、skill 的依赖清单一起都在 [`catalog.json`](../../../../toolbox/generate/catalog.json)
里——这就是完整的选择模型；新工具加一条 JSON 记录即可加入生成器。

## 内置的诚实规则

- 一个 skill **只有当它引用的所有东西都在包里时才随包**——包里永远不会出现
  指向包中不存在工具的 skill。
- 枚举整个工具箱的文档（charter、Ansible 线 README）只随全选包走，理由相同。
- 每个被复制的工具保留自己的 `Tested on:` 行——包继承仓库的诚实标注，
  而不是重新声称。

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 包已写出（或已显示 `--list`）|
| 1 | 选集有误：未知关注点/profile，或什么都没匹配上 |
| 2 | 用法/环境：缺 `--out`、目标非空且无 `--force`、checkout 不完整 |

## 验证环境

仅 Python 3.9+ 标准库。已验证：macOS 26（Python 3.14）与 Ubuntu 24.04 容器
（Python 3.12）——生成过 `security-baseline`、`linux-shop` 和平台过滤包；
从包根目录实跑过包内工具，并演练过拒绝/未知选集路径。lab 验证过，非生产级加固。
