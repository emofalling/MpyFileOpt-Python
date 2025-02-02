🌐 [English]("./import_usage.md")
# `mpyfopt`导入用法
## 连接
```python
opt = mpyfopt.MpyFileOpt(self, 
                         port: str, 
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
参数：
- `port`: 串口名
- `baudrate`: 波特率，对于几乎所有micropython设备应为115200
- `parity`: 奇偶校验，对于几乎所有micropython设备应为无校验(`serial.PARITY_NONE`)
- `stopbits`: 停止位，对于几乎所有micropython设备应为1
- `timeout`: 超时时间，单位秒。若需要禁用超时，应为`None`
- `write_timeout`: 写入超时时间，单位秒。若需要禁用超时，应为`None`
- `inter_byte_timeout`: 字节间隔超时时间，单位秒。若需要禁用超时，应为`None`
- `wait_timeout`: 等待micropython设备的超时时间，单位秒。若需要禁用超时，应为`None`
- `immediate_connect`: 是否立即连接。若为`True`，则在创建对象时立即连接，否则在创建对象后需要手动调用`connect`方法时连接  
注：在创建对象时，无论`immediate_connect`是否为`True`，都会连接串口，但是是否连接micropython设备取决于`immediate_connect`是否为`True`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

## 方法
```python
opt.connect(*, verbose: bool = True) -> None
```
连接micropython设备。  
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

```python
opt.uname(isstr: bool = True, *, verbose: bool = False) -> uname_result
#uname_result(sysname:str|bytes, nodename:str|bytes, release:str|bytes, version:str|bytes, machine:str|bytes)
```
获取micropython设备的系统信息。返回值类似于`os.uname`的返回值。  
参数：
- `isstr`: 返回的元组中内容是否为字符串。若为`True`，则返回的元组中内容为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：
- 设备系统信息，类似于`os.uname`的返回值。其中每个元素均对应[`os.uname`](https://docs.micropython.org/en/latest/library/os.html#os.uname)的返回值。

```python
opt.get_uid(*, verbose: bool = False) -> bytes
```
获取micropython设备的UID（`machine.unique_id()`的返回值）。  
参数：
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：
- UID。在不同的设备上，其长度可能不同

```python
opt.get_freq(*, verbose: bool = False) -> int
```
获取micropython设备的CPU频率（`machine.freq()`的返回值）。  
参数：
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：
- CPU频率，单位Hz

```python
opt.getcwd(isstr: bool = True, *, verbose: bool = False) -> str | bytes
```
获取micropython设备的当前工作目录（`os.getcwd()`的返回值）。  
参数：
- `isstr`: 返回的值是否为字符串。若为`True`，则返回的值为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：
- 当前工作目录

```python
opt.chdir(path: str | bytes | bytearray, *, verbose: bool = False) -> None
```
更改micropython设备的当前工作目录（`os.chdir()`的返回值）。  
参数：
- `path`: 新的工作目录
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

```python
opt.listdir(path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[str | bytes]
```
获取micropython设备指定目录下的文件和文件夹列表（`os.listdir()`的返回值）。  
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
获取micropython设备指定目录下的文件和文件夹列表（类似于`os.ilistdir()`的返回值）。  
参数：
- `path`: 指定的目录
- `isstr`: 返回的列表中的每个`ilistdir_item`对象的`name`属性内容是否为字符串。若为`True`，则返回的值为字符串，否则为`bytes`
- `verbose`: 是否打印调试信息。若出现异常情况，可以设为`True`以查看调试信息

返回值：
- 指定目录下文件和文件夹的名称列表，每个元素为`ilistdir_item`对象，其中所有属性均对应[`os.ilistdir()`](https://docs.micropython.org/en/latest/library/os.html#os.ilistdir)的返回值。为了提高兼容性，`ilistdir_item`不包含`size`属性。