"""main.py"""

import time

from .storyboard import TableOfContents
from .job_queue import StoryboardJobQueue
from .text_to_image import do_next_text_to_image_job
from .song_storage import get_song_ids_from_WIP_directory, song_is_in_done_directory

def storyboard_exists(song_id):
  return TableOfContents.exists(song_id) and StoryboardJobQueue.exists(song_id)

def storyboard_is_done(song_id):
  return song_is_in_done_directory(song_id)

def start_new_storyboard(song_id, audio_file):
  """
  """
  assert not TableOfContents.exists(song_id)
  table_of_contents = TableOfContents.create_new(song_id, audio_file)
  job_queue = StoryboardJobQueue.create_new(table_of_contents)

  table_of_contents.upload()
  job_queue.upload()

  queue_song_for_music_video_generation(song_id, audio_file)
  time.sleep(1)
  
def get_storyboard_song_ids():
  return get_song_ids_from_WIP_directory()

def storyboard_has_work(song_id):
  return StoryboardJobQueue.download(song_id).has_idle_jobs()

def complete_next_storyboard_job(song_id):
  do_next_text_to_image_job(song_id)
  if StoryboardJobQueue.download(song_id).is_complete():
    move_song_to_done_directory()

def generate_incomplete_jobs(song_id):
  while storyboard_has_work():
    yield StoryboardJobQueue.download(song_id).get_next_job()
    time.sleep(3)

def do_job(song_id, job):
  text_to_image(job.prompt, job.output_directory)
  # re-download job queue because other jobs could have finished while this job was being done
  job_queue = StoryboardJobQueue.download(song_id)
  job_queue.finish_job(job.job_id)
  job_queue.upload()

