# Import and Usage of `mpyfopt`

🌐 [简体中文](./import_usage_zh.md)

🔙 [Back](../README.md)

## Create Object

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

Create an object of `MpyFileOpt` and connect to the serial port.

Args:

- `port`: Serial port name
- `baudrate`: Baudrate. For almost all micropython devices, it should be 115200
- `parity`: Parity check. For almost all micropython devices, it should no parity check(`serial.PARITY_NONE`)
- `stopbits`: Stop position. For almost all micropython devices, it should be 1
- `timeout`: Timeout time, in seconds. When disabling timeout, the parameter should be `None`
- `write_timeout`: Write timeout, in seconds. When disabling timeout, the parameter should be `None`
- `inter_byte_timeout`: Byte interval timeout, in seconds. When disabling timeout, the parameter should be `None`
- `wait_timeout`: The timeout in seconds for waiting for a response from the micropython device. When disabling timeout, the parameter should be `None`
- `immediate_connect`: Whether to connect immediately. If `True`, it will connect upon object creation; otherwise, you need to manually call the `connect` method after object creation to establish the connection.
Note: When creating an object, the serial port will always be connected, regardless of whether `immediate_connect` is `True` or `False`. However, whether to connect to the micropython device depends on whether `immediate_connect` is `True`.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

## Methods

### Connect

```python
opt.connect(*, verbose: bool = True) -> None
```

Connect to the MicroPython device. If already connected, this method is equivalent to reconnecting.

Args:

- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

### About the Tool

```python
opt.get_source_version(*, verbose: bool = False) -> tuple[int, int]
```

Get the instruction code program version number of this tool.

Args:

- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- The instruction code program version number, where the elements `(a, b)` in the tuple correspond to the version number `a.b`.

### Device info

```python
opt.uname(isstr: bool = True, *, verbose: bool = False) -> uname_result
#uname_result(sysname:str|bytes, nodename:str|bytes, release:str|bytes, version:str|bytes, machine:str|bytes)
```

