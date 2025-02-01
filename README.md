# `MpyFileOpt`--高效的micropython设备文件系统管理工具
一个用于管理micropython设备文件系统的工具，支持文件上传、下载、删除、查看、重命名、创建文件夹等针对文件和文件夹的操作。

特点：
- 相比[ampy](https://github.com/scientifichackers/ampy)，支持文件夹的操作，和一些文件的特殊操作
- 文件上传平均速度高达`8.70KB/s`，下载平均速度高达`11.00KB/s`，远高于[ampy](https://github.com/scientifichackers/ampy)  
注：`1K = 1024`，测试所用设备：[掌控板(HandPy)](https://labplus.cn/handPy)
- 支持非空文件夹的递归上传、递归下载、递归删除
- 完善的设备异常处理机制，保证稳定性

### 安装

