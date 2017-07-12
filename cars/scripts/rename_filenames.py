import argparse
import hashlib
import os
import re

from os import walk

def rename(file_dir):
    print("Directory: {}".format(file_dir))

    file_list = []

    for (dirpath, dirnames, filenames) in walk(file_dir):
        file_list.extend(filenames)
        break

    for file_name in file_list:
        name_prefix = re.sub(r'.jpg$', '', file_name)
        name_prefix = name_prefix.replace('(', '')
        name_prefix = name_prefix.replace(')', '')
        hash_name = hashlib.sha1(name_prefix).hexdigest()
        os.rename(file_dir + '/' + file_name, file_dir + '/' + hash_name + '.jpg')
        print("{}.jpg <- {}".format(hash_name, file_name))

parser = argparse.ArgumentParser()
parser.add_argument('--file_dir', type=str, default='./data',
                  help='Directory for renaming files')
flags, unparsed = parser.parse_known_args()

rename(flags.file_dir)
