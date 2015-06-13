import swap_config
import glob
from itertools import izip
import csv

args = swap_config.args
policy_size = 32
if args.number=="11" or args.number=="12":
    delta = 30
else:
    delta = 5 * 60

traces = glob.glob(args.number+"_disk*")
policy_code = "PointerCount"+str(args.prealloc)

ptr_cnt_file = policy_code+"_"+args.number+".txt"

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

def add_pointers(current_req, pointer_dict):
    for request in current_req.requests:
        #Block number is in 512byte sectors, we want 4KB blocks
        blk_num = request[2] / 8
        pointer_dict[blk_num] = True

for filename in traces:
    print filename

    #INITIALIZE
    bucket = delta
    current_reqs = None
    pointers = {}
    outfile = policy_code+"_"+filename

    with open(outfile, "w") as out:
        out.truncate(0)

    with open(filename, "r") as input, open(outfile, "a") as output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(output, delimiter=' ')
        for row in reader:
            time = float(row[0])
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            flag = int(row[4])

            while time >= bucket:
                writer.writerow([bucket, len(pointers)])
                bucket += delta

            row[2] = block_num
            row[3] = block_size
            row[4] = flag

            if not current_reqs:
                #this is the first row
                current_reqs = CurrentReq(row)
                continue
            else:
                if current_reqs.is_sequential(row):
                    #continuation of current request
                    current_reqs.add_req(row)
                else:
                    #this is the beginning of a new request.
                    #first deal with the old request.
                    if current_reqs.should_shelter():
                        add_pointers(current_reqs, pointers)
                    current_reqs = CurrentReq(row)

        #Now flush final pointer count to outfile
        if current_reqs.should_shelter():
            add_pointers(current_reqs, pointers)
        writer.writerow([bucket, len(pointers)])

#add up number of pointers per disk


#Add up fill counts for each disk
files = [open(policy_code+"_"+args.number+"_"+"disk"+str(i)+".txt", "r") for (i, trc) in enumerate(traces)]
readers = [csv.reader(file, delimiter=' ') for file in files]
ptrs = []
times = []

#fills is list of lists of fills from each disk
for reader in readers:
    (time, ptr) = zip(*[(row[0], row[1]) for row in reader])
    times.append(list(time))
    ptrs.append(list(ptr))

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

ptr_sums = reduce(add_lists, ptrs, [])

#Now just get (longest) list of times
time_list = max(times, key=lambda l: len(l))

#merge them together and write them out
with open(ptr_cnt_file, "w") as out:
    writer = csv.writer(out, delimiter=' ')
    assert(len(time_list) == len(ptr_sums))
    for (time, csd) in izip(time_list, ptr_sums):
        writer.writerow([time, csd])

#cleanup
for file in files:
    file.close()


