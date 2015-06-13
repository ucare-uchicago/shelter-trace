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
parser.add_argument("-t", "---TPC", help="""Some slight differences in handling TPC* traces.""", action="store_true")

args = parser.parse_args()

#time resolution of 5 minutes for long traces, 30 seconds for TPC*
if args.TPC:
    delta = 30
else:
    delta = 5 * 60
bucket = delta

#cutoff sizes for "small I/O", in KB
sizes = [4, 8, 16, 32, 64]

#look up last block #, running request size by disk
per_disk = {}

#look up cumulative small write size (in blocks) by policy
cum_size = {sz : 0 for sz in sizes}
#look up number of small writes by policy
cum_count = {sz : 0 for sz in sizes}


total_size = 0
total_io = 0

PS_out = "PS"+args.number+".txt"
PIO_out = "PIO"+args.number+".txt"

#start w/ zeroes so no gap at beginning of graph
zeroes = [0] * 6

with open(PS_out, "wb") as f:
    f.truncate(0)
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(zeroes)

with open(PIO_out, "wb") as f:
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

def printrow (timestamp, ps_writer, pio_writer):
    ps_row = [timestamp]
    pio_row = [timestamp]
    for size in sizes:
        size_percent = (cum_size[size] / float(total_size)) * 100
        ps_row.append(size_percent)
        count_percent = (cum_count[size] / float(total_io)) * 100
        pio_row.append(count_percent)
    ps_writer.writerow(ps_row)
    pio_writer.writerow(pio_row)
    return

    
for filename in traces:
    print filename
    #offset of this trace from beginning of whole trace
    offset = time_offset
    with open(filename, "rb") as input, open(PS_out,"ab") as psout, open(PIO_out, "ab") as pioout:
        reader = csv.reader(input, delimiter=' ')
        ps_writer = csv.writer(psout, delimiter=' ')
        pio_writer = csv.writer(pioout, delimiter=' ')
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
                per_disk[disk_num] = [0, 0, flag]
                seek_time = -1 #so it doesn't get appended to previous I/O
            if seek_time != 0 or flag != per_disk[disk_num][2]:
                #end of a series of sequential requests
                #increment total_io, this counts as one request
                total_io += 1
                #update cum_size
                req_size = per_disk[disk_num][1]
                if req_size > 0:
                    for size in sizes:
                    #it's a "small request" for this size
                        if req_size <= size * 2:
                            cum_size[size] += req_size
                            cum_count[size] += 1
                #reset current request size for this disk
                if flag == 0:
                    per_disk[disk_num][1] = block_size
                else:
                    per_disk[disk_num][1] = 0
                per_disk[disk_num][2] = flag
            else:
                #it's part of this series of requests
                if int(row[4]) == 0:
                    #it's a write, so we care about it
                    per_disk[disk_num][1] += block_size
            #write it if we're in a new time bucket
            if time >= bucket:
                bucket += delta
                printrow(time, ps_writer, pio_writer)
            #bookkeeping for offsets/block number/etc.
            per_disk[disk_num][0] = block_num + block_size
            time_offset = time
            total_size += block_size
                            
                
            
