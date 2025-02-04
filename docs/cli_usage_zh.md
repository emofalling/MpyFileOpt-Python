# `mpyfopt`命令用法

🌐 [English](./cli_usage.md)

注意：如果是通过定位目录而非安装的方式使用`mpyfopt`，则下文所有命令中的`mpyfopt`应替换为`./mpyfopt.py`或`.\mpyfopt.py`。

## 命令规则

```shell
mpyfopt <args> {<subcommand> <subcommand_args>}*n
# 此处{<Any>}*n 表示Any可以被重复任意次（即这部分可以是<Any>，也可以是<Any> <Any> <Any>...）
```

关于`<args>`，请参考命令`mpyfopt --help`的输出。  
关于`<subcommand>`，请参考命令`mpyfopt --subcmd-help *`的输出和下文**子命令**章节。
关于`<subcommand_args>`，请参考命令`mpyfopt --subcmd-help :<subcommand>`的输出(如`mpyfopt --subcmd-help :cd`)和下文**子命令**章节。

例如：

```shell
mpyfopt -p /dev/ttyUSB0 cd /lib ls
mpyfopt -p /dev/ttyUSB1 -To 20 write ./main.py ./your_project/main.py
mpyfopt -p /dev/ttyUSB0 -To 10 cd ./lib/your_module cat README.md
```
