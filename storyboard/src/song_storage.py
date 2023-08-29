
import os
from . import config
from . import cloud_storage

IN_PROGRESS_DIRECTORY = 'wip'

DONE_DIRECTORY = 'done'

def add_new_song(song_id, audio_file):
  """
  """
  cloud_storage.upload_file(
    audio_file,
    os.path.join(IDLE_DIRECTORY, song_id), 
    config.get_queued_songs_bucket_name()
  )

def get_song_ids_from_WIP_directory():
  """
  """
  return cloud_storage.list_files(
    config.get_queued_songs_bucket_name(),
    directory = IN_PROGRESS_DIRECTORY
  )

def song_is_in_done_directory(song_id):
  return cloud_storage.file_exists(
    os.path.join(DONE_DIRECTORY, song_id), 
    config.get_queued_songs_bucket_name()
  )

def move_song_to_done_directory(song_id):
  """
  """
  cloud_storage.move_file(
    os.path.join(IN_PROGRESS_DIRECTORY, song_id), 
    os.path.join(DONE_DIRECTORY, song_id), 
    config.get_queued_songs_bucket_name()
  )
