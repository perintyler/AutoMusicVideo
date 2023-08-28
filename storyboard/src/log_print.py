"""logprint.py"""

import os
from datetime import datetime

PRINT_TO_STDOUT = True

WRITE_LOGS_TO_FILE = True

STORE_LOGS_ON_GCP = False

LOG_DIRECTORY = '../logs'

LOG_FILENAME = f'logs-{datetime.now().strftime("%m-%d-%y_%H-%M-%S")}.txt'

print(f'logging to {LOG_FILENAME}')

__logs__ = []

def _save_log(log):
  """..."""
  __logs__.append(log)

  if WRITE_LOGS_TO_FILE:
    if not os.path.exists(LOG_DIRECTORY):
      os.mkdir(LOG_DIRECTORY)

    logfile_path = os.path.join(LOG_DIRECTORY, LOG_FILENAME)

    with open(logfile_path, 'w+') as logfile:
      logs_string = '\n'.join(__logs__)
      logfile.write(logs_string)  

def logprint_message(message, author = None):
  """..."""
  log = f'[{author}]: {message}' if author is not None else message
  if PRINT_TO_STDOUT: print(log)
  _save_log(log)

def logprint_header(title):
  """..."""
  title = ' '.join(word.title() for word in title.split(' '))
  header = f'<><><> {title} <><><>'
  indent = ' '*int((128 - len(header))/2 + 1)
  headerDivider = '-'*128
  logprint_message(f"\n{headerDivider}\n{indent}{header}\n{headerDivider}\n")

def logprint_divider():
  """..."""
  logprint_message('\n')
  logprint_message('-'*128)
  logprint_message('/'*64 + '\\'*64)
  logprint_message('\\'*64 + '/'*64)
  logprint_message('-'*128)
  logprint_message('')

def logprint_bullet(message, indent=1):
  """..."""
  margin = '  '*indent
  logprint_message(f'{margin}- {message}')
