"""AutoMusicVideo::cloud_storage.outputs"""

from io import BytesIO
from pathlib import Path
from .. import config
from . import buckets

def download_video(song_id: str, local_path: Path):
  """
  """
  cloud_path = song_id
  buckets.download_file(str(cloud_path), str(local_path), config.get_output_bucket_name())

def upload_video(song_id: str, path_to_video: Path):
  """
  """
  print(f"uploaded music video | bucket = '{config.get_output_bucket_name()}' | path = '{song_id}'")
  buckets.upload_file(
    str(path_to_video), # local path
    str(song_id), # cloud path
    config.get_output_bucket_name()
  )
  
def upload_video(song_id: str, video_bytes: BytesIO):
  """
  """
  bucket_name = config.get_output_bucket_name()
  cloud_path = song_id
  buckets.upload_from_string(video_bytes.getvalue(), cloud_path, bucket_name)
  print("uploaded music video | bucket = '{bucket_name}' | path = '{cloud_path}'")
