U8="utf-8"
S=b"\x99"
E=b"\x55"
Version=(1,0)
speed=1024
import machine,os,time,struct
sp=struct.pack
sup=struct.unpack

from flashbdev import bdev
try:
    if bdev:
        if isinstance(bdev,list):bdev = bdev[0]
        os.mount(bdev, "/")
except OSError:
    import inisetup;vfs=inisetup.setup()
from machine import UART
uart=UART(1,baudrate=115200,tx=1,rx=3)
uw=uart.write
ur=uart.read
ua=uart.any
def sint(i):uw(sp("<i",i))
def suint(i):uw(sp("<I",i))
def sstr(s):
    suint(len(s));uw(s.encode(U8))
def err(e):
    uw(E);sstr(e.__class__.__name__+": "+str(e))
uw(b"\xaa")
while True:
    if ua():
        code=ur(1)
        if code==b"\x10":
            try:cwd = os.getcwd()
            except Exception as e:err(e)
            else:
                uw(S);sstr(cwd)
