import string
import hexdump

def strings_from_exe(path_to_exe, min=4):
    # with open(filename, errors="ignore") as f:  # Python 3.x
    with open(path_to_exe, "rb") as f:  # Python 2.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result


# for my_string in strings_from_exe("binary.dat"):
#     print my_string