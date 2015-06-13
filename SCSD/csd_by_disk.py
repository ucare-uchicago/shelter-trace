"""
Given one trace for each disk,
calculate combined CSD for all of them.
"""

import config
import glob
import csv
from math import fabs
from itertools import izip
from os import remove

#Some configuration things
args = config.args

if args.code and args.prealloc:
    prefix = "P"+args.code+str(args.prealloc)+"_"
else:
    prefix=""

traces = glob.glob(prefix+args.number+"_disk*")

if args.number=="11" or args.number=="12":
    delta = 30
else:
    delta = 5 * 60

#Initialize output file

output = prefix+args.number+"_CSD.txt"

with open(output, "w") as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerow([0, 0])

#Generate CSD for each disk
for (index, trace) in enumerate(traces):
    csd = 0
    last = -1
    bucket = delta
    tmp_out = "tmp_"+str(index)+".txt"
    with open(trace, "r") as infile, open(tmp_out, "w") as outfile:
        reader = csv.reader(infile, delimiter=' ')
        writer = csv.writer(outfile, delimiter=' ')
        for row in reader:
            time = float(row[0])
            blk = int(row[2])
            size = int(row[3])
            while time >= bucket:
                writer.writerow([bucket, csd])
                bucket += delta
            if last >= 0:
                csd += fabs(blk - last)
            last = blk + size
        #flush last bucket
        writer.writerow([bucket, csd])


#Add up CSDs for each disk
files = [open("tmp_"+str(i)+".txt", "r") for (i, trc) in enumerate(traces)]
readers = [csv.reader(file, delimiter=' ') for file in files]
csds = []
times = []

#CSDS is list of lists of CSDS from each disk
for reader in readers:
    (time, csd) = zip(*[(row[0], row[1]) for row in reader])
    times.append(list(time))
    csds.append(list(csd))

#Add lists in csds elementwise
def add_lists(l1, l2):
    if len(l1) > len(l2):
        longer = l1
        shorter = l2
    else:
        longer = l2
        shorter = l1
    diff = len(longer) - len(shorter)
    if shorter:
        shorter.extend([shorter[-1]] * diff)
    else:
        shorter = ([0] * diff)
    assert (len(shorter) == len(longer))
    return [float(a) + float(b) for (a, b) in izip(longer, shorter)]

csd_sums = reduce(add_lists, csds, [])

#Now just get (longest) list of times
time_list = max(times, key=lambda l: len(l))

#merge them together and write them out
with open(output, "a") as out:
    writer = csv.writer(out, delimiter=' ')
    assert(len(time_list) == len(csd_sums))
    for (time, csd) in izip(time_list, csd_sums):
        writer.writerow([time, csd])

#cleanup
for file in files:
    file.close()

filenames = ["tmp_"+str(i)+".txt" for (i, trc) in enumerate(traces)]

for file in filenames:
    remove(file)
