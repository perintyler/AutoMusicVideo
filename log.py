
import os
import json
from datetime import datetime

VERBOSE = True

LOGFILE_NAME = f'./logs/{datetime.now().isoformat()}.json'

__print_logs__ = True
__logs__ = []

def start_printing(): __print_logs__ = False
def stop_printing(): __print_logs__ = True

def new_message(msg):
  """prints if verbose mode is on, otherwise gets written to log file
  """
  __logs__.append(msg)
  if __print_logs__:
    print(f'  - {msg}')

def save_all():
  """saves all messages to a json file
  """
  if not os.path.isdir('logs'): 
    os.mkdir('logs')

  with open(LOGFILE_NAME, 'w') as logfile:
    json.dump(__logs__, logfile)
