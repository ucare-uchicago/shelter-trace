#!/usr/bin/env python

import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Filename", type=str)
args = parser.parse_args()

current_hour = 1

totalShelteredBytes = 0
totalShelteredIO = 0
max_totalShelteredIO = (-1, -1)

with open(args.filename, "r") as input:
	reader = csv.reader(input, delimiter=' ')
	for row in reader:    	
		if row[6] == '1':
			io_size = int(row[3])*512
			
			totalShelteredBytes += io_size
			totalShelteredIO += 1

		if float(row[0]) > current_hour * 3600: # 3600 seconds = 1 hour
			print totalShelteredBytes
			print totalShelteredIO

			if max_totalShelteredIO[1] < totalShelteredIO:
				max_totalShelteredIO = (current_hour, totalShelteredIO)

			current_hour += 1
			totalShelteredBytes = 0
			totalShelteredIO = 0

print max_totalShelteredIO			
