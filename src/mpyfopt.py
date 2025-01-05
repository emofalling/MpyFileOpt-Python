#!/usr/bin/env python3

import sys
if sys.version_info < (3, 10):
    import warnings
    warnings.warn("Python 3.10 or later is required. That are not supported feautures below Python 3.10 (not include Python 3.10) include:\n                    Advanced Type Annotation (type_a | type_b, type[types], and more)", RuntimeWarning)

# startdard
import os
import time
import struct
from typing import Callable
# serial
import serial

# types
from collections import namedtuple

__version__ = '1.0'

micropython_code_file = f"{os.path.dirname(__file__)}/on_micropython/src.py"
encoding = "ascii"
# Serial Terminal Codes
TER_INTP = b"\x03" # Terminal_Interrupt
TER_NEWL = b"\r\n" # Terminal_NewLine
# Commands
ANS = b"\xaa" # Answer
ERR = b"\xff" # Error
SUC = b"\x00" # Success

TRUE = b"\x00"
FALSE = b"\x01"
NONE = b"\x02"

GSV = b"\x00" # get source version
GUN = b"\x01" # get uname
GID = b"\x02" # get uid
GFQ = b"\x03" # get cpu freq

GWD = b"\x10" # getcwd
SWD = b"\x11" # setcwd
LSDIR = b"\x12" # listdir
ILDIR = b"\x13" # ilistdir

FW = b"\x20" # file write
FR = b"\x21" # file read
BW = b"\x00" # [in file write / file read]block writing
BE = b"\xff" # [in file write / file read]block end
FRM = b"\x22" # remove file = remove
DRM = b"\x23" # remove dir = rmdir
MKDIR = b"\x24" # mkdir
RN = b"\x25" # rename

STAT  = b"\x30" # stat
VSTAT = b"\x31" # statvfs

GCI = b"\x40" # gc_info

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
    class gc_info(namedtuple("gc_info", ["used", "free"])):
        pass
