import argparse

parser = argparse.ArgumentParser()
parser.add_argument("number", help="Trace number", type=str)
parser.add_argument("-p", "---prealloc", help="""Configuration of preallocated shelter.""",
                    type=int, choices=[1, 2, 3])

args = parser.parse_args()
