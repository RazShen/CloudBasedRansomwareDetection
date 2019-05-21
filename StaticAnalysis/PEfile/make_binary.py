import os


def line_to_bytes(line):
    return line[8:].replace(" ", "").rstrip().decode('hex')


directory = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(directory):

    if filename.endswith(".bytes"):
        print(filename)
        fullname = os.path.join(directory, filename)
        fin = open(fullname, "r")
        fout = open(fullname+".bin", "wb")

        for line in fin:
            fout.write(line_to_bytes(line))

        fin.close()
        fout.close()
