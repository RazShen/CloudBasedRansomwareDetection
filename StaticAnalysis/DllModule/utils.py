
def get_dll_list_from_hexrays_desassembler(filename, min=4):
    with open(filename, "rb") as asm_file:           # Python 2.x
        dll_list = []
        for line in asm_file.readlines():
            if line.__contains__("db") and line.__contains__(".DLL"):
                dll_index = line.index(".DLL")
                line = line[:dll_index]
                apostrophe_index = line.rfind('\'')
                if apostrophe_index == -1:
                    continue
                dll_list.append(line[apostrophe_index + 1:])  
    return dll_list