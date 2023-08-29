"""config.py"""

import os
import json
import pathlib
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEFAULT_CONFIG = {
  'VERBOSE': False,
  'INPUT_AUDIO_BUCKET_NAME': 'music-video-audio',
  'STORYBOARD_BUCKET_NAME': 'music-video-storyboards',
  'LOG_BUCKET': 'music-video-storyboard-logs',
  'PRODUCTION': True
}

class InvalidConfig(Exception):
  """program input is invalid, refer to the config section in the README"""

def get_enviroment_variable(key):
  """
  """
  if os.environ.get(key):
    return os.environ.get(key)
  elif key in DEFAULT_CONFIG:
    return DEFAULT_CONFIG[key]
  else:
    raise InvalidConfig(f'enviroment variable does not exist for "{key}"')

def is_verbose():
  return get_enviroment_variable('VERBOSE')

def is_production():
  return get_enviroment_variable('PRODUCTION')

def get_storyboard_bucket_name():
  """
  """
  return get_enviroment_variable('STORYBOARD_BUCKET_NAME')

def get_input_audio_bucket_name():
  """
  """
  return get_enviroment_variable('INPUT_AUDIO_BUCKET_NAME')

def get_gcp_project_id():
  """
  """
  return get_enviroment_variable('STORAGE_SERVICE_PROJECT_ID')

def get_storage_service_account_info():
  """
  """
  return {
    'type': 'service_account',
    "project_id": get_enviroment_variable('STORAGE_SERVICE_PROJECT_ID'),
    "private_key_id": get_enviroment_variable('STORAGE_SERVICE_PRIVATE_KEY_ID'),
    "private_key": get_enviroment_variable('STORAGE_SERVICE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": get_enviroment_variable('STORAGE_SERVICE_CLIENT_EMAIL'),
    "client_id": get_enviroment_variable('STORAGE_SERVICE_CLIENT_ID'),
    "auth_uri": get_enviroment_variable('STORAGE_SERVICE_AUTH_URI'),
    "token_uri": get_enviroment_variable('STORAGE_SERVICE_TOKEN_URI')
  }

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
    "song_id": "my-song-id"
  }  
  ```
  """

  audio_file: pathlib.Path
  song_id: str

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
    if not 'song_id' in config:
      raise InvalidConfig("missing 'storyboard_directory' key in config file")

    audio_file = config['audio_file']
    if not os.path.exists(audio_file):
      raise InvalidConfig(f"audio file does not exist: {audio_file}")
    if not audio_file.endswith('.mp3') and not audio_file.endswith('.wav'):
      raise InvalidConfig(f"audio file is not an mp3 or wav: {audio_file}")

    song_id = config['song_id']

    return Cls(audio_file, song_id)

def load_from_file(path_to_config_file): 
  return Config.load(path_to_config_file)

