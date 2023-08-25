"""cloud_sync.py"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google.cloud import storage
from google.oauth2 import service_account

from . import config

PATH_TO_SERVICE_KEY = 'service-keys/bucket-service-key.json'

BUCKET_NAME = 'music-video-multimedia'

OVERWRITE_EXISTING_FILES = False

EXIT_IF_NO_CREDENTIALS = False

def _get_client():
  """
  """
  gcp_project_id = config.get_gcp_project_id()
  service_account_info = config.get_storage_service_account_info()
  credentials = service_account.Credentials.from_service_account_info(service_account_info)
  return storage.Client(project=gcp_project_id, credentials=credentials)

def _upload_item(path_to_item, destination_directory, item_name, bucket_name = BUCKET_NAME):
  """
  """
  client = _get_client()
  bucket = client.get_bucket(bucket_name)
  path_to_blob = os.path.join(destination_directory, item_name)
  blob = bucket.blob(path_to_blob)
  if not blob.exists(client) or OVERWRITE_EXISTING_FILES:
    blob.upload_from_filename(path_to_item)

def _apply_gcp_updates_to_local_segments_file(path_to_segments_file, gcp_music_video_directory):
  """
  """
  client = _get_client()
  bucket = client.get_bucket(BUCKET_NAME)
  path_to_blob = os.path.join(gcp_music_video_directory, 'chapters.json')
  blob = bucket.blob(path_to_blob)
  gcp_segments = json.loads(blob.download_as_string(client=None)) if blob.exists(client) else None

  if gcp_segments is not None:

    with open(path_to_segments_file, 'r') as segments_file:
      local_segments = json.load(segments_file)

    for gcp_segment, local_segment in zip(gcp_segments['chapters'], local_segments['chapters']):
      if local_segment['multimedia'] is None and gcp_segment['multimedia'] is not None:
        local_segment['multimedia'] = gcp_segment['multimedia']

    with open(path_to_segments_file, 'w') as segments_file:
      json.dump(local_segments, segments_file, indent=4)

def apply_local_updates_to_gcp(music_video_directory, bucket_name = BUCKET_NAME):
  """
  """
  if not config.has_storage_service_account_info():
    if EXIT_IF_NO_CREDENTIALS:
      print('GCP service account does not exist. Exiting.')
      sys.exit()
    else:
      print('GCP service account does not exist. Skipping cloud sync.')
      return

  root_gcp_directory = Path(music_video_directory).name

  local_path_to_segments_file = os.path.join(music_video_directory, 'chapters.json')
  assert os.path.exists(local_path_to_segments_file)
  _apply_gcp_updates_to_local_segments_file(local_path_to_segments_file, root_gcp_directory)
  _upload_item(local_path_to_segments_file, root_gcp_directory, 'chapters.json', bucket_name=bucket_name)

  local_path_to_multimedia_directory = os.path.join(music_video_directory, 'multimedia')
  path_to_gcp_multimedia_directory = os.path.join(root_gcp_directory, 'multimedia')

  for child_of_multimedia_directory in os.listdir(local_path_to_multimedia_directory):
    local_path_to_line_directory = os.path.join(local_path_to_multimedia_directory, child_of_multimedia_directory)
    if os.path.isdir(local_path_to_line_directory):
      for multimedia_file in os.listdir(local_path_to_line_directory):
        local_path_to_multimedia = os.path.join(local_path_to_line_directory, multimedia_file)
        gcloud_directory = os.path.join(path_to_gcp_multimedia_directory, child_of_multimedia_directory)
        gcloud_item_name = multimedia_file
        _upload_item(local_path_to_multimedia, gcloud_directory, gcloud_item_name, bucket_name=bucket_name)

  local_path_to_music_video = os.path.join(music_video_directory, 'music-video.mp4')
  gcp_path_to_segments_file = os.path.join(root_gcp_directory, 'music-video.mp4')
  if os.path.exists(local_path_to_music_video):
    _upload_item(local_path_to_music_video, root_gcp_directory, 'music-video.mp4', bucket_name=bucket_name)

def apply_gcp_updates_to_local(music_video_directory, bucket_name = BUCKET_NAME):
  """
  """
  if not config.has_storage_service_account_info():
    if EXIT_IF_NO_CREDENTIALS:
      print('GCP service account does not exist. Exiting.')
      sys.exit()
    else:
      print('GCP service account does not exist. Skipping cloud sync.')
      return
    
  if not os.path.exists(music_video_directory):
    os.mkdir(music_video_directory)

  client = _get_client()
  bucket = client.get_bucket(bucket_name)
  root_gcp_directory = Path(music_video_directory).name

  local_path_to_segments_file = os.path.join(music_video_directory, 'chapters.json')
  gcp_path_to_segments_file = os.path.join(root_gcp_directory, 'chapters.json')

  if bucket.blob(gcp_path_to_segments_file).exists(client) and not os.path.exists(local_path_to_segments_file):
    bucket.blob(gcp_path_to_segments_file).download_to_filename(local_path_to_segments_file)
  elif bucket.blob(gcp_path_to_segments_file).exists(client) and os.path.exists(local_path_to_segments_file):
    _apply_gcp_updates_to_local_segments_file(local_path_to_segments_file, root_gcp_directory)

  local_path_to_multimedia_directory = os.path.join(music_video_directory, 'multimedia')
  path_to_gcp_multimedia_directory = os.path.join(root_gcp_directory, 'multimedia')

  if not os.path.exists(local_path_to_multimedia_directory):
    os.mkdir(local_path_to_multimedia_directory)

  for blob in bucket.list_blobs(prefix=path_to_gcp_multimedia_directory):
    gcp_path_to_multimedia = blob.name
    local_path_to_multimedia = Path(music_video_directory).parent.absolute().joinpath(blob.name)
    local_path_to_multimedia_subdirectory = local_path_to_multimedia.parent.absolute()

    if not os.path.exists(local_path_to_multimedia_subdirectory):
      os.mkdir(local_path_to_multimedia_subdirectory)
    if not os.path.exists(local_path_to_multimedia):
      blob.download_to_filename(local_path_to_multimedia)

if __name__ == '__main__':
  apply_gcp_updates_to_local('music-videos/something-music-video')
