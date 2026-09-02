---
kind: lab
axis: the-stack
themes: [virtualization, storage-backup]
platforms: []
derived: true
mirrors: the-stack/labs/04-backup-not-snapshot/README.md
summary: "不用云、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+ 和它自带的 sqlite3。"
---
# Lab 04 —— 备份不是快照（亲手把它证明出来）

> 🌐 **语言：** [English（默认）](../../../../../the-stack/labs/04-backup-not-snapshot/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`the-stack/labs/04-backup-not-snapshot/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把[第 04 章](../../04-storage.md)那个中心教训变得摸得着 —— **复制和快照会忠实地把破坏
也拷贝过去；只有一份独立的、时间点的备份才救得了你，而且只救到它的 RPO 为止。** 你会跑一个演练：
它给一个数据库灌上数据、把它复制出去、备份一次、再写进更多数据，然后把那张表 `DROP` 掉 ——
然后看清楚到底什么活了下来。

**你会练到：** 复制和备份之间的差别、真的去做一次恢复（而不只是"有一份备份存在"），以及测量
**RTO**（恢复花了多久）和 **RPO**（那份备份没能还给你多少数据）—— 每一次关于备份的对话真正在谈的
那两个数字。

## 这个 lab 为什么是纯本地的

不用云、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+ 和它自带的 `sqlite3`。三个目录替代三个
**故障域**：

| 目录 | 模拟什么 | 在真实世界里 |
| --- | --- | --- |
| `primary/` | 那个在线数据库 | 你的块存储卷（第 04 章） |
| `replica/` | 一份持续同步的拷贝 | RAID / 一个同步副本 / 同一个卷上的快照 |
| `vault/` | 独立的时间点拷贝 | 3-2-1 说的那份异地、独立账号的备份 |

用目录来替代*分离*是诚实的，但它替代不了介质或者地理位置 —— 重点是那个 vault 相对于 primary 的
命运的**独立性**，而那正是真正救人的那个属性。

## 跑它

```bash
python3 backup_drill.py
```

就这样 —— 不用装任何东西。exit code `0` 表示关于这个教训的每一条断言都成立，所以它兼作一个 CI
检查。几个有用的参数：

```bash
python3 backup_drill.py --seed-rows 5000 --post-backup-rows 500  # 更大的 RPO 缺口
python3 backup_drill.py --keep                                   # 把工作区留下来翻一翻
```

## 你会看到什么

这个演练会叙述八个步骤，并以三条被检查过的教训收尾：

```
=== 6. Assess the damage — what actually survived? ===
  ✓ primary is destroyed (table gone) — as expected
  ✓ replica is ALSO destroyed — replication is not backup (LESSON 1)
  ✓ the vault backup is untouched — independence is what saved it (LESSON 2)
...
=== 8. Count the RPO — what the backup could not give back ===
  rows LOST (RPO)  : 250   ← everything written after the last backup
  ✓ RPO cost exactly the 250 post-backup rows — RPO is real (LESSON 3)
```

## 验证（别光信这个脚本说的）

带 `--keep` 跑，然后自己去查那几个故障域：

```bash
python3 backup_drill.py --keep
# primary 和 replica 都丢了那张表：
sqlite3 drill-workspace/primary/app.db  "SELECT count(*) FROM widgets;"   # error: no such table
sqlite3 drill-workspace/replica/app.db  "SELECT count(*) FROM widgets;"   # error: no such table
# 只有 vault 里那份备份还有数据：
sqlite3 drill-workspace/vault/backup-0001.db "SELECT count(*) FROM widgets;"   # 一个真实的数字
```

（如果你没有 `sqlite3` 命令行，同样的查询在 Python 里也跑得了 —— 这个脚本只用标准库。）看见
primary 和 replica **两边**给出一模一样的 "no such table"，而 vault 用一个行数回答你 ——
这就是整个教训，三条命令。

## 重点

- **复制 ≠ 备份。** 那个副本瞬间而忠实地把那次 `DROP` 也镜像过去了 —— 面对一次 `DROP TABLE`、
  一次 `rm -rf` 或者一次勒索软件，一个同步副本或者一个同卷快照做的正是这件事。它熬得过*硬件*
  故障，熬不过*逻辑*破坏。
- **独立性才是那个救你的属性。** vault 里那份拷贝之所以能把数据恢复回来，只是因为那场灾难够不
  到它。
- **RPO 和 RTO 是数字，不是形容词。** 这个演练把两个都递给你：一次测量出来的恢复时间，以及最后
  一次备份之后写进去、任何恢复都还不回来的那些行的确切数目。"我们能丢多少，多久能回来？"现在有
  了一个你自己产出的具体答案。
- **一份你没恢复过的备份是一个愿望。** 你刚刚恢复了一份。

## 拆除

没有创建任何持久化的东西 —— 除非你传 `--keep`，否则那个工作区会被自动删掉。要删掉一个被留下来的
工作区：

```bash
rm -rf drill-workspace
```
