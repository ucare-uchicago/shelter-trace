#!/usr/bin/python

"""This simple script takes a directory and combine all eps files
in that directory (and its subdirs) into a single all.pdf.

Example:

./printeps.py graphs

"""

import os, sys, tempfile

epsfiles = ["total_sizes.eps", "total_counts.eps",
            "1_by_trace.eps", "2_by_trace.eps", 
            "1_reads_by_trace.eps", "2_reads_by_trace.eps", 
            "1_writes_by_trace.eps", "2_writes_by_trace.eps", 
            "by_size.eps", "reads_by_size.eps", "writes_by_size.eps",
            "1_ps_by_trace.eps", "2_ps_by_trace.eps", "ps_by_size.eps",
            "1_pio_by_trace.eps", "2_pio_by_trace.eps", "pio_by_size.eps",
            "csd.eps", "pa_diff.eps", "PB_diff.eps", "PC_diff.eps"]

# Prepare the latex file.
foundeps = False
tex = open('all.tex', 'w')
tex.write('\\documentclass[10pt]{article}\n')
tex.write('\\usepackage[margin=0.5in]{geometry}\n')
tex.write('\\usepackage{epsfig}\n')
tex.write('\\begin{document}\n\n')
tex.write('\\pagestyle{empty}\n')
#for (dp, dn, filenames) in os.walk(os.path.abspath(inputdir)):

for f in epsfiles:
    foundeps = True
    tex.write('\\begin{figure}\n')
    tex.write('\\includegraphics[scale=2, width=\\textwidth]{%s}\n' % f)
    tex.write('\\end{figure}\n\n')
    tex.write('\\clearpage\n')
tex.write('\\end{document}\n')
tex.close()

# Generate pdf file and clean up.
if not foundeps:
    print 'No eps files found'
    sys.exit(-1)


os.system('latex all')
os.system('dvips -o all.ps all')
os.system('ps2pdf14 all.ps')

#clean up
os.system('rm all.aux')
os.system('rm all.dvi')
os.system('rm all.ps')
os.system('rm all.tex')
os.system('rm all.log')

