"""
for each benchmark:
total_read_size total_read_request_count
total_write_size total_write_request_count
(just once for whole trace, not at five-minute intervals)
total_size in KB
"""
#FIXME: use num_disk(disknum).txt format

import csv
import glob
import swap_config

args = config.args


class CurrentReq:
    """Keep track of information about current sequential series of writes."""
    def __init__(self, request):
        #total size of current series of requests
        self.size = request[3]
        #the requests themselves
        self.requests = [request]
        #are these reads or writes?
        self.flag = request[4]
        return
    #the next sequential block in this series
    def get_next_blk(self):
        #we just look at last block; after shifting, this series may no longer be sequential
        return self.requests[-1][2] + self.requests[-1][3]
    def is_sequential(self, req):
        #the next request is sequential IF we have some requests already, 
        #AND its starting block comes after the tail of these requests, AND it's the same
        #type of I/O (i.e. read or write)
        return (self.requests and self.get_next_blk() == req[2] and self.flag == req[4])
    def add_req(self, request):
        assert(self.is_sequential(request))
        self.size += request[3]
        self.requests.append(request)
        return
    def should_shelter(self):
        return (self.size <= policy_size * 2 and self.flag == 0)

#look up last block #, running request size by disk
per_disk = {}

total_read_size = 0
total_read_io = 0
total_write_size = 0
total_write_io = 0

out = "totals"+args.number+".txt"

traces = glob.glob(args.number+"_disk*")

for filename in traces:
    print filename

    current_reqs = None

    #offset of this trace from beginning of whole trace
    with open(filename, "r") as input:
        reader = csv.reader(input, delimiter=' ')
        for row in reader:
            #time is in milliseconds, we want seconds,
            #so divide by 1000 then add offset
            time = float(row[0])/1000.0 + offset
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            flag = int(row[4])

            row[2] = block_num
            row[3] = block_size
            row[4] = flag

            if not current_reqs:
                current_reqs = CurrentReq(row)
                continue
            else:
                if current_reqs.is_sequential(row):
                    current_reqs.add_req(row)
                else:
                    if flag == 0:
                        total_write_io += 1
                        total_write_size += current_reqs.size
                    else:
                        total_read_io += 1
                        total_read_size += current_reqs.size
                    current_reqs = CurrentReq(row)

reads_row  = [total_read_size, total_read_io]
writes_row = [total_write_size, total_write_io]

with open(out, "w") as output:
    writer = csv.writer(out, delimiter=' ')
    writer.writerow(reads_row)
    writer.writerow(writes_row)
                
            
