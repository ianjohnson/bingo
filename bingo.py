#! /usr/bin/python3
import argparse
import getkey
import os
import pyttsx3
import random
import subprocess
import sys


default_max_number = 75

parser = argparse.ArgumentParser(prog = "bingo",
                                 description = "Bingo Caller")
parser.add_argument('--numbers', '-n',
                    dest = 'max_number',
                    type = int,
                    default = default_max_number,
                    help = "Maximum number to call (default: %s)" % default_max_number)
parser.add_argument('--seed', '-s',
                    dest = 'seed',
                    type = int,
                    default = None,
                    help = "Maximum number to call (default: currect time)")
parser.add_argument('--calls-file', '-f',
                    dest = 'calls_file',
                    type = str,
                    default = None,
                    help = "Number calls file")
parser.add_argument('--call-numbers', '-c',
                    dest = 'call_numbers',
                    action = 'store_true',
                    help = "Call numbers")
parser.add_argument('--no-keyboard-cont', '-k',
                    dest = 'keyboard_continue',
                    action = 'store_false',
                    help = "Continue without key presses")
args = parser.parse_args()

if args.max_number > 90:
  print("Bingo cannot have more than 90 numbers, you chose %d" % args.max_number)
  sys.exit(1)

engine = None
if args.call_numbers:
  engine = pyttsx3.init()
  voices = engine.getProperty('voices')
  engine.setProperty('voice', 'english-north')
  engine.setProperty('rate', 130)

calls = list()
if args.calls_file:
  with open(args.calls_file, "r") as cf:
    l = cf.readline()
    while(l):
      l = l.strip()
      calls.append(l)
      l = cf.readline()

seed = args.seed if args.seed else None
random.seed(a = seed)

if engine:
  engine.say("Ladies and Gentlemen, eyes down for a full house")
  engine.runAndWait();

called_numbers = list()
while(True):
  os.system('clear')
  number = random.randint(1, args.max_number)
  if number not in called_numbers:
    called_numbers.append(number)
    if args.calls_file:
      try:
        number_call = calls[number - 1] + ", "
        print("\n%s\n" % number_call)
      except:
        number_call = ""
    subprocess.check_call("banner %d" % number, stdout = sys.stdout, shell = True)
    print("\nCalled Numbers: %s\n" % " ".join(map(lambda x: str(x), called_numbers)))

    continue_calling = False
    
    if engine:
      if args.calls_file:
        text =  number_call + " %d" % number
      else:
        text = str(number)
      while(True):
        engine.say(text)
        engine.runAndWait()
        if args.keyboard_continue:
          print("Press R to repeat, SPACE next call...")
          key = getkey.getkey(blocking = True)
          if not(key == 'r' or key == 'R'):
            continue_calling = True
            break
        else:
          continue_calling = True
          break

    if not continue_calling and args.keyboard_continue:
      print("Press SPACE to continue...")
      key = getkey.getkey(blocking = True)
      while(key != getkey.keys.SPACE):
        key = getkey.getkey(blocking = True)

  if len(called_numbers) == args.max_number:
    break

if engine:
  engine.stop()
