
import os
from pytest import fixture
from . import cloud_storage
from .config import get_storyboard_bucket_name
from .text_to_image import text_to_image

TEST_BUCKET = 'automusicvideo-test-bucket'
TEST_DIRECTORY = 'test-text-to-image-output'
TEST_ARE_ON = True # these tests take a while, so i don't always keep them on. TODO: figure out a better solution

@fixture(autouse=True)
def bucket_test_runner():
  if TEST_ARE_ON:
    cloud_storage.delete_directory(TEST_DIRECTORY, TEST_BUCKET)
    yield
    cloud_storage.delete_directory(TEST_DIRECTORY, TEST_BUCKET)

def test_text_to_image():

  save_every = 1
  num_iterations = 2

  text_to_image(
    'a town from a midwestern movie with a blue sky', 
    TEST_DIRECTORY, 
    bucket_name=TEST_BUCKET,
    num_epochs=1, 
    num_layers=1,
    num_iterations=2,
    save_every=1
  )

  expected_num_images = int(num_iterations / save_every)
  generated_files = cloud_storage.list_files(TEST_BUCKET, directory=TEST_DIRECTORY)

  assert len(generated_files) == expected_num_images
