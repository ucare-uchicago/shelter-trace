"""
for each benchmark:
timestamp total_size total_io_count
total_size in KB
"""
import argparse
import csv
from datetime import datetime
import glob
import re

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
parser.add_argument("-r", "--readme", help=""""Use readme to sort traces.
                               Needed when AM/PM not included in
                               trace title""", type=str)
parser.add_argument("-t", "---TPC", help="""Some slight differences in handling TPC* traces.""", action="store_true")

args = parser.parse_args()

#time resolution of 5 minutes for long traces, 30 seconds for TPC*
if args.TPC:
    delta = 30
else:
    delta = 5 * 60
bucket = delta

#look up last block #, running request size by disk
per_disk = {}

total_size = 0
total_io = 0

out = "All"+args.number+".txt"

#start w/ zeroes so no gap at beginning of graph
zeroes = [0] * 3

with open(out, "wb") as f:
    f.truncate(0)
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(zeroes)

if args.TPC:
    traces = glob.glob("*.out.txt")
else:
    traces = glob.glob("*.csv.txt")

#sort traces! How depends on filename format

timestamp_date_dict = {}
def get_date_r (name):
    trace_pattern = re.compile(args.readme+".(.*).trace.csv.csv.txt")
    match = re.search(trace_pattern, name)
    return timestamp_date_dict[match.group(1)]

starts = {}

def get_date (name): 
    return starts[name]

if args.readme:
    timestamp_date_dict = {}
    with open ("../"+args.readme+".ReadMe.txt", "rb") as readme:
        trace_pattern = re.compile("Trace Start: ([0-9]+)(.)* Trace Name: "+args.readme+".([0-9]{4}(-[0-9]{2}){2}.[0-9]{2}-[0-9]{2}).trace")
        for line in readme:
            match = re.search(trace_pattern, line)
            if match:
                stamp = float(match.group(1))/1000.0
                timestamp_date_dict[match.group(3)] = stamp
    traces.sort(key=get_date_r)

else:
    with open("format_string.txt", "rb") as f:
        format_string = f.read().strip()
    for trace in traces:
        starts[trace] = datetime.strptime(trace, format_string)
    traces.sort(key=get_date)

time_offset = 0

def printrow (timestamp, writer):
    row = [timestamp]
    row.append(total_size)
    row.append(total_io)
    writer.writerow(row)
    return

    
for filename in traces:
    print filename
    #offset of this trace from beginning of whole trace
    offset = time_offset
    with open(filename, "rb") as input, open(out,"ab") as output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(output, delimiter=' ')
        for row in reader:
            #time is in milliseconds, we want seconds,
            #so divide by 1000 then add offset
            time = float(row[0])/1000.0 + offset
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            flag = int(row[4])
            if disk_num in per_disk:
                seek_time = block_num - per_disk[disk_num][0]
            else:
                per_disk[disk_num] = [0, flag]
                seek_time = -1 #so it doesn't get appended to previous I/O
            if seek_time != 0 or flag != per_disk[disk_num][1]:
                #end of a series of sequential requests
                #increment total_io, this counts as one request
                total_io += 1
                #update whether current request is read or write
                per_disk[disk_num][1] = flag
            #update size
            total_size += float(block_size)/2
            #write it if we're in a new time bucket
            while time >= bucket:
                bucket += delta
                printrow(time, writer)
            #bookkeeping for offsets/block number/etc.
            per_disk[disk_num][0] = block_num + block_size
            time_offset = time

                            
                
            
