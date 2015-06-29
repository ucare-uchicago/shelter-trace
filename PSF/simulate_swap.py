#!/usr/bin/env python
"""
Sheltering Simulator.
Writes <= 32 KB are sheltered.
"""

#IMPORTS
import sys
import swap_config
import glob
import csv
from copy import copy

#CONSTANTS/CONFIG

args = swap_config.args

#cutoff size in KB
policy_size = 32

#MB in sectors
one_MB = 2 * 1024

#info about size of preallocated shelters:
if args.prealloc == 1:
    x = 1 * one_MB
elif args.prealloc == 2:
    x = 5 * one_MB
else:
    x = 10 * one_MB
y = x * 10

traces = glob.glob(args.number+"_disk*")
policy_code = "SwapSim"+str(args.prealloc)

if args.number=="11" or args.number=="12":
    delta = 30
else:
    delta = 5 * 60


#LIST OF ALL THE SHELTERS
shelters = {}

#FUNCTIONS

def round_down(num, divisor):
    return num - (num%divisor)

#return 1st block number of next shelter after block_num
def get_next_shelter (block_num):
    shelter = round_down(block_num, y) + (x * 9)
    #If shelter starts before block_num, last write must have been sheltered too
    #That's okay--we just want beginning of shelter
    return shelter

#given a request, break it into a list of requests 
#none of which overlaps with a shelter
def dodge_shelters(req):
    start = req[2]
    size = req[3]
    next_shelter = get_next_shelter(start)
    if start + size <= next_shelter:
        return [req]
    else:
        overlap = start + size - next_shelter
        new_req = copy(req)
        new_req[3] = size - overlap
        next_req = copy(req)
        next_req[2] = next_shelter + x
        next_req[3] = overlap
        new_reqs = dodge_shelters(next_req)
        new_reqs.append(new_req)
        return new_reqs

#Reduction for finding emptiest shelter
def min(shelt1, shelt2):
    if shelt1.size_sheltered() < shelt2.size_sheltered():
        return shelt1
    else:
        return shelt2

def shelter_swap(shelt, req_size):
    emptiest_shelter = reduce(min, shelters.values())
    if emptiest_shelter.space_left() < req_size:
        #The shelters are all too full. Time for a full reset.
        for s in shelters.values():
            print "reset!"
            s.reset()
    else:
        #swap!
        print "swap!"
        tmp = shelt.tail
        shelt.tail = emptiest_shelter.tail
        emptiest_shelter.tail = tmp

            
#modify requests in request[disk_num] so they're sheltered
def shelter_writes (current_requests):
    #if tail is negative, there's nothing to shelter behind,
    #because this is the first request for this disk
    #so don't change it
    if tail >= 0:
        shelter_blk = get_next_shelter(tail)
        if shelter_blk not in shelters:
            print "adding another shelter!"
            shelters[shelter_blk] = Shelter(shelter_blk)
        if shelter_blk < tail and not(last_sheltered):
            #the tail is inside a shelter
            #this should only happen if we're in policy B, so not shifting
            #in which case we jump to next shelter
            #assert (args.code == "B")
            print "shelter block: "+str(shelter_blk)
            print "tail: "+str(tail)
            sys.exit(0)
        shelter = shelters[shelter_blk]
        shelter.shelter_writes(current_requests)
        return shelter.tail
    else:
        return current_requests.get_next_blk()

def count_full_shelters():
    count = 0
    for shelter in shelters.values():
        if shelter.is_full():
            count += 1
    return count


#CLASSES

class Shelter:
    """Keep track of information about shelter,
    including how full it is and requests in it that need to be cleaned."""
    def __init__(self, blk):
        self.start = blk
        self.tail = blk
        self.end = self.start + x
        assert(self.end % y == 0)
        return
    def reset(self):
        self.tail = self.start
    def size_sheltered(self):
        return (self.tail - self.start)
    def space_left(self):
        return (self.end - self.tail)
    def enough_space(self, reqs):
        if reqs.size <= (self.end - self.tail):
            return True
        else:
            return False
    def is_full(self):
        if self.space_left() <= policy_size * 2:
            return True
        else:
            return False
    def shelter_writes(self, current_reqs):
        #We shelter all requests in current_reqs together.
        #If there's not enough space for all of them, 
        #we swap (and reset if needed) to make space.
        if not(self.enough_space(current_reqs)):
            shelter_swap(self, current_reqs.size)
        self.tail += current_reqs.size
        return

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
    def shift_requests(self):
        new_reqs = []
        for req in self.requests:
            start_blk = req[2]
            size = req[3]
            #num_shelters is number of shelters that END behind the FIRST 
            #block of the request
            num_shelters = start_blk / y
            shift = num_shelters * x
            new_start = start_blk + shift
            next_shelter = get_next_shelter(new_start)
            if new_start >= next_shelter:
                #new_start is inside a shelter, so we need to shift it another shelter's length
                #new_start = next_shelter + x
                new_start += x
                next_shelter = get_next_shelter(new_start)
            req[2] = new_start
            #split up request as needed so it doesn't run into a shelter
            split_reqs = dodge_shelters(req)
            split_reqs.reverse()
            if not split_reqs:
                print "no split_reqs!"
            new_reqs.extend(split_reqs)
        self.requests = new_reqs
        return

#MAIN PROCESSING LOOP

for filename in traces:
    print filename

    #INITIALIZE
    bucket = delta
    tail = -1
    current_reqs = None
    shelters = {}
    #remember whether last write was sheltered; 
    #this affects how we shelter a write when the current tail is inside a shelter
    last_sheltered = False
    outfile = policy_code+"_"+filename

    #First, we look for highest block number,
    #from which we extrapolate the total number of shelters.
    with open(filename, "r") as input, open(outfile, "w") as output:
        reader = csv.reader(input, delimiter=' ')
        max_block = max([int(row[2]) + int(row[3]) for row in reader])
        #We add enough space to account for shifting
        max_block = max_block * 1.1
        print max_block
        #Then we initialize shelters
        shelter_blk = y - x
        while shelter_blk <= max_block - x:
            shelters[shelter_blk] = Shelter(shelter_blk)
            shelter_blk += y
        header = "Total number of shelters: "+str(len(shelters))
        output.write(header)


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
                writer.writerow([bucket, count_full_shelters()])
                bucket += delta

            #make row entries ints now so we don't have to cast them later
            row[2] = block_num
            row[3] = block_size
            row[4] = flag

            if not current_reqs:
                #this is the first row!
                current_reqs = CurrentReq(row)
                continue

            if current_reqs.is_sequential(row):
                #this is a continuation of the current request
                current_reqs.add_req(row)
            else:
                #this is the beginning of a new request
                #first, deal with old request.
                if current_reqs.should_shelter():
                    tail = shelter_writes(current_reqs)
                    last_sheltered = True
                else:
                    current_reqs.shift_requests()
                    last_sheltered = False
                    #update tail
                    tail = current_reqs.get_next_blk()

                #reset current_reqs
                current_reqs = CurrentReq(row)
        #Now flush final full-shelter count to outfile
        if current_reqs.should_shelter():
            shelter_writes(current_reqs)
        else:
            current_reqs.shift_requests()
        bucket = writer.writerow([bucket, count_full_shelters()])

                

