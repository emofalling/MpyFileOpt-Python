en="ascii"
A=b"\xaa"
S=b"\x00"
E=b"\xff"
T=b"\x00"
F=b"\x01"
N=b"\x02"
BW=b"\x00"
BE=b"\xff"
ver=(1,0)
speed=1024
import machine,os,struct,gc
from mpython import *
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
uri=uart.readinto
ua=uart.any
def rbool():return ur(1)==T
def rint():return sup("<i", ur(4))[0]
def sint(i):uw(sp("<i",i))
def ruint():return sup("<I", ur(4))[0]
def suint(i):uw(sp("<I",i))
def rstr(s=True):o=ur(ruint());return o.decode(en) if s else o
def sstr(s,iss=True):suint(len(s));uw(s.encode(en) if iss else s)
def err(e):uw(E);sstr(e.__class__.__name__+": "+str(e))
uw(A)
while True:
    code=ur(1)
    if code is None:pass

    elif code==b"\x00":
        try:uw(S);suint(ver[0]);suint(ver[1])
        except Exception as e:err(e)
    elif code==b"\x01":
        try:c=os.uname()
        except Exception as e:err(e)
        else:
            uw(S)
            for i in c:sstr(i)
    elif code==b"\x02":
        try:uid=machine.unique_id()
        except Exception as e:err(e)
        else:
            uw(S);sstr(uid,False)
    elif code==b"\x03":
        try:f=machine.freq()
        except Exception as e:err(e)
        else:uw(S);suint(f)
    
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
    
    elif code==b"\x20":
        p=rstr();fs=ruint();bs=ruint()
        try:
            bf=bytearray(bs)
            with open(p,"wb") as f:
                uw(S)
                while fs>0:
                    ib=ur(1)
                    if ib==BW:
                        uri(bf)
                    else:
                        del bf;bs=ruint();bf=ur(bs)
                    try:f.write(bf)
                    except Exception as e:err(e);break
                    else:uw(S)
                    fs-=bs
        except Exception as e:err(e)
    elif code==b"\x21":
        p=rstr();bs=ruint()
        try:
            fs=os.stat(p)[6];bf=bytearray(bs)
            with open(p,"rb") as f:
                uw(S);suint(fs)
                while fs>0:
                    st=ur(1)
                    if st==BW:
                        try:f.readinto(bf)
                        except Exception as e:err(e);break
                        else:uw(S)
                    else:
                        del bf;bs=ruint()
                        try:bf=f.read(bs)
                        except Exception as e:err(e);break
                        else:uw(S)
                    uw(bf)
                    fs-=bs
        except Exception as e:err(e)
    elif code==b"\x22":
        try:os.remove(rstr())
        except Exception as e:err(e)
        else:uw(S)
    elif code==b"\x23":
        try:os.rmdir(rstr())
        except Exception as e:err(e)
        else:uw(S)
    elif code==b"\x24":
        try:os.mkdir(rstr())
        except Exception as e:err(e)
        else:uw(S)
    elif code==b"\x25":
        try:os.rename(rstr(),rstr())
        except Exception as e:err(e)
        else:uw(S)

    elif code==b"\x30":
        try:r=os.stat(rstr())
        except Exception as e:err(e)
        else:
            uw(S)
            for i in r:sint(i)
    elif code==b"\x31":
        try:r=os.statvfs(rstr())
        except Exception as e:err(e)
        else:
            uw(S)
            for i in r:sint(i)
    
    elif code==b"\x40":
        cl=rbool()
        try:
            if cl:gc.collect()
            f=gc.mem_free();a=gc.mem_alloc()
        except Exception as e:err(e)
        else:uw(S);sint(a);sint(f)
    
    elif code==b"\xff":
        try:machine.reset()
        except Exception as e:err(e)
