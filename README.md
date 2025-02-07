# `MpyFileOpt`--Efficient MicroPython Device File System Management Tool

🌐 [简体中文](./README_zh.md)

This tool is designed for managing the file system of MicroPython devices, supporting operations such as uploading, downloading, deleting, viewing, renaming, and creating folders for the file system.

Features:

- Compared to [ampy](https://github.com/scientifichackers/ampy), it supports more file system operations.
- The average file upload speed is as high as `8.70KB/s`, and the average download speed is as high as `11.00KB/s`, which is much higher than [ampy](https://github.com/scientifichackers/ampy) and most similar tools.  
Note: `1K = 1024`, the device used for testing: [HandPy](https://labplus.cn/handPy)
- Supports recursive upload, download, and deletion of non-empty folders.
- A complete device exception handling mechanism ensures stability.

It is suitable for scenarios where efficient operations on the MicroPython device file system are required, and its speed advantage is particularly evident when transferring large files.

## Installation and use

### Install

If you prefer to install directly, you can use pip (depending on the situation):

```shell
pip install mpyfileopt
```

Or, manually package and install (depending on the situation):

```shell
git clone https://github.com/emofalling/MpyFileOpt-Python.git
cd ./MpyFileOpt-Python

python -m build --wheel
# If `build` is not installed, please install `build` first (depending on the situation):
# python -m pip install build

# Then find the file with the .whl extension in ./dist, and install it using pip (depending on the situation):
python -m pip install ./dist/your_whl_file.whl
```

Otherwise, you can first clone this project and then navigate directly to the directory [./mpyfopt](./mpyfopt):

```shell
git clone https://github.com/emofalling/MpyFileOpt-Python.git
cd ./MpyFileOpt-Python/mpyfopt
# If you use this way, in subsequent commands related to mpyfopt, replace mpyfopt with ./mpyfopt or .\mpyfopt (as appropriate).
```

### Using as a Command Line Tool

Verify that you can run the mpyfopt program and get the help output:

```shell
mpyfopt --help
```

Using example:

```shell
~/myproject/micropython/mpyzip $ mpyfopt -p /dev/ttyUSB3 ls
boot.py    lib    main.py    mpyzip.mpy
~/myproject/micropython/mpyzip $ mpyfopt -p /dev/ttyUSB3 shell
/ > push / ./tests/test_unzip.zip
Write file: /test_unzip.zip
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.64/60.64 KB 8.89 KB/s eta 0:00:00
Wrote in 8.32 seconds, average speed: 8.41 KB/s
Total report: Wrote 0 directories, 1 files
/ > ls
boot.py    lib    main.py    mpyzip.mpy    test_unzip.zip
/ > exit
~/myproject/micropython/mpyzip $
```

For detailed command-line usage of `mpyfopt`, please refer to [Usage of mpyfopt Commands](./docs/cli_usage.md).

### Using as a Python Library

Execute this code in Python to import (depending on the situation):

```python
import mpyfopt
```

For detailed usage of importing `mpyfopt`, please refer to [Import and Usage of mpyfopt](./docs/import_usage.md).

## Appendix

### The choice of Block Size

It depends on the device.

When reading, the larger the block size, the faster the read speed, but it will gradually approach a critical point $^1$.  
When writing, the block size is fastest at a certain critical point $^2$, but the speed decreases when it is above or below this critical point.

Whether reading or writing, if the block size is too large, the device will throw a `MemoryError` (but don't worry, the robust exception handling mechanism of `mpyfopt` makes it difficult for errors to cause crashes), making it impossible to read.

$^1$: Baudrate ÷ 8, in units of `B/s`. When the baudrate is `115200`, this critical point is `14.4KB/s` (`1K=1024`).  
$^2$: It depends on the device. Actual tests show that a block size of `4096` bytes can ensure that most devices are close to this critical point.
