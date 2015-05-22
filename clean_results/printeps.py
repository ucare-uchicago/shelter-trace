#!/usr/bin/python

"""This simple script takes a directory and combine all eps files
in that directory (and its subdirs) into a single clean.pdf.

Example:

./printeps.py graphs

"""

import os, sys, tempfile

epsfiles = ["freq.eps", "cum_freq.eps"]

# Prepare the latex file.
foundeps = False
tex = open('clean.tex', 'w')
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


os.system('latex clean')
os.system('dvips -o clean.ps clean')
os.system('ps2pdf14 clean.ps')

#clean up
os.system('rm clean.aux')
os.system('rm clean.dvi')
os.system('rm clean.ps')
os.system('rm clean.tex')
os.system('rm clean.log')