class MpyFileOpt:
    def __init__(self, 
                 port: str, 
                 baudrate: int                  = 115200, 
                 parity                         = serial.PARITY_NONE, 
                 stopbits: float                = 1, 
                 timeout: int | None            = 1, 
                 write_timeout: int | None      = 1,
                 inter_byte_timeout: int | None = 0.1,
                 *,
                 verbose: bool = True
                ) -> None:
        """Connect to micropython device

            Args
            ---
            `port`: Port name to connect to micropython device
            `baudrate` ... `inter_byte_timeout`: Serial port settings, see `serial.Serial`
            `verbose`: if True, print debug info
    
            Returns
            ---
            None
    
            Raises
            ---
            `TimeoutError`: if read or write time out
            `MpyFileOptError`: if device return error string
            Other: not to elaborate 
        """
        self.verbose = verbose
        self.ser = None
        self.ser = serial.Serial(port      ,          # port
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
        """If the error throwed from micropython device, call it to throw error"""
        raise MpyFileOptError(f"On {funcname}(): In Micropython Device: \n    {errstr.decode(encoding)}")
    def _dev_reset(self) -> None:
        """reset device"""
        self.ser.dtr = False
        time.sleep(0.01)
        self.ser.dtr = True
    def _dev_wait_in_repl(self) -> None:
        """send interrupt until device in REPL mode"""
        while True:
            time.sleep(0.05)
            self._com_write(TER_INTP)
            if b"\n>>> " in self.ser.read_all():
                
                ## Special Code: If this code is not included, the serial port output error rate will reach 50%
                time.sleep(0.1)
                self.ser.reset_input_buffer()
                ## Special Code End

                break
    def _dev_send_src(self) -> None:
        """send source code to device"""
        with open(micropython_code_file, "r", encoding=encoding) as f:
            self._com_write(b"exec(\'")
            self._com_write(repr(f.read())[1:-1].encode(encoding))
            self._com_write(b"\',globals())")
        self._com_write(TER_NEWL)
    def _com_write(self, data: bytes) -> int:
        """write data to the serial port, but it can handling the timeout error."""
        ret = self.ser.write(data)
        if ret == None:
            raise TimeoutError("Write time out.")
        return ret
    def _com_wait_ans(self):
        """wait device answer"""
        while True:
            #rdall = self.ser.read_all()
            #print(rdall.decode(encoding, "ignore"),end="")
            #if ANS in rdall:
            #    break
            if self.ser.read(1) == ANS:
                break
    def _connect(self) -> None:
        """Connect to device"""
        if self.verbose: print("[1/5] Reset device...")
        self._dev_reset()
        if self.verbose: print("[2/5] Wait device in REPL...")
        self._dev_wait_in_repl()
        if self.verbose: print("[3/5] Send source code...")
        self._dev_send_src()
        if self.verbose: print("[4/5] Wait device answer...")
        self._com_wait_ans()
        if self.verbose: print("[5/5] Done.")
    def _com_read_bool(self) -> bool | None:
        """read boolean data or nonetype from the serial port"""
        ret = self.ser.read(1)
        if ret == b"":
            raise TimeoutError("Read time out.")
        if ret == TRUE:
            return True
        elif ret == FALSE:
            return False
        elif ret == NONE:
            return None
        else:
            raise MpyFileOptError(f"Unknown code: {ret}")
    def _com_write_bool(self, b: bool | None) -> None:
        """write boolean data or nonetype to the serial port"""
        if b is None:
            self._com_write(NONE)
        else:
            self._com_write(TRUE if b else FALSE)
    def _com_read_int(self) -> int:
        """read int data from the serial port"""
        ret = self.ser.read(4)
        if ret == b"":
            raise TimeoutError("Read time out.")
        return struct.unpack("<i", ret)[0]
    def _com_write_int(self, i: int) -> None:
        """write int data to the serial port"""
        ret = self.ser.write(struct.pack("<i", i))
        if ret == None:
            raise TimeoutError("Write time out.")
    def _com_read_uint(self) -> int:
        """read unsigned int data from the serial port"""
        ret = self.ser.read(4)
        if ret == b"":
            raise TimeoutError("Read time out.")
        return struct.unpack("<I", ret)[0]
    def _com_write_uint(self, i: int) -> None:
        """write unsigned int data to the serial port"""
        ret = self.ser.write(struct.pack("<I", i))
        if ret == None:
            raise TimeoutError("Write time out.")
    def _com_read_string(self) -> bytes:
        """read string data from the serial port"""
        len = self._com_read_uint()
        ret = self.ser.read(len)
        if ret == b"":
            raise TimeoutError("Read time out.")
        return ret
    def _com_write_string(self, str: bytes | bytearray) -> None:
        """write string data to the serial port"""
        self._com_write_uint(len(str))
        ret = self.ser.write(str)
        if ret == None:
            raise TimeoutError("Write time out.")
    
    def get_source_version(self, *, verbose: bool = False) -> tuple[int, int]:
        """Get source version

           Args
           ---
           `verbose`: if True, print debug info

           Returns
           ---
           a tuple, info is `(major, minir)`

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate 
        """
        if verbose: print("[1/4] Send command VER...")
        self._com_write(GSV)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read version...")
            ver = (self._com_read_int(), self._com_read_int())
            if verbose: print("[4/4] Done.")
            return ver
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("get_source_version", err)
    def uname(self, isstr: bool = True, *, verbose: bool = False) -> tuple[str, str, str, str, str] | tuple[bytes, bytes, bytes, bytes, bytes]:
        """Read sys.uname from the device

           Args
           ---
           `isstr`: if True, return str, else return bytes
           `verbose`: if True, print debug info

           Returns
           ---
           a tuple, info is `uname_result(sysname=sysname, nodename=nodename, release=release, version=version, machine=machine)`

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if verbose: print("[1/4] Send command GUN...")
        self._com_write(GUN)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read uname...")
            result = __types__.uname_result(
                self._com_read_string().decode(encoding) if isstr else self._com_read_string(),
                self._com_read_string().decode(encoding) if isstr else self._com_read_string(),
                self._com_read_string().decode(encoding) if isstr else self._com_read_string(),
                self._com_read_string().decode(encoding) if isstr else self._com_read_string(),
                self._com_read_string().decode(encoding) if isstr else self._com_read_string()
            )
            if verbose: print("[4/4] Done.")
            return result
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("uname", err)
    def get_uid(self, *, verbose: bool = False) -> bytes:
        """Read unique(machine.unique_id) id from the device

           Args
           ---
           `verbose`: if True, print debug info

           Returns
           ---
           unique id. About content of unique_id, see `machine.unique_id`

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if verbose: print("[1/4] Send command GID...")
        self._com_write(GID)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read unique id...")
            uid = self._com_read_string()
            if verbose: print("[4/4] Done.")
            return uid
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("unique_id", err)
    def get_freq(self, *, verbose: bool = False) -> int:
        """Read CPU frequency from the device

           Args
           ---
           `verbose`: if True, print debug info

           Returns
           ---
           CPU frequency

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if verbose: print("[1/4] Send command GFQ...")
        self._com_write(GFQ)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read frequency...")
            freq = self._com_read_uint()
            if verbose: print("[4/4] Done.")
            return freq
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("get_freq", err)



    def getcwd(self, isstr: bool = True, *, verbose: bool = False) -> str | bytes:
        """Read current workdir(os.getcwd) from the device  

           Args
           ---
           `isstr`: if True, return str, else return bytes
           `verbose`: if True, print debug info

           Returns
           ---
           current workdir. If `isstr` is True, return type is `str`, else `bytes`

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if verbose: print("[1/4] Send command GWD...")
        self._com_write(GWD)
        if verbose: print("[2/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[3/4] Success, Read path string...")
            wd = self._com_read_string()
            if verbose: print("[4/4] Done.")
            return wd.decode(encoding) if isstr else wd
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[3/4] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[4/4] Done.")
            self._dev_raise("getcwd", err)
    def chdir(self, path: str | bytes | bytearray, *, verbose: bool = False) -> None:
        """Change current workdir(os.chdir) to the device

           Args
           ---
           `path`: path to change to
           `verbose`: if True, print debug info

           Returns
           ---
           None

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if isinstance(path, str): 
            if verbose: print("[?/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/4] Send command SWD...")
        self._com_write(SWD)
        if verbose: print("[2/4] Send path string...")
        self._com_write_string(path)
        if verbose: print("[3/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/4] Success.")
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("chdir", err)
    def listdir(self, path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[str | bytes]:
        """Read path list(os.listdir) from the device

           Args
           ---
           `path`: path to read. default is current directory(.)
           `isstr`: if True, path in list is str, else is bytes
           `verbose`: if True, print debug info

           Returns
           ---
           path list. If `isstr` is True, return type is `list[str]`, else `list[bytes]`

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if isinstance(path, str): 
            if verbose: print("[?/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command LSDIR...")
        self._com_write(LSDIR)
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
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("listdir", err)
    def ilistdir(self, path: str | bytes | bytearray = b".", isstr: bool = True, *, verbose: bool = False) -> list[tuple[str | bytes, int, int]]:
        """Read path info list(os.ilistdir) from the device

           Args
           ---
           `path`: path to read. default is current directory(.)
           `isstr`: if True, path in list is str, else is bytes
           `verbose`: if True, print debug info

           Returns
           ---
           path info list. If `isstr` is True, return type is `list[tuple[str, int, int]]`, else `list[tuple[bytes, int, int]]`.  

           It likes `[ilistdir_item(path=path, type=type, inode=inode), ...]`

           Raises
           ---
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if isinstance(path, str): 
            if verbose: print("[?/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command ILDIR...")
        self._com_write(ILDIR)
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
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("ilistdir", err)
    def upload(self, mpy_dst_file: str | bytes | bytearray, src_file: str, block_size: int = 4096, write_callback_function: Callable[[int, int], None] = None, *, verbose: bool = False) -> None:
        """Upload file to the device

           Args
           ---
           `mpy_dst_file`: path to write in the device
           `src_file`: path to read in the host
           `block_size`: block size to transmit data. It must be > 0. The larger `block_size`, the faster write speed, but the more memory usage on device.
           `write_callback_function`: callback function to print progress.
            - `write_callback_function(total:int, cur:int)` is called every time a block is transmitted. `total` is the total size of the file, `cur` is the current size of the file.
            - in check progress(before sending file), call it with arguments `-1, -1` to test the function not to throw error.
        
           `verbose`: if True, print debug info

           Returns
           ---
           None

           Raises
           ---
           `ValueError`: if block_size <= 0
           `TypeError`: if read_callback_function is not callable
           `TimeoutError`: if read or write time out
           `MpyFileOptError`: if device return error string
           Other: not to elaborate
        """
        if isinstance(mpy_dst_file, str): 
            if verbose: print("[?/5] Convert path str to bytes...")
            mpy_dst_file = mpy_dst_file.encode(encoding)
        if verbose: print("[?/5] Check callback function...")
        if write_callback_function is None:
            write_callback_function = lambda total, cur: None
        if not callable(write_callback_function):
            raise TypeError("write_callback_function must be callable or None")
        write_callback_function(-1, -1)
        if verbose: print("[?/5] Check blocksize...")
        if block_size <= 0:
            raise ValueError("block_size must be > 0")
        with open(src_file, "rb") as f:
            if verbose: print("[1/5] Send command FW...")
            self._com_write(FW)
            if verbose: print("[2/5] Send path string, file size, and block size...")
            self._com_write_string(mpy_dst_file)
            file_size = os.path.getsize(src_file)
            self._com_write_uint(file_size)
            self._com_write_uint(block_size)
            if verbose: print("[3/5] Wait answer...")
            ret = self.ser.read(1)
            if ret == SUC:
                if verbose: print("[4/5] Success, Send file data...")
            elif ret == b"":
                raise TimeoutError("Read time out.")
            else:
                if verbose: print("[4/5] Failed, Read error string...")
                err = self._com_read_string()
                if verbose: print("[5/5] Done.")
                self._dev_raise("upload", err)
            buffer = bytearray(block_size)
            total = file_size
            cur = 0
            write_callback_function(total, cur)
            while file_size > 0:
                if file_size >= block_size:
                    self._com_write(BW)
                    lendata = block_size
                    f.readinto(buffer)
                else:
                    del buffer
                    self._com_write(BE)
                    lendata = file_size
                    self._com_write_uint(lendata)
                    buffer = f.read(lendata)
                self._com_write(buffer)
                if verbose: print(f"Send {lendata} bytes")
                ret = self.ser.read(1)
                if ret != SUC:
                    if ret == b"":
                        raise TimeoutError("Read time out.")
                    else:
                        if verbose: print("[5/6] Failed, Read error string...")
                        err = self._com_read_string()
                        if verbose: print("[6/6] Done.")
                        self._dev_raise("upload", err)
                file_size -= lendata
                cur += lendata
                write_callback_function(total, cur)
                if verbose: print(f"Sended {lendata} bytes, {cur}/{total}")
        if verbose: print("[5/5] Done.")
    def download(self, mpy_src_file: str | bytes | bytearray, dst_file: str, block_size: int = 4096, read_callback_function: Callable[[int, int], None] = None, *, verbose: bool = False) -> None:
        """Download file from the device

            Args
            ---
            `mpy_src_file`: path to read in the device
            `dst_file`: path to write in the host
            `block_size`: block size for read/write
            `read_callback_function`: callback function to print progress.
                - `read_callback_function(total:int, cur:int)` is called every time a block is transmitted. `total` is the total size of the file, `cur` is the current size of the file.
                - in check progress(before sending file), call it with arguments `-1, -1` to test the function not to throw error.

            `verbose`: if True, print debug info

            Returns
            ---
            None

            Raises
            ---
            `ValueError`: if block_size <= 0
            `TypeError`: if read_callback_function is not callable
            `TimeoutError`: if read or write time out
            `MpyFileOptError`: if device return error string
            Other: not to elaborate

        """
        if isinstance(mpy_src_file, str):
            if verbose: print("[?/5] Convert path str to bytes...")
            mpy_src_file = mpy_src_file.encode(encoding)
        if verbose: print("[?/5] Check callback function...")
        if read_callback_function is None:
            read_callback_function = lambda total, cur: None
        if not callable(read_callback_function):
            raise TypeError("read_callback_function must be callable or None")
        read_callback_function(-1, -1)
        if verbose: print("[?/5] Check blocksize...")
        if block_size <= 0:
            raise ValueError("block_size must be > 0")
        with open(dst_file, "wb") as f:
            if verbose: print("[1/5] Send command FR...")
            self._com_write(FR)
            if verbose: print("[2/5] Send path string, and block size...")
            self._com_write_string(mpy_src_file)
            self._com_write_uint(block_size)
            if verbose: print("[3/5] Wait answer...")
            ret = self.ser.read(1)
            if ret == SUC:
                if verbose: print("[4/5] Success, Read file data...")
            elif ret == b"":
                raise TimeoutError("Read time out.")
            else:
                if verbose: print("[4/5] Failed, Read error string...")
                err = self._com_read_string()
                if verbose: print("[5/5] Done.")
                self._dev_raise("download", err)
            file_size = self._com_read_uint()
            if verbose: print(f"File size: {file_size}")
            total = file_size
            cur = 0
            read_callback_function(total, cur)
            while file_size > 0:
                if file_size >= block_size:
                    lendata = block_size
                    self._com_write(BW)
                else:
                    lendata = file_size
                    self._com_write(BE)
                    self._com_write_uint(lendata)
                if verbose: print(f"Read {lendata} bytes")
                ret = self.ser.read(1)
                if ret != SUC:
                    if ret == b"":
                        raise TimeoutError("Read time out.")
                    else:
                        if verbose: print("[5/6] Failed, Read error string...")
                        err = self._com_read_string()
                        if verbose: print("[6/6] Done.")
                        self._dev_raise("download", err)
                f.write(self.ser.read(lendata))
                file_size -= lendata
                cur += lendata
                read_callback_function(total, cur)
                if verbose: print(f"Readed {lendata} bytes, {cur}/{total}")
        if verbose: print("[5/5] Done.")
    def remove(self, file: str | bytes | bytearray, *, verbose: bool = False) -> None:
        """Remove file(os.remove) from the device

        Args
        ---
        `file`: file path to remove
        `verbose`: if True, print debug info

        Returns
        ---
        None

        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if isinstance(file, str): 
            if verbose: print("[?/4] Convert path str to bytes...")
            file = file.encode(encoding)
        if verbose: print("[1/4] Send command FRM...")
        self._com_write(FRM)
        if verbose: print("[2/4] Send path string...")
        self._com_write_string(file)
        if verbose: print("[3/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/4] Success.")
            return
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("remove", err)
    def rmdir(self, dir: str | bytes | bytearray, *, verbose: bool = False) -> None:
        """Remove dir(os.rmdir) from the device

        Args
        ---
        `dir`: dir path to remove
        `verbose`: if True, print debug info

        Returns
        ---
        None

        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if isinstance(dir, str): 
            if verbose: print("[?/4] Convert path str to bytes...")
            dir = dir.encode(encoding)
        if verbose: print("[1/4] Send command DRM...")
        self._com_write(DRM)
        if verbose: print("[2/4] Send path string...")
        self._com_write_string(dir)
        if verbose: print("[3/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/4] Success.")
            return
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("rmdir", err)
    def mkdir(self, dir: str | bytes | bytearray, *, verbose: bool = False) -> None:
        """Make dir(os.mkdir) from the device

        Args
        ---
        `dir`: dir path to make
        `verbose`: if True, print debug info

        Returns
        ---
        None

        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if isinstance(dir, str): 
            if verbose: print("[?/4] Convert path str to bytes...")
            dir = dir.encode(encoding)
        if verbose: print("[1/4] Send command MKDIR...")
        self._com_write(MKDIR)
        if verbose: print("[2/4] Send path string...")
        self._com_write_string(dir)
        if verbose: print("[3/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/4] Success.")
            return
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("mkdir", err)
    def rename(self, old: str | bytes | bytearray, new: str | bytes | bytearray, *, verbose: bool = False) -> None:
        """Rename path(os.rename) from the device

        Args
        ---
        `old`: old path
        `new`: new path
        `verbose`: if True, print debug info

        Returns
        ---
        None

        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if isinstance(old, str): 
            if verbose: print("[?/4] Convert old path str to bytes...")
            old = old.encode(encoding)
        if isinstance(new, str):
            if verbose: print("[?/4] Convert new path str to bytes...")
            new = new.encode(encoding)
        if verbose: print("[1/4] Send command RN...")
        self._com_write(RN)
        if verbose: print("[2/4] Send old path string and new path string...")
        self._com_write_string(old)
        self._com_write_string(new)
        if verbose: print("[3/4] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/4] Success.")
            return
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("rename", err)

    def stat(self, path: str | bytes | bytearray, *, verbose: bool = False) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        """Get stat(os.stat) from the device

        Args
        ---
        `path`: path to get stat
        `verbose`: if True, print debug info

        Returns
        ---
        a tuple, info is `stat_result(st_mode=st_mode, st_ino=st_ino, st_dev=st_dev, st_nlink=st_nlink, st_uid=st_uid, st_gid=st_gid, st_size=st_size, st_atime=st_atime, st_mtime=st_mtime, st_ctime=st_ctime)`
        
        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if isinstance(path, str): 
            if verbose: print("[?/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command STAT...")
        self._com_write(STAT)
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
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("stat", err)
    def statvfs(self, path: str | bytes | bytearray, *, verbose: bool = False) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        """Get filesystem stat(os.statvfs) from the device

        Args
        ---
        `path`: path to get stat
        `verbose`: if True, print debug info

        Returns
        ---
        a tuple, info is `statvfs_result(f_bsize=f_bsize, f_frsize=f_frsize, f_blocks=f_blocks, f_bfree=f_bfree, f_bavail=f_bavail, f_files=f_files, f_ffree=f_ffree, f_favail=f_favail, f_flag=f_flag, f_namemax=f_namemax)`
        
        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if isinstance(path, str): 
            if verbose: print("[?/5] Convert path str to bytes...")
            path = path.encode(encoding)
        if verbose: print("[1/5] Send command VSTAT...")
        self._com_write(VSTAT)
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
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("statvfs", err)

    def get_gc_info(self, collect: bool = True, *, verbose: bool = False) -> tuple[int, int, int]:
        """Get GC info from the device

        Args
        ---
        `collect`: if True, call gc.collect() before get info
        `verbose`: if True, print debug info

        Returns
        ---
        a tuple, info is `gc_info(used=mem_alloc, free=mem_free)`

        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        if verbose: print("[1/5] Send command GCI...")
        self._com_write(GCI)
        if verbose: print("[2/5] Send collect bool...")
        self._com_write_bool(collect)
        if verbose: print("[3/5] Wait answer...")
        ret = self.ser.read(1)
        if ret == SUC:
            if verbose: print("[4/5] Success, Read gc info...")
            result = __types__.gc_info(
                self._com_read_int(), # mem_alloc
                self._com_read_int(), # mem_free
            )
            if verbose: print("[5/5] Done.")
            return result
        elif ret == b"":
            raise TimeoutError("Read time out.")
        else:
            if verbose: print("[4/5] Failed, Read error string...")
            err = self._com_read_string()
            if verbose: print("[5/5] Done.")
            self._dev_raise("gc_info", err)
    def _reset(self, *, verbose: bool = False) -> None:
        """reset device"""
        if verbose: print("[1/2] Send command RST...")
        self._com_write(RST)
        if verbose: print("[2/2] Done.")
    def close(self, *, verbose: bool = False) -> None:
        """Reset device and close the serial port
        
        Args
        ---
        `verbose`: if True, print debug info
        
        Raises
        ---
        `TimeoutError`: if read or write time out
        `MpyFileOptError`: if device return error string
        Other: not to elaborate
        """
        self._reset(verbose = verbose)
        self.ser.close()
    def __del__(self):
        """call self.close when this object is deleted"""
        if self.ser is None:
            return
        if self.ser.is_open:
            self.close()



if __name__ == '__main__':
    # errors
    import traceback
    # command line
    import argparse
    import shlex
    # hex & calculation
    import binascii
    import math
    # terminal codes
    ANSI_RESET_ALL          = "\x1b[0m"
    ANSI_COLOR_BLACK        = "\x1b[30m"
    ANSI_COLOR_RED          = "\x1b[31m"
    ANSI_COLOR_GREEN        = "\x1b[32m"
    ANSI_COLOR_YELLOW       = "\x1b[33m"
    ANSI_COLOR_BLUE         = "\x1b[34m"
    ANSI_COLOR_PURPLE       = "\x1b[35m"
    ANSI_COLOR_CYAN         = "\x1b[36m"
    ANSI_COLOR_WHITE        = "\x1b[37m"
    ANSI_COLOR_LIGHT_BLACK  = "\x1b[90m"
    ANSI_COLOR_LIGHT_RED    = "\x1b[91m"
    ANSI_COLOR_LIGHT_GREEN  = "\x1b[92m"
    ANSI_COLOR_LIGHT_YELLOW = "\x1b[93m"
    ANSI_COLOR_LIGHT_BLUE   = "\x1b[94m"
    ANSI_COLOR_LIGHT_PURPLE = "\x1b[95m"
    ANSI_COLOR_LIGHT_CYAN   = "\x1b[96m"
    ANSI_COLOR_LIGHT_WHITE  = "\x1b[97m"



    BASE_COMPUTER = 1024
    BASE_GENERAL  = 1000
    SUFFIX_LIST_COMPUTER = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi", "Yi", "Bi"]
    SUFFIX_LIST_GENERAL =  ["", "K" , "M" , "G" , "T" , "P" , "E" , "Z" , "Y" , "B" ]
    def auto_suffix(num: int, base: int = BASE_GENERAL, suffix_list: list[str] = SUFFIX_LIST_GENERAL) -> tuple[int, str]:
        lf = math.floor(math.log(num, base))
        try:
            suffix = suffix_list[lf]
        except IndexError:
            return 1, suffix_list[0]
        return base ** lf, suffix



    all_commands = ["var", "shell", "ver", "uname", "uid", "freq", "pwd", "cd", "ls", "ils", "cat", "push", "pull", "rm", "rmdir", "mkdir", "mv", "gc", "stat", "statvfs"]
    argv = sys.argv[1:]
    colorful = False
    def logerr(msg, prefix = "Error: "):
        print((ANSI_COLOR_RED if colorful else "") + prefix + msg + (ANSI_RESET_ALL if colorful else ""))
    def subcmd_parse_args(parser: argparse.ArgumentParser, args: list[str]):
        try:
            return parser.parse_args(args[1:])
        except SystemExit:
            return False

    main_parser = argparse.ArgumentParser(description = "Connect to MicroPython device and do something with subcommands.", epilog = "See README.md for more information.", add_help = True)
    main_parser.add_argument("port", help="serial port")
    main_parser.add_argument("-B" , "--baudrate"          , type=int,                                   default=115200, help="serial baudrate. default 115200")
    main_parser.add_argument("-P" , "--parity"            ,             choices=serial.Serial.PARITIES, default="N",    help="serial parity. default N")
    main_parser.add_argument("-S" , "--stopbits"          , type=float, choices=serial.Serial.STOPBITS, default=1,      help="serial stopbits. default 1")
    main_parser.add_argument("-To", "--timeout"           , type=float,                                 default=1,      help="serial timeout. if 0, no timeout. default 0")
    main_parser.add_argument("-Tw", "--write-timeout"     , type=float,                                 default=1,      help="serial write timeout. if 0, no timeout. default 0")
    main_parser.add_argument("-Tb", "--inter-byte-timeout", type=float,                                 default=0.1,    help="serial inter-byte timeout. default 0.1")
    
    main_parser.add_argument("-v" , "--verbose"           , action="store_true", help="output debug info")
    main_parser.add_argument("-nc" , "--no-colorful"          , action="store_false", help="make output not colorful. if terminal not support ANSI color escape sequence, recommended select this option")

    # main_parser.add_argument("subcommands", nargs=0, help="subcommand and its arguments")

    # shell
    subcmd_shell_parser = argparse.ArgumentParser("shell", description = "Into a shell to key and run subcommands conveniently.", epilog = "See README.md for more information.", add_help = True)
    # shell-exit
    subcmd_shell_exit_parser = argparse.ArgumentParser("exit", description = "Exit shell.", epilog = "See README.md for more information.", add_help = True)
    # ver
    subcmd_ver_parser = argparse.ArgumentParser("ver", description="Print version of this project", epilog="See README.md for more information.", add_help = True)
    subcmd_ver_parser.add_argument("-c", "--csv", action="store_true", help="output csv format")
    subcmd_ver_parser.add_argument("-v", "--verbose", action="store_true", help="output debug info")
    # uname
    subcmd_uname_parser = argparse.ArgumentParser("uname", description="Print device's system information. if no option(except --csv(-c) and --verbose), output kernel name.", epilog="See README.md for more information.", add_help = True)
    subcmd_uname_parser.add_argument("-a", "--all", action="store_true", help="output all information")
    subcmd_uname_parser.add_argument("-s", "--kernel-name", action="store_true", help="output the kernel name. this is the normal option")
    subcmd_uname_parser.add_argument("-n", "--nodename", action="store_true", help="output the network node hostname")
    subcmd_uname_parser.add_argument("-r", "--kernel-release", action="store_true", help="output the kernel release")
    subcmd_uname_parser.add_argument("-v", "--kernel-version", action="store_true", help="output the kernel version")
    subcmd_uname_parser.add_argument("-m", "--machine", action="store_true", help="output the machine hardware name")
    subcmd_uname_parser.add_argument("-c", "--csv", action="store_true", help="output csv format")
    subcmd_uname_parser.add_argument(      "--verbose", action="store_true", help="output debug info")
    # uid
    subcmd_uid_parser = argparse.ArgumentParser("uid", description="Print device's unique id", epilog="See README.md for more information.", add_help = True)
    subcmd_uid_parser.add_argument("-v", "--verbose", action="store_true", help="output debug info")
    # freq
    subcmd_freq_parser = argparse.ArgumentParser("freq", description="Print device's cpu frequency", epilog="See README.md for more information.", add_help = True)
    subcmd_freq_parser.add_argument("-r", "--raw", action="store_true", help="output raw cpu frequency. it has no suffix, unit Hz.")
    subcmd_freq_parser.add_argument("-v", "--verbose", action="store_true", help="output debug info")
    # pwd
    subcmd_pwd_parser = argparse.ArgumentParser("pwd", description="Print device's current working directory", epilog="See README.md for more information.", add_help = True)
    subcmd_pwd_parser.add_argument("-v", "--verbose", action="store_true", help="output debug info")
    # cd
    subcmd_cd_parser = argparse.ArgumentParser("cd", description="Change device's current working directory", epilog="See README.md for more information.", add_help = True)
    subcmd_cd_parser.add_argument("dir", nargs="?", default="/", help="dir to change to. if not specified, change to /")
    subcmd_cd_parser.add_argument("-v", "--verbose", action="store_true", help="output debug info")


    maincmd_argv = []
    subcmd_argv_list = []
    is_subcmd = False
    for i in argv:
        if i in all_commands:
            is_subcmd = True
            current_subcmd_argv = [i]
            subcmd_argv_list.append(current_subcmd_argv)
        else:
            if is_subcmd:
                current_subcmd_argv.append(i)
            else:
                maincmd_argv.append(i)
    print(maincmd_argv)
    print(subcmd_argv_list)
    args = main_parser.parse_args(maincmd_argv)
    colorful = args.no_colorful
    try:
        opt = MpyFileOpt(
            args.port,
            baudrate = args.baudrate,
            parity = args.parity,
            stopbits = args.stopbits,
            timeout = None if args.timeout == 0 else args.timeout,
            write_timeout = None if args.write_timeout == 0 else args.write_timeout,
            inter_byte_timeout = None if args.inter_byte_timeout == 0 else args.inter_byte_timeout,

            verbose = args.verbose,
        )
    except BaseException:
        logerr(traceback.format_exc(), "")
        exit(1)
    shell_workdir = ""
    def match_subcmd(subcmd_argv: list[str]):
        global shell_workdir
        subcmd = subcmd_argv[0]
        match subcmd:
            case "shell":
                s_args = subcmd_parse_args(subcmd_shell_parser, subcmd_argv)
                if not s_args: return
                try:
                    shell()
                except KeyboardInterrupt:
                    logerr("KeyboardInterrupt", "")
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    pass
            case "ver":
                s_args = subcmd_parse_args(subcmd_ver_parser, subcmd_argv)
                if not s_args: return
                try:
                    srcver = opt.get_source_version(verbose = s_args.verbose)
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    return
                if s_args.csv:
                    print(f"{__version__},{srcver[0]}.{srcver[1]}")
                else:
                    print(f"mpyfopt version: {__version__}")
                    print(f"source version: {srcver[0]}.{srcver[1]}")
            case "uname":
                s_args = subcmd_parse_args(subcmd_uname_parser, subcmd_argv)
                if not s_args: return
                try:
                    uname = opt.uname(verbose = s_args.verbose)
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    return
                if s_args.csv:
                    uname_infos = []
                    if s_args.kernel_name or s_args.all or not any([s_args.kernel_name, s_args.nodename, s_args.kernel_release, s_args.kernel_version, s_args.machine]):
                        uname_infos.append(uname[0])
                    if s_args.nodename or s_args.all:
                        uname_infos.append(uname[1])
                    if s_args.kernel_release or s_args.all:
                        uname_infos.append(uname[2])
                    if s_args.kernel_version or s_args.all:
                        uname_infos.append(uname[3])
                    if s_args.machine or s_args.all:
                        uname_infos.append(uname[4])
                    print(",".join(uname_infos))
                else:
                    if s_args.kernel_name or s_args.all or not any([s_args.kernel_name, s_args.nodename, s_args.kernel_release, s_args.kernel_version, s_args.machine]):
                        print("Kernel name:", uname[0])
                    if s_args.nodename or s_args.all:
                        print("Node name:", uname[1])
                    if s_args.kernel_release or s_args.all:
                        print("Kernel release:", uname[2])
                    if s_args.kernel_version or s_args.all:
                        print("Kernel version:", uname[3])
                    if s_args.machine or s_args.all:
                        print("Machine:", uname[4])
            case "uid":
                s_args = subcmd_parse_args(subcmd_uid_parser, subcmd_argv)
                if not s_args: return
                try:
                    uid = opt.get_uid(verbose = s_args.verbose)
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    return
                uid_s = binascii.hexlify(uid).decode("ascii")
                print(uid_s)
            case "freq":
                s_args = subcmd_parse_args(subcmd_freq_parser, subcmd_argv)
                if not s_args: return
                try:
                    freq = opt.get_freq(verbose = s_args.verbose)
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    return
                if s_args.raw:
                    print(freq)
                else:
                    div, sif = auto_suffix(freq)
                    print(f"{freq / div} {sif}Hz")
            case "pwd":
                s_args = subcmd_parse_args(subcmd_pwd_parser, subcmd_argv)
                if not s_args: return
                try:
                    path = opt.getcwd()
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    return
                print(path)
                shell_workdir = path
            case "cd":
                s_args = subcmd_parse_args(subcmd_cd_parser, subcmd_argv)
                if not s_args: return
                try:
                    opt.chdir(s_args.dir)
                except BaseException:
                    logerr(traceback.format_exc(), "")
                    return
                shell_workdir = opt.getcwd()
            case "ls":...
                 

                
            case _:
                logerr(f"unknown subcommand: {subcmd}", "")
    def shell():
        global shell_workdir
        shell_workdir = opt.getcwd()
        while True:
            line = input(f"{ANSI_COLOR_GREEN}{shell_workdir}{ANSI_RESET_ALL} > ")
            line = line.replace("$PWD", shell_workdir)
            args = shlex.split(line)
            #print(args)
            if len(args) == 0:
                continue
            if args[0] == "exit":
                if len(args) > 1:
                    subcmd_parse_args(subcmd_shell_exit_parser, args)
                    continue
                else:
                    break
            match_subcmd(args)
    for subcmd_argv in subcmd_argv_list:
        match_subcmd(subcmd_argv)

    opt.close()
