import os
import hexdump
import io
import pydasm

'''
get a hexdump of all the files in the folder
'''
def get_hexdump_output(exe_file_path):
    exe_file = open(exe_file_path, "rb")
    exe_file_bytes = hexdump.dump(exe_file.read())
    ans = ""
    splitted = exe_file_bytes.split()
    i = 0
    while i < len(splitted) - 16:
        ans += ' '.join(splitted[i:i+16]) + "\n"
        i+=16
    exe_file.close()
    with open(exe_file_path+"exe_hexdump.bytes", "w") as exe_hexdump:
        exe_hexdump.write(ans)

for file_x in os.listdir(os.curdir):
    if (len(file_x) > 7):
        get_hexdump_output(file_x)