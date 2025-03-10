import sys
sys.path.append(".")
import unittest
import mpyfopt
import os
import traceback
import hashlib # Hash file

PORT = "COM3"
os.chdir(os.path.dirname(__file__))

def _callback_progress(total, cur):
    print("[Callback::Info] Progress:", f"{cur}/{total}", "bytes")

error_count = 0
opt = None
s256 = -1

class TestMpyFileOpt(unittest.TestCase):
    def setUp(self):
        print()
    def test_0_getinfo(self):
        global error_count, opt
        print("MpyFileOpt test start ...")
        print("[Info] MpyFileOpt version:", mpyfopt.__version__)
        print("[Info] MpyFileOpt author:", mpyfopt.__author__)
    def test_1_connect(self):
        global error_count, opt
        print("[Info] Connect to", PORT, "with verbose ...")
        try:
            opt = mpyfopt.MpyFileOpt(PORT, verbose=True)
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] Connection failed. [exit]")
            exit()
        print("[Info] Connected.")
    def test_2_get_source_version(self):
        global error_count, opt
        print("[Info] Testing get_source_version...")
        try:
            print("[Lout] Version:", opt.get_source_version(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] get_version failed.")
    def test_3_uname(self):
        global error_count, opt
        print("[Info] Testing uname...")
        try:
            print("[Lout] Uname:", opt.uname(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] uname failed.")
    def test_4_get_uid(self):
        global error_count, opt
        print("[Info] Testing get_uid...")
        try:
            print("[Lout] UID:", opt.get_uid(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] get_uid failed.")
    def test_5_get_freq(self):
        global error_count, opt
        print("[Info] Testing get_freq...")
        try:
            print("[Lout] Freq:", opt.get_freq(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] get_freq failed.")
    def test_6_getcwd(self):
        global error_count, opt
        print("[Info] Testing getcwd...")
        try:
            print("[Lout] CWD:", opt.getcwd(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] getcwd failed.")
    def test_7_chdir(self):
        global error_count, opt
        print("[Info] Testing chdir...")
        try:
            opt.chdir("lib", verbose=True)
            print("[Info] Chdir OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] chdir failed.")
    def test_8_listdir(self):
        global error_count, opt
        print("[Info] Testing listdir...")
        try:
            print("[Lout] Listdir:", opt.listdir(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] listdir failed.")
    def test_9_ilistdir(self):
        global error_count, opt
        print("[Info] Testing ilistdir...")
        try:
            print("[Lout] ilistdir:", opt.ilistdir(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] ilistdir failed.")
    def test_A_reset_dir(self):
        global error_count, opt
        print("[Info] Reset curren work dir...")
        try:
            opt.chdir("/", verbose=True)
            print("[Info] Reset OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] reset failed.")
    def test_B_upload(self):
        global error_count, opt, s256
        print("[Info] Testing upload...")
        with open("test.txt", "rb") as f:
            s256 = hashlib.sha256(f.read()).hexdigest()
        print("[Info] test.txt SHA256:", s256)
        try:
            with open("test.txt", "rb") as f:
                opt.upload("test.txt", f, os.path.getsize("test.txt"), _callback_progress, verbose=True)
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] upload failed.")
    def test_C_download(self):
        global error_count, opt, s256
        print("[Info] Testing download...")
        try:
            with open("rtest.txt", "wb") as f:
                opt.download("test.txt", f, _callback_progress, verbose=True)
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] download failed.")
        with open("rtest.txt", "rb") as f:
            s256r = hashlib.sha256(f.read()).hexdigest()
        print("[Info] rtest.txt SHA256:", s256r)
        if s256 == s256r:
            print("[Info] SHA256 match.")
            print("[Info] Download OK.")
        else:
            print("[Err!] SHA256 mismatch. Download is not successful.")
            error_count += 1
    def test_D_remove(self):
        global error_count, opt
        print("[Info] Testing remove...")
        try:
            opt.remove("test.txt", verbose=True)
            print("[Info] Remove OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] remove failed.")
    def test_E_mkdir(self):
        global error_count, opt
        print("[Info] Testing mkdir...")
        try:
            opt.mkdir("test", verbose=True)
            print("[Info] mkdir OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] mkdir failed.")
    def test_F_rename(self):
        global error_count, opt
        print("[Info] Testing rename...")
        try:
            opt.rename("test", "test2", verbose=True)
            print("[Info] rename OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] rename failed.")
    def test_G_rmdir(self):
        global error_count, opt
        print("[Info] Testing rmdir...")
        try:
            opt.rmdir("test2", verbose=True)
            print("[Info] rmdir OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] rmdir failed.")
    def test_H_stat(self):
        global error_count, opt
        print("[Info] Testing stat...")
        try:
            print("[Lout] stat:", opt.stat("lib", verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] stat failed.")
    def test_I_statvfs(self):
        global error_count, opt
        print("[Info] Testing statvfs...")
        try:
            print("[Lout] statvfs:", opt.statvfs("/", verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] statvfs failed.")
    def test_J_get_gc_info(self):
        global error_count, opt
        print("[Info] Testing get_gc_info...")
        try:
            print("[Lout] gc_info:", opt.get_gc_info(verbose=True))
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] get_gc_info failed.")
    def test_K_close(self):
        global error_count, opt
        print("[Info] Testing close...")
        try:
            opt.close(verbose=True)
            print("[Info] Close OK.")
        except:
            print(traceback.format_exc())
            error_count += 1
            print("[Err!] close failed.")
        print("[Info] Test finished. Error count:", error_count)
    def tearDown(self):
        print(f"------ error_count: {error_count} ------")

if __name__ == "__main__":
    unittest.main()