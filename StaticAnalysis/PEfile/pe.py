import pefile
import sys

file_name = "/Users/raz.shenkman/Desktop/SharedFiles.exe"
pe = pefile.PE(file_name)

s = pe.NT_HEADERS.OPTIONAL_HEADER.DATA_DIRECTORY[1]

for section in pe.sections:
    if section.Name == b'.text\x00\x00\x00':
        data = pe.get_memory_mapped_image()[section.VirtualAddress:section.VirtualAddress + section.SizeOfRawData]
        with open('%s.bin' % file_name, 'wb+') as file_data:
            file_data.write(data)

