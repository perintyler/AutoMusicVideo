"""config.py"""

import os
import json
import pathlib
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class InvalidConfig(Exception):
  """program input is invalid, refer to the config section in the README"""

def get_absolute_path(relative_path):
  return os.path.join(ROOT_PATH, relative_path)
  
def get_gcp_project_id():
  """
  """
  project_id = os.environ.get('STORAGE_SERVICE_PROJECT_ID')

  if project_id is None:
    raise InvalidConfig('missing GCP project ID (environment file does not exist or is not configured properly)')

  return project_id

def get_storage_service_account_info():
  """
  """
  service_account_info = {
    'type': 'service_account',
    "project_id": os.environ.get('STORAGE_SERVICE_PROJECT_ID'),
    "private_key_id": os.environ.get('STORAGE_SERVICE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('STORAGE_SERVICE_PRIVATE_KEY'),
    "client_email": os.environ.get('STORAGE_SERVICE_CLIENT_EMAIL'),
    "client_id": os.environ.get('STORAGE_SERVICE_CLIENT_ID'),
    "auth_uri": os.environ.get('STORAGE_SERVICE_AUTH_URI'),
    "token_uri": os.environ.get('STORAGE_SERVICE_TOKEN_URI')
  }

  if None in service_account_info.values():
    raise InvalidConfig('missing GCP storage account info (environment file is not valid or does not exist)')
  else:
    service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')

  return service_account_info

def has_storage_service_account_info():
  """
  """
  try:
    get_storage_service_account_info()
  except InvalidConfig:
    return False

  return True

@dataclass
class Config:
  """main program inputs

  Created from a JSON file that will look like this:

  ```
  {
    "audio_file": "path/to/song.mp3",
    "storyboard_directory": "path/to/directory/that/will/contain/the/generated/music/video"
  }  
  ```
  """

  audio_file: pathlib.Path
  storyboard_directory: pathlib.Path

  @classmethod
  def load(Cls, path_to_config):
    """loads the program inputs from a JSON file
    """
    if not os.path.exists(path_to_config):
      raise InvalidConfig(f'config file does not exist: {path_to_config}')

    with open(path_to_config) as config_file:
      config = json.load(config_file)

    if not 'audio_file' in config:
      raise InvalidConfig("missing 'audio_file' key in config file")
    if not 'storyboard_directory' in config:
      raise InvalidConfig("missing 'storyboard_directory' key in config file")

    audio_file = config['audio_file']
    if not os.path.exists(audio_file):
      raise InvalidConfig(f"audio file does not exist: {audio_file}")
    if not audio_file.endswith('.mp3') and not audio_file.endswith('.wav'):
      raise InvalidConfig(f"audio file is not an mp3 or wav: {audio_file}")

    storyboard_directory = config['storyboard_directory']

    return Cls(audio_file, storyboard_directory)

def load_from_file(path_to_config_file): 
  return Config.load(path_to_config_file)

