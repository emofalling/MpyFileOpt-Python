import sys
import time
import serial
import struct

micropython_code_file = "src/on_micropython/main.py"
# Terminal Codes
TM_CLRLINE = "\033[K"
TM_MVLSTLINE = "\033[1A" # \033[<N>A
# Serial Terminal Codes
TER_INTP = b"\x03" # Terminal_Interrupt
TER_NEWL = b"\x0d" # Terminal_NewLine
# Commands
ANS = b"\xaa" # Answer
ERR = b"\x55" # Error
SUC = b"\x99" # Success

GWD = b"\x10" # getcwd

class MpyFileOptError(Exception):
    pass
class MpyFileOpt:
    def __init__(self, 
                 com: str, 
                 baudrate: int                  = 115200, 
                 parity                         = serial.PARITY_NONE, 
                 stopbits: int                  = 1, 
                 timeout: int | None            = None, 
                 write_timeout: int | None      = None,
                 inter_byte_timeout: int | None = None,
                 *,
                 verbose: bool = True
                ):
        self.verbose = verbose
        self.ser = serial.Serial(com      ,          # port
                                 baudrate ,          # baudrate
                                 8        ,          # bytesize
                                 parity   ,          # parity
                                 stopbits ,          # stopbits
                                 timeout  ,          # timeout
                                 False    ,          # xonxoff
                                 False    ,          # rtscts
                                 write_timeout,      # write_timeout
                                 False    ,          # dsrdtr
                                 inter_byte_timeout, # inter_byte_timeout
                                )
        self._connect()
    def _dev_raise(self, errstr: bytes):
        raise MpyFileOptError("On getcwd(): In Micropython Device: \n    {}".format(errstr.decode("utf-8")))
    def _dev_reset(self):
        self.ser.dtr = False
        time.sleep(0.01)
        self.ser.dtr = True
    def _dev_wait_in_repl(self):
        while True:
            self.ser.write(TER_INTP)
            if self.ser.in_waiting > 0:
                time.sleep(0.1)
                if b"\n>>> " in self.ser.read_all():
                    break
    def _dev_send_src(self):
        with open(micropython_code_file, "r", encoding="utf-8") as f:
            self.ser.write(b"exec(\'")
            for line in f.readlines():
                time.sleep(0.01)
                self.ser.write(repr(line)[1:-1].encode("utf-8"))
            self.ser.write(b"\',globals())")
        self.ser.write(TER_NEWL)
    def _com_wait_ans(self):
        while True:
            if self.ser.in_waiting > 0:
                if self.ser.read_all() == ANS:
                    break
    def _connect(self):
        if self.verbose: print("[1/5] Reset device...")
        self._dev_reset()
        if self.verbose: print("[2/5] Wait device in REPL...")
        self._dev_wait_in_repl()
        if self.verbose: print("[3/5] Send source code...")
        self._dev_send_src()
        if self.verbose: print("[4/5] Wait device answer...")
        self._com_wait_ans()
        if self.verbose: print("[5/5] Done.")

    def _com_read_int(self):
        ret = self.ser.read(4)
        return struct.unpack("<i", ret)[0]
    def _com_write_int(self, i: int):
        self.ser.write(struct.pack("<i", i))
    def _com_read_uint(self):
        ret = self.ser.read(4)
        return struct.unpack("<I", ret)[0]
    def _com_write_uint(self, i: int):
        self.ser.write(struct.pack("<I", i))
    def _com_read_string(self):
        len = self._com_read_uint()
        return self.ser.read(len)
    def _com_write_string(self, str: bytes):
        self.ser.write(self._com_write_uint(len(str)))
        self.ser.write(str)
    
    def getcwd(self, str: bool = True, verbose: bool = False):
        if verbose: print("[0/2] Send command GWD...")
        self.ser.write(GWD)
        if verbose: print("[1/2] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[2/2] Success.")
            wd = self._com_read_string()
            return wd.decode("utf-8") if str else wd
        else:
            if verbose: print("[2/2] Failed.")
            self._dev_raise(self._com_read_string())
            
    def close(self):
        self.ser.close()
    def __del__(self):
        self.close()

        
if __name__ == '__main__':
    pass