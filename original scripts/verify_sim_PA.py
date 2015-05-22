"""
Verify that there are no writes smaller than 32 KB.
They should all be sheltered.
"""

import csv
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)

args = parser.parse_args()

trace_file = "PA"+args.number+".txt"

policy = 32

#tails: last block read, per disk
tails = {}
#cum_sizes: cumulative size of current request, per disk
cum_sizes = {}
#flags: read/write flag for current request, per disk
flags = {}
#sheltered: if we have a series of sequential requests switching from read to write, we assume it's sheltered
#we also assume this if it's the first request for that disk, because there would be no place to shelter it
sheltered = {}

with open(trace_file, "rb") as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        time = float(row[0])
        disk_num = row[1]
        block_num = int(row[2])
        block_size = int(row[3])
        flag = int(row[4])
        if disk_num in tails:
            seek_time = block_num - tails[disk_num]
        else:
            tails[disk_num] = 0
            cum_sizes[disk_num] = 0
            flags[disk_num] = flag
            sheltered[disk_num] = True
            seek_time = -1 # so we know it's a new request

        #a switch from reading to writing in a sequential stream is evidence of sheltering
        #a switch from writing to reading is a coincidence, so we treat it as a new request
        if seek_time == 0 and not (flag == 1 and flags[disk_num] == 0):
            cum_sizes[disk_num] += block_size
            tails[disk_num] = block_num + block_size
            if flags[disk_num] == 1 and flag == 0:
                sheltered[disk_num] = True
            flags[disk_num] = flag
        elif cum_sizes[disk_num] <= policy * 2 and flags[disk_num] == 0 and not sheltered[disk_num]:
            print "FAIL: found write that should be sheltered.\n"
            print "size: "+str(cum_sizes[disk_num])+"\n"
            print "timestamp: "+row[0]+"\n"
            sys.exit()
        else:
            cum_sizes[disk_num] = block_size
            tails[disk_num] = block_num + block_size
            flags[disk_num] = flag
            if seek_time > 0:
                sheltered[disk_num] = False

print "Success!\n"
            
            
            

        
