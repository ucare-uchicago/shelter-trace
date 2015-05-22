import argparse
import csv
from datetime import datetime
import glob
import re

timestamp_date_dict = {}
starts = {}

#sort traces! How depends on filename format

def get_date_r (name, readme):
    trace_pattern = re.compile(readme+".(.*).trace.csv.csv.txt")
    match = re.search(trace_pattern, name)
    return timestamp_date_dict[match.group(1)]

def get_date (name): 
    return starts[name]

def get_traces ():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Trace number", type=str)
    parser.add_argument("-r", "--readme", help=""""Use readme to sort traces.
                               Needed when AM/PM not included in
                               trace title""", type=str)
    parser.add_argument("-t", "---TPC", help="""Some slight differences in handling TPC* traces.""", action="store_true")
    
    args = parser.parse_args()
    
    if args.TPC:
        traces = glob.glob("*.out.txt")
    else:
        traces = glob.glob("*.csv.txt")
    

    if args.readme:
        with open ("../"+args.readme+".ReadMe.txt", "rb") as readme:
            trace_pattern = re.compile("Trace Start: ([0-9]+)(.)* Trace Name: "+args.readme+".([0-9]{4}(-[0-9]{2}){2}.[0-9]{2}-[0-9]{2}).trace")
            for line in readme:
                match = re.search(trace_pattern, line)
                if match:
                    stamp = float(match.group(1))/1000.0
                    timestamp_date_dict[match.group(3)] = stamp
            traces.sort(key=lambda name: get_date_r(name, args.readme))
                
    else:
        with open("format_string.txt", "rb") as f:
            format_string = f.read().strip()
            for trace in traces:
                starts[trace] = datetime.strptime(trace, format_string)
            traces.sort(key=get_date)

    return (args.number, traces)
