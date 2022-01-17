import sys
from usefulpy.IDE import ide, run_path
import argparse

arguments = list(sys.argv)
if len(arguments) <= 1:
    ide()
    sys.exit()

my_parser = argparse.ArgumentParser(prog='usefulpy', usage='%(prog)s [options] [path]', description='run path with usefulpy or launch usefulpy')
my_parser.add_argument('Path', action='store', type=str, help='program to run')
my_parser.add_argument('-i', '--interactive', action='store_true', help='Enable interactive mode')
args = my_parser.parse_args()

input_path = args.Path

print(input_path)
space = run_path(input_path)

if args.interactive:
    ide(space)
n = list(sys.argv)
