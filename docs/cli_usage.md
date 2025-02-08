# Usage of `mpyfopt` Commands

🌐 [简体中文](./cli_usage_zh.md)

🔙 [Back](../README.md)

Note: If you are using `mpyfopt` by locating the directory instead of installing it, then `mpyfopt` in all commands below should be replaced with `./mpyfopt.py` or `.\mpyfopt.py` (as appropriate).

## Command rule

```shell
mpyfopt <args> {<subcommand> <subcommand_args>}*n
# In Here, `{<Any>}*n` indicates that `Any` can be repeated any number of times (i.e., this part can be `<Any>`, `<Any> <Any> <Any>...`).
```

When `mpyfopt` is functioning correctly, it first establishes a connection to the micropython device using the parameters specified in `<args>`. Afterward, it executes the `<subcommand>` and its associated arguments `<subcommand_args>` in a sequential manner.

For detailed information on `<args>`, you can refer to the output of the command `mpyfopt --help`.  
For `<subcommand>`, you can refer to the output of the command `mpyfopt --subcmd-help *` as well as the **Subcommands and their parameters** section below.
For `<subcommand_args>`, you can refer to the output of the command `mpyfopt --subcmd-help :<subcommand>` (for example, `mpyfopt --subcmd-help :cd`) and the **Subcommands and their parameters** section below.

For example:

```shell
mpyfopt -p /dev/ttyUSB0 cd /lib ls # mpyfopt -p /dev/ttyUSB0 -> cd /lib -> ls
mpyfopt -p /dev/ttyUSB1 -To 20 write ./main.py ./your_project/main.py # mpyfopt -p /dev/ttyUSB1 -To 20 -> write ./main.py ./your_project/main.py
mpyfopt -p /dev/ttyUSB0 -To 10 cd ./lib/your_module cat README.md # mpyfopt -p /dev/ttyUSB0 -To 10 -> cd ./lib/your_module -> cat README.md
```

Due to the direct command name matching used for subcommand separation, the command parsing may not be as expected in some cases. For example:

```shell
mpyfopt -p /dev/ttyUSB0 push ./receive push # mpyfopt -p /dev/ttyUSB0 -> push ./receive -> push
```

The above command can be modified to the following format to prevent parsing errors:

```shell
mpyfopt -p /dev/ttyUSB0 push ./receive ./push # mpyfopt -p /dev/ttyUSB0 -> push ./receive ./push
```

## Main command parameters

```shell
mpyfopt [-h] [--subcmd-help SUBCMD_HELP] [-V] [-s] 
        [-p PORT] [-B BAUDRATE] [-P PARITY] [-S STOPBITS] 
        [-To TIMEOUT] [-Tw WRITE_TIMEOUT] [-Tb INTER_BYTE_TIMEOUT] [-wt WAIT_TIMEOUT]
        [-pbmaxw PROGRESSBAR_MAXWIDTH] [-pbminw PROGRESSBAR_MINWIDTH] [-nc] [-v]
```

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `--subcmd-help SUBCMD_HELP`: Displays the help information for the subcommands and exits. The syntax for `SUBCMD_HELP` is:
  - When `SUBCMD_HELP` is `*`, it displays the help information for all subcommands but does not show the usage of each subcommand.
  - When `SUBCMD_HELP` is `:<subcmd>`, it displays the help information for the subcommand `<subcmd>` and shows its usage.
