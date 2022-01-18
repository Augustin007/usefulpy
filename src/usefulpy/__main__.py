import sys
from usefulpy.IDE import ide, run_path
import argparse
import logging
import os
import time
import traceback

arguments = list(sys.argv)
if len(arguments) <= 1:
    ide()
    sys.exit()

my_parser = argparse.ArgumentParser(prog='usefulpy', usage='%(prog)s [options] [path]', description='run path with usefulpy or launch usefulpy')
my_parser.add_argument('Path', action='store', type=str, help='program to run')
my_parser.add_argument('-i', '--interactive', action='store_true', help='Enable interactive mode')
my_parser.add_argument('-l', '--log', action='count', help='increase logging level by 10')
my_parser.add_argument('extra_args', nargs=argparse.REMAINDER, help='arguments for code')

args = my_parser.parse_args()

input_path = args.Path

if not os.path.exists(input_path):
    print('No such file or directory:', input_path, '\n')
    sys.exit()

sys.argv = [os.path.realpath(args.Path)] + args.extra_args

if args.log:
    logging.basicConfig(level=args.log*10)

if args.interactive:
    filename = args.Path.split(os.sep)[-1]
    print(f'Running {filename} at {time.time()}')
try:
    space = run_path(input_path)
except Exception:
    traceback.print_exc()
    space = None

if args.interactive:
    ide(space)
