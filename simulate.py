#!/usr/bin/env python
"""
Sheltering Simulator.
Writes <= 32 KB are sheltered.
"""

#IMPORTS
import sys
import argparse
import glob
import csv
import subprocess
import os
from copy import copy

#CONSTANTS/CONFIG

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Filename", type=str)
#parser.add_argument("number", help="Trace number", type=str)
#parser.add_argument("-p", "---prealloc", help="""Configuration of preallocated shelter.""",
#                    type=int, choices=[1, 2, 3])
parser.add_argument("-s", "---sheltersize", required=True, help="""Size in MB of Shelter.""",
					type=int)
parser.add_argument("-r", "---shelterrange", required=True, help="""Allocate 1 shelter for every MB""",
					type=int)
parser.add_argument("-c", "---code", help="""Sheltering policy code.""",
					type=str, choices=["B", "C", "D", "E"], default="C")

args = parser.parse_args()

#cutoff size in KB
policy_size = 32

#MB in sectors
one_MB = 2 * 1024

#info about size of preallocated shelters:
"""
if args.prealloc == 1:
	x = 1 * one_MB
elif args.prealloc == 2:
	x = 5 * one_MB
else:
	x = 10 * one_MB
y = x * 10
"""
x = args.sheltersize * one_MB
y = args.shelterrange * one_MB
assert x < y

#info about cleanup:
if args.code =="B" or args.code =="C":
	cleanup = False
else:
	cleanup = True

#traces = glob.glob(args.number+"_disk*")
policy_code = "P"+args.code+str(args.sheltersize)+str(args.shelterrange)


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

#CLASSES

class Shelter:
	"""Keep track of information about shelter,
	including how full it is and requests in it that need to be cleaned."""
	def __init__(self, blk):
		self.start = blk
		self.tail = blk
		self.end = self.start + x
		assert(self.end % y == 0)
		#a request is of the form (blknum, blksize)
		#we only keep track of these if we are cleaning up
		self.reqs = []
		return
	def enough_space(self, reqs):
		if not(cleanup):
			#no cleanup, so doesn't matter
			return True
		else:
			total_size = sum([row[3] for row in reqs])
			if total_size <= (self.end - self.tail):
				return True
			else:
				return False
	def shelter_writes(self, current_reqs):
		assert self.enough_space(current_reqs.requests)
		#if we need to clean up later, consolidate this list of requests,
		#which we know are sequential, into one request, remembering
		#where it will need to be written later
		if cleanup:
			cleanup_req_blk = requests[0][2]
			cleanup_req_size = 0
		for req in current_reqs.requests:
			size = req[3]
			req[6] = 1 # mark as sheltered
			#make sure request isn't larger than whole shelter
			if size > x:
				print req
				print x
				sys.exit(0)
			if self.tail + size > self.end:
				#out of space, back to beginning of buffer
				self.tail = self.start
			#modify request to write to tail of shelter
			req[2] = self.tail
			self.tail += size
			if cleanup:
				cleanup_req_size += size
		if cleanup:
			self.reqs.append(cleanup_req_blk, cleanup_req_size)
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
		#if our code is B, don't modify requests
		if args.code != "B":
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
				   #new_start is inside a shelter, shift it to just after shelter
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

#HERE IS ANOTHER FUNCTION    
			
#modify requests in request[disk_num] so they're sheltered
def shelter_writes (current_requests):
	#if tail is negative, there's nothing to shelter behind,
	#because this is the first request for this disk
	#so don't change it
	if tail >= 0:
		shelter_blk = get_next_shelter(tail)
		if shelter_blk < tail and not(last_sheltered):
			#the tail is inside a shelter
			#this should only happen if we're in policy B, so not shifting
			#in which case we jump to next shelter
			#assert (args.code == "B")
			if args.code != "B":
				print "shelter block: "+str(shelter_blk)
				print "tail: "+str(tail)
				sys.exit(0)
			shelter_blk += y
		if shelter_blk not in shelters:
			shelters[shelter_blk] = Shelter(shelter_blk)
		shelter = shelters[shelter_blk]
		shelter.shelter_writes(current_requests)
	return


#MAIN PROCESSING LOOP


#INITIALIZE
tail = -1
current_reqs = None
#shelters: look up shelter by blk_num
shelters = {}
#remember whether last write was sheltered; 
#this affects how we shelter a write when the current tail is inside a shelter
last_sheltered = False
outfile = os.path.dirname(args.filename) + "/" + policy_code+"_"+os.path.basename(args.filename)
print "input:"+args.filename+" output:"+outfile

with open(args.filename, "r") as input, open(outfile, "w") as output:
	reader = csv.reader(input, delimiter=' ')
	writer = csv.writer(output, delimiter=' ')
	for row in reader:    		
		disk_num = row[1]
		block_num = int(row[2])
		block_size = int(row[3])
		flag = int(row[4])

		#make row entries ints now so we don't have to cast them later
		row[2] = block_num
		row[3] = block_size
		row[4] = flag
		row.append(0) # row[6]; default; not shelter

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
				shelter_writes(current_reqs)
				last_sheltered = True
			else:
				current_reqs.shift_requests()
				last_sheltered = False
			#Now that requests have been modified as needed,
			#we can write them to outfile
			for req in current_reqs.requests:
				writer.writerow(req)
			#update tail
			tail = current_reqs.get_next_blk()
			current_reqs = CurrentReq(row)
	#Now flush any remaining requests to outfile
	if current_reqs.should_shelter():
		shelter_writes(current_reqs)
	else:
		current_reqs.shift_requests()
	for req in current_reqs.requests:
		writer.writerow(req)
					

