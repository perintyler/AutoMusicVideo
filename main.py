"""main.py"""

import os
import json
import argparse

from music_video import MusicVideo
from text_to_image import generate_image

def prompt_user_is_ready_to_generate_multimedia() -> bool:
  """give the user a chance to stop the program and verify that lyrics are correct in the segments JSON file
  """
  prompt = 'Do you want to check that the lyrics were transcribed correctly before generating images? (y/n)'
  return input(prompt) == 'y'

def prompt_user_is_ready_to_compile_segments() -> bool:
  """give the user a chance to stop the program and verify that each segment's multimedia looks good
  """
  prompt = 'All multimedia for the video has been successfully generated. Are you ready to compile and save the final video? (y/n)'
  return input(prompt) == 'y': 

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

  if not os.path.exists(output_directory):
    os.mkdir(output_directory)

  multimedia_directory = os.path.join(output_directory, 'multimedia')
  if not os.path.exists(multimedia_directory):
    os.mkdir(multimedia_directory)

  ###
  # STEP 2: generate or load segments
  ###

  segments_file = os.path.join(output_directory, 'segments.json')

  if os.path.exists(segments_file):
    # segments file has already been created. create the music video object
    # by loading it from the existing segments file 
    music_video = MusicVideo.load_from_json(segments_file)

  else:
    # segments file has not been created. Create a new music video 
    # object save the incomplete segments to a JSON file
    music_video = MusicVideo.create_new(path_to_song)
    music_video.save_as_json(segments_file)

  if not prompt_user_is_ready_to_generate_multimedia(): return

  ###
  # STEP 3: generate multimedia for any incomplete segment (i.e. segment is missing multimedia)
  ###

  for segment in music_video.get_incomplete_segments()
    path_to_multimedia = os.path.join(output_directory, 'multimedia', segment.bar.line_number)
    generate_image(segment.bar.text, output_file)
    music_video.set_multimedia(line_number, output_file)
    music_video.save_as_json(segments_json_file)

  if not prompt_user_is_ready_to_compile_segments(): return

  ###
  # STEP 4: compile the final mp4 file using the now completed segments
  ###

  path_to_music_video = os.path.join(output_directory, 'music-video.mp4')
  music_video.compile(path_to_music_video)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--audio-file', required=True)
  parser.add_argument('--output-directory', required=True)
  args = parser.parse_args()
  main(args.audio_file, args.output_directory)
