#!/usr/bin/env python3

import sys,os
import time
import traceback
import serial
import struct

from collections import namedtuple

__version__ = '1.0'

micropython_code_file = f"{os.path.dirname(__file__)}/on_micropython/src.py"
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

GSV = b"\x00" # get_source_version
GUN = b"\x01" # get_uname

GWD = b"\x10" # getcwd
SWD = b"\x11" # setcwd
LSDIR = b"\x12" # listdir
ILDIR = b"\x13" # ilistdir



STAT  = b"\x30" # stat
VSTAT = b"\x31" # statvfs

RST = b"\xff" # reset

class MpyFileOptError(Exception):
    pass
class __types__:
    class uname_result(namedtuple("uname_result", ["sysname", "nodename", "release", "version" ,"machine"])):
        pass
    class ilistdir_item(namedtuple("ilistdir_item", ["name", "type", "inode"])):
        pass
    class stat_result(namedtuple("stat_result", ["st_mode", "st_ino", "st_dev", "st_nlink", "st_uid", "st_gid", "st_size", "st_atime", "st_mtime", "st_ctime"])):
        pass
    class statvfs_result(namedtuple("statvfs_result", ["f_bsize", "f_frsize", "f_blocks", "f_bfree", "f_bavail", "f_files", "f_ffree", "f_favail", "f_flag", "f_namemax"])):
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
        raise MpyFileOptError(f"On {funcname}(): In Micropython Device: \n    {errstr.decode(encoding)}")
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
    def get_source_version(self, *, verbose: bool = False) -> tuple[int, int]:
        if verbose: print("[1/4] Send command VER...")
        self.ser.write(GSV)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read version...")
            ver = (self._com_read_int(), self._com_read_int())
            if verbose: print("[4/4] Done.")
            return ver
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("get_source_version", err)
    def uname(self, *, verbose: bool = False) -> tuple[str, str, str, str, str]:
        if verbose: print("[1/4] Send command GUN...")
        self.ser.write(GUN)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read uname...")
            result = __types__.uname_result(
                self._com_read_string().decode(encoding),
                self._com_read_string().decode(encoding),
                self._com_read_string().decode(encoding),
                self._com_read_string().decode(encoding),
                self._com_read_string().decode(encoding)
            )
            if verbose: print("[4/4] Done.")
            return result
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("uname", err)
    def getcwd(self, isstr: bool = True, *, verbose: bool = False) -> str | bytes:
        if verbose: print("[1/4] Send command GWD...")
        self.ser.write(GWD)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read path string...")
            wd = self._com_read_string()
            if verbose: print("[4/4] Done.")
            return wd.decode(encoding) if isstr else wd
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("getcwd", err)
    def chdir(self, path: str | bytes | bytearray, *, verbose: bool = False) -> None:
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
    def listdir(self, path: str | bytes | bytearray, isstr: bool = True, *, verbose: bool = False) -> list[str | bytes]:
        if isinstance(path, str): 
            if verbose: print("[0/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command LSDIR...")
        self.ser.write(LSDIR)
        if verbose: print("[2/5] Send path string...")
        self._com_write_string(path)
        if verbose: print("[3/5] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/5] Success, Read dir list...")
            result = []
            length = self._com_read_uint()
            for _ in range(length):
                dir = self._com_read_string()
                result.append(dir.decode(encoding) if isstr else dir)
            if verbose: print("[5/5] Done.")
            return result
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("listdir", err)
    def ilistdir(self, path: str | bytes | bytearray, isstr: bool = True, *, verbose: bool = False) -> list[tuple[str | bytes, int, int]]:
        if isinstance(path, str): 
            if verbose: print("[0/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command ILDIR...")
        self.ser.write(ILDIR)
        if verbose: print("[2/5] Send path string...")
        self._com_write_string(path)
        if verbose: print("[3/5] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/5] Success, Read dir list...")
            result = []
            length = self._com_read_uint()
            for _ in range(length):
                name  = self._com_read_string()
                type  = self._com_read_uint()
                inode = self._com_read_uint()
                result.append(__types__.ilistdir_item(name.decode(encoding) if isstr else name, type, inode))
            if verbose: print("[5/5] Done.")
            return result
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("ilistdir", err)
    

    def stat(self, path: str | bytes | bytearray, *, verbose: bool = False) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        if isinstance(path, str): 
            if verbose: print("[0/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command STAT...")
        self.ser.write(STAT)
        if verbose: print("[2/5] Send path string...")
        self._com_write_string(path)
        if verbose: print("[3/5] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/5] Success, Read stat...")
            result = __types__.stat_result(
                self._com_read_uint(), # st_mode
                self._com_read_uint(), # st_ino
                self._com_read_uint(), # st_dev
                self._com_read_uint(), # st_nlink
                self._com_read_uint(), # st_uid
                self._com_read_uint(), # st_gid
                self._com_read_uint(), # st_size
                self._com_read_uint(), # st_atime
                self._com_read_uint(), # st_mtime
                self._com_read_uint()  # st_ctime
            )
            if verbose: print("[5/5] Done.")
            return result
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("stat", err)
    def statvfs(self, path: str | bytes | bytearray, *, verbose: bool = False) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        if isinstance(path, str): 
            if verbose: print("[0/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command VSTAT...")
        self.ser.write(VSTAT)
        if verbose: print("[2/5] Send path string...")
        self._com_write_string(path)
        if verbose: print("[3/5] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/5] Success, Read statvfs...")
            result = __types__.statvfs_result(
                self._com_read_int(), # f_bsize
                self._com_read_int(), # f_frsize
                self._com_read_int(), # f_blocks
                self._com_read_int(), # f_bfree
                self._com_read_int(), # f_bavail
                self._com_read_int(), # f_files
                self._com_read_int(), # f_ffree
                self._com_read_int(), # f_favail
                self._com_read_int(), # f_fsid
                self._com_read_int()  # f_flag
            )
            if verbose: print("[5/5] Done.")
            return result
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("statvfs", err)
    def _reset(self, *, verbose: bool = False) -> None:
        if verbose: print("[1/2] Send command RST...")
        self.ser.write(RST)
        if verbose: print("[2/2] Done.")
    def close(self, *, verbose: bool = False) -> None:
        self._reset(verbose = verbose)
        self.ser.close()
    def __del__(self):
        if self.ser.is_open:
            self.close()

        
if __name__ == '__main__':
    pass