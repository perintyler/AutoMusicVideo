import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google.cloud import storage
from google.oauth2 import service_account

from . import config
from log_print import logprint_bullet

BUCKET_NAME = config.get_enviroment_variable('STORYBOARD_BUCKET_NAME')

OVERWRITE_EXISTING_FILES = False

def get_client():
  """
  """
  service_account_info = config.get_storage_service_account_info()
  return storage.Client(
    project = config.get_gcp_project_id(), 
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
  )

def download(cloud_path, local_path):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(cloud_path)
  assert blob.exists()
  blob.download_to_filename(local_path)

def upload(local_path, cloud_path, overwrite = False, bucket_name = BUCKET_NAME):
  client = get_client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(cloud_path)
  if not blob.exists(client) or overwrite:
    blob.upload_from_filename(cloud_path)

