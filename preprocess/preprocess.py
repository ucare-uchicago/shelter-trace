#!/usr/bin/env python
# -*- coding: utf-8 -*-

#modified to use event START time, and to include elapsed time as well

import re

def preprocess(infile, outfile):
    with open(infile, "r") as f, open(outfile, "w") as output :
	# skip header
	for line in f:
            if line[:9] == "EndHeader":
	        break

        re_p = re.compile("(\w+) \(\ ?(\d+)\)")
        
        for line in f:		
            tok = map(str.lstrip, line.split(","))
            flags = -1
            is_swap = 0

            if tok[0] == "DiskWrite":
                flags = 0
            elif tok[0] == "DiskRead":
                flags = 1

            if flags == -1:
                continue

            if tok[-1].endswith("pagefile.sys\""):
                is_swap = 1

            #p_info = re_p.search(tok[2])
            t = {
                "time": ((float(tok[1]) - float(tok[7])) / 1000.0),
                "devno": int(tok[8]),
                "blkno": int(tok[5], 16) / 512,
                "bcount": int(tok[6], 16) / 512,
                "flags": flags,
                "elapsed": float(tok[7]) / 1000.0,
                "is_swap" : is_swap
                #"pname": p_info.group(1),
                #"pid": int(p_info.group(2)),
                };

            output.write("%s %d %d %d %d %s %d\n" % ("{0:.3f}".format(t['time']), t['devno'], t['blkno'], t['bcount'], t['flags'], "{0:.3f}".format(t['elapsed']), t['is_swap']))