Get the system information of the micropython device ([`os.uname`](https://docs.micropython.org/en/latest/library/os.html#os.uname)).

Args:

- `isstr`: Whether the content in the returned tuple is a string. If `True`, the content in the returned tuple is a string; otherwise, it is `bytes`.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- Device system information, similar to the return value of `os.uname`. Each element corresponds to the return value of [`os.uname`](https://docs.micropython.org/en/latest/library/os.html#os.uname).

```python
opt.get_uid(*, verbose: bool = False) -> bytes
```

Get the UID of the micropython device ([`machine.unique_id`](https://docs.micropython.org/en/latest/library/machine.html#machine.unique_id)).

Args:

- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- UID. The length may vary on different devices.

```python
opt.get_freq(*, verbose: bool = False) -> int
```

Get the CPU frequency of the micropython device ([`machine.freq`](https://docs.micropython.org/en/latest/library/machine.html#machine.freq)).

Args:

- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- CPU frequency, in Hz.

### Directory

```python
opt.getcwd(isstr: bool = True, *, verbose: bool = False) -> str | bytes
```

Get the current working directory of the micropython device ([`os.getcwd`](https://docs.micropython.org/en/latest/library/os.html#os.getcwd)).

Args:

- `isstr`: Whether the returned value is a string. If `True`, the returned value is a string; otherwise, it is `bytes`.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- Current working directory.

```python
opt.chdir(path: str | bytes | bytearray, *, verbose: bool = False) -> None
```

Change the current working directory of the micropython device ([`os.chdir`](https://docs.micropython.org/en/latest/library/os.html#os.chdir)).

Args:

- `path`: The new working directory.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

```python
opt.listdir(path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[str | bytes]
```

Get a list of files and folders in the specified directory of the micropython device ([`os.listdir`](https://docs.micropython.org/en/latest/library/os.html#os.listdir)).

Args:

- `path`: The specified directory.
- `isstr`: Whether the content in the returned list is a string. If `True`, the content in the returned list is a string; otherwise, it is `bytes`.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- A list of the names of files and folders in the specified directory.

```python
opt.ilistdir(path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[ilistdir_item]
# list[ilistdir_item(name:str|bytes, type:int, inode:int)]
```

Get a list of files and folders in the specified directory of the micropython device (similar to [`os.ilistdir`](https://docs.micropython.org/en/latest/library/os.html#os.ilistdir)).

Args:

- `path`: The specified directory.
- `isstr`: Whether the `name` attribute content of each `ilistdir_item` object in the returned list is a string. If `True`, the returned value is a string; otherwise, it is `bytes`.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- A list of the names of files and folders in the specified directory. Each element is an `ilistdir_item` object, where all attributes correspond to the return value of [`os.ilistdir`](https://docs.micropython.org/en/latest/library/os.html#os.ilistdir). For better compatibility, `ilistdir_item` does not contain the `size` attribute.

### File

```python
opt.upload(mpy_dst_file: str | bytes | bytearray, src_fp: SupportsReadBinaryIO, src_size: int, write_callback_function: Callable[[int, int], None] = None, block_size: int = 4096, *, verbose: bool = False) -> None
# SupportsReadBinaryIO: Readable binary IO object that includes methods such as read, readinto, and readable.
```

Upload a file from the local machine to the micropython device ([`open(mpy_dst_file,"wb")`](https://docs.micropython.org/en/latest/library/builtins.html#open), but the data to be written is uploaded from the local machine).

Args:

- `mpy_dst_file`: The target file path on the micropython device. If the path does not exist, the file will be automatically created.
- `src_fp`: Readable binary IO object. Data will be read from this object for `src_size` bytes.
- `src_size`: The size of the data to be uploaded. Unit is byte.
- `write_callback_function`: Callback function. This function will be called when a block is uploaded. The function is typically defined as `write_callback_function(total, cur)`, where `total` is the total data size (`=src_size`), and `cur` is the currently uploaded data size, in bytes.
- `block_size`: Block size. Unit is byte. Larger blocks can improve the upload speed, but the possibility of the device raise `MemoryError` also increases. The recommended value depends on the heap memory size. The default value is 4096.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

```python
opt.download(mpy_src_file: str | bytes | bytearray, dst_fp: SupportsWriteBinaryIO, read_callback_function: Callable[[int, int], None] = None, block_size: int = 4096, *, verbose: bool = False) -> None
# SupportsWriteBinaryIO: Writable binary IO object that includes methods such as write and writable.
```

Download a file from the micropython device to the local machine ([`open(mpy_src_file,"rb")`](https://docs.micropython.org/en/latest/library/builtins.html#open), but the data is read from the micropython device).

Args:

- `mpy_src_file`: The source file path on the micropython device. It should be a valid file path.
- `dst_fp`: Writable binary IO object. The file content will be written to this object.
- `read_callback_function`: Callback function. This function will be called when a block is read. The function is typically defined as `read_callback_function(total, cur)`, where `total` is the total file size, and `cur` is the currently read data size, in bytes.
- `block_size`: Block size. Unit is byte. Larger blocks can improve the download speed, but the possibility of the device raise `MemoryError` also increases. The recommended value depends on the heap memory size. The default value is 4096.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

### Path

```python
opt.remove(file: str | bytes | bytearray, *, verbose: bool = False) -> None
```

Delete a file on the micropython device ([`os.remove`](https://docs.micropython.org/en/latest/library/os.html#os.remove)).

Args:

- `file`: The file path on the micropython device. It should be a valid file path.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

```python
opt.rmdir(dir: str | bytes | bytearray, *, verbose: bool = False) -> None
```

Delete a folder on the micropython device ([`os.rmdir`](https://docs.micropython.org/en/latest/library/os.html#os.rmdir)).

Args:

- `dir`: The folder path on the micropython device. It should be a valid folder path.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

```python
opt.mkdir(dir: str | bytes | bytearray, *, verbose: bool = False) -> None
```

Create a folder on the micropython device ([`os.mkdir`](https://docs.micropython.org/en/latest/library/os.html#os.mkdir)).

Args:

- `dir`: The folder path on the micropython device. It should be a valid folder path.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

```python
opt.rename(src: str | bytes | bytearray, dst: str | bytes | bytearray, *, verbose: bool = False) -> None
```

Rename (move) a path on the micropython device ([`os.rename`](https://docs.micropython.org/en/latest/library/os.html#os.rename)).

Args:

- `src`: The source file or folder path on the micropython device. It should be a valid path.
- `dst`: The target file or folder path on the micropython device. It should be a non-existent path.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

### Path info

```python
opt.stat(path: str | bytes | bytearray, *, verbose: bool = False) -> stat_result
# stat_result(st_mode:int, st_ino:int, st_dev:int, st_nlink:int, st_uid:int, st_gid:int, st_size:int, st_atime:int, st_mtime:int, st_ctime:int)
```

Get the information of a path on the micropython device ([`os.stat`](https://docs.micropython.org/en/latest/library/os.html#os.stat)).

Args:

- `path`: The path on the micropython device. It should be a valid path.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- Path information. Each element in the return value corresponds to the return value of [`os.stat`](https://docs.micropython.org/en/latest/library/os.html#os.stat).

```python
opt.statvfs(path: str | bytes | bytearray, *, verbose: bool = False) -> statvfs_result
# statvfs_result(f_bsize:int, f_frsize:int, f_blocks:int, f_bfree:int, f_bavail:int, f_files:int, f_ffree:int, f_favail:int, f_flag:int, f_namemax:int)
```

Get the file system information of a path on the micropython device ([`os.statvfs`](https://docs.micropython.org/en/latest/library/os.html#os.statvfs)).

Args:

- `path`: The path on the micropython device. It should be a valid path.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- File system status. Each element in the return value corresponds to the return value of [`os.statvfs`](https://docs.micropython.org/en/latest/library/os.html#os.statvfs).

### RAM

```python
opt.get_gc_info(collect: bool = True, *, verbose: bool = False) -> gc_info
# gc_info(used:int, free:int)
```

Get the heap memory information on the micropython device ([`gc.mem_alloc`](https://docs.micropython.org/en/latest/library/gc.html#gc.mem_alloc), [`gc.mem_free`](https://docs.micropython.org/en/latest/library/gc.html#gc.mem_free)).

Args:

- `collect`: Whether to perform garbage collection before getting the information. The default value is `True`.
- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

Result:

- Heap memory information. The `used` attribute is the size of the used heap memory, and the `free` attribute is the size of the free heap memory, in bytes.

### Disconnect

```python
opt.close(*, verbose: bool = False) -> None
```

Disconnect from the micropython device and close the serial port.

Args:

- `verbose`: Whether to print debugging information. If an exception occurs, it can be set to `True` to view the debugging information.

## Destroy Object

When the `opt` object is destroyed (or manually calling `opt.__del__`), if the `opt` object is still connected to the micropython device (i.e., `opt.close` has not been called), `opt.close` is automatically called to disconnect and close the serial port.
