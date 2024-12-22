#!/usr/bin/env python3

import sys
import time
import traceback
import serial
import struct

micropython_code_file = "src/on_micropython/main.py"
encoding = "ascii"
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
SWD = b"\x11" # setcwd

RST = b"\xff" # reset

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
                ) -> None:
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
    def _dev_raise(self, funcname: str, errstr: bytes) -> None:
        raise MpyFileOptError("On {}(): In Micropython Device: \n    {}".format(funcname, errstr.decode(encoding)))
    def _dev_reset(self) -> None:
        self.ser.dtr = False
        time.sleep(0.01)
        self.ser.dtr = True
    def _dev_wait_in_repl(self) -> None:
        while True:
            time.sleep(0.05)
            self.ser.write(TER_INTP)
            if b"\n>>> " in self.ser.read_all():
                
                ## Special Code: If this code is not included, the serial port output error rate will reach 50%
                time.sleep(0.1)
                self.ser.reset_input_buffer()
                ## Special Code End

                break
    def _dev_send_src(self) -> None:
        with open(micropython_code_file, "r", encoding=encoding) as f:
            self.ser.write(b"exec(\'")
            self.ser.write(repr(f.read())[1:-1].encode(encoding))
            self.ser.write(b"\',globals())")
        self.ser.write(TER_NEWL)
    def _com_wait_ans(self):
        while True:
            #rdall = self.ser.read_all()
            #print(rdall.decode(encoding, "ignore"),end="")
            #if ANS in rdall:
            #    break
            if self.ser.read(1) == ANS:
                break
    def _connect(self) -> None:
        if self.verbose: print("[1/5] Reset device...")
        self._dev_reset()
        if self.verbose: print("[2/5] Wait device in REPL...")
        self._dev_wait_in_repl()
        if self.verbose: print("[3/5] Send source code...")
        self._dev_send_src()
        if self.verbose: print("[4/5] Wait device answer...")
        self._com_wait_ans()
        if self.verbose: print("[5/5] Done.")

    def _com_read_int(self ) -> int:
        ret = self.ser.read(4)
        return struct.unpack("<i", ret)[0]
    def _com_write_int(self, i: int) -> None:
        self.ser.write(struct.pack("<i", i))
    def _com_read_uint(self) -> int:
        ret = self.ser.read(4)
        return struct.unpack("<I", ret)[0]
    def _com_write_uint(self, i: int) -> None:
        self.ser.write(struct.pack("<I", i))
    def _com_read_string(self) -> bytes:
        len = self._com_read_uint()
        return self.ser.read(len)
    def _com_write_string(self, str: bytes) -> None:
        self._com_write_uint(len(str))
        self.ser.write(str)
    
    def getcwd(self, str: bool = True, *, verbose: bool = False) -> str | bytes:
        if verbose: print("[1/4] Send command GWD...")
        self.ser.write(GWD)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read path string...")
            wd = self._com_read_string()
            if verbose: print("[4/4] Done.")
            return wd.decode(encoding) if str else wd
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("getcwd", err)
    def chdir(self, path: str | bytes | bytearray, *, verbose: bool = False):
        if isinstance(path, str): 
            if verbose: print("[0/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/4] Send command SWD...")
        self.ser.write(SWD)
        if verbose: print("[2/4] Send path string...")
        self._com_write_string(path)
        if verbose: print("[3/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/4] Done.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("chdir", err)
    def _reset(self, *, verbose: bool = False):
        if verbose: print("[1/2] Send command RST...")
        self.ser.write(RST)
        if verbose: print("[2/2] Done.")
    def close(self, *, verbose: bool = False):
        self._reset(verbose = verbose)
        self.ser.close()
    def __del__(self):
        if self.ser.is_open:
            self.close()

        
if __name__ == '__main__':
    pass