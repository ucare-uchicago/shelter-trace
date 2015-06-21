#import argparse
import os
import csv
from datetime import datetime
import glob
import re
import sys
import settings #settings.py has our format strings

timestamp_date_dict = {}
starts = {}

#sort traces! How depends on filename format

def get_date_r(name, readme):
    trace_pattern = re.compile(readme+".(.*).trace.csv.csv.txt")
    match = re.search(trace_pattern, name)
    return timestamp_date_dict[match.group(1)]

def get_date(name): 
    return starts[name]

def get_traces(idx, trace_name, readme_path):
    traces = glob.glob(trace_name+"*.txt")

    #some traces don't have AM/PM in filenames,
    #so we look up each trace in the README to see it start time
    readme_traces = [2, 3, 5, 6]

    if idx in readme_traces:
        readme_file="{}/{}.Readme.txt".format(readme_path, trace_name)
        #if the readme is missing, the rest of the traces probably are too, so just skip it
        if not os.path.isfile(readme_file):
            print "Not processing this trace, ReadMe is missing"
            return []
        with open (readme_file, "rb") as readme:
            trace_pattern = re.compile("Trace Start: ([0-9]+)(.)* Trace Name: "+trace_name+".([0-9]{4}(-[0-9]{2}){2}.[0-9]{2}-[0-9]{2}).trace")
            for line in readme:
                match = re.search(trace_pattern, line)
                if match:
                    stamp = float(match.group(1))/1000.0
                    timestamp_date_dict[match.group(3)] = stamp
            traces.sort(key=lambda name: get_date_r(name, trace_name))
                
    else:
        format_string = settings.format_strings[idx-1]
        for trace in traces:
            starts[trace] = datetime.strptime(trace, format_string)
        traces.sort(key=get_date)

    return traces
