import sort_traces
import csv

(num, traces) = sort_traces.get_traces()

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
                disk_out_filename = num+"_disk"+disk+".txt"
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
