import os
import pydasm


def main():
    # if len(os.sys.argv) < 2:
    #     print"Usage: %s <file> [-a|-i] [bytes]\n" \
    #     "  file    file to be disassembled (required)\n" \
    #     "  -a      format: ATT (optional)\n" \
    #     "  -i      format: INTEL (optional, default)\n" \
    #     "  bytes   show raw instruction data (optional, default 8)\n" % os.sys.argv[0]
    #     os.sys.exit(1)

    file_name = "/Users/raz.shenkman/Desktop/ImageService.exe.bin"
    fd = file(file_name, 'rb')
    data = fd.read()
    fd.close()

    bytes = 8
    format = pydasm.FORMAT_INTEL

    if len(os.sys.argv) > 2:
        if os.sys.argv[2] == '-a':
            format = pydasm.FORMAT_ATT
        elif os.sys.argv[2] == '-i':
            format = pydasm.FORMAT_INTEL
        else:
            bytes = int(os.sys.argv[2])
        if len(os.sys.argv) > 3:
            bytes = int(os.sys.argv[3])

    offset = 0
    while offset < len(data):
        #
        # get_instruction() has the following parameters:
        #
        # - data: data to be disassembled
        # - disassemble in 32-bit mode: MODE_32
        #
        instruction = pydasm.get_instruction(data[offset:], pydasm.MODE_32)

        str = '%.8x ' % (offset)

        # Illegal opcode or opcode longer than remaining buffer
        if not instruction or instruction.length + offset > len(data):
            if bytes:
                str += '%.2x  ' % ord(data[offset]) + ' ' * (bytes - 1) * 2
            if format == pydasm.FORMAT_INTEL:
                str += 'db 0x%.2x' % ord(data[offset])
            else:
                str += '.byte 0x%.2x' % ord(data[offset])
            print
            str
            offset += 1
            continue

        ilen = instruction.length

        #
        # Print absolute offset and raw data bytes up to 'bytes'
        # (not needed, but looks nice).
        #
        if bytes:
            for i in range(min(bytes, ilen)):
                str += '%.2x' % ord(data[offset + i])
            str += '  '
            for i in range(min(bytes, ilen), bytes * 2 - ilen):
                str += ' '

        #
        # Print the parsed instruction, format using user-supplied
        # format. We could of course format the instruction in some
        # other way by accessing struct INSTRUCTION members directly.
        #
        str += pydasm.get_instruction_string(instruction, format, offset)
        print str

        offset += ilen

    with open('%s.asm' % file_name, 'wb+') as output_file:
        output_file.write(str)


if __name__ == '__main__':
    main()