#!/usr/bin/env python 
"""Generate all the *.csv.txt and N_diskm.txt files consumed by other scripts.
Currently does not support T11 or T12, or the time offset argument that original preprocess.py had.
"""
import sys
import os
import glob
import preprocess
sys.path.append("../")

import settings

for idx, trace in enumerate(settings.traces):
    traces_path = "{}/{}/Traces/*.csv".format(settings.traces_path, trace)
    processed_traces_path = "{}/{}/".format(settings.preprocessed_traces_path, trace)
    raw_traces = glob.glob(traces_path)
    if not os.path.exists(processed_traces_path):
        os.makedirs(processed_traces_path)
    #run preprocess.py
    for raw_trace in raw_traces:
        processed_trace=settings.preprocessed_traces_path + "/"
        outfile = "{}/{}.txt".format(processed_traces_path, os.path.basename(raw_trace))
        preprocess.preprocess_func(raw_trace, outfile)
        
            
        
