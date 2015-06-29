#!/usr/bin/env python
import csv
import sys
import glob

#use shelter-trace/commons/settings.py to tell us location of input & results
sys.path.append("../common/")
import settings 

#results files:
#PS.dat gives the size of sheltered writes as a percentage of the total size of *all* I/O
#PIO.dat gives the number of sheltered writes as a percentage of the total number of I/O requests
ps_results_file="{}/PS-PIO/dat/PS.dat".format(settings.results_path)
pio_results_file="{}/PS-PIO/dat/PIO.dat".format(settings.results_path)

sizes = [4, 8, 16, 32, 64] #in KB

def gen_data():
    with open(ps_results_file, "w") as ps_results, open(pio_results_file, "w") as pio_results:
        ps_writer = csv.writer(ps_results, delimiter=' ')
        pio_writer = csv.writer(pio_results, delimiter=' ')
    
        #headers
        header = ["Trace"]
        for size in sizes:
            header.append(size)
        header.append("Rest")
        ps_writer.writerow(header)
        pio_writer.writerow(header)

        #process one trace at a time
        for (idx, trace) in enumerate(settings.traces, 1):
            print idx

            #get our input files (one file/disk)
            traces_glob = "{}/{}/*_consolidated.txt".format(settings.preprocessed_traces_path, trace)
            trace_files = glob.glob(traces_glob)

            if not trace_files:
                print "Skipping this trace, no files found"
                continue

            #initialize our dictionaries
            #note that percentages are cumulative over ALL disks in a given trace
            pio_dict = {}
            ps_dict = {}
            for size in sizes:
                pio_dict[size] = 0 #number of writes where previous size < request size <= size
                ps_dict[size] = 0  #total size of all writes where previous size < request size <= size
            ps_dict["total"] = 0  #total size of all requests (reads and writes)
            pio_dict["total"] = 0 #total number of requests (reads and writes)
            ps_dict["rest"] = 0   #total size of all writes larger than max size
            pio_dict["rest"] = 0  #total number of all writes larger than max size

            for file in trace_files:
                with open(file, "r") as input:
                    reader = csv.reader(input, delimiter=' ')
                    for row in reader:
                        #request size in blocks
                        req_size = int(row[3])

                        #update totals
                        ps_dict["total"] += req_size
                        pio_dict["total"] += 1
                        
                        #categorize it if it's a write
                        if int(row[4]) == 0:

                            #convert request size to KB
                            req_size_KB = req_size / 2

                            #put this request in the right bucket
                            for size in sizes:
                                if req_size_KB <= size:
                                    ps_dict[size] += req_size
                                    pio_dict[size] += 1
                                    break
                            if req_size_KB > sizes[-1]:
                                ps_dict["rest"] += req_size
                                pio_dict["rest"] += 1

            #write out PS results for this traces
            ps_results = ["T"+str(idx)]
            total_size = float(ps_dict["total"])
            for size in sizes:
                percent = ps_dict[size] / total_size
                ps_results.append(percent * 100)
            #calculate percent greater than largest size
            percent = ps_dict["rest"] / total_size
            ps_results.append(percent * 100)
            ps_writer.writerow(ps_results)

            #write out PIO results
            pio_results = ["T"+str(idx)]
            total_count = float(pio_dict["total"])
            for size in sizes:
                percent = pio_dict[size] / total_count
                pio_results.append(percent * 100)
            #calculate percent greater than largest size
            percent = pio_dict["rest"] / total_count
            pio_results.append(percent * 100)
            pio_writer.writerow(pio_results)

    return
        
        
