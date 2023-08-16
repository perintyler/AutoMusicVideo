"""main.py"""

import os
import json
import argparse
import pathlib
from dataclasses import dataclass
from music_video import MusicVideo
from text_to_image import text_to_image
from pretty_print import print_header, print_bullet

CONFIG_FILE = './config.json'

EXIT_BEFORE_COMPLETING_SEGMENTS = False

EXIT_BEFORE_COMPILING_SEGMENTS = False

class InvalidConfig(Exception):
  """program input is invalid, refer to the config section in the README
  """

@dataclass
class Config:
  """main program inputs

  Created from a JSON file that will look like this:

  ```
  {
    "audio_file": "path/to/song.mp3",
    "output_directory": "path/to/directory/that/will/contain/the/generated/music/video"
  }  
  ```
  """

  audio_file: pathlib.Path
  output_directory: pathlib.Path

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
    if not 'output_directory' in config:
      raise InvalidConfig("missing 'output_directory' key in config file")

    audio_file = config['audio_file']
    if not os.path.exists(audio_file):
      raise InvalidConfig(f"audio file does not exist: {audio_file}")
    if not audio_file.endswith('.mp3') and not audio_file.endswith('.wav'):
      raise InvalidConfig(f"audio file is not an mp3 or wav: {audio_file}")

    output_directory = config['output_directory']

    return Cls(audio_file, output_directory)

def main(audio_file, output_directory):
  """Entry point for music video generation

  This function can be run multiple times for a single music video generation. The user is prompted 
  inbetween steps, giving him/her a chance to verify lyrics or the multimedia that corresponds to those
  lyrics. Progress is saved in the `segments.json` file, as well as the `multimedia` directory, so 
  for each run, this function will load any completed progress and continue from there.
  """

  ###
  # STEP 1: setup directories (if needed)
  ###

  print_header('setting up directories')

  if not os.path.exists(output_directory):
    print_bullet(f'creating output directory {output_directory}')
    os.mkdir(output_directory)

  multimedia_directory = os.path.join(output_directory, 'multimedia')
  if not os.path.exists(multimedia_directory):
    print_bullet(f'creating multimedia directory {multimedia_directory}')
    os.mkdir(multimedia_directory)

  ###
  # STEP 2: generate or load segments
  ###

  print_header('generating segments (lyrics)')

  segments_file = os.path.join(output_directory, 'segments.json')

  if os.path.exists(segments_file):
    # segments file has already been created. create the music video object
    # by loading it from the existing segments file 
    print_bullet(f'creating segments file: {segments_file}')
    music_video = MusicVideo.load_from_json(segments_file)

  else:
    # segments file has not been created. Create a new music video 
    # object save the incomplete segments to a JSON file
    print_bullet(f'loading segments file: {segments_file}')
    music_video = MusicVideo.create_new(audio_file)
    music_video.save_as_json(segments_file)

  if EXIT_BEFORE_COMPILING_SEGMENTS: return

  ###
  # STEP 3: generate multimedia for any incomplete segment (i.e. segment is missing multimedia)
  ###

  print_header("generating segments' multimedia")

  for segment in music_video.get_incomplete_segments():
    line_number = segment.bar.line_number
    multimedia_directory = os.path.join(output_directory, 'multimedia', f'line-{line_number}')
    if not os.path.exists(multimedia_directory): os.mkdir(multimedia_directory)
    print_bullet(f'generating images for "{segment.bar.text}" to {multimedia_directory}')
    text_to_image(segment.bar.text, multimedia_directory)
    output_file = multimedia_directory # fix this
    music_video.add_multimedia(line_number, output_file)
    music_video.save_as_json(segments_file  )

  if EXIT_BEFORE_COMPILING_SEGMENTS: return

  ###
  # STEP 4: compile the final mp4 file using the now completed segments
  ###

  print_header("compiling final video")

  path_to_music_video = os.path.join(output_directory, 'music-video.mp4')
  music_video.compile(path_to_music_video)

if __name__ == '__main__':
  try:
    config = Config.load(CONFIG_FILE)
    audio_file = config.audio_file
    output_directory = config.output_directory
  except InvalidConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio-file', required=True)
    parser.add_argument('--output-directory', required=True)
    args = parser.parse_args()
    audio_file = args.audio_file
    output_directory = args.output_directory

  main(audio_file, output_directory)
