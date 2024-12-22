import main,os
import time
opt = main.MpyFileOpt("COM3", verbose=True)
print("Start to chdir")
opt.chdir("/lib", verbose=True)
print("Start to getcwd")
print(opt.getcwd(verbose=True))
print("Close")
opt.close(verbose=True)