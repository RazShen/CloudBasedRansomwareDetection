import os
import re

def get_num_of_hashed_files(folder_path):
    l = os.listdir(folder_path)
    c = 0
    for item in l:
        result = re.search(r"[0-9a-f]{10}",item)
        if (result):
            print item
            c += 1
    print "There are " + str(c) + " items with hash-based file name"
    return c

get_num_of_hashed_files('/Users/raz.shenkman/Desktop/folder_files')