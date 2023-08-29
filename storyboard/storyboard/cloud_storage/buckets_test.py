
import os
from importlib.resources import files
from PIL import Image, ImageChops
import numpy as np

from . import buckets

TEST_STORAGE_BUCKET = 'automusicvideo-test-bucket'

TEST_IMAGE_NAME = 'test-image.jpeg'

PATH_TO_TEST_IMAGE = files('storyboard.data').joinpath(TEST_IMAGE_NAME)

def test_upload_pil_image():
  local_path = files('storyboard.data').joinpath(TEST_IMAGE_NAME)
  cloud_path = TEST_IMAGE_NAME
  original_image = Image.open(PATH_TO_TEST_IMAGE)
  buckets.upload_pil_image(original_image, cloud_path, TEST_STORAGE_BUCKET)
  assert buckets.file_exists(cloud_path, TEST_STORAGE_BUCKET)

  download_path = os.path.join('/tmp', TEST_IMAGE_NAME)
  buckets.download_file(cloud_path, download_path, TEST_STORAGE_BUCKET)
  downloaded_image = Image.open(download_path)
  downloaded_image.verify()
  assert original_image.format == downloaded_image.format

  # TODO: assert that original image contents == downloaded image contents

  buckets.delete_file(cloud_path, TEST_STORAGE_BUCKET)