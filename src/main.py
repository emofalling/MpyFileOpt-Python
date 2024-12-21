import sys
import time
import serial
import struct

micropython_code_file = "src/on_micropython/main.py"

TER_INTP = b"\x03" #Terminal_Interrupt
TER_NEWL = b"\x0d" #Terminal_NewLine
ANS = b"\xaa"
ERR = b"\x55"
SUC = b"\x99"

GWD = b"\x10"

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
                ):
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
        self.getcwd()
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
        print("Reset device...")
        self._dev_reset()
        print("Wait device in REPL...")
        self._dev_wait_in_repl()
        print("Send source code...")
        self._dev_send_src()
        print("Wait answer...")
        self._com_wait_ans()
        print("Done.")

    def _com_read_int(self):
        ret = self.ser.read(4)
        return struct.unpack("<i", ret)[0]
    def _com_read_uint(self):
        ret = self.ser.read(4)
        return struct.unpack("<I", ret)[0]
    def _com_read_string(self):
        len = self._com_read_uint()
        return self.ser.read(len)
    
    def getcwd(self, str: bool = True):
        self.ser.write(GWD)
        ret = self.ser.read(1)
        if ret == SUC:
            self.wd = self._com_read_string()
            return self.wd if str else self.wd.decode("utf-8")
        elif ret == ERR:
            err = self._com_read_string().decode("utf-8")
            raise MpyFileOptError("On getcwd(): In Micropython Device: \n    {}".format(err))

    def __del__(self):
        self.ser.close()

        
if __name__ == '__main__':
    pass