# backup-restore-drill

> **输入：** 一个 tar 归档；可选它所备份的源目录 · **输出：** stdout 上恢复报告 ·
> **风险：** 对你的系统只读——只写它退出时会删掉的临时目录 · **root：** 不需要

用恢复来证明备份。把归档解压进一个用完即弃的临时目录，清点解出的内容，并——加
`--against` 时——将恢复结果与源目录逐字节比对。一个从未被恢复过的备份是一份指望，
不是备份（[the-stack lab 04](../../../the-stack/labs/04-backup-not-snapshot/)）。

## 用法

```bash
./backup-restore-drill.sh nightly-etc.tar.gz                       # 到底能不能解开？
./backup-restore-drill.sh nightly-etc.tar.gz --against /etc        # 和现实对得上吗？
```

备份任务跑完后立刻运行以获得最强保证；对着较旧的归档运行，则能了解一次真实恢复
会带来多少漂移。

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 恢复成功（给了 `--against` 时并与源一致）|
| 1 | 解压失败、恢复为空、或恢复与源不一致 |
| 2 | 用法错误 |

## 验证环境

macOS 26（bsdtar）与 Ubuntu 24.04 容器（GNU tar）：一致、篡改、损坏归档三种情形。
lab 验证过，非生产级加固。
