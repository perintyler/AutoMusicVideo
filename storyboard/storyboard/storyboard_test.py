"""music_video_test.py"""

from importlib.resources import files
from .storyboard import TableOfContents

TEST_VIDEO_ID = 'test-video'
PATH_TO_TEST_FILE = files('storyboard.data').joinpath('test-input.mp3')

def test_create_table_of_contents():

  assert not TableOfContents.exists(TEST_VIDEO_ID)

  test_table_of_contents = TableOfContents.create_new(TEST_VIDEO_ID, PATH_TO_TEST_FILE)
  
  assert TableOfContents.exists(TEST_VIDEO_ID)

  assert TableOfContents.download(TEST_VIDEO_ID).serialize() == test_table_of_contents.serialize()

  test_table_of_contents.delete()

  assert not TableOfContents.exists(TEST_VIDEO_ID)
