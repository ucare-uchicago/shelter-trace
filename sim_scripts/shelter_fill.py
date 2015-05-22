"""
Reads a shelter simulation trace, and produce the following:
1.
P[code]_[trace number]_fill_count.txt
in the format:
timestamp      cumulative # of times shelters have filled up.
(every 5 minutes)
2.
P[code]_[trace number]_fill_time.txt
a list of times taken for shelters to fill up, in no particular order
i.e. whenever we hit the end of a shelter (or end of the whole trace)
we output (current time - time of most recent write to beginning of shelter)

so for each shelter, we keep track of:
-shelter start
-time of last write to start
"""

import config
import glob
import csv
from simulate import get_next_shelter

args = config.args

#we assume we'll only see writes to beginning of shelter if it's actually sheltered,
#so this must be policy C
assert(args.code == "C")
assert(args.prealloc)

prefix = "P"+args.code+str(args.prealloc)+"_"

delta = 5 * 60
bucket = delta

shelter_starts = {}

#traces = glob.glob(prefix+args.number+"_disk*")

#for now, since we're looking at a one-disk wonder, don't worry about dealing w/
#multiple disks

trace = prefix+args.number+"_disk0.txt"
fill_cnt_file = prefix+args.number+"_fill_count.txt"
fill_time_file = prefix+args.number+"_fill_time.txt"


fill_count = 0

with open(trace, "r") as input, open(fill_cnt_file, "w") as cnt_output, open (fill_time_file, "w") as time_output:
    reader = csv.reader(input, delimiter=' ')
    writer = csv.writer(cnt_output, delimiter=' ')
    for row in reader:
        time = float(row[0])
        blk_num = int(row[2])
        #if we're in a new bucket, write current fill count to fill_cnt_file
        while time >= bucket:
            writer.writerow([bucket, fill_count])
            bucket += delta
        if blk_num == get_next_shelter(blk_num):
            #we are writing to the beginning of a shelter!
            if blk_num in shelter_starts:
                #we've written to it before, so this is a new fill-up
                fill_count += 1
                #write time it took to fill up to fill_time_file
                fill_time = time - shelter_starts[blk_num]
                time_output.write(str(fill_time) + "\n")
            #need to update shelter_starts
            shelter_starts[blk_num] = time

    #now flush fill time for every shelter
    for shelter in shelter_starts:
        fill_time = time - shelter_starts[shelter]
        time_output.write(str(fill_time) + "\n")

    #and flush last bucket
    writer.writerow([bucket, fill_count])
