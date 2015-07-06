import argparse

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
parser.add_argument("-p", "---prealloc", help="""Configuration of preallocated shelter.""",
                    type=int, choices=[1, 2, 3])

parser.add_argument("-c", "---code", help="""Sheltering policy code.""",
                    type=str, choices=["B", 
                                       "C", 
                                       "S"]) #S for swap -- tracks how many times shelters fill up and need to be swapped or reset

args = parser.parse_args()
