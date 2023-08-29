"""main.py"""

import time

from .storyboard import TableOfContents
from .job_queue import StoryboardJobQueue
from .text_to_image import text_to_image
from . import cloud_storage

def write_table_of_contents(song_id, song_path):
  """
  """
  if cloud_storage.inputs.is_new_song(song_id):
    cloud_storage.inputs.upload_song(song_id, song_path)

  if not TableOfContents.exists(song_id):
    table_of_contents = TableOfContents.create_new(song_id, song_path)
    table_of_contents.upload()
    job_queue = StoryboardJobQueue.create_new(table_of_contents)
    job_queue.upload()

def get_chapters(song_id):
  assert TableOfContents.exists(song_id)
  return TableOfContents.download(song_id).chapters

def generate_jobs(song_id):
  job_queue = StoryboardJobQueue.download(song_id)
  next_job = job_queue.next_job()
  while next_job:
    job_queue.upload()
    yield next_job
    time.sleep(1)
    job_queue = StoryboardJobQueue.download(song_id)
    next_job = job_queue.next_job()

def is_complete(song_id):
  return StoryboardJobQueue.download(song_id).is_complete()

def do_job(song_id, job):
  text_to_image(job.prompt, job.output_directory)
  # re-download job queue because other jobs could have finished while this job was being done
  job_queue = StoryboardJobQueue.download(song_id)
  job_queue.finish_job(job.job_id)
  job_queue.upload()

  if job_queue.is_complete():
    input_audio.archive_song(song_id)
    # TODO: send me notification saying storyboard is complete with a messaging service