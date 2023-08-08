
import os
import json
from datetime import datetime

VERBOSE = True

LOGFILE_NAME = f'./logs/{datetime.now().isoformat()}.json'

__logs__ = []

def message(msg):
  """prints if verbose mode is on, otherwise gets written to log file"""
  __logs__.append(msg)
  if (VERBOSE):
    print(f'  - {msg}')

def header(title):
  title = ' '.join(word.title() for word in title.split(' '))
  header = f'<><><> {title} <><><>'
  indent = ' '*int((128 - len(header))/2 + 1)
  headerDivider = '-'*128
  print(f"\n{headerDivider}\n{indent}{header}\n{headerDivider}\n")

def divider():
  print('\n')
  print('-'*128)
  print('/'*64 + '\\'*64)
  print('\\'*64 + '/'*64)
  print('-'*128)
  print('')

def save_all():
  if VERBOSE: header(f'saving logs to {LOGFILE_NAME}')
  if not os.path.isdir('logs'): os.mkdir('logs')
  with open(LOGFILE_NAME, 'w') as logfile:
    json.dump(__logs__, logfile)

