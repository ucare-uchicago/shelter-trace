#!/usr/bin/env python
"""
Sheltering Simulator.
Writes <= 32 KB are sheltered.
"""

#IMPORTS
import os
import sys
import config
import glob
import csv
import subprocess
from copy import copy

#user shelter-trace/commons/settings.py to tell us location of input/results
sys.path.append("../common/")
import settings

#CONSTANTS/CONFIG

args = config.args

#cutoff size in KB
#policy_size = 32

#MB in sectors
one_MB = 2 * 1024

#info about size of preallocated shelters:
#x is the size of a shelter, 
#y is the distance between the start of one shelter and start of the next (shelter range)
if args.prealloc == 1:
    x = 1 * one_MB
elif args.prealloc == 2:
    x = 5 * one_MB
else:
    x = 10 * one_MB
y = x * 10

#info about cleanup:
if not(args.code =="B" or args.code =="C"):
    print "Cleanup not supported! Please choose policy B or C."
    sys.exit(0)


#get list of input files
trace_name = settings.traces[int(args.number) - 1]
traces_glob = "{}/{}/*_consolidated.txt".format(settings.preprocessed_traces_path, trace_name)
traces = glob.glob(traces_glob)
policy_code = "P"+args.code+str(args.prealloc)

#create output directory if it doesn't exist
if not os.path.exists(settings.simulated_traces_path):
    os.makedirs(settings.simulated_traces_path)


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

def shift_request(req):
    if args.code == "B":
        #Policy B indicates we don't shift requests to avoid shelters,
        #so do nothing
        return [req]
    else:
        #how far down do we have to push start of request?
        #num_shelters is number of shelters that END before the FIRST block of the request
        start_blk = req[2]
        num_shelters = start_blk / y
        shift = num_shelters * x
        new_start = start_blk + shift
        if new_start >= next_shelter:
            #new start is inside a shelter
            #so shift it one more shelter's-length down
            new_start += x
            next_shetler = get_next_shelter(new_start)
        req[2] = new_start
        #split up request as needed so it doesn't run into a shelter
        split_req = dodge_shelters(req)
        split_reqs.reverse() #dodge_shelters returns requests in reverse because recursion
        if not split_reqs:
            print "dodge_shelters returned an empty request!"
            sys.exit(0)
        return split_reqs


#should this request be sheltered?
def should_shelter(request):
    return (request[3] <= settings.shelter_size * 2 and request[4]==0)


#this function just finds the appropriate shelter for the current request
#the shelter.shelter_writes method actually modifies the request
def shelter_write (current_request):
    #if tail is negative, there's nothing to shelter behind,
    #because this is the first request for this disk
    #so don't change it
    if tail >= 0:
        shelter_blk = get_next_shelter(tail)
        if shelter_blk < tail and not(last_sheltered):
            #the tail is inside a shelter
            #this should only happen if we're in policy B, so not shifting
            #in which case we jump to next shelter
            if args.code != "B":
                #something is wrong; print debugging info and quit
                print "shelter block: "+str(shelter_blk)
                print "tail: "+str(tail)
                sys.exit(0)
            shelter_blk += y #shelter_blk + y is the location of the next shelter
        if shelter_blk not in shelters:
            shelters[shelter_blk] = Shelter(shelter_blk)
        shelter = shelters[shelter_blk]
        shelter.shelter_write(current_request)
    return


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
    def enough_space(self, request):
        if request[3] <= (self.end - self.tail):
            return True
        else:
            return False
    def shelter_write(self, request):
        #modify request so it's at appropriate point in shelter
        size = request[3]
        #make sure this request isn't bigger than the whole shelter
        if size > x:
            print request
            print x
            sys.exit(0)
        request[6] = 1 #mark it as sheltered
        if self.tail + size > self.end:
            #out of space, back to beginning of shelter
            self.tail = self.start
        #modify request to write to tail of shelter
        request[2] = self.tail
        self.tail += size
        return


#MAIN PROCESSING LOOP
#we process traces separately by disk
for filename in traces:
    print filename

    #INITIALIZE
    tail = -1    #tail is location of disk head after latest request
    current_reqs = None
    #shelters: look up shelter by blk_num
    shelters = {}
    #remember whether last write was sheltered; 
    #this affects how we shelter a write when the current tail is inside a shelter
    last_sheltered = False
    outfile = "{}/{}_{}".format(settings.simulated_traces_path, policy_code, os.path.basename(filename))

    with open(filename, "r") as input, open(outfile, "w") as output:
        reader = csv.reader(input, delimiter=' ')
        writer = csv.writer(output, delimiter=' ')
        for row in reader:    
            time = row[0]
            disk_num = row[1]
            block_num = int(row[2])
            block_size = int(row[3])
            flag = int(row[4])

            #make row entries ints now so we don't have to cast them later
            simulated_request = [time,
                                 disk_num,
                                 block_num,
                                 block_size,
                                 flag,
                                 row[5],
                                 0] #flag indicating whether request was sheltered; not sheltered by default

            simulated_requests = [simulated_request]  #we may break this up into multiple requests to dodge shelters
            if should_shelter(simulated_request):
                #modify block number so it's sheltered
                shelter_write(simulated_request) 
                last_sheltered = True
            else:
                #move requests to avoid a shelter
                #NOTE: in some cases, this could cause a request that wouldn't be sheltered
                #to be broken up into requests that would be
                #but we don't shelter them in that case
                simulated_requests = shift_request(simulated_request)
                last_sheltered = False
            #update tail - start of last request + length of last request
            tail = simulated_requests[-1][2] + simulated_requests[-1][3]

            for request in simulated_requests:
                writer.writerow(request)

