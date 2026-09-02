---
kind: adr
axis: meta
themes: []
platforms: []
derived: true
mirrors: docs/adr/0017-a-drill-carries-its-own-reporter.md
summary: "二十三个 drill 带着同一段十五行的 reporter，手工复制，而它的两种方言已经分道扬镳。显而易见的修法是一个共享模块。决定恰恰相反：drill 不从这个仓库 import 任何东西，reporter 是一个只有一份正本的 vendored block，check.py 断言每一份拷贝逐字节一致。"
---
# drill 自带 reporter

> 🌐 **语言：** [English（默认）](../../../../docs/adr/0017-a-drill-carries-its-own-reporter.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/adr/0017-a-drill-carries-its-own-reporter.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

这个仓库里每个 drill 的结尾都一样：一个 `log()`，一个 `step()`，一个打印 ✓ 或 ✗ 并累计失败的
`check()`，以及一个只有每条教训都成立才以 `0` 退出的判决。
[`runnable-lab`](../../../../.claude/skills/runnable-lab/SKILL.md) 规定了这个模式，二十三个文件
遵守它 —— 靠的是带着同样的十五行，手工粘进去，一个文件一份。

放着不管，拷贝会漂，而这些已经漂了。九个 drill 在模块层定义 `check()`，配一个 `FAILURES` 列表；
其余的把它定义成 `main()` 里的闭包。一派在 `=== 3. title ===` 的横幅下打印 `✓` 和 `✗`；另一派在
`[3] title` 下打印 `OK` 和 `XX`。两种都没有错，也没有任何东西在两者之间做过决定 —— 它们是两位作者
的习惯，第三位作者理所当然会写出第三种。

显而易见的修法是一个共享模块：一个 `labkit.py`，每个 drill 都 import 它，改一处即可。这条记录存在，
是因为这个修法被拒绝了。

## 决定

**drill 不从这个仓库 import 任何东西。** [`CONTEXT.md`](../../CONTEXT.md) 把 lab 定义为*纯本地、
零依赖、自验证*，而它说的依赖不只是 `pip install`。一个 drill 是在 GitHub 页面上被读到、被拷进终端、
然后被跑起来的；它第一件不可以做的事就是以 `ModuleNotFoundError: labkit` 失败，因为一个第一课是
*你需要整个仓库*的 lab，教的是关于这个仓库的错误的东西。

**reporter 是一个 vendored block。** 一份正本 —— `log`、`step`、`check` 和判决 —— 逐字拷进每个
drill。它只是 reporter：fixture 数据、模型、教训和 `--break-it` 的机制仍然是 drill 自己的，因为那些
才是一个 drill *是什么*，而 reporter 只是它怎么说话。

**[`check.py`](../../../../check.py) 持有正本，并断言每个 drill 与之逐字节一致。** 一份走样的拷贝
是一个失败的检查，不是一种风格选择。这把二十三份粘贴的拷贝从负债变成被验证的约定 —— `check.py`
已经在为自己的 `slug()` 手工做这件事了：它的 docstring 写着*与另一个文件逐字节一致*，却没有任何
办法知道这句话是否仍然为真。

**这个 block 是 `=== n. title ===` 下的 `✓` / `✗`。** 那个 skill 在这条记录之前就规定了这一点；
另一派向它收敛，一个 drill 改一次。

**用 shell 写的 drill 在 shell 里带同样的契约**，对照一个 shell 的 block 检查，或者在
`check.py --list` 里被点名豁免。它不可以做的是被静默跳过 —— 这个仓库反复重新发现的那种失败。

## 考虑过的选项

- **一个通过 `sys.path` 找到的共享 `labkit.py`。** 改一处，不漂移，教科书答案。因上面的理由否决：
  它改变了 drill 是什么。每个 drill 都会多一行只在这个 checkout 里才能工作的代码，而词表的定义将
  不得不长出一个它没法向拷走了一个文件的读者解释的例外。

- **让拷贝保持原样，不检查。** 现状，而它在不到三个月里就产生了两种方言。按
  [ADR-0008](0008-a-count-is-not-a-bound.md) 的同一条教训否决：只活在散文和习惯里的约定是没有人在
  检查的约定，二十三份没有 guard 的拷贝就是二十三个漂移的地方。

- **从模板生成 drill。** reporter 归模板，教训归作者。否决，因为它颠倒了哪一半更重要：drill 是
  带断言的散文，而散文是模板最不擅长持有的那一半。生成器还会变成第二个要跑的东西，而 check 与
  build 那条链不需要它。

- **松散地检查拷贝 —— 一个指纹，或者*包含一个 `check()` 函数*。** 否决，因为松散的检查放进了
  它本该终结的漂移。逐字节一致是唯一意味着*这就是那个 block*的断言，而做到它不多花一分钱。

## 后果

- **`check.py` 多一个常量和一个检查。** block 以文本形式住在 `check.py` 里，`--list` 可以把它
  打印出来，drills 那一组把每个 `*_drill.py` 和它比对。
  [`runnable-lab`](../../../../.claude/skills/runnable-lab/SKILL.md) 这个 skill 指向那个常量，而不是
  带第二份拷贝。
- **每个 drill 被改一次**以向 block 收敛 —— 一次机械的改动，一次一个文件，干净运行和 `--break-it`
  运行的退出码都和之前一样。
- **改 block 是一次二十四个文件的改动，这是设计如此。** 这个代价就是重点：一个很少改、一改就到处
  一起改的 reporter 是约定，一个只在一处改的是依赖。谁觉得这个代价太高，谁就找到了支持
  `labkit.py` 的论据，应该重开这条记录，而不是绕过它。
- **bash 那个 drill 不豁免契约**，只豁免 Python 的 block。它的 `check()` 打印同样的记号、数同样的
  失败；`check.py` 在清单里说明这一点，而不是留读者去纳闷为什么少了一个 lab。
- **drill 仍然是可以拷走的。** 这一直都是不变量；这条记录做的是把它从一个习惯变成一个决定。
