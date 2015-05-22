import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--busy", help="Only look at busiest hour of each trace", action='store_true')
args = parser.parse_args()

if args.busy:
    result_file = "dsph-busy.dat"
    with open("busy_hours.dat", "r") as busy_file:
        busy_timestamps = [float(x) * 60 * 60 for x in busy_file.readline().split()]
else:
    result_file = "dsph-avg.dat"

with open(result_file, "w") as file:
    writer = csv.writer(file, delimiter=' ')
    writer.writerow(["Trace", 4, 8, 16, 32, 64])

    for i in range(1, 13):
        data_file = "T"+str(i) + "-write.txt"
        trace_row = ["T"+str(i)]
        with open(data_file, "r") as data:
            if args.busy:
                busy_start = busy_timestamps[i - 1]
                busy_end = busy_start + (60 * 60)
                reader = csv.reader(data, delimiter=' ')
                start_row = []
                end_row = []
                for row in reader:
                    if float(row[0]) >= busy_start:
                        start_row = row
                        print start_row
                        break
                for row in reader:
                    if float(row[0]) >= busy_end:
                        end_row = row
                        print end_row
                        break
                shelter_sizes = [float(end) - float(start) for start, end in zip(start_row[1:], end_row[1:])]
            else:
                last_line = data.readlines()[-1]
                vals = last_line.split()
                time = float(vals[0])
                #convert from seconds to hours
                num_hours = time / (60 * 60)
                shelter_sizes = [float(val) / num_hours for val in vals[1:]]
            #percent within each interval
            last_size = 0
            for size in shelter_sizes:
                trace_row.append(size - last_size)
                last_size = size
        writer.writerow(trace_row)
            
        
