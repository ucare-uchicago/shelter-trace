#!/usr/bin/env python
import sys
import os
import gen_ps_pio

sys.path.append("../common/")
import settings

#Create all directories we need if they don't already exist
basedir="{}/PS-PIO/".format(settings.results_path)
dirs = [basedir + "dat/",
        basedir + "eps/",
        basedir + "plt/"]

for dir in dirs:
    if not os.path.isdir(dir):
        os.makedirs(dir)

#run python script to create data
gen_ps_pio.gen_data()
    
#run bash script to create and run PS-PIO.plt
#TODO

#generate all.sh
#TODO