- `-V`,`--version`: Displays the program version number and exits.
- `-s`,`--scan`: scan and show all serial ports then exit.
- `-p PORT`,`--port PORT`: The name of the serial port.
- `-B BAUDRATE`,`--baudrate BAUDRATE`: The baud rate of the serial port, with a default of 115200.
- `-P PARITY`,`--parity PARITY`: The parity bit of the serial port, with a default of N (no parity check, specifics refer to actual output).
- `-S STOPBITS`,`--stopbits STOPBITS`: The stop bit of the serial port, with a default of 1 (specifics refer to actual output).
- `-To TIMEOUT`,`--timeout TIMEOUT`: The timeout period for the serial port, measured in seconds, with a default of 1.
- `-Tw WRITE_TIMEOUT`,`--write-timeout WRITE_TIMEOUT`: The write timeout period for the serial port, measured in seconds, with a default of 1.
- `-Tb INTER_BYTE_TIMEOUT`,`--inter-byte-timeout INTER_BYTE_TIMEOUT`: The inter-byte timeout period for the serial port, measured in seconds, with a default of 0.1.
- `-wt WAIT_TIMEOUT`,`--wait-timeout WAIT_TIMEOUT`: The timeout period for waiting for a response from the micropython device, measured in seconds, with a default of 10.
- `-pbmaxw PROGRESSBAR_MAXWIDTH`,`--progressbar-maxwidth PROGRESSBAR_MAXWIDTH`: The maximum width of the progress bar, measured in characters, must be greater than 0, with a default of 50.
- `-pbminw PROGRESSBAR_MINWIDTH`,`--progressbar-minwidth PROGRESSBAR_MINWIDTH`: The minimum width of the progress bar, measured in characters, must be greater than 0, with a default of 5.
- `-nc`,`--no-colorful`: Makes the output monochrome. It is recommended to choose this option if the terminal cannot parse ANSI color escape sequences.
- `-v`,`--verbose`: Outputs debug information.

## Subcommands and their parameters

