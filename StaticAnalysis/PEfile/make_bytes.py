import os
from random import *
import boto


def create_bytes(filename):

    fin = open(filename, "rb")

    fullout = filename + ".bytes"
    fout = open(fullout, "w")

    fin.seek(4096)
    count = 4096 + randint(0, 0xFFFFFF)

    while True:
        b = fin.read(16)
        if not b:
            # eof
            break
        fout.write("%08x" % count)
        for byt in b:
            fout.write(" %02x" % ord(byt))

        fout.write("\n")

        count += 16

    fin.close()
    fout.close()


def upload_to_s3(matches):
    directories = os.listdir('/home/user/zips/')
    s3_connection = boto.connect_s3()
    for dir in directories:
        try:
            b = s3_connection.create_bucket('biu-malwares/%s' % dir)
        except S3CreateError as e:
            print e.message()
        bucket = s3_connection.get_bucket('biu-malwares/%s' % dir)
        for match in matches:
            if dir in match:
                key = boto.s3.key.Key(bucket, match)
                with open(match) as f:
                    key.send_file(f)


def main():
    matches = []
    directories = os.listdir('/home/user/zips/')
    if 'scripts' in directories:
        del directories[directories.index('scripts')]
    for dir in directories:
        # listing all files in directory
        for root, dirnames, filenames in os.walk('/home/user/zips/%s' % dir):
            for filename in filenames:
                matches.append(os.path.join(root, filename))

    for match in matches:
        create_bytes(match)


if __name__ == '__main__':
    main()
