import pydasm
import sys
import string
import io
import re
import os
import hexdump
"""
In this file we have all the methods that extract the information from the executable 
"""

# parse executable hexdump to a list of it's recognized opcodes
def get_opcodes_from_hexa_bytes(path_to_bytes):
    buffer = open(path_to_bytes, "r")
    known_op_codes = get_op_codes()
    buffer = buffer.read()
    offset = 0
    opcodes_unfiltered = []
    while offset < len(buffer) and offset < 30000:
        i = pydasm.get_instruction(buffer[offset:], pydasm.MODE_32)
        try:
            full_command = re.split(" |,", pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, 0))
            if not full_command:
                continue
            first_command = str(full_command[0]).lower()
            if len(full_command) >= 2 and first_command in known_op_codes:
                opcodes_unfiltered.append(first_command)
            if not i:
                break     
            offset += i.length
        except:
            if not i:
                break     
            offset += i.length    
    return opcodes_unfiltered


# get all the known opcodes as a list
def get_op_codes(opcodes_path="model_data/opcodes"):
    opcodes_file = open(opcodes_path, "r")
    opcodes_file = opcodes_file.readlines()
    opcodes = set()
    for opcode in opcodes_file:
        opcodes.add(opcode.lower().strip("\n"))
    return opcodes

# get the hexa bytes of all the files in the folder in a dictionary form
def get_dict_filename_op_codes(file_folder_path, opcodes_path="model_data/opcodes"):
    file_names = os.listdir(file_folder_path)
    file_names = [file for file in file_names if '.bytes' in file]
    file_op_codes_dict = {}
    for file_name in file_names:
        file_op_codes_dict[file_name[:-6]] = get_opcodes_from_hexa_bytes(file_folder_path + "/" + file_name)
    return file_op_codes_dict

# get hexdump of an exe
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
    with open("exe_hexdump", "w") as exe_hexdump:
        exe_hexdump.write(ans)

    