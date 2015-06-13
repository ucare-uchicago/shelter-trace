#!/usr/bin/env python 
"""Generate all the *.csv.txt and N_diskm.txt files consumed by other scripts.
Currently does not support T11 or T12, or the time offset argument that original preprocess.py had.
"""
import sys
import os
import glob
import preprocess
import split_by_disk

#lets us import shelter-trace/settings.py
sys.path.append("../common/") 
import settings

for idx, trace in enumerate(settings.traces, 1):
    print idx
    traces_path = "{}/{}/Traces/*".format(settings.traces_path, trace)
    processed_traces_path = "{}/{}/".format(settings.preprocessed_traces_path, trace)
    raw_traces = glob.glob(traces_path)
    #create directory for this preprocessed trace if it doesn't already exist
    if not os.path.exists(processed_traces_path):
        os.makedirs(processed_traces_path)
    for raw_trace in raw_traces:
        #run preprocess.py
        processed_trace=settings.preprocessed_traces_path + "/"
        outfile = "{}/{}.txt".format(processed_traces_path, os.path.basename(raw_trace))
        preprocess.preprocess(raw_trace, outfile)
    #now run split_by_disk
    print "split by disk!"
    split_by_disk.split_by_disk(idx, 
                                trace, 
                                processed_traces_path, 
                                "{}/{}".format(settings.traces_path, trace)) #path to these trace's README file    
        
