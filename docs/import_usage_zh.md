# `mpyfopt`导入用法

🌐 [English]("./import_usage.md")

## 创建对象

```python
opt = mpyfopt.MpyFileOpt(port: str, 
                         baudrate: int = 115200, 
                         parity: str = serial.PARITY_NONE, 
                         stopbits: float = 1, 
                         timeout: int | None = 1, 
                         write_timeout: int | None = 1,
                         inter_byte_timeout: int | None = 0.1,
                         wait_timeout: int = 10,
                         immediate_connect: bool = True,
                         *,
                         verbose: bool = True
                        ) -> None:
```

创建一个`MpyFileOpt`对象，并连接串口。

参数：

- `port`: 串口名
- `baudrate`: 波特率，对于几乎所有micropython设备应为115200
- `parity`: 奇偶校验，对于几乎所有micropython设备应为无校验(`serial.PARITY_NONE`)
- `stopbits`: 停止位，对于几乎所有micropython设备应为1
- `timeout`: 超时时间，单位秒。禁用超时时，该参数应为`None`
- `write_timeout`: 写入超时时间，单位秒。禁用超时时，该参数应为`None`
- `inter_byte_timeout`: 字节间隔超时时间，单位秒。禁用超时时，该参数应为`None`
- `wait_timeout`: 等待micropython设备响应的超时时间，单位秒。禁用超时时，该参数应为`None`
- `immediate_connect`: 是否立即连接。若为`True`，则在创建对象时立即连接，否则在创建对象后需要手动调用`connect`方法时连接  
注：在创建对象时，无论`immediate_connect`是否为`True`，都会连接串口，但是是否连接micropython设备取决于`immediate_connect`是否为`True`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

## 方法

### 工具

```python
opt.connect(*, verbose: bool = True) -> None
```

连接micropython设备。如果已连接，则该函数相当于重新连接。

参数：

- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.get_source_version(*, verbose: bool = False) -> tuple[int, int]
```

获取该工具的指令码程序版本号。

参数：

- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 指令码程序版本号，元组中元素`(a,b)`对应版本号`a.b`

### 设备信息

```python
opt.uname(isstr: bool = True, *, verbose: bool = False) -> uname_result
#uname_result(sysname:str|bytes, nodename:str|bytes, release:str|bytes, version:str|bytes, machine:str|bytes)
```

获取micropython设备的系统信息（[`os.uname`](https://docs.micropython.org/en/latest/library/os.html#os.uname)）。

参数：

- `isstr`: 返回的元组中内容是否为字符串。若为`True`，则返回的元组中内容为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 设备系统信息，类似于`os.uname`的返回值。其中每个元素均对应[`os.uname`](https://docs.micropython.org/en/latest/library/os.html#os.uname)的返回值。

```python
opt.get_uid(*, verbose: bool = False) -> bytes
```

获取micropython设备的UID（[`machine.unique_id`](https://docs.micropython.org/en/latest/library/machine.html#machine.unique_id)）。

参数：

- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- UID。在不同的设备上，其长度可能不同

```python
opt.get_freq(*, verbose: bool = False) -> int
```

获取micropython设备的CPU频率（[`machine.freq`](https://docs.micropython.org/en/latest/library/machine.html#machine.freq)）。

参数：

- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- CPU频率，单位Hz

### 目录

```python
opt.getcwd(isstr: bool = True, *, verbose: bool = False) -> str | bytes
```

获取micropython设备的当前工作目录（[`os.getcwd`](https://docs.micropython.org/en/latest/library/os.html#os.getcwd)）。

参数：

- `isstr`: 返回的值是否为字符串。若为`True`，则返回的值为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 当前工作目录

```python
opt.chdir(path: str | bytes | bytearray, *, verbose: bool = False) -> None
```

更改micropython设备的当前工作目录（[`os.chdir`](https://docs.micropython.org/en/latest/library/os.html#os.chdir)）。

参数：

- `path`: 新的工作目录
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.listdir(path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[str | bytes]
```

