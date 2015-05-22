#!/usr/bin/env python

#IMPORTS
import argparse
import csv
import operator
from math import log, pow

# from basicBySize
throughput = {
	4096: 0.6054,
	8192: 1.2031,
	16384: 2.323,
	32768: 4.6266,
	65536: 9.0633,
	131072: 17.1117,
	262144: 31.4623,
	524288: 53.7186,
	1048576: 83.2694,
	2097152: 111.7642,
	4194304: 137.3785,
	8388608: 128.8016,
	16777216: 166.6678,
	33554432: 183.3871,
	67108864: 186.8764,
	134217728: 189.3183,

	512: 0.0754,
	1024: 0.1518,
	1536: 0.227,
	2048: 0.30275,
	2560: 0.3790666667,
	3072: 0.4547,
	3584: 0.5284,
	7168: 1.03715,
	11264: 1.625,
	12288: 1.76995,
	20480: 2.9051,
	29184: 4.152
}

def guess_bandwidth(size):
	x = int(pow(2,int(log(size, 2))))
	y = int(pow(2,int(log(size, 2))+1))
	throughput[size] = throughput[x]+(throughput[y]-throughput[x])/(y-x)*(size-x)

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Filename", type=str)
parser.add_argument("-s", "---span", help="""Hour span.""", type=int)
args = parser.parse_args()

bucket = []
bucket_2 = []
current_hour = 1

totalShelteredBytes = {}
writeTime = {}
with open(args.filename, "r") as input:
	reader = csv.reader(input, delimiter=' ')
	for row in reader:    	
		if row[6] == '1':
			io_size = int(row[3])*512
			disk_num = int(row[1])
			if disk_num not in totalShelteredBytes:
				totalShelteredBytes[disk_num] = 0				
			totalShelteredBytes[disk_num] += io_size
			if io_size not in throughput:
				guess_bandwidth(io_size)
			if disk_num not in writeTime:
				writeTime[disk_num] = 0
			writeTime[disk_num] += (io_size/throughput[io_size]/1e6) # since our throughput is MB/s
		if float(row[0]) > current_hour * 3600: # 3600 seconds = 1 hour
			print totalShelteredBytes
			readTime = max(totalShelteredBytes.itervalues())/228.832/1e6 # 228.832 MB/s is max bandwidth from fio

			bucket.append((max(writeTime.itervalues()), readTime, readTime + max(writeTime.itervalues())))
			bucket_2.append((writeTime,totalShelteredBytes))

			current_hour += 1
			totalShelteredBytes = {}
			writeTime = {}

#print "sheltered_count:%d other_count:%d" % (sheltered_count, other_count)
#print "totalShelteredBytes:%d" % totalShelteredBytes
#print "writeTime:%f readTime:%f total:%f" % (writeTime, readTime, writeTime+readTime)
# merge buckets
for b in bucket:
	print "%lf %lf %lf" % (b[0], b[1], b[2])

max_str = ""
for span in [1, 2, 4, 8, 16, 24]:
	max_b = 0

	if span > len(bucket):
		continue

	for i, b in enumerate(bucket):
		if i + span - 1 >= len(bucket):
			continue
		total = 0
		for j in range(i, i+span):
			total += bucket[j][2]
		if total > max_b:
			max_b = total
	print "%f" % (max_b)
	max_str += "%f " % (max_b)

print max_str

max_str = ""

for span in [1, 2, 4, 8, 16, 24]:
	max_b = 0

	if span > len(bucket):
		continue

	for i, b in enumerate(bucket):
		if i + span - 1 >= len(bucket):
			continue
		_totalShelteredBytes = {}
		_writeTime = {}
		for j in range(i, i+span):
			for d in bucket_2[j][1]:
				if d not in _writeTime:
					_writeTime[d] = 0
					_totalShelteredBytes[d] = 0
				_writeTime[d] += bucket_2[j][0][d]
				_totalShelteredBytes[d] += bucket_2[j][1][d]
		readTime = max(_totalShelteredBytes.itervalues())/228.832/1e6 # 228.832 MB/s is max bandwidth from fio
		total = readTime + max(_writeTime.itervalues())

		if total > max_b:
			max_b = total
	print "%f" % (max_b)
	max_str += "%f " % (max_b)

print max_str