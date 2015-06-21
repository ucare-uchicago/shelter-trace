import csv
import os
import sys

#lets us import shelter-trace/common/sort_traces.py
sys.path.append("../common/")
import sort_traces

def split_by_disk(idx, trace_name, trace_path, readme_path):
    current_dir = os.getcwd()
    os.chdir(trace_path)
    traces = sort_traces.get_traces(idx, trace_name, readme_path)

    #one file per disk
    files = {}

    csvwriters = {}

    current_offset = 0

    for trace in traces:
        print trace
        offset = current_offset

        with open(trace, "r") as trace:
            reader = csv.reader(trace, delimiter=' ')
            for row in reader:
                disk = row[1]
                if not disk in files:
                    disk_out_filename = str(idx)+"_disk"+disk+".txt"
                    file = open(disk_out_filename, "w")
                    files[disk] = file
                    writer = csv.writer(file, delimiter=' ')
                    csvwriters[disk] = writer
                else:
                    writer = csvwriters[disk]
                #convert time from ms to s
                time = round((float(row[0]) / 1000.0), 6) + offset
                row[0] = time
                writer.writerow(row)

                current_offset = time

    #cleanup
    for k, file in files.iteritems():
        file.close()
    os.chdir(current_dir)
        
