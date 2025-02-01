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
                 *,
                 verbose: bool = True
                ) -> None:
```
参数：
- `port`: 串口名
- 