import time
import os, sys
PORT = "COM3"
iswin = sys.platform in ("win32", "win64")
if iswin:
    pss = "powershell "
else:
    pss = ""
def testtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Used time: {time.perf_counter() - start_time:.02f} s")
        return result
    return wrapper

@testtime
def ampy():
    # ampy
    cmd = f"{pss}ampy -p {PORT} put test.txt"
    print(f"ampy test start, command: {cmd}")
    os.system(cmd)
@testtime
def mpyf():
    cmd = f"{pss}\"../mpyfopt/mpyfopt.py\" -p {PORT} write test.txt test.txt"
    print(f"mpyfopt test start, command: {cmd}")
    # mpyfopt
    os.system(cmd)

def main():
    os.chdir(os.path.dirname(__file__))
    print("test.txt size:", os.path.getsize("test.txt"))
    ampy()
    time.sleep(1)
    mpyf()

if __name__ == "__main__":
    main()