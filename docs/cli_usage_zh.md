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

## 命令参数

usage: mpyfopt [-h] [-p PORT] [-B BAUDRATE] [-P PARITY] [-S STOPBITS] [-To TIMEOUT] [-Tw WRITE_TIMEOUT] [-Tb INTER_BYTE_TIMEOUT] [-wt WAIT_TIMEOUT] [--subcmd-help SUBCMD_HELP]
               [-pbmaxw PROGRESSBAR_MAXWIDTH] [-pbminw PROGRESSBAR_MINWIDTH] [-v] [-nc] [--version]

Connect to MicroPython device and do something with subcommands.

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  serial port
  -B BAUDRATE, --baudrate BAUDRATE
                        serial baudrate. default 115200
  -P PARITY, --parity PARITY
                        serial parity. default N
  -S STOPBITS, --stopbits STOPBITS
                        serial stopbits. default 1
  -To TIMEOUT, --timeout TIMEOUT
                        serial timeout. if 0, no timeout. default 1
  -Tw WRITE_TIMEOUT, --write-timeout WRITE_TIMEOUT
                        serial write timeout. if 0, no timeout. default 1
  -Tb INTER_BYTE_TIMEOUT, --inter-byte-timeout INTER_BYTE_TIMEOUT
                        serial inter-byte timeout. default 0.1
  -wt WAIT_TIMEOUT, --wait-timeout WAIT_TIMEOUT
                        serial wait timeout. default 10
  --subcmd-help SUBCMD_HELP
                        print help message of subcommand
  -pbmaxw PROGRESSBAR_MAXWIDTH, --progressbar-maxwidth PROGRESSBAR_MAXWIDTH
                        progressbar max width. unit is chars. it must be > 0. default 50.
  -pbminw PROGRESSBAR_MINWIDTH, --progressbar-minwidth PROGRESSBAR_MINWIDTH
                        progressbar min width. unit is chars. it must be > 0. default 5.
  -v, --verbose         output debug info
  -nc, --no-colorful    make output not colorful. if terminal not support ANSI color escape sequence, recommended select this option
  --version             show program's version number and exit

See README.md for more information.

```shell
mpyfopt [-h] [-p PORT] [-B BAUDRATE] [-P PARITY] [-S STOPBITS] [-To TIMEOUT] [-Tw WRITE_TIMEOUT] [-Tb INTER_BYTE_TIMEOUT] [-wt WAIT_TIMEOUT] [--subcmd-help SUBCMD_HELP]  [-pbmaxw PROGRESSBAR_MAXWIDTH] [-pbminw PROGRESSBAR_MINWIDTH] [-v] [-nc] [--version]
```

- `-h, --help`: 显示帮助信息并退出。
- `-p PORT, --port PORT`: 串口名。
- `-B BAUDRATE, --baudrate BAUDRATE`: 串口波特率，默认为115200。
- `-P PARITY, --parity PARITY`: 串口校验位，默认为N，即无校验（具体参考实际输出）。
- `-S STOPBITS, --stopbits STOPBITS`: 串口停止位，默认为1。
- `-To TIMEOUT, --timeout TIMEOUT`: 串口超时时间，单位为秒，默认为1。
- `-Tw WRITE_TIMEOUT, --write-timeout WRITE_TIMEOUT`: 串口写入超时时间，单位为秒，默认为1。
- `-Tb INTER_BYTE_TIMEOUT, --inter-byte-timeout INTER_BYTE_TIMEOUT`: 串口字节间超时时间，单位为秒，默认为0.1。
- `-wt WAIT_TIMEOUT, --wait-timeout WAIT_TIMEOUT`: 等待micropython设备响应的超时时间，单位为秒，默认为10。
- `--subcmd-help SUBCMD_HELP`: 显示子命令的帮助信息并退出。`SUBCMD_HELP`语法：
  - 当`SUBCMD_HELP`为`*`时，显示所有子命令的帮助信息，但不显示每个子命令的用法。
  - 当`SUBCMD_HELP`为`:<subcmd>`时，显示子命令`<subcmd>`的帮助信息，且显示它的用法。
- `-pbmaxw PROGRESSBAR_MAXWIDTH, --progressbar-maxwidth PROGRESSBAR_MAXWIDTH`: 进度条的最大宽度，单位为字符，必须大于0，默认为50。
- `-pbminw PROGRESSBAR_MINWIDTH, --progressbar-minwidth PROGRESSBAR_MINWIDTH`: 进度条的最小宽度，单位为字符，必须大于0，默认为5。
- `-v, --verbose`: 输出调试信息。
- `-nc, --no-colorful`: 使输出单色。如果终端无法解析ANSI颜色转义序列，建议选择此选项。
- `--version`: 显示程序版本号并退出。
