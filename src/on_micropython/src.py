en="ascii"
A=b"\xaa"
S=b"\x99"
E=b"\x55"
ver=(1,0)
speed=1024
import machine,os,time,struct
#from mpython import *
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
uart=UART(1,baudrate=115200,tx=1,rx=3,timeout=10000)
uw=uart.write
ur=uart.read
ua=uart.any
def rint():return sup("<i", ur(4))[0]
def sint(i):uw(sp("<i",i))
def ruint():return sup("<I", ur(4))[0]
def suint(i):uw(sp("<I",i))
def rstr(s=True):o=ur(ruint());return o.decode(en) if s else o
def sstr(s):suint(len(s));uw(s.encode(en))
def err(e):uw(E);sstr(e.__class__.__name__+": "+str(e))
uw(A)
while True:
    code=ur(1)
    if code==b"\x00":
        try:uw(S);suint(ver[0]);suint(ver[1])
        except Exception as e:err(e)
    elif code==b"\x01":
        try:c=os.uname()
        except Exception as e:err(e)
        else:
            uw(S)
            for i in c:sstr(i)
    

    elif code==b"\x10":
        try:cwd = os.getcwd()
        except Exception as e:err(e)
        else:uw(S);sstr(cwd)
    elif code==b"\x11":
        try:os.chdir(rstr())
        except Exception as e:err(e)
        else:uw(S)
    elif code==b"\x12":
        try:l=os.listdir(rstr())
        except Exception as e:err(e)
        else:
            uw(S);suint(len(l))
            for i in l:sstr(i)
    elif code==b"\x13":
        try:r=list(os.ilistdir(rstr()))
        except Exception as e:err(e)
        else:
            uw(S);suint(len(r))
            for a in r:sstr(a[0]);suint(a[1]);suint(a[2])
    
    elif code==b"\x30":
        try:r=os.stat(rstr())
        except Exception as e:err(e)
        else:
            uw(S)
            for i in r:suint(i)
    elif code==b"\x31":
        try:r=os.statvfs(rstr())
        except Exception as e:err(e)
        else:
            uw(S)
            for i in r:sint(i)
    
    elif code==b"\xff":
        try:machine.reset()
        except Exception as e:err(e)
