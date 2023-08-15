
import os
import json
import pathlib
from dataclasses import dataclass

class InvalidConfig(Exception):
  """program input is invalid, refer to the config section in the README"""

@dataclass
class Config:

  audio_file: pathlib.Path
  output_directory: pathlib.Path

  @classmethod
  def load(Cls, path_to_config):
    with open(path_to_config) as config_file:
      config = json.load(config_file)

    if not 'audio_file' in config:
      raise InvalidConfig("missing 'audio_file' key in config file")
    if not 'output_directory' in config:
      raise InvalidConfig("missing 'output_directory' key in config file")

    audio_file = config['audio_file']
    if not os.path.exists(audio_file):
      raise InvalidConfig()
    if not audio_file.endswith('.mp3') and not audio_file.endswith('.wav'):
      raise InvalidConfig()

    output_directory = config['output_directory']
    if not os.path.exists(output_directory):
      os.mkdir(output_directory)
    elif not os.path.isdir(output_directory):
      raise InvalidConfig()

    return Cls(audio_file, output_directory)

def load_config(path = './config.json'):
  return Config.load(path) if os.path.exists(path) else None
