#!/usr/bin/env python
"""
consolidate each sequential series of requests into a single request
for example, the following trace:
Time Disk-number Block-number Block-count flags
1    0           16           4           0    
2    0           20           4           0    
would become:
Time Disk-number Block-number Block-count flags
1    0           16           8           0
because the two requests are sequential, and would be treated as a single request for sheltering purposes  
"""
import os
import csv
import sys
import glob

#lets us import shelter-trace/common/settings.py
sys.path.append("../common/")
import settings

for idx, trace in enumerate(settings.traces, 1):
    print idx
    #traces_path is where our input files ({tracenum}_disk{disknum}.txt) live,
    #and where our output files ({tracenum_disk{disknum}_consolidate.txt) live
    traces_path = "{}/{}/".format(settings.preprocessed_traces_path, trace)
    input_glob = "{}/{}_disk*[0-9].txt".format(traces_path, str(idx))
    input_traces = glob.glob(input_glob)
    for trace in input_traces:
        output_trace = os.path.splitext(trace)[0] + "_consolidated.txt"
        with open(trace, "r") as input, open(output_trace, "w") as output:
            reader = csv.reader(input, delimiter=' ')
            writer = csv.writer(output, delimiter=' ')
            #we initialize last_blk here so we can calculate seek time for first request,
            #and seek time won't be zero, 
            #so we can treat it as first in a series of sequential requests
            next_blk = -1 #where the disk head points at the end of the request.
                          #e.g. if a request starts at block 16 and is 4 blocks long,
                          #next_blk = 20
            flag = -1     #0 for reads, 1 for writes (or vice versa?)
            for row in reader:
                #calculate seek time
                seek_time = int(row[2]) - next_blk
                if seek_time == 0 and flag == row[4]:
                    #add this to the current series of sequential requests
                    block_size += int(row[3])
                    next_blk += int(row[3])
                else:
                    #first write the old request, unless this is the first request
                    if flag != -1:
                        writer.writerow([time, disk_num, str(block_num), str(block_size), flag, elapsed, swap])
                    #now set up the new request
                    time = row[0]
                    disk_num = row[1] #don't really need to update per row, all requests in a file are on same disk
                    block_num = int(row[2])
                    block_size = int(row[3])
                    flag = row[4]
                    elapsed = row[5]
                    swap = row[6]
                    next_blk = block_num + block_size
            #write last request
            writer.writerow([time, disk_num, str(block_num), str(block_size), flag, elapsed, swap])
            
