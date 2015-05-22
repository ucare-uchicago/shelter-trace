"""
Reads a shelter simulation trace, and produce a list of "fill counts":
for each shelter, the number of times it fills up.

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

traces = glob.glob(prefix+args.number+"_disk*")

fill_cnt_file = prefix+args.number+"_fill_count.txt"

with open(fill_cnt_file, "w") as f:
    f.truncate(0)

for trace in traces:
    shelter_starts = {}
    with open(trace, "r") as input, open(fill_cnt_file, "a") as output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(output, delimiter=' ')
        for row in reader:
            blk_num = int(row[2])

            if blk_num == get_next_shelter(blk_num):
            #we are writing to the beginning of a shelter!
                if blk_num in shelter_starts:
                    #this isn't our first time writing to it; increment fill count
                    shelter_starts[blk_num] += 1
                else:
                    shelter_starts[blk_num] = 0
        #now write these counts to output before we move on to next trace
        for count in shelter_starts.values():
            writer.writerow([count])