Note: Subcommands marked with `*` are similar to [GNU](https://www.gnu.org/) subcommands. Their command format and output format are similar to the corresponding commands in the **GNU toolkit**, but they are not exactly the same.

### `shell`

```shell
shell [-h]
```

The `shell` subcommand provides an interactive command line interface for conveniently manually entering subcommands.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.

The `shell` command is similar to:

```shell
/ >
```

`/` represents the current working directory of the device.

Example of entering subcommands through `shell`:

```shell
~ $ mpyfopt -p /dev/ttyUSB0 shell
/ > cd /lib
/lib > ls
uasyncio repl.py
/lib > exit
~ $
```

In `shell`, the `exit` command is used to exit `shell`, but the subcommands after `shell` will still continue to execute. The `exit` command has no arguments or options.

### `help`

```shell
help [-h] [-u] [cmds ...]
```

Output help information for the subcommands.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-u`,`--usage`: Displays the usage of the subcommands.
- `cmds`: The subcommands for which to display the help information. If not specified, it displays the help information for all subcommands.

### `ver`

```shell
ver [-h] [-c] [-v]
```

Output the tool version number and the instruction code program version number.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-c`,`--csv`: Outputs in CSV format.
- `-v`,`--verbose`: Outputs debug information.

If `-c` or `--csv` is not specified, the output is similar to:

```text
mpyfopt version: x.x
   code version: x.x
```

If `-c` or `--csv` is specified, the output is similar to:

```text
x.x,y.y
```

`x.x` corresponds to `mpyfopt version`, and `y.y` corresponds to `code version`.

### `uname`*

```shell
uname [-h] [-a] [-s] [-n] [-r] [-v] [-m] [-c] [--verbose]
```

Output device information.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-a`,`--all`: Displays all information.
- `-s`,`--kernel-name`: Displays the kernel name. This is the default option.
- `-n`,`--nodename`: Displays the hostname of the network node.
- `-r`,`--kernel-release`: Displays the kernel release version.
- `-v`,`--kernel-version`: Displays the kernel version.
- `-m`,`--machine`: Displays the machine hardware name.
- `-c`,`--csv`: Outputs in CSV format.
- `--verbose`: Outputs debug information.

### `uid`

```shell
uid [-h] [-v]
```

Output the UID of the device. The length of the UID may vary across different devices.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-v`,`--verbose`: Outputs debug information.

### `freq`

```shell
freq [-h] [-r] [-v]
```

Output the CPU frequency of the device.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-r`,`--raw`: Outputs in raw data format.
- `-v`,`--verbose`: Outputs debug information.

If `-r` or `--raw` is not specified, it outputs in a human-readable format (1M=1000k, 1k=1000), similar to:

```text
240.0 MHz
```

If `-r` or `--raw` is specified, it outputs in raw data format, similar to:

```text
240000000
```

### `pwd`*

```shell
pwd [-h] [-l] [-v]
```

Output the current working directory.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-l`,`--local`: If specified, it outputs the local host's working directory. Otherwise, it outputs the device's working directory.
- `-v`,`--verbose`: Outputs debug information.

### `cd`*

```shell
cd [dir] [-h] [-l] [-v]
```

Change the current working directory.

Args & Options:

- `dir`: The directory to change to.
- `-h`,`--help`: Displays the help information and exits.
- `-l`,`--local`: If specified, it changes the local host's working directory. Otherwise, it changes the device's working directory.
- `-v`,`--verbose`: Outputs debug information.

### `ls`*

```shell
ls [dir] [-h] [-a] [-R] [-l] [-S | -N] [-r] [--row | -c] [--sep SEP] [-sC] [-Q] [-s] [-si | -bi] [-dp DECIMAL_PLACES] [-J] [-v]
```

List the items in the specified directory on the device.

Args & Options:

- `dir`: The directory to list. If not specified, it lists the current working directory.
- `-h`,`--help`: Displays the help information and exits.
- `-a`,`--all`: Displays all items, including hidden items.
- `-R`,`--recursive`: Recursively lists directories.
- `-l`,`--long`: Displays detailed information about items.
- `-S`,`--sort-size`: Sorts by size.
- `-N`,`--sort-name`: Sorts by name.
- `-r`,`--reverse`: Reverses the sort order.
- `--row`: Displays items in a single row.
- `-c`,`--column`: Displays one item per line.
- `--sep SEP`: The minimum number of spaces between items. Must be greater than or equal to 0. The default is 3.
- `-sC`,`--sep-comma`: Separates items with commas.
- `-Q`,`--quote`: Adds quotes around items.
- `-s`,`--slash`: Adds a `/` after directories.
- `-si`,`--si`: Uses SI units. 1k=1000.
- `-bi`,`--bi`: Uses BI units. 1K=1024.
- `-dp DECIMAL_PLACES`,`--decimal-places DECIMAL_PLACES`: The number of decimal places. Must be greater than or equal to -1. If it is -1, there is no limit to the number of decimal places. The default is 3.
- `-J`,`--json`: Outputs in JSON format.
- `-v`,`--verbose`: Outputs debug information.

When neither `--row` nor `-c` (`--column`) is specified, the output is similar to:

```text
Obloq.py             Servo.py             blynklib.py          blynktimer.py        dog
face                 hcsr04.py            helloFly.py          ir_remote.py         lib
main.py              microbit.py          mpython_ble          mpython_online.py    mpythonbox.py
nplus                siot.py              smartcamera.py       smartcamera_new.py   tinywebio.py
user.xml             uwebsockets          xgo.py               xunfei.py            yeelight.py
```

When `--row` is specified, the output is similar to:

```text
Obloq.py   Servo.py   blynklib.py   blynktimer.py   dog   face   hcsr04.py   helloFly.py   ir_remote.py   lib   main.py   microbit.py   mpython_ble   mpython_online.py   mpythonbox.py   nplus   siot.py   smartcamera.py   smartcamera_new.py   tinywebio.py   user.xml   uwebsockets   xgo.py   xunfei.py   yeelight.py
```

When `-c` (`--column`) is specified, the output is similar to:

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

Lists the items in the specified directory on the device in a tree structure.

Args & Options:

- `dir`: The directory to list. If not specified, it lists the current working directory.
- `-h`,`--help`: Displays the help information and exits.
- `-sl`,`--slash`: Adds a `/` after directories.
- `-hl HLINE_LEN`,`--hline-len HLINE_LEN`: The length of the horizontal line for each item. Must be greater than or equal to 0. The default is 2.
- `--noreport`: Disables the file/directory count at the end of the tree structure list.
- `-Q`,`--quote`: Adds quotes around items.
- `-L LEVEL`,`--level LEVEL`: The maximum traversal depth of the directory tree. Must be greater than 0. By default, there is no limit.
- `-J`,`--json`: Outputs in JSON format.
- `-X`,`--xml`: Outputs in XML format.
- `-v`,`--verbose`: Outputs debug information.

When `--noreport` is not specified, the output is similar to:

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

Write a local file to a device file.

Args & Options:

- `dst`: The device file to write to.
- `src`: The local file to transfer.
- `-h`,`--help`: Displays the help information and exits.
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: The block size. A larger block size can bring faster transfer speed but requires more memory on the device. The default is 4096.
- `-q`,`--quiet`: Does not display the progress bar and does not output a report.
- `--noreport`: Does not output a report.
- `-w`,`--warning`: If `dst` already exists, the user can choose whether to overwrite it. If not specified, it always overwrites it.
- `-v`,`--verbose`: Outputs debug information.

When this command is executed successfully, it will transfer the contents of the local file `src` to the target device file `dst`.

### `push`

```shell
push [-h] [-b BLOCKSIZE] [-nr] [-q] [--noreport] [-w] [-v] dst src [src ...]
```

Push one or more local files or directories to the device.

Args & Options:

- `dst`: The target device path to receive the items.
- `src`: The items to be pushed to the local host. They can be files or directories. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: The block size. A larger block size can bring faster transfer speed but requires more memory on the device. The default is 4096.
- `-nr`,`--no-recursive`: When pushing directories, it does not recursively push child items.
- `-q`,`--quiet`: Does not display the progress bar and does not output a report.
- `--noreport`: Does not output a report.
- `-w`,`--warning`: If there is a file with the same path on the device during the push, the user can choose whether to overwrite it. If not specified, it always overwrites it.
- `-v`,`--verbose`: Outputs debug information.

When this command is executed successfully, it will push all items from one or more local `src` to the target device path `dst`.

### `read`

```shell
read [-h] [-b BLOCKSIZE] [-q] [--noreport] [-w] [-v] dst src
```

Read a file from the device and writes it to a local file.

Args & Options:

- `dst`: The local file to write to.
- `src`: The device file to read from.
- `-h`,`--help`: Displays the help information and exits.
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: The block size. A larger block size can bring faster transfer speed but requires more memory on the device. The default is 4096.
- `-q`,`--quiet`: Does not display the progress bar and does not output a report.
- `--noreport`: Does not output a report.
- `-w`,`--warning`: If `src` already exists, the user can choose whether to overwrite it. If not specified, it always overwrites it.
- `-v`,`--verbose`: Outputs debug information.

When this command is executed successfully, it will read the contents of the device file `src` and write it to the local file `dst`.

### `cat`*

```shell
cat [-h] [-b BLOCKSIZE] [-n] [-s] [-q] [-w] [-v] src [src ...]
```

Print the contents of one or more device files.

Args & Options:

- `src`: The device file(s) to print. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: The block size. A larger block size can bring faster transfer speed but requires more memory on the device. The default is 4096.
- `-n`,`--number`: Numbers the output lines.
- `-s`,`--squeeze-blank`: Suppresses repeated empty output lines. If `-n` is also specified, the line numbers will be collapsed.
- `-q`,`--quiet`: Does not display the progress bar and does not output a report.
- `-w`,`--warning`: If `src` already exists, the user can choose whether to overwrite it. If not specified, it always overwrites it.
- `-v`,`--verbose`: Outputs debug information.

When this command is executed successfully, it will print the contents of one or more device files `src` in order to the console. When multiple `src` are specified, if the end of the content of one file is not a newline character, a newline character will be added before printing the content of the next file.

### `pull`

```shell
pull [-h] [-b BLOCKSIZE] [-nr] [-q] [--noreport] [-w] [-v] dst src [src ...]
```

Pull one or more items from the device.

Args & Options:

- `dst`: The local path to pull to.
- `src`: The device file(s) or directory(ies) to pull. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-b BLOCKSIZE`,`--blocksize BLOCKSIZE`: The block size. A larger block size can bring faster transfer speed but requires more memory on the device. The default is 4096.
- `-nr`,`--no-recursive`: When pulling directories, it does not recursively pull child items.
- `-q`,`--quiet`: Does not display the progress bar and does not output a report.
- `--noreport`: Does not output a report.
- `-w`,`--warning`: If there is a file with the same path on the local host during the pull, the user can choose whether to overwrite it. If not specified, it always overwrites it.
- `-v`,`--verbose`: Outputs debug information.

When this command is executed successfully, it will pull all items from one or more device `src` to the local path `dst`.

### `rm`*

```shell
rm [-h] [-d] [-R] [-p] [-v] paths [paths ...]
```

Delete one or more items on the device.

Args & Options:

- `paths`: The device items to delete. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-d`,`--dir`: Supports deleting directories. If this option is not specified, only non-directory items can be deleted.
- `-R`,`-r`,`--recursive`: Deletes items. If it is a directory, it recursively deletes its contents.
- `-p`,`--print`: Outputs all deleted items. When recursively deleting folders, this option makes it convenient to view the deleted file sub-items.
- `-v`,`--verbose`: Outputs debug information.

### `rmdir`*

```shell
rmdir [-h] [-v] dirs [dirs ...]
```

Delete one or more empty directories on the device.

Args & Options:

- `dirs`: The device directories to delete. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-v`,`--verbose`: Outputs debug information.

### `mkdir`*

```shell
mkdir [-h] [-v] dirs [dirs ...]
```

Create one or more directories on the device.

Args & Options:

- `dirs`: The device directories to create. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-v`,`--verbose`: Outputs debug information.

### `mv`*

```shell
mv [-h] [-v] src dst
```

Move or renames one or more items on the device.

Args & Options:

- `src`: The device item to move or rename.
- `dst`: The target device item.
- `-h`,`--help`: Displays the help information and exits.
- `-v`,`--verbose`: Outputs debug information.

### `gc`

```shell
gc [-h] [-r] [-cl] [-c] [-v]
```

Retrieve the memory usage of the device.

Args & Options:

- `-h`,`--help`: Displays the help information and exits.
- `-r`,`--raw`: Outputs the raw GC information. It has no suffix and the unit is bytes. If not specified, it outputs a readable format based on 1024.
- `-cl`,`--collect`: Calls `gc.collect()` before retrieving the information.
- `-c`,`--csv`: Outputs in CSV format.
- `-v`,`--verbose`: Outputs debug information.

When `-c` or `--csv` is not specified, the output is similar to:

```text
Total: 108.56 K
 Free: 88.94 K
 Used: 19.62 K
```

When `-c` or `--csv` is specified, the output is similar to:

```text
t,f,u
```

`t` is `Total`, `f` is `Free`, `u` is `Used`.

### `stat`*

```shell
stat [-h] [-f] [-v] paths [paths ...]
```

Retrieve the path information or file system information for the specified path on the device.

Args & Options:

- `paths`: The device paths for which to retrieve information. There should be at least one item.
- `-h`,`--help`: Displays the help information and exits.
- `-f`,`--file-system`: Retrieves file system information. If not specified, it retrieves path information.
- `-v`,`--verbose`: Outputs debug information.

When `-f` or `--file-system` is not specified, the output is similar to:

```text
  File: file
  Size: size   type
Device: dev  Inode: ino     Links: links
Access: access  Uid: uid  Gid: gid
Access: atime
Modify: mtime
Change: ctime
```

- `file`: The path.
- `size`: The size. If it is a directory, it does not reflect the actual situation.
- `type`: The path type, which can be `file`, `dir`, `link`, etc.
- `dev`: The device ID. If not supported, it is `/`.
- `ino`: The inode number. If not supported, it is `/`.
- `links`: The number of hard links. If not supported, it is `/`.
- `access`: The access permissions, in the format `(o/taaaaaaaaas)`, where `o` is the permission in octal form (if not supported, it is `-`), `t` is the type abbreviation, `a` is the access permissions (if not supported, it is `?`), and `s` is always empty.
- `uid`: The user ID. If not supported, it is `/`.
- `gid`: The group ID. If not supported, it is `/`.
- `atime`: The last access time. If not supported, it is `/`.
- `mtime`: The last modification time. If not supported, it is `/`.
- `ctime`: The last status change time. If not supported, it is `/`.

When `-f` or `--file-system` is specified, the output is similar to:

```text
  File: file
    ID: id   Namelen: nlen        Flag: flag
Block size: bsize       Fundamental block size: fbsize
Blocks: blen        Free: bfree       Available: bavail
 Files: files       Free: ffree       Available: favail
```

- `file`: The path.
- `id`: The file system ID. If not supported, it is `/`.
- `nlen`: The maximum length of the file name. If not supported, it is `/`.
- `flag`: The file system flag. If not supported, it is `/`.
- `bsize`: The block size.
- `fbsize`: The fundamental block size.
- `blen`: The total number of blocks.
- `bfree`: The number of free blocks.
- `bavail`: The number of free blocks available to non-superusers. If not supported, it is `/`.
- `files`: The total number of files. If not supported, it is `/`.
- `ffree`: The number of free files. If not supported, it is `/`.
- `favail`: The number of free files available to non-superusers. If not supported, it is `/`.
