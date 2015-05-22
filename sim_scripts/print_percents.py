import config
import csv
import sys

args = config.args

for i in [1, 2, 3]:
    code = str(i) + "_" + args.number
    diff_file = "diff"+code+".txt"
    percents_file = "percents"+code+".txt"

    with open(diff_file, "r") as diff, open(percents_file, "w") as percents:
        reader = csv.reader(diff, delimiter=' ')
        writer = csv.writer(percents, delimiter=' ')
        for row in reader:
            time = row[0]
            base_size = float(row[1])
            sim_size = float(row[2])
            if base_size < 1:
                print time
                continue
            percent = (sim_size/base_size)*100.0
            writer.writerow([time, percent])
        
        
