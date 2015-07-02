import argparse

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
parser.add_argument("-p", "---prealloc", help="""Configuration of preallocated shelter.""",
                    type=int, choices=[1, 2, 3])

#POLICIES D AND E NOT SUPPORTED!!!
parser.add_argument("-c", "---code", help="""Sheltering policy code.""",
                    type=str, choices=["B", "C", "D", "E"])

args = parser.parse_args()
