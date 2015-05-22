import argparse
import csv
from math import fabs

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
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


#start w/ zeroes so no gap at beginning of graph
zeroes = [0] * 6

infile = "PA"+args.number+".txt"
outfile = "PA_CSD"+args.number+".txt"

with open(outfile, "wb") as f:
    f.truncate(0)
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(zeroes)

csd = 0
    
with open(infile, "rb") as input, open(outfile,"ab") as out:
    reader = csv.reader(input, delimiter=' ')
    writer = csv.writer(out, delimiter=' ')
    for row in reader:
        time = float(row[0])
        disk_num = row[1]
        block_num = int(row[2])
        block_size = int(row[3])
        if disk_num in per_disk:
            seek_time = fabs(block_num - per_disk[disk_num])
        else:
            per_disk[disk_num] = 0
            seek_time = 0
        csd += seek_time
        #write it if we're in a new time bucket
        if time >= bucket:
            bucket += delta
            writer.writerow([time, csd])
        #bookkeeping for offsets/last block
        per_disk[disk_num] = block_num + block_size
                            
                
            
