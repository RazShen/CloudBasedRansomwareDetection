import os
import sys

asm_files = os.listdir('.')
headers_list = []
sections_file_path = sys.argv[1]

with open(sections_file_path, 'wb+') as sections_file:
    for f in asm_files:
        try:
            with open(f, 'r') as asm_file:
                data = asm_file.readlines()
            sections = {'.text': 0, '.bss': 0, '.rdata': 0, '.data': 0, '.idata': 0,
                        '.reloc': 0}
            for data_line in data:
                for key in sections.keys():
                    if key in data_line:
                        sections[key] += 1
            print sections
            sections_file.write('%s,' % f)
            for key in sections:
                sections_file.write('%s,' % key)
                sections_file.write('%s,' % str(sections[key]))
            sections_file.write('\n')
        except Exception as e:
            with open('error_files', 'a+') as faults:
                faults.write(f)
