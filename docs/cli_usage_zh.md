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

由于子命令分隔方式为直接命令名匹配，所以在某些情况下，命令的解析可能不会符合预期。例如：

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

注：标`*`的子命令为类[GNU](https://www.gnu.org/)子命令，其命令格式和输出格式与**GNU工具集**中的对应命令格式和输出格式相似，但并非完全相同。

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

其中，`/`表示当前设备工作目录。

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

### `pwd`*

```shell
pwd [-h] [-l] [-v]
```

输出当前工作目录。

参数&选项：

- `-h`,`--help`: 显示帮助信息并退出。
- `-l`,`--local`: 若指定，则输出本机工作目录，否则输出设备工作目录。
- `-v`,`--verbose`: 输出调试信息。

### `cd`*

```shell
cd [dir] [-h] [-l] [-v]
```

更改当前工作目录。

参数&选项：

- `dir`: 要更改到的目录。
- `-h`,`--help`: 显示帮助信息并退出。
- `-l`,`--local`: 若指定，则更改本机工作目录，否则更改设备工作目录。
- `-v`,`--verbose`: 输出调试信息。

### `ls`*

```shell
ls [dir] [-h] [-a] [-R] [-l] [-S | -N] [-r] [--row | -c] [--sep SEP] [-sC] [-Q] [-s] [-si | -bi] [-dp DECIMAL_PLACES] [-J] [-v]
```

列出设备上指定目录下的项。

参数&选项：

- `dir`: 要列出的目录。不指定则列出当前工作目录。
- `-h`,`--help`: 显示帮助信息并退出。
- `-a`,`--all`: 显示所有项，包括隐藏项。
- `-R`,`--recursive`: 递归列出目录。
- `-l`,`--long`: 显示项的详细信息。
- `-S`,`--sort-size`: 按大小排序。
- `-N`,`--sort-name`: 按名称排序。
- `-r`,`--reverse`: 反转排序顺序。
- `--row`: 将项显示在一行中。
- `-c`,`--column`: 一行只显示一个项。
- `--sep SEP`: 项之间最少的间隔空格数。必须大于等于0。默认为3。
- `-sC`,`--sep-comma`: 使用逗号分隔项。
- `-Q`,`--quote`: 在项周围加上引号。
- `-s`,`--slash`: 在目录后添加`/`。
- `-si`,`--si`: 使用SI单位。1k=1000。
- `-bi`,`--bi`: 使用BI单位。1K=1024。
- `-dp DECIMAL_PLACES`,`--decimal-places DECIMAL_PLACES`: 小数位数。必须大于等于-1。如果为-1，则小数位数无限制。默认为3。
- `-J`,`--json`: 以JSON格式输出。
- `-v`,`--verbose`: 输出调试信息。

在未指定`--row`和`-c`(`--column`)时，输出类似于：
```text
Obloq.py             Servo.py             blynklib.py          blynktimer.py        dog
face                 hcsr04.py            helloFly.py          ir_remote.py         lib
main.py              microbit.py          mpython_ble          mpython_online.py    mpythonbox.py
nplus                siot.py              smartcamera.py       smartcamera_new.py   tinywebio.py
user.xml             uwebsockets          xgo.py               xunfei.py            yeelight.py
```

在指定`--row`时，输出类似于：

```text
Obloq.py   Servo.py   blynklib.py   blynktimer.py   dog   face   hcsr04.py   helloFly.py   ir_remote.py   lib   main.py   microbit.py   mpython_ble   mpython_online.py   mpythonbox.py   nplus   siot.py   smartcamera.py   smartcamera_new.py   tinywebio.py   user.xml   uwebsockets   xgo.py   xunfei.py   yeelight.py
```

在指定`-c`(`--column`)时，输出类似于：

```text
Obloq.py
Servo.py
blynklib.py
blynktimer.py
dog
face
hcsr04.py
helloFly.py
ir_remote.py
lib
main.py
microbit.py
mpython_ble
mpython_online.py
mpythonbox.py
nplus
siot.py
smartcamera.py
smartcamera_new.py
tinywebio.py
user.xml
uwebsockets
xgo.py
xunfei.py
yeelight.py
```

### `tree`*

```shell
tree [dir ...] [-h] [-sl] [-hl HLINE_LEN] [--noreport] [-Q] [-L LEVEL] [-J | -X] [-v]
```

以树状结构列出设备上指定目录下的项。

参数&选项：

- `dir`: 要列出的目录。不指定则列出当前工作目录。
- `-h`,`--help`: 显示帮助信息并退出。
- `-sl`,`--slash`: 在目录后添加`/`。
- `-hl HLINE_LEN`,`--hline-len HLINE_LEN`: 每个项的水平线长度。必须大于等于0。默认为2。
- `--noreport`: 关闭树状结构列表末尾的文件/目录计数。
- `-Q`,`--quote`: 在项周围加上引号。
- `-L LEVEL`,`--level LEVEL`: 目录树的最大遍历深度。必须大于0。默认不限制。
- `-J`,`--json`: 以JSON格式输出。
- `-X`,`--xml`: 以XML格式输出。
- `-v`,`--verbose`: 输出调试信息。

在未指定`--noreport`时，输出类似于：

```text
./lib
├── k210_ai
│   ├── __init__.py
│   ├── ai.py
│   ├── asr.py
│   └── public.py
├── k210
│   ├── Easy_AI.py
│   ├── __init__.py
│   ├── asr.py
│   ├── color.py
│   ├── face_recognization.py
│   ├── image.py
│   ├── kpu.py
│   ├── lcd.py
│   ├── peripheral.py
│   ├── qrcode.py
│   ├── self_learning_classifier.py
│   └── sensor.py
└── repl.py
3 directories, 17 files
```

### `write`

```shell
write [-h] [-b BLOCKSIZE] [-q] [--noreport] [-w] [-v] dst src
```

将本地文件写入设备文件。

参数&选项：

- `dst`: 要写入的设备文件。
- `src`: 要传输的本地文件。
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: 写入块大小。更大的块大小可以带来更快的传输速度，但设备需要更多的内存。默认为4096。
- `-q`,`--quiet`: 不显示进度条，不输出报告。
- `--noreport`: 不输出报告。
- `-w`,`--warning`: 如果目标文件存在，用户可以选择是否覆盖它。如果未指定，则始终覆盖它。

当该命令正常执行时，它将会把本地文件`src`中的内容传输并写入到目标设备的文件`dst`中。

### `push`

```shell
push [-h] [-b BLOCKSIZE] [-nr] [-q] [--noreport] [-w] [-v] dst src [src ...]
```

将本地文件或目录推送到设备上。

参数&选项：

- `dst`: 要接收项的目标设备路径。
- `src`: 要推送到本地主机的项。可以是文件或目录。应至少有一个项。
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: 推送块大小。更大的块大小可以带来更快的传输速度，但设备需要更多的内存。默认为4096。
- `-nr`,`--no-recursive`: 当推送目录时，不递归推送子项。
- `-q`,`--quiet`: 不显示进度条，不输出报告。
- `--noreport`: 不输出报告。
- `-w`,`--warning`: 如果目标文件存在，用户可以选择是否覆盖它。如果未指定，则始终覆盖它。
- `-v`,`--verbose`: 输出调试信息。

当该命令正常执行时，它将会把本地`src`中的所有项目推送到目标设备的路径`dst`中。
