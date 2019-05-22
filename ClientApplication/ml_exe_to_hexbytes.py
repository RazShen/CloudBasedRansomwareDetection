import hexdump
import time

def get_hexdump_output(exe_file_path):
    time.sleep(1)
    exe_file = open(exe_file_path, "rb")
    exe_file_bytes = hexdump.dump(exe_file.read())
    ans = ""
    splitted = exe_file_bytes.split()
    i = 0
    while i < len(splitted) - 16:
        ans += ' '.join(splitted[i:i+16]) + "\n"
        i+=16
    exe_file.close()
    with open('bytes_from_exe.bytes', "w") as exe_hexdump:
        exe_hexdump.write(ans)
    return 'bytes_from_exe.bytes'