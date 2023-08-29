"""cloud_storage.py"""

import os
import io
import sys
import json
from typing import List, Iterator
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google.cloud import storage
from google.oauth2 import service_account

from .. import config

PATH_TO_SERVICE_KEY = 'service-keys/bucket-service-key.json'

OVERWRITE_EXISTING_FILES = False

EXIT_IF_NO_CREDENTIALS = False

def get_client() -> storage.Client:
  """
  """
  gcp_project_id = config.get_gcp_project_id()
  service_account_info = config.get_storage_service_account_info()
  credentials = service_account.Credentials.from_service_account_info(service_account_info)
  return storage.Client(project=gcp_project_id, credentials=credentials)

def get_blob(cloud_path, bucket_name) -> storage.Blob:
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  return bucket.blob(str(cloud_path))

def file_exists(cloud_path, bucket_name) -> bool:
  return get_blob(cloud_path, bucket_name).exists()

def move_file(old_cloud_path, new_cloud_path, bucket_name):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(old_cloud_path))
  assert blob.exists()
  bucket.rename_blob(blob, new_name=str(new_cloud_path))

def list_files(bucket_name, directory=None) -> List[storage.Blob]:
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  return list(bucket.list_blobs(prefix=directory))

def generate_files_as_bytes(cloud_path, bucket_name) -> Iterator[io.BytesIO]:
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  for blob in bucket.list_blobs(prefix=directory):
    yield io.BytesIO(blob.download_as_bytes())

def num_files(bucket_name, directory=None) -> int:
  return len(list_files(bucket_name, directory=directory))

def delete_file(cloud_path, bucket_name):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(cloud_path))
  assert blob.exists()
  blob.delete()

def delete_directory(cloud_path, bucket_name):
  for blob in list_files(bucket_name, directory=cloud_path):
    blob.delete()

def upload_pil_image(pil_image, cloud_path, bucket_name, image_format='jpeg'):
  image_bytes = io.BytesIO()
  pil_image.save(image_bytes, format=image_format)
  get_blob(cloud_path, bucket_name).upload_from_string(
    image_bytes.getvalue(), 
    content_type=f'image/{image_format}'
  )

def upload_json(json_data, cloud_path, bucket_name):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(cloud_path))
  json_string = json.dumps(json_data, indent=2)
  blob.upload_from_string(json_string)

def download_json(cloud_path, bucket_name) -> dict:
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(cloud_path))
  json_string = blob.download_as_bytes(client=client)
  return json.loads(json_string)

def download_bytes(cloud_path, bucket_name) -> dict:
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(cloud_path))
  return blob.download_as_bytes(client=client)

def download_file(cloud_path, local_path, bucket_name, overwrite = True):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(cloud_path))
  assert blob.exists()
  blob.download_to_filename(local_path)

def upload_file(local_path, cloud_path, bucket_name, overwrite = True):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(str(cloud_path))
  if not blob.exists(client) or overwrite:
    blob.upload_from_filename(local_path)

