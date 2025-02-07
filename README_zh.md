# `MpyFileOpt`——高效的micropython设备文件系统管理工具

🌐 [English](./README.md)

该工具是一个用于管理micropython设备文件系统的工具，支持文件上传、下载、删除、查看、重命名、创建文件夹等针对文件系统的操作。

特点：

- 相比[ampy](https://github.com/scientifichackers/ampy)，支持更多的文件系统操作
- 文件上传平均速度高达`8.70KB/s`，下载平均速度高达`11.00KB/s`，远高于[ampy](https://github.com/scientifichackers/ampy)和大部分同类工具  
注：`1K = 1024`，测试所用设备：[掌控板(HandPy)](https://labplus.cn/handPy)
- 支持非空文件夹的递归上传、递归下载、递归删除
- 完善的设备异常处理机制，保证稳定性

它适合于需要高效操作micropython设备文件系统的场景，在传输大文件时，其速度优势尤为明显。

## 安装和使用

### 安装

如果希望直接安装，可以使用pip安装（具体视情况而定）：

```shell
pip install mpyfileopt
```

或者，手动打包安装（具体视情况而定）：

```shell
git clone https://github.com/emofalling/MpyFileOpt-Python.git
cd ./MpyFileOpt-Python

python -m build --wheel
# 若未安装`build`，需先安装`build`（具体视情况而定）：
# python -m pip install build

# 然后找到./dist下后缀为.whl的文件，使用pip进行安装（具体视情况而定）：
python -m pip install ./dist/your_whl_file.whl
```

否则，可以先拷贝此项目后直接定位到目录[./mpyfopt](./mpyfopt)

```shell
git clone https://github.com/emofalling/MpyFileOpt-Python.git
cd ./MpyFileOpt-Python/mpyfopt
# 若使用此方法，在之后关于mpyfopt中的命令的mpyfopt应替换为./mpyfopt或.\mpyfopt(视情况而定)
```

### 以命令行方式使用

验证您可以运行mpyfopt程序并获得帮助输出：

```shell
mpyfopt --help
```

使用示例：

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

关于`mpyfopt`的命令行方式详细使用方法，请参阅[MpyFileOpt命令行用法](./docs/cli_usage_zh.md)

### 以导入方式使用

在python中执行此代码以导入（具体视情况而定）：

```python
import mpyfopt
```

关于`mpyfopt`的导入方式详细使用方法，请参阅[MpyFileOpt导入用法](./docs/import_usage_zh.md)

## 附录

### 关于块大小的选择

具体取决于设备。

在读取时，块大小越大，读取速度越快，但会逐渐趋向一个临界点 $^1$。  
在写入时，块大小在某一临界点 $^2$时速度最快，但超过或小于该临界点时，速度会降低。

无论是读取还是写入，块大小过大时，设备会抛出`MemoryError`错误（但不必担心，`mpyfopt`完善的异常处理机制使得其难以由于错误导致崩溃），从而无法读取。  

$^1$: 波特率 ÷ 8，单位为`B/s`。当波特率为`115200`时，该临界点为`14.4KB/s`(`1K=1024`)。  
$^2$: 取决于设备。实测得块大小为`4096`字节时能确保对于大部分设备都接近该临界点。
