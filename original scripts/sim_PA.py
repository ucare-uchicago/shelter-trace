"""
Simulate policy 1:
A small (<= 32 KB) write is appended to the end of the write before.
We ignore persistence (sheltered writes may be overwritten.)
"""
import sort_traces
import csv
import subprocess

#cutoff size in KB
policy_size = 32
eps = 0.0000005

#technically this gets the block AFTER the last one read,
#i.e. what we'd expect to see if next request is sequential
def get_last (disk_num):
    rows = requests[disk_num]
    if rows:
        last_row = rows[-1]
        last_blk = int(last_row[2]) + int(last_row[3])
    else:
        #we haven't seen any requests for this disk yet,
        #so we should definitely count this as a new request
        last_blk = -1
    return last_blk

#modify requests in request[disk_num] so they're sheltered
def shelter_writes (disk_num):
    tail = tails[disk_num]
    #if tail is negative, there's nothing to shelter behind,
    #because this is the first request for this disk
    #so don't change it
    if tail >= 0:
        for row in requests[disk_num]:
            row[2] = tail
            tail += int(row[3])

(num, traces) = sort_traces.get_traces ()

#tails: last block accessed per disk (ignoring current request)
tails = {}
#sizes: size of current request, per disk
sizes = {}
#requests: list of all rows in current request, per disk
requests = {}
#flags: r/w flag for current request, per disk
flags = {}

#initialize time_offset
time_offset = 0

#initialize output
outfile = "out.txt"
with open(outfile, "wb") as f:
    f.truncate(0)

for filename in traces:
    print filename
    #offset for this file is last timestamp for previous file
    offset = time_offset
    
    with open(filename, "rb") as input, open(outfile, "ab") as output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(output, delimiter=' ')
        for row in reader:
            #time in seconds.
            #time is relative to whole trace
            row[0] = round((float(row[0])/1000.0 + offset), 7)
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            flag = int(row[4])

            #avoid identical timestamps because it breaks sorting
            while row[0] - time_offset < eps:
                row[0] += eps
                
            if disk_num not in tails:
                #we haven't seen this disk before, so initialize it
                tails[disk_num] = 0
                sizes[disk_num] = 0
                requests[disk_num] = []
                flags[disk_num] = flag
            #is this a new request?
            last_blk = get_last(disk_num)
            if last_blk == block_num and flags[disk_num] == flag:
                #this is a continuation of the current request
                requests[disk_num].append(row)
                sizes[disk_num] += block_size
            else:
                #this is the beginning of a new request
                #first, deal with old request.
                #if lst_blk is -1, just-finished request is the first for this disk
                if flags[disk_num] == 0 and sizes[disk_num] <= policy_size * 2:
                    #this request should be sheltered
                    shelter_writes(disk_num)
                #Now that requests have been modified if needed,
                #we can write them to outfile
                for req in requests[disk_num]:
                    writer.writerow(req)
                #update tail
                tails[disk_num] = get_last(disk_num)
                #reset sizes, flags & requests dicts to only reflect
                #current row
                requests[disk_num] = [row]
                sizes[disk_num] = block_size
                flags[disk_num] = flag
            time_offset = row[0]
                
#Now flush any remaining requests for each disk to outfile
with open(outfile, "ab") as output:
    writer = csv.writer(output, delimiter=' ')
    for disk_num in tails:
        if flags[disk_num] == 0 and sizes[disk_num] <= policy_size * 2:
            shelter_writes(disk_num)
        for req in requests[disk_num]:
            writer.writerow(req)

#Our sheltering simulation may reorder requests, so we sort by timestamp
final_out = "PA"+num+".txt"
with open(final_out, "wb") as f:
    subprocess.check_call(["sort", "-k1", "-n", outfile], stdout=f)

subprocess.check_call(["rm", outfile])

