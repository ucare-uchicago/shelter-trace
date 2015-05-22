"""
for each benchmark:
timestamp 4KB_cum_size 8KB_cum_size 16KB_cum_size 32KB_cum_size 64KB_cum_size

all sizes are in KB
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
cum_size = {sz : 0 for sz in sizes}

outfile = "T"+args.number
if type_filter == 0:
    outfile += "-write"
elif type_filter == 1:
    outfile += "-read"

outfile += ".txt"

with open(outfile, "wb") as f:
    f.truncate(0)

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
            time = float(row[0])/1000.0 + offset
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            if disk_num in per_disk:
                seek_time = block_num - per_disk[disk_num][0]
            else:
                per_disk[disk_num] = [0, 0, row[4]]
                seek_time = -1
            if seek_time != 0 or per_disk[disk_num][2] != row[4]:
                #end of a series of sequential requests, update cum_size accordingly
                req_size = per_disk[disk_num][1]
                flag = row[4]
                if req_size > 0:
                    for size in sizes:
                    #it's a "small request" for this size
                        if req_size <= size * 2:
                            cum_size[size] += req_size
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
                    outrow.append(float(cum_size[size]) / (2.0 * 1024.0 * 1024.0))
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
            outrow.append(float(cum_size[size]) / (2.0 * 1024.0 * 1024.0))
        writer.writerow(outrow)

                            
                
            
