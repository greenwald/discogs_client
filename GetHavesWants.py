#!/usr/bin/env python3

import argparse
import csv
import discogs_client
import os.path
import time
import sys

parser = argparse.ArgumentParser(description='grab wants and haves from discogs database')
mutex_group = parser.add_mutually_exclusive_group(required=True)
mutex_group.add_argument('-a', '--append', action='store_true', default=False)
mutex_group.add_argument('-o', '--overwrite', action='store_true', default=False)
parser.add_argument('user_token')
parser.add_argument('filename')

args = parser.parse_args()

d = discogs_client.Client("GetHavesWants/0.1", user_token=args.user_token)

count = 0 if args.overwrite or not os.path.isfile(args.filename) else len(open(args.filename).readlines(  ))
outputfile = open(args.filename, mode='w+' if args.overwrite else 'a+')
outputwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

def starting_with(arr, start_index):
     # use xrange instead of range in python 2
     for i in range(start_index, len(arr)):
        yield arr[i]
     for i in range(start_index):
        yield arr[i]
        
for disc in starting_with(d.identity().collection_folders[0].releases, count):
    info = None
    while info is None:
        try:
            R = disc.release
            info = [R.id, R.community.have, R.community.want]
        except:
            sys.stdout.write('waiting 30 seconds ')
            sys.stdout.flush()
            print("waiting 30 seconds", end=" ")
            for i in range(30):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write('\n')
            sys.stdout.flush()
            pass
    outputwriter.writerow(info)
    outputfile.flush()
    print(info)

