# -*- coding: utf-8 -*-
# python

import os
import random
import sys
import hashlib
import getopt

MAX_BYTES = 128
WIKI_FILE = "wiki.txt"


def shred(f, count=5):
    descriptor = None
    try:
        file_length = os.path.getsize(f)
        for iterator in range(count):
            dig = hashlib.md5(file(f).read()).hexdigest()
            print >> sys.stderr, "pass:", ++iterator,
            print >> sys.stderr, "origin : ", dig

            char_buffer = [chr(current) for current in range(MAX_BYTES)]
            random.shuffle(char_buffer)
            char_buffer = "".join(char_buffer)
            bytes_length = file_length
            descriptor = file(f, mode="wb")

            write_safely(bytes_length, char_buffer, descriptor)
            dig = hashlib.md5(file(f).read()).hexdigest()
            print >> sys.stderr, "modified :", dig

            # 1970-1-1 00:00:00
            os.utime(f, (0, 0))
            descriptor.close()
    except:

        if descriptor is not None:
            descriptor.close()


def write_safely(bytes_length, char_bytes, descriptor):
    while bytes_length:
        byte_overhead = min(bytes_length, MAX_BYTES)

        descriptor.write(char_bytes[:byte_overhead])
        bytes_length -= byte_overhead
        descriptor.flush()



def get_wiki_file_internal():
    return os.path.join(os.getcwd(), WIKI_FILE)


if __name__ == "__main__":

    optlist = None
    args = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'x', ['file='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print >> sys.stderr, 'option not recognized'
        sys.exit(2)

    if (optlist is None or not len(optlist)) or (optlist[0][1] is None or not os.path.exists(optlist[0][1])):
        print >> sys.stderr, "Please, check input arguments - file not exist"
        exit(2)

    stub_file = optlist[0][1]
    file(stub_file, mode="wb").write(file(get_wiki_file_internal()).read() * 5)
    shred(stub_file)

