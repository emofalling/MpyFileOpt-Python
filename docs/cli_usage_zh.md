# `mpyfopt`命令用法

🌐 [English](./cli_usage.md)

注意：如果是通过定位目录而非安装的方式使用`mpyfopt`，则下文所有命令中的`mpyfopt`应替换为`./mpyfopt.py`或`.\mpyfopt.py`（视情况而定）。

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
mpyfopt -p /dev/ttyUSB0 cd /lib ls # mpyfopt -p /dev/ttyUSB0 -> cd /lib -> ls
mpyfopt -p /dev/ttyUSB1 -To 20 write ./main.py ./your_project/main.py # mpyfopt -p /dev/ttyUSB1 -To 20 -> write ./main.py ./your_project/main.py
mpyfopt -p /dev/ttyUSB0 -To 10 cd ./lib/your_module cat README.md # mpyfopt -p /dev/ttyUSB0 -To 10 -> cd ./lib/your_module -> cat README.md
```

由于子命令分隔方式为直接命令名匹配，所以在一些特殊情况下，命令的解析可能不会符合预期。例如：

```shell
mpyfopt -p /dev/ttyUSB0 push ./receive push # mpyfopt -p /dev/ttyUSB0 -> push ./receive -> push
```

上述命令可以改为如下形式以避免解析错误：

```shell
mpyfopt -p /dev/ttyUSB0 push ./receive ./push # mpyfopt -p /dev/ttyUSB0 -> push ./receive ./push
```

## 主命令参数

```shell
mpyfopt [-h] [--subcmd-help SUBCMD_HELP] [--version]
        [-p PORT] [-B BAUDRATE] [-P PARITY] [-S STOPBITS]
        [-To TIMEOUT] [-Tw WRITE_TIMEOUT] [-Tb INTER_BYTE_TIMEOUT] [-wt WAIT_TIMEOUT]
        [-pbmaxw PROGRESSBAR_MAXWIDTH] [-pbminw PROGRESSBAR_MINWIDTH] [-nc] [-v]
```

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `--subcmd-help SUBCMD_HELP`: 显示子命令的帮助信息并退出。`SUBCMD_HELP`语法：
  - 当`SUBCMD_HELP`为`*`时，显示所有子命令的帮助信息，但不显示每个子命令的用法。
  - 当`SUBCMD_HELP`为`:<subcmd>`时，显示子命令`<subcmd>`的帮助信息，且显示它的用法。
- `--version`: 显示程序版本号并退出。
- `-p PORT`,`--port PORT`: 串口名。
- `-B BAUDRATE`,`--baudrate BAUDRATE`: 串口波特率，默认为115200。
- `-P PARITY`,`--parity PARITY`: 串口校验位，默认为N，即无校验（具体参考实际输出）。
- `-S STOPBITS`,`--stopbits STOPBITS`: 串口停止位，默认为1（具体参考实际输出）。
- `-To TIMEOUT`,`--timeout TIMEOUT`: 串口超时时间，单位为秒，默认为1。
- `-Tw WRITE_TIMEOUT`,`--write-timeout WRITE_TIMEOUT`: 串口写入超时时间，单位为秒，默认为1。
- `-Tb INTER_BYTE_TIMEOUT`,`--inter-byte-timeout INTER_BYTE_TIMEOUT`: 串口字节间超时时间，单位为秒，默认为0.1。
- `-wt WAIT_TIMEOUT`,`--wait-timeout WAIT_TIMEOUT`: 等待micropython设备响应的超时时间，单位为秒，默认为10。
- `-pbmaxw PROGRESSBAR_MAXWIDTH`,`--progressbar-maxwidth PROGRESSBAR_MAXWIDTH`: 进度条的最大宽度，单位为字符，必须大于0，默认为50。
- `-pbminw PROGRESSBAR_MINWIDTH`,`--progressbar-minwidth PROGRESSBAR_MINWIDTH`: 进度条的最小宽度，单位为字符，必须大于0，默认为5。
- `-nc`,`--no-colorful`: 使输出单色。如果终端无法解析ANSI颜色转义序列，建议选择此选项。
- `-v`,`--verbose`: 输出调试信息。

## 子命令及其参数

注：标`*`的子命令为类[GNU](https://www.gnu.org/)子命令，其命令格式与**GNU工具集**中的对应命令格式相似，但并非完全相同。

### `shell`

```shell
shell [-h]
```

提供一个交互式命令行界面用于更方便的手动键入子命令。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。

shell类似于：

```shell
/ >
```

其中，`/`表示当前工作目录。

通过shell键入子命令的示例：

```shell
~ $ mpyfopt -p /dev/ttyUSB0 shell
/ > cd /lib
/lib > ls
uasyncio repl.py
/lib > exit
~ $
```

在`shell`中，`exit`命令用于退出`shell`，但`shell`之后的子命令仍会继续执行。`exit`命令无参数和选项。

### `help`

```shell
help [-h] [-u] [cmds ...]
```

显示子命令的帮助信息。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `-u`,`--usage`: 显示子命令的用法。
- `cmds`: 要显示帮助信息的子命令，不指定则显示所有子命令的帮助信息。

### `ver`

```shell
ver [-h] [-c] [-v]
```

输出工具版本号和指令码程序版本号。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `-c`,`--csv`: 以CSV格式输出。
- `-v`,`--verbose`: 输出调试信息。

在不指定`-c`或`--csv`时，输出类似于：

```text
mpyfopt version: x.x
   code version: x.x
```

在指定`-c`或`--csv`时，输出类似于：

```text
x.x,y.y
```

其中，`x.x`对应`mpyfopt version`，`y.y`对应`code version`。

### `uname`*

```shell
uname [-h] [-a] [-s] [-n] [-r] [-v] [-m] [-c] [--verbose]
```

输出设备信息。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `-a`,`--all`: 显示所有信息。
- `-s`,`--kernel-name`: 显示内核名称。这是默认选项。
- `-n`,`--nodename`: 显示网络节点主机名。
- `-r`,`--kernel-release`: 显示内核发布版本。
- `-v`,`--kernel-version`: 显示内核版本。
- `-m`,`--machine`: 显示机器硬件名称。
- `-c`,`--csv`: 以CSV格式输出。
- `--verbose`: 输出调试信息。

### `uid`

```shell
uid [-h] [-v]
```

输出设备的UID。在不同的设备上，其长度可能不同。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `-v`,`--verbose`: 输出调试信息。

### `freq`

```shell
freq [-h] [-r] [-v]
```

输出设备CPU频率。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `-r`,`--raw`: 以原始数据形式输出。
- `-v`,`--verbose`: 输出调试信息。

在不指定`-r`或`--raw`时，以人类可读的方式输出（1M=1000k, 1k=1000），输出类似于：

```text
240.0 MHz
```

在指定了`-r`或`--raw`时，以原始数据形式输出，输出类似于：

```text
240000000
```
