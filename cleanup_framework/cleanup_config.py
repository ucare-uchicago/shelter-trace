#Configuration information for cleanup framework.

#Argument parsing
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
parser.add_argument('-p', '--prealloc', help="""Configuration of preallocated shelter.""",
                    type=int, choices=[1, 2, 3], required=True)
parser.add_argument('-c', '--code', help="""Sheltering policy code.""",
                    type=str, choices=['C', 'D', 'E', 'F'])
parser.add_argument('-o', '--outfile', help="""Filename to use for simulated trace output.""",
                    type=str, default='outfile') 
parser.add_argument('-t', '--timespan', help="""Length of time to output trace for, in hours.""",
                    type=int, default=1)
parser.add_argument('-s', '--starttime', help="""Time to start trace output""",
                    type=int, default=0)

(args, cleanup_args) = parser.parse_known_args()

pre = args.prealloc
code = args.code
num = args.number
out = args.outfile
time = args.timespan
starttime = args.starttime

#Database name:
db = 'trace'+num+'.db'

#Table names:
reqs_t = 'requests'
series_t = 'series'
shelter_t = 'shelter'

#Cutoff is size of sheltered request in sectors
cutoff_KB = 32
cutoff = cutoff_KB * 2
