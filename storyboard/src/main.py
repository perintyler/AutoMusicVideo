"""main.py"""

import os
import json
import argparse
from pathlib import Path
from .storyboard import Storyboard
from .text_to_image import text_to_image
from .log_print import logprint_header, logprint_bullet
from .job_queue import TextToImageJobQueue
from . import cloud_sync
from . import config

USE_JOB_QUEUE = False

COMPILE_VIDEO = False

def create_storyboard(audio_file, storyboard_directory):
  """Entry point for music video generation

  This function can be run multiple times for a single music video generation. The user is prompted 
  inbetween steps, giving him/her a chance to verify lyrics or the multimedia that corresponds to those
  lyrics. Progress is saved in the `chapters.json` file, as well as the `multimedia` directory, so 
  for each run, this function will load any completed progress and continue from there.
  """

  ###
  # STEP 1: setup directories (if needed)
  ###

  logprint_header('setting up directories')

  if not os.path.exists(storyboard_directory):
    logprint_bullet(f'creating storyboard directory {storyboard_directory}')
    os.mkdir(storyboard_directory)

  multimedia_directory = os.path.join(storyboard_directory, 'multimedia')
  if not os.path.exists(multimedia_directory):
    logprint_bullet(f'creating multimedia directory {multimedia_directory}')
    os.mkdir(multimedia_directory)

  cloud_sync.apply_gcp_updates_to_local(storyboard_directory)

  ###
  # STEP 2: generate or load chapters
  ###

  logprint_header('generating chapters')

  chapters_file = os.path.join(storyboard_directory, 'chapters.json')

  if os.path.exists(chapters_file):
    # chapters file has already been created. create the music video object
    # by loading it from the existing chapters file 
    logprint_bullet(f'creating chapters file: {chapters_file}')
    storyboard = Storyboard.load_from_json(chapters_file)
  else:
    # chapters file has not been created. Create a new music video 
    # object save the incomplete chapters to a JSON file
    logprint_bullet(f'loading chapters file: {chapters_file}')
    storyboard = Storyboard.create_new(audio_file)
    storyboard.save_as_json(chapters_file)

  cloud_sync.apply_local_updates_to_gcp(storyboard_directory)

  ###
  # STEP 3: generate multimedia for any incomplete chapter (i.e. chapter is missing multimedia)
  ###

  logprint_header("generating text to image jobs")

  path_to_queue_file = os.path.join(storyboard_directory, 'jobs.json')
  job_queue = TextToImageJobQueue(path_to_queue_file)
  if os.path.exists(path_to_queue_file): 
    logprint_bullet(f'loaded job queue from {path_to_queue_file}')
  else:
    logprint_bullet(f'created job queue file: {path_to_queue_file}')

  for chapter in storyboard.chapters:
    
    if chapter.is_complete():
      continue

    line_number = chapter.bar.line_number
    multimedia_directory = os.path.join(storyboard_directory, 'multimedia', f'line-{line_number}')

    if not os.path.exists(multimedia_directory): 
      os.mkdir(multimedia_directory)

    if not USE_JOB_QUEUE:
      logprint_bullet(f'generating images for "{chapter.bar.text}" to {multimedia_directory}')
      text_to_image(chapter.bar.text, multimedia_directory)
      chapter.set_multimedia(multimedia_directory)
      storyboard.save_as_json(chapters_file)
      cloud_sync.apply_local_updates_to_gcp(storyboard_directory)
    elif job_queue.has_job(multimedia_directory):
      logprint_bullet(f'deleting job for {multimedia_directory}')
      job_queue.delete_job(multimedia_directory)
    else:
      logprint_bullet(f'new text-to-image job -> prompt = "{chapter.bar.text}" | output = {multimedia_directory}')
      job_queue.add_job(chapter.bar.text, multimedia_directory)

def compile_music_video(storyboard_directory, path_to_music_video):
  """
  """
  logprint_header("compiling final video")
  chapters_file = os.path.join(storyboard_directory, 'chapters.json')
  storyboard = Storyboard.load_from_json(chapters_file)
  # storyboard.compile(path_to_music_video)
  cloud_sync.apply_local_updates_to_gcp(storyboard_directory)

def main(
  audio_file = None, 
  storyboard_directory = None,
  config_file = None,
  job_queue_file = None
):
  """
  """
  if audio_file:
    storyboard_directory = storyboard_directory if storyboard_directory else str(Path(audio_file).stem)
    create_storyboard(audio_file, storyboard_directory)
  elif job_queue:
    pass
  elif config_file:
    config = config.load_from_file(args.config)
    create_storyboard(config.audio_file, config.storyboard_directory)
  else:
    audio_file = str(files('storyboard.data').joinpath('vocab-data.txt'))
    create_storyboard(audio_file, storyboard_directory if storyboard_directory else 'test-music-video')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--audio-file')
  parser.add_argument('--storyboard-directory')
  parser.add_argument('-c', '--config')
  args = parser.parse_args()

  main(
    audio_file=args.audio_file, 
    storyboard_directory=args.storyboard_directory,
    config=args.config
  )
