# `MpyFileOpt`——高效的micropython设备文件系统管理工具

一个用于管理micropython设备文件系统的工具，支持文件上传、下载、删除、查看、重命名、创建文件夹等针对文件和文件夹的操作。

特点：

- 相比[ampy](https://github.com/scientifichackers/ampy)，支持更多的文件系统操作
- 文件上传平均速度高达`8.70KB/s`，下载平均速度高达`11.00KB/s`，远高于[ampy](https://github.com/scientifichackers/ampy)和大部分同类工具  
注：`1K = 1024`，测试所用设备：[掌控板(HandPy)](https://labplus.cn/handPy)
- 支持非空文件夹的递归上传、递归下载、递归删除
- 完善的设备异常处理机制，保证稳定性

它适合于需要高效操作micropython设备文件系统的场景，在传输大文件时，其速度优势尤为明显。

## 安装和使用

### 以命令行方式使用

如果希望直接安装，可以使用pip安装（具体视情况而定）：

```shell
pip install mpyfileopt
```

否则，可以先拷贝此项目后直接定位到目录[./mpyfopt](./mpyfopt)

```shell
git clone https://github.com/emofalling/MpyFileOpt-Python.git
cd ./MpyFileOpt-Python/mpyfopt
# 若使用此方法，在之后关于mpyfopt中的命令的mpyfopt应替换为./mpyfopt或.\mpyfopt(视情况而定)
```

然后，验证您可以运行mpyfopt程序并获得帮助输出：

```shell
mpyfopt --help
```

关于`mpyfopt`的命令行方式详细使用方法，请参阅[MpyFileOpt命令行用法](./docs/cli_usage_zh.md)

### 以导入方式使用

在python中执行此代码以导入（具体视情况而定）：

```python
import mpyfopt
```

关于`mpyfopt`的导入方式详细使用方法，请参阅[MpyFileOpt导入用法](./docs/import_usage_zh.md)
