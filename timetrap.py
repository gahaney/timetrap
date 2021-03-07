#!env python3
import sys
import argparse
sys.path.append('./timetrap')
from db import db 

commands =['start', 'stop', 'pause', 'init', 'flush', 'post', 'show']
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command', required=True)
for command in commands:
  globals()[command] = subparser.add_parser(command)

start.add_argument('-t', '--ticket', type=str, required=True)
start.add_argument('-c', '--comment', type=str)

stop.add_argument('-c', '--comment', type=str)

args = parser.parse_args()

command = args.command
if args.command in ['start']: ticket = args.ticket
if args.command in ['start', 'stop']: comment = args.comment

with db() as db:
  if command=='start':
    db.insert(ticket, comment)
  elif command=='stop':
    db.stop()
  elif command=='flush' or command=='init':
    db.init_db()
  elif command=='show':
    time = db.show()
    for row in time:
      print(row)