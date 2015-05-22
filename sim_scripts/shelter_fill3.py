"""
Reads a shelter simulation trace, and produce the following:.
P[code]_[trace number]_fill_count.txt
in the format:
timestamp      cumulative # of times shelters have filled up.
(every 5 minutes)

so for each shelter, we keep track of:
-shelter start
-time of last write to start
"""

import config
import glob
import csv
from simulate import get_next_shelter
from itertools import izip
from os import remove

args = config.args

#we assume we'll only see writes to beginning of shelter if it's actually sheltered,
#so this must be policy C
assert(args.code == "C")
assert(args.prealloc)

prefix = "P"+args.code+str(args.prealloc)+"_"

delta = 5 * 60

traces = glob.glob(prefix+args.number+"_disk*")

fill_cnt_file = prefix+args.number+"_fill_count.txt"

for (index, trace) in enumerate(traces):
    shelter_starts = {}
    fill_count = 0
    bucket = delta
    print trace
    tmp_out = "tmp_fill_"+str(index)+".txt"
    with open(trace, "r") as input, open(tmp_out, "w") as cnt_output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(cnt_output, delimiter=' ')
        for row in reader:
            time = float(row[0])
            blk_num = int(row[2])
            #if we're in a new bucket, write current fill count to output
            while time >= bucket:
                print time
                print bucket
                print fill_count
                writer.writerow([bucket, fill_count])
                bucket += delta
            if blk_num == get_next_shelter(blk_num):
                #we are writing to the beginning of a shelter!
                if blk_num in shelter_starts:
                #we've written to it before, so this is a new fill-up
                    fill_count += 1
            #mark that we've hit this shelter before
                shelter_starts[blk_num] = True

        #now flush final count:
        writer.writerow([bucket, fill_count])

#Add up fill counts for each disk
files = [open("tmp_fill_"+str(i)+".txt", "r") for (i, trc) in enumerate(traces)]
readers = [csv.reader(file, delimiter=' ') for file in files]
fills = []
times = []

#fills is list of lists of fills from each disk
for reader in readers:
    (time, fill) = zip(*[(row[0], row[1]) for row in reader])
    times.append(list(time))
    fills.append(list(fill))

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

fill_sums = reduce(add_lists, fills, [])

#Now just get (longest) list of times
time_list = max(times, key=lambda l: len(l))

#merge them together and write them out
with open(fill_cnt_file, "w") as out:
    writer = csv.writer(out, delimiter=' ')
    assert(len(time_list) == len(fill_sums))
    for (time, csd) in izip(time_list, fill_sums):
        writer.writerow([time, csd])

#cleanup
for file in files:
    file.close()

#filenames = ["tmp_"+str(i)+".txt" for (i, trc) in enumerate(traces)]

#for file in filenames:
 #   remove(file)

