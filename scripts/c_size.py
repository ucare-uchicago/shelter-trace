"""
for each benchmark:
timestamp 4KB_iop_count 8KB_iop_count 16KB_iop_count 32KB_iop_count 64KB_iop_count

all sizes are in KB
"""
import argparse
import csv
from datetime import datetime
import glob
import re

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
parser.add_argument("-f", "--filter", help="filter only read/write events", choices=['write', 'read'])

args = parser.parse_args()

type_filter = -1
if args.filter == "write":
    type_filter = 0
elif args.filter == "read":
    type_filter = 1

#time resolution of 5 minutes
delta = 5 * 60
bucket = delta

#cutoff sizes for "small I/O", in KB
sizes = [4, 8, 16, 32, 64]

#look up last block #, running request size by disk
per_disk = {}

#look up cumulative small I/O size (in blocks) by "small I/O" cutoff
iop_count = {sz : 0 for sz in sizes}

outfile = "T"+args.number
if type_filter == 0:
    outfile += "-write"
elif type_filter == 1:
    outfile += "-read"

outfile += ".txt"

with open(outfile, "wb") as f:
    f.truncate(0)

traces = glob.glob("*merged.txt")
time_offset = 0

for filename in traces:
    print filename
    #offset of this trace from beginning of whole trace
    offset = time_offset
    with open(filename, "rb") as input, open(outfile,"ab") as output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(output, delimiter=' ')
        for row in reader:
            #filter by read or write if needed
            if type_filter != -1 and type_filter != int(row[4]):
                continue
            #time is in milliseconds, we want seconds,
            #so divide by 1000 then add offset
            #time = float(row[0])/1000.0 + offset
            time = float(row[0]) + offset
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            if disk_num in per_disk:
                seek_time = block_num - per_disk[disk_num][0]
            else:
                per_disk[disk_num] = [0, 0, row[4]]
                seek_time = -1
            if seek_time != 0 or per_disk[disk_num][2] != row[4]:
                #end of a series of sequential requests, update iop_count accordingly
                req_size = per_disk[disk_num][1]
                flag = row[4]
                if req_size > 0:
                    for size in sizes:
                    #it's a "small request" for this size
                        if req_size <= size * 2:
                            iop_count[size] += 1
                #reset current request size & flag for this disk
                per_disk[disk_num][1] = block_size
                per_disk[disk_num][2] = row[4]
            else:
                #it's part of this series of requests, so just add to it
                per_disk[disk_num][1] += block_size
            #write it if we're in a new time bucket
            while time >= bucket:
                bucket += delta
                outrow = [time]
                for size in sizes:
                    #print in GB
                    outrow.append(iop_count[size])
                writer.writerow(outrow)
            #bookkeeping for offsets/last block number
            per_disk[disk_num][0] = block_num + block_size
            time_offset = time

#flush last bucket
with open(outfile, "ab") as output:
        writer = csv.writer(output, delimiter=' ')    
        outrow = [time]
        for size in sizes:
            #print in GB
            outrow.append(iop_count[size])
        writer.writerow(outrow)
