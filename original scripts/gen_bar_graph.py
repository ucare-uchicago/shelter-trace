import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reads", help="""Reads/Total (default is Writes/Total)""", action='store_true')
parser.add_argument("-c", "--count", help="""Number of I/O requests (default is total I/O size)""", action='store_true')
args = parser.parse_args()

if args.reads:
    r_w_flag = "R"
else:
    r_w_flag = "W"

if args.count:
    i_o_flag = "PIO"
else:
    i_o_flag = "PS"

result_graph = i_o_flag + "-All-" + r_w_flag
result_file = result_graph + ".dat"

with open(result_file, "w") as file:
    writer = csv.writer(file, delimiter=' ')
    writer.writerow(["Trace", 4, 8, 16, 32, 64, "rest"])

    for i in range(1, 13):
        if args.reads:
            percents_file = i_o_flag+str(i)+"-R.txt"
        else:
            percents_file = i_o_flag+str(i)+".txt"
        totals_file = "totals"+str(i)+".txt"
        trace_row = ["T"+str(i)]
        #get last line of results file
        with open(percents_file, "r") as percents:
            last_line = percents.readlines()[-1]
            vals = last_line.split()
        last_size = 0
        #percent within each interval
        for val in vals[1:]:
            trace_row.append(float(val) - last_size)
            last_size = float(val)
        #percent greater than 64 KB
        with open(totals_file, "r") as totals:
            reader = csv.reader(totals, delimiter=' ')
            reads = reader.next()
            writes = reader.next()
            if args.count:
                total_i_o = float(reads[1]) + float(writes[1])
                if args.reads:
                    rest_percent = (float(reads[1]) / total_i_o) * 100
                else:
                    rest_percent = (float(writes[1]) / total_i_o) * 100
            else:
                total_i_o = float(reads[0]) + float(writes[0])
                if args.reads:
                    rest_percent = (float(reads[0]) / total_i_o) * 100
                else:
                    rest_percent = (float(writes[0]) / total_i_o) * 100
        trace_row.append(rest_percent - last_size)
        writer.writerow(trace_row)        
