"""AutoMusicVideo::cloud_storage.inputs"""

import os
import io
from . import buckets
from .. import config

IN_PROGRESS_DIRECTORY = 'wip'

DONE_DIRECTORY = 'done'

def song_is_in_wip_directory(song_id):
  return buckets.file_exists(
    os.path.join(IN_PROGRESS_DIRECTORY, song_id), 
    config.get_input_audio_bucket_name()
  )

def song_is_in_done_directory(song_id):
  return buckets.file_exists(
    os.path.join(DONE_DIRECTORY, song_id), 
    config.get_input_audio_bucket_name()
  )

def is_new_song(song_id):
  """
  """
  return not song_is_in_wip_directory(song_id) and not song_is_in_done_directory(song_id)

def upload_song(song_id, audio_file):
  """
  """
  buckets.upload_file(
    audio_file,
    os.path.join(IN_PROGRESS_DIRECTORY, song_id), 
    config.get_input_audio_bucket_name()
  )

def get_audio_bytes(song_id):
  """
  """
  assert song_is_in_wip_directory(song_id) or song_is_in_done_directory(song_id)

  cloud_path = os.path.join(
    IN_PROGRESS_DIRECTORY if song_is_in_wip_directory(song_id) else DONE_DIRECTORY, 
    song_id
  )

  audio_bytes = buckets.download_bytes(cloud_path, config.get_input_audio_bucket_name())
  
  return io.BytesIO(audio_bytes)

def get_song_ids_from_WIP_directory():
  """
  """
  return buckets.list_files(
    config.get_input_audio_bucket_name(),
    directory = IN_PROGRESS_DIRECTORY
  )

def archive_song(song_id):
  """
  """
  buckets.move_file(
    os.path.join(IN_PROGRESS_DIRECTORY, song_id), 
    os.path.join(DONE_DIRECTORY, song_id), 
    config.get_input_audio_bucket_name()
  )
