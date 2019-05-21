import pefile

def text_section_bytes(filename):
    pe = pefile.PE(filename)
    text = pe.sections[0].get_data()
    for byte in text:
        yield byte.encode('hex')

def create_bytes_file(filename):
    name = filename[:filename.find('.exe')]
    new_file = open(name+'.bytes', 'w')
    counter = 0
    pe = pefile.PE(filename)
    new_file.write("00000000 ")
    byte_index = pe.sections[0].VirtualAddress
    byte_index = hex(byte_index)
    for byte in text_section_bytes(filename):
        if counter == 16:
            new_file.write("\n00000000 ")
            counter = 0
        new_file.write(byte +" ")
        counter += 1
    new_file.close()

create_bytes_file("/Users/raz.shenkman/Desktop/SharedFiles.exe")
