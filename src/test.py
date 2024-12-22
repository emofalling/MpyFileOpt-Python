import main,os
import time
obj = main.MpyFileOpt("COM3", verbose=True)
print("Start to getcwd")
print(obj.getcwd(verbose=True))
print("Start to chdir")