获取micropython设备指定目录下的文件和文件夹列表（[`os.listdir`](https://docs.micropython.org/en/latest/library/os.html#os.listdir)）。

参数：

- `path`: 指定的目录
- `isstr`: 返回的列表中内容是否为字符串。若为`True`，则返回的值为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 指定目录下文件和文件夹的名称列表

```python
opt.ilistdir(path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[ilistdir_item]
# list[ilistdir_item(name:str|bytes, type:int, inode:int)]
```

获取micropython设备指定目录下的文件和文件夹列表（类似于[`os.ilistdir`](https://docs.micropython.org/en/latest/library/os.html#os.ilistdir)）。

参数：

- `path`: 指定的目录
- `isstr`: 返回的列表中的每个`ilistdir_item`对象的`name`属性内容是否为字符串。若为`True`，则返回的值为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 指定目录下文件和文件夹的名称列表，每个元素为`ilistdir_item`对象，其中所有属性均对应[`os.ilistdir`](https://docs.micropython.org/en/latest/library/os.html#os.ilistdir)的返回值。为了提高兼容性，`ilistdir_item`不包含`size`属性。

### 文件

```python
opt.upload(mpy_dst_file: str | bytes | bytearray, src_fp: SupportsReadBinaryIO, src_size: int, write_callback_function: Callable[[int, int], None] = None, block_size: int = 4096, *, verbose: bool = False) -> None
# SupportsReadBinaryIO: 包含read、readinto和readable方法的可读二进制IO对象
```

将文件从本机上传到micropython设备（[`open(mpy_dst_file,"wb")`](https://docs.micropython.org/en/latest/library/builtins.html#open)，但是是从本机上传待写入数据）。

参数：

- `mpy_dst_file`: micropython设备上的目标文件路径。如果路径不存在，则会自动创建文件
- `src_fp`: 可读二进制IO对象。将从此对象读取`src_size`字节的数据
- `src_size`: 待上传的数据大小。单位字节。
- `write_callback_function`: 回调函数。当一个块上传完毕时，会调用该函数，函数定义通常为`write_callback_function(total, cur)`，其中`total`为数据总大小（=`src_size`），`cur`为当前已上传的数据大小，单位字节
- `block_size`: 块大小。单位字节。较大的块可以提高上传速度，但设备上报`MemoryError`的可能性也就越高。建议值取决于堆内存大小。默认值为4096。
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.download(mpy_src_file: str | bytes | bytearray, dst_fp: SupportsWriteBinaryIO, read_callback_function: Callable[[int, int], None] = None, block_size: int = 4096, *, verbose: bool = False) -> None
# SupportsWriteBinaryIO: 包含write、writable方法的可写二进制IO对象
```

将文件从micropython设备下载到本机（[`open(mpy_src_file,"rb")`](https://docs.micropython.org/en/latest/library/builtins.html#open)，但是是从micropython设备读取数据）。

参数：

- `mpy_src_file`: micropython设备上的源文件路径。应为有效文件路径
- `dst_fp`: 可写二进制IO对象。将向此对象写入文件内容
- `read_callback_function`: 回调函数。当读取了1个块时，会调用该函数，函数定义通常为`read_callback_function(total, cur)`，其中`total`为文件总大小，`cur`为当前已读取的数据大小，单位字节
- `block_size`: 块大小。单位字节。较大的块可以提高下载速度，但设备上报`MemoryError`的可能性也就越高。建议值取决于堆内存大小。默认值为4096。
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

### 路径

```python
opt.remove(file: str | bytes | bytearray, *, verbose: bool = False) -> None
```

删除micropython设备上的文件（[`os.remove`](https://docs.micropython.org/en/latest/library/os.html#os.remove)）。

参数：

- `file`: micropython设备上的文件路径。应为有效文件路径
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.rmdir(dir: str | bytes | bytearray, *, verbose: bool = False) -> None
```

删除micropython设备上的文件夹（[`os.rmdir`](https://docs.micropython.org/en/latest/library/os.html#os.rmdir)）。

参数：

- `dir`: micropython设备上的文件夹路径。应为有效文件夹路径
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.mkdir(dir: str | bytes | bytearray, *, verbose: bool = False) -> None
```

创建micropython设备上的文件夹（[`os.mkdir`](https://docs.micropython.org/en/latest/library/os.html#os.mkdir)）。

参数：

- `dir`: micropython设备上的文件夹路径。应为有效文件夹路径
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.rename(src: str | bytes | bytearray, dst: str | bytes | bytearray, *, verbose: bool = False) -> None
```

重命名（移动）micropython设备上的路径（[`os.rename`](https://docs.micropython.org/en/latest/library/os.html#os.rename)）。

参数：

- `src`: micropython设备上的源文件或文件夹路径。应为有效路径。
- `dst`: micropython设备上的目标文件或文件夹路径。应为不存在路径。
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

### 路径信息

```python
opt.stat(path: str | bytes | bytearray, *, verbose: bool = False) -> stat_result
# stat_result(st_mode:int, st_ino:int, st_dev:int, st_nlink:int, st_uid:int, st_gid:int, st_size:int, st_atime:int, st_mtime:int, st_ctime:int)
```

获取micropython设备上路径的信息（[`os.stat`](https://docs.micropython.org/en/latest/library/os.html#os.stat)）。

参数：

- `path`: micropython设备上的路径。应为有效路径。
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 路径信息。返回值中的每个元素均对应[`os.stat`](https://docs.micropython.org/en/latest/library/os.html#os.stat)的返回值。

```python
opt.statvfs(path: str | bytes | bytearray, *, verbose: bool = False) -> statvfs_result
# statvfs_result(f_bsize:int, f_frsize:int, f_blocks:int, f_bfree:int, f_bavail:int, f_files:int, f_ffree:int, f_favail:int, f_flag:int, f_namemax:int)
```

获取micropython设备上路径的文件系统信息（[`os.statvfs`](https://docs.micropython.org/en/latest/library/os.html#os.statvfs)）。

参数：

- `path`: micropython设备上的路径。应为有效路径。
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 文件系统状态。返回值中的每个元素均对应[`os.statvfs`](https://docs.micropython.org/en/latest/library/os.html#os.statvfs)的返回值。

### 内存

```python
opt.get_gc_info(collect: bool = True, *, verbose: bool = False) -> gc_info
# gc_info(used:int, free:int)
```

获取micropython设备上的堆内存信息（[`gc.mem_alloc`](https://docs.micropython.org/en/latest/library/gc.html#gc.mem_alloc)`,`[`gc.mem_free`](https://docs.micropython.org/en/latest/library/gc.html#gc.mem_free)）。

参数：

- `collect`: 是否在获取信息前进行垃圾回收。默认值为`True`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：

- 堆内存信息。`used`属性为已使用堆内存大小，`free`属性为堆内存大小，单位字节。

### 断开连接

```python
opt.close(*, verbose: bool = False) -> None
```

断开与micropython设备的连接并关闭串口。

参数：

- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

## 对象周期结束

当`opt`对象被销毁时（或手动调用`opt.__del__`时），若`opt`对象与micropython设备仍在连接（未调用`opt.close`），则自动调用`opt.close`断开连接并关闭串口。